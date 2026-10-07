# /// script
# requires-python = ">=3.12"
# dependencies = ["google-api-python-client>=2.150", "google-auth>=2.35", "requests>=2.32"]
# ///
"""Fill workshop Google Workspace accounts with the fictional accountant pack.

For the facilitator only, after the second brain pack's setup (same tenant, same service account and
domain-wide delegation; see ../../second-brain-pack/README.md). Nothing is sent: emails are imported,
files are shared without notification emails.

  drive  uploads drive/ once into the owner's My Drive as "Juniper accounting (fictional)", shares it
         read-only with the participants and adds a shortcut to their My Drive. The full pack (with the
         answer key and the Stripe snapshot) goes to "Accountant pack (facilitator only)", not shared.
  gmail  imports Mira Beispiel's emails (mailbox/eml) into each participant's mailbox with their dates,
         under the label "Juniper accounting" and its sublabels. Mira's address becomes the participant's
         own. Without --inbox they stay out of the inbox, so they do not mix with Alex's second brain mail.

  uv run --no-project --script data/accountant-pack/generator/seed_workspace.py \\
      --sa seed@PROJECT.iam.gserviceaccount.com --owner maria@DOMAIN --users a@DOMAIN,b@DOMAIN
Without --apply it only prints what it would do. Re-running skips what is already there.
"""

import argparse
import base64
import email
import email.utils
import json
import sys
from email import policy
from pathlib import Path

GEN = Path(__file__).resolve().parent
PACK = GEN.parent
sys.path.insert(0, str(PACK.parent / "second-brain-pack" / "generator"))
import seed_workspace as sw  # noqa: E402  (keyless credentials, retries and uploads)

MIRA = "mira@juniper-workshop.invalid"
PARENT_LABEL = "Juniper accounting"
SHARED_FOLDER = "Juniper accounting (fictional)"
FACILITATOR_FOLDER = "Accountant pack (facilitator only)"
FACILITATOR_PARTS = ["README.md", "manifest.json", "answer-key", "stripe", "mailbox/mira-beispiel.mbox", "mailbox/labels.json"]


def emails():
    items = []
    for f in (PACK / "mailbox" / "eml").glob("*.eml"):
        m = email.message_from_bytes(f.read_bytes(), policy=policy.default)
        items.append(dict(path=f, msgid=m["Message-ID"].strip(), date=email.utils.parsedate_to_datetime(m["Date"])))
    return sorted(items, key=lambda x: x["date"])


def seed_drive(args, users):
    print(f"{args.owner} (owner):")
    if not args.apply:
        n = sum(1 for p in (PACK / "drive").rglob("*") if p.is_file())
        print(f"  drive: would upload {n} files to '{SHARED_FOLDER}' and share it read-only with {len(users)} people")
        print(f"  drive: would upload the answer key and the Stripe snapshot to '{FACILITATOR_FOLDER}' (not shared)")
        return
    drive = sw.api(args, args.owner, "drive", "v3")
    shared = sw.find_folder(drive, SHARED_FOLDER)
    if shared:
        print(f"  drive: '{SHARED_FOLDER}' already exists, upload skipped")
    else:
        shared = sw.run(drive.files().create(body={"name": SHARED_FOLDER, "mimeType": sw.FOLDER,
                                                   "description": "Fictional workshop data: Juniper Workshop Lab's accounting folder."},
                                             fields="id"))["id"]
        sw.upload_tree(drive, PACK / "drive", shared, SHARED_FOLDER)
    if not sw.find_folder(drive, FACILITATOR_FOLDER):
        from googleapiclient.http import MediaFileUpload
        import mimetypes
        fac = sw.run(drive.files().create(body={"name": FACILITATOR_FOLDER, "mimeType": sw.FOLDER,
                                                "description": "Fictional workshop data incl. answer key. Do not share with participants."},
                                          fields="id"))["id"]
        for part in FACILITATOR_PARTS:
            src = PACK / part
            if src.is_file():
                mime = mimetypes.guess_type(src.name)[0] or "application/octet-stream"
                sw.run(drive.files().create(body={"name": src.name, "parents": [fac]},
                                            media_body=MediaFileUpload(str(src), mimetype=mime, resumable=True), fields="id"))
            elif src.is_dir():
                sub = sw.run(drive.files().create(body={"name": part, "mimeType": sw.FOLDER, "parents": [fac]}, fields="id"))["id"]
                sw.upload_tree(drive, src, sub, f"{FACILITATOR_FOLDER}/{part}")
    existing = {p.get("emailAddress", "").lower() for p in
                sw.run(drive.permissions().list(fileId=shared, fields="permissions(emailAddress,role)"))["permissions"]}
    for u in users:
        if u.lower() not in existing:
            sw.run(drive.permissions().create(fileId=shared, sendNotificationEmail=False,
                                              body={"type": "user", "role": "reader", "emailAddress": u}))
    for u in users:
        udrive = sw.api(args, u, "drive", "v3")
        q = f"name = '{SHARED_FOLDER}' and mimeType = 'application/vnd.google-apps.shortcut' and 'root' in parents and trashed = false"
        if not sw.run(udrive.files().list(q=q, fields="files(id)"))["files"]:
            sw.run(udrive.files().create(body={"name": SHARED_FOLDER, "mimeType": "application/vnd.google-apps.shortcut",
                                               "shortcutDetails": {"targetId": shared}}, fields="id"))
    print(f"  drive: '{SHARED_FOLDER}' shared read-only with {len(users)} people, shortcut in each My Drive, no notification emails")


def seed_gmail(args, user):
    items = emails()
    if not args.apply:
        print(f"  gmail: would import {len(items)} emails under '{PARENT_LABEL}'" + (" and in the inbox" if args.inbox else ""))
        return
    gmail = sw.api(args, user, "gmail", "v1")
    if sw.run(gmail.users().messages().list(userId="me", q=f"rfc822msgid:{items[0]['msgid'].strip('<>')}"))["resultSizeEstimate"]:
        print("  gmail: already filled, skipped")
        return
    meta = json.loads((PACK / "mailbox" / "labels.json").read_text())
    wanted = {PARENT_LABEL} | {f"{PARENT_LABEL}/{l}" for v in meta.values() for l in v if l not in ("Inbox", "Sent")}
    existing = {l["name"]: l["id"] for l in sw.run(gmail.users().labels().list(userId="me"))["labels"]}
    ids = {}
    for name in sorted(wanted):  # the parent first, so Gmail nests the sublabels under it
        ids[name] = existing.get(name) or sw.run(gmail.users().labels().create(userId="me", body={
            "name": name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}))["id"]
    for it in items:
        raw = it["path"].read_bytes().replace(MIRA.encode(), user.encode())
        labels = meta[f"mailbox/eml/{it['path'].name}"]
        label_ids = [ids[PARENT_LABEL]] + [ids[f"{PARENT_LABEL}/{l}"] for l in labels if l not in ("Inbox", "Sent")]
        if "Sent" in labels:
            label_ids.append("SENT")
        else:
            label_ids.append("UNREAD")
            if args.inbox:
                label_ids.append("INBOX")
        sw.run(gmail.users().messages().import_(userId="me", body={"raw": base64.urlsafe_b64encode(raw).decode(), "labelIds": label_ids},
                                                internalDateSource="dateHeader", neverMarkSpam=True, processForCalendar=False, fields="id"))
    print(f"  gmail: imported {len(items)} emails under '{PARENT_LABEL}'")


def check(args, users):
    items = emails()
    for u in users:
        gmail = sw.api(args, u, "gmail", "v1")
        has = bool(sw.run(gmail.users().messages().list(userId="me", q=f"rfc822msgid:{items[0]['msgid'].strip('<>')}"))["resultSizeEstimate"])
        n = sw.run(gmail.users().messages().list(userId="me", q=f'label:"{PARENT_LABEL}"', maxResults=100)).get("resultSizeEstimate", 0)
        drive = sw.api(args, u, "drive", "v3")
        sc = len(sw.run(drive.files().list(q=f"name = '{SHARED_FOLDER}' and trashed = false", fields="files(id)"))["files"])
        print(f"{u}: accountant mail {'yes' if has else 'no'} ({n} under '{PARENT_LABEL}'), '{SHARED_FOLDER}' visible {sc > 0}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    auth = ap.add_mutually_exclusive_group(required=True)
    auth.add_argument("--sa", help="service account email (keyless; uses the signed-in Google Cloud user)")
    auth.add_argument("--key", help="service account JSON key, kept outside Git")
    ap.add_argument("--owner", required=True, help="account whose Drive holds the shared folder, e.g. maria@DOMAIN")
    ap.add_argument("--users", required=True, help="comma-separated participant addresses (the accountant group)")
    ap.add_argument("--only", default="drive,gmail")
    ap.add_argument("--inbox", action="store_true", help="also put the emails in the inbox (for accounts without the second brain mail)")
    ap.add_argument("--apply", action="store_true", help="really write; without it nothing changes")
    ap.add_argument("--check", action="store_true", help="only report what each account contains")
    args = ap.parse_args()
    users = [u.strip() for u in args.users.split(",") if u.strip()]
    if args.check:
        return check(args, users)
    parts = args.only.split(",")
    if "drive" in parts:
        seed_drive(args, users)
    for u in users:
        print(f"{u}:")
        if "gmail" in parts:
            seed_gmail(args, u)
    if not args.apply:
        print("\nDry run: nothing changed. Add --apply to write.")


if __name__ == "__main__":
    main()
