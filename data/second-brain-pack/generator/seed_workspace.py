# /// script
# requires-python = ">=3.12"
# dependencies = ["google-api-python-client>=2.150", "google-auth>=2.35", "requests>=2.32"]
# ///
"""Fill workshop Google Workspace accounts with the fictional second brain pack.

For the facilitator only. Nothing is sent: emails are imported, files are shared without
notification emails, calendar events are added without invitations.

  drive     uploads drive/ once into the owner's My Drive as "Juniper (fictional)", shares it
            read-only with every participant and adds a shortcut to each participant's My Drive.
            The full pack (with the answer key) goes to "Second brain pack (facilitator only)",
            which is not shared.
  gmail     imports every email of mailbox/eml into each participant's mailbox with its original
            date, labels, read/unread state and star (users.messages.import)
  calendar  adds the story's events to each participant's primary calendar

Alex Example's address in the emails becomes the participant's own address, so everybody reads
the mailbox as Alex. Re-running is safe: work that is already done is skipped.

Authorisation: a service account with domain-wide delegation for these scopes:
  https://www.googleapis.com/auth/gmail.modify
  https://www.googleapis.com/auth/drive
  https://www.googleapis.com/auth/calendar
Either keyless (recommended): the signed-in Google Cloud user needs the role
"Service Account Token Creator" on the service account; pass --sa EMAIL.
Or with a JSON key kept outside Git: pass --key private/sa.json.

  uv run --no-project --script data/second-brain-pack/generator/seed_workspace.py \\
      --sa seed@PROJECT.iam.gserviceaccount.com --owner maria@DOMAIN --users a@DOMAIN,b@DOMAIN
Without --apply it only prints what it would do.
"""

import argparse
import base64
import datetime as dt
import json
import mimetypes
import sys
import time
from pathlib import Path

GEN = Path(__file__).resolve().parent
PACK = GEN.parent
sys.path.insert(0, str(GEN))
from notes import CALENDAR  # noqa: E402

ALEX = "alex@juniper-workshop.invalid"
SCOPES = ["https://www.googleapis.com/auth/gmail.modify", "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/calendar"]
CUSTOM_LABELS = ["Bills", "Newsletters", "Project Lantern", "Receipts", "Subscriptions", "Travel"]
SHARED_FOLDER = "Juniper (fictional)"
FACILITATOR_FOLDER = "Second brain pack (facilitator only)"
# "Juniper (fictional)" already holds drive/; the single .mbox file stands in for the 84 .eml files.
FACILITATOR_PARTS = ["README.md", "manifest.json", "answer-key", "mailbox/alex-example.mbox", "mailbox/labels.json", "downloads",
                     "notes", "records", "calendar", "telegram", "notion"]
FIRST_MESSAGE_ID = None  # filled from the first .eml; used to see whether a mailbox is already filled
MARKER_EVENT = "Learning day (Project Lantern)"
FOLDER = "application/vnd.google-apps.folder"


def credentials(args, subject):
    if args.key:
        from google.oauth2 import service_account
        return service_account.Credentials.from_service_account_file(args.key, scopes=SCOPES).with_subject(subject)
    import google.auth
    import google.auth.iam
    import google.auth.transport.requests
    from google.oauth2 import service_account
    source, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    request = google.auth.transport.requests.Request()
    signer = google.auth.iam.Signer(request, source, args.sa)
    return service_account.Credentials(signer, args.sa, "https://oauth2.googleapis.com/token", scopes=SCOPES, subject=subject)


def api(args, subject, name, version):
    from googleapiclient.discovery import build
    return build(name, version, credentials=credentials(args, subject), cache_discovery=False)


def run(call, tries=6):
    for k in range(tries):
        try:
            return call.execute()
        except Exception as e:  # rate limits and transient errors
            text = str(e)
            if k == tries - 1 or not any(code in text for code in ("429", "500", "502", "503", "rateLimitExceeded", "userRateLimitExceeded")):
                raise
            time.sleep(2 ** k)


# ---------------------------------------------------------------------------------- drive

def find_folder(drive, name, parent="root"):
    q = f"name = '{name}' and mimeType = '{FOLDER}' and '{parent}' in parents and trashed = false"
    files = run(drive.files().list(q=q, fields="files(id,name)", spaces="drive"))["files"]
    return files[0]["id"] if files else None


def upload_tree(drive, local_root, parent_id, label):
    from googleapiclient.http import MediaFileUpload
    folders = {Path("."): parent_id}
    count = 0
    for p in sorted(local_root.rglob("*")):
        rel = p.relative_to(local_root)
        if p.name.startswith(".") or "__pycache__" in rel.parts:
            continue
        if p.is_dir():
            folders[rel] = run(drive.files().create(body={"name": p.name, "mimeType": FOLDER, "parents": [folders[rel.parent]]},
                                                   fields="id"))["id"]
            continue
        mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat().replace("+00:00", "Z")
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        # message/* files break the client's multipart encoder, so send them (and big files) as resumable uploads
        resumable = mime.startswith("message/") or p.stat().st_size > 5_000_000
        run(drive.files().create(body={"name": p.name, "parents": [folders[rel.parent]], "modifiedTime": mtime},
                                 media_body=MediaFileUpload(str(p), mimetype=mime, resumable=resumable), fields="id"))
        count += 1
    print(f"  drive: uploaded {count} files to '{label}'")
    return count


def seed_drive(args, users):
    owner = args.owner
    print(f"{owner} (owner):")
    if not args.apply:
        n = sum(1 for p in (PACK / "drive").rglob("*") if p.is_file())
        print(f"  drive: would upload {n} files to '{SHARED_FOLDER}' and share it read-only with {len(users)} people")
        print(f"  drive: would upload the full pack to '{FACILITATOR_FOLDER}' (not shared)")
        return
    drive = api(args, owner, "drive", "v3")
    shared = find_folder(drive, SHARED_FOLDER)
    if shared:
        print(f"  drive: '{SHARED_FOLDER}' already exists, upload skipped")
    else:
        shared = run(drive.files().create(body={"name": SHARED_FOLDER, "mimeType": FOLDER,
                                                "description": "Fictional workshop data: Alex Example's Google Drive."}, fields="id"))["id"]
        upload_tree(drive, PACK / "drive", shared, SHARED_FOLDER)
    fac = find_folder(drive, FACILITATOR_FOLDER)
    if fac:
        print(f"  drive: '{FACILITATOR_FOLDER}' already exists, upload skipped")
    else:
        fac = run(drive.files().create(body={"name": FACILITATOR_FOLDER, "mimeType": FOLDER,
                                             "description": "Fictional workshop data incl. answer key. Do not share with participants."},
                                       fields="id"))["id"]
        total = 0
        for part in FACILITATOR_PARTS:
            src = PACK / part
            if src.is_file():
                from googleapiclient.http import MediaFileUpload
                mime = mimetypes.guess_type(src.name)[0] or "application/octet-stream"
                run(drive.files().create(body={"name": src.name, "parents": [fac]},
                                         media_body=MediaFileUpload(str(src), mimetype=mime, resumable=True), fields="id"))
                total += 1
            else:
                sub = run(drive.files().create(body={"name": part, "mimeType": FOLDER, "parents": [fac]}, fields="id"))["id"]
                total += upload_tree(drive, src, sub, f"{FACILITATOR_FOLDER}/{part}")
    existing = {p.get("emailAddress", "").lower() for p in
                run(drive.permissions().list(fileId=shared, fields="permissions(emailAddress,role)"))["permissions"]}
    for u in users:
        if u.lower() not in existing:
            run(drive.permissions().create(fileId=shared, sendNotificationEmail=False,
                                           body={"type": "user", "role": "reader", "emailAddress": u}))
    print(f"  drive: '{SHARED_FOLDER}' shared read-only with {len(users)} people, no notification emails")
    for u in users:
        udrive = api(args, u, "drive", "v3")
        q = f"name = '{SHARED_FOLDER}' and mimeType = 'application/vnd.google-apps.shortcut' and 'root' in parents and trashed = false"
        if not run(udrive.files().list(q=q, fields="files(id)"))["files"]:
            run(udrive.files().create(body={"name": SHARED_FOLDER, "mimeType": "application/vnd.google-apps.shortcut",
                                            "shortcutDetails": {"targetId": shared}}, fields="id"))
    print(f"  drive: shortcut '{SHARED_FOLDER}' in each participant's My Drive")


# ---------------------------------------------------------------------------------- gmail

def first_message_id():
    import email
    from email import policy
    first = sorted((PACK / "mailbox" / "eml").glob("*.eml"))[0]
    return email.message_from_bytes(first.read_bytes(), policy=policy.default)["Message-ID"].strip("<>")


def eml_index():
    """Every pack email with its headers, oldest first, so a reply is imported after the message it answers."""
    import email
    import email.utils
    import re
    from email import policy
    items = []
    for f in (PACK / "mailbox" / "eml").glob("*.eml"):
        m = email.message_from_bytes(f.read_bytes(), policy=policy.default)
        refs = (m.get("References", "") + " " + m.get("In-Reply-To", "")).split()
        subject = re.sub(r"^((re|aw|fwd?|wg)\s*:\s*)+", "", (m["Subject"] or "").strip(), flags=re.I).lower()
        items.append(dict(path=f, msgid=m["Message-ID"].strip(), refs=[r.strip() for r in refs], subject=subject,
                          date=email.utils.parsedate_to_datetime(m["Date"])))
    return sorted(items, key=lambda x: x["date"])


def seed_gmail(args, user):
    items = eml_index()
    if not args.apply:
        print(f"  gmail: would import {len(items)} emails as threaded conversations")
        return
    gmail = api(args, user, "gmail", "v1")
    if args.reimport_mail:
        trashed = 0
        for it in items:
            for m in run(gmail.users().messages().list(userId="me", q=f"rfc822msgid:{it['msgid'].strip('<>')}")).get("messages", []):
                run(gmail.users().messages().trash(userId="me", id=m["id"])); trashed += 1
        print(f"  gmail: moved {trashed} earlier pack emails to Trash (recoverable)")
    elif run(gmail.users().messages().list(userId="me", q=f"rfc822msgid:{first_message_id()}"))["resultSizeEstimate"]:
        print("  gmail: already filled, skipped")
        return
    labels_meta = json.loads((PACK / "mailbox" / "labels.json").read_text())
    existing = {l["name"]: l["id"] for l in run(gmail.users().labels().list(userId="me"))["labels"]}
    ids = {}
    for name in CUSTOM_LABELS:
        ids[name] = existing.get(name) or run(gmail.users().labels().create(userId="me", body={
            "name": name, "labelListVisibility": "labelShow", "messageListVisibility": "show"}))["id"]
    thread_of, subject_of = {}, {}
    threaded = 0
    for it in items:
        raw = it["path"].read_bytes().replace(ALEX.encode(), user.encode())
        labels = labels_meta[f"mailbox/eml/{it['path'].name}"]
        label_ids = [{"Inbox": "INBOX", "Sent": "SENT", "Starred": "STARRED"}.get(l, ids.get(l)) for l in labels if l != "Opened"]
        label_ids = [l for l in label_ids if l]
        if "Opened" not in labels and "Sent" not in labels:
            label_ids.append("UNREAD")
        body = {"raw": base64.urlsafe_b64encode(raw).decode(), "labelIds": label_ids}
        # Gmail threads an imported reply only when told the thread and the subjects match.
        for ref in reversed(it["refs"]):
            if ref in thread_of and subject_of[ref] == it["subject"]:
                body["threadId"] = thread_of[ref]; threaded += 1
                break
        res = run(gmail.users().messages().import_(userId="me", body=body, internalDateSource="dateHeader",
                                                   neverMarkSpam=True, processForCalendar=False))
        thread_of[it["msgid"]] = res["threadId"]; subject_of[it["msgid"]] = it["subject"]
    print(f"  gmail: imported {len(items)} emails ({threaded} replies joined to their conversations)")


# ---------------------------------------------------------------------------------- calendar

def seed_calendar(args, user):
    events = [e for e in CALENDAR if e.get("status") != "CANCELLED"]
    if not args.apply:
        print(f"  calendar: would add {len(events)} events")
        return
    cal = api(args, user, "calendar", "v3")
    found = run(cal.events().list(calendarId="primary", q=MARKER_EVENT, timeMin="2026-10-01T00:00:00Z", timeMax="2026-11-01T00:00:00Z"))
    if found.get("items"):
        print("  calendar: already filled, skipped")
        return
    for ev in events:
        body = {"summary": ev["title"], "location": ev.get("location", ""),
                "description": (ev.get("note", "") + " Fictional workshop data.").strip(),
                "status": "tentative" if ev.get("status") == "TENTATIVE" else "confirmed"}
        if ev.get("allday"):
            body["start"] = {"date": ev["start"]}; body["end"] = {"date": ev["end"]}
        else:
            body["start"] = {"dateTime": dt.datetime.fromisoformat(ev["start"]).isoformat(), "timeZone": "Europe/Berlin"}
            body["end"] = {"dateTime": dt.datetime.fromisoformat(ev["end"]).isoformat(), "timeZone": "Europe/Berlin"}
        if ev.get("rrule"):
            body["recurrence"] = [f"RRULE:{ev['rrule']}"]
        run(cal.events().insert(calendarId="primary", body=body, sendUpdates="none"))
    print(f"  calendar: added {len(events)} events")


# ---------------------------------------------------------------------------------- check

def check(args, users):
    first = first_message_id()
    for u in users:
        gmail = api(args, u, "gmail", "v1")
        n = run(gmail.users().messages().list(userId="me", q="-in:chats", maxResults=500)).get("resultSizeEstimate", 0)
        has = bool(run(gmail.users().messages().list(userId="me", q=f"rfc822msgid:{first}"))["resultSizeEstimate"])
        cal = api(args, u, "calendar", "v3")
        evs = len(run(cal.events().list(calendarId="primary", timeMin="2026-09-01T00:00:00Z", timeMax="2026-12-31T00:00:00Z",
                                        singleEvents=False, maxResults=100)).get("items", []))
        drive = api(args, u, "drive", "v3")
        sc = len(run(drive.files().list(q=f"name = '{SHARED_FOLDER}' and trashed = false", fields="files(id)"))["files"])
        print(f"{u}: mail {n} (pack {'yes' if has else 'no'}), calendar events {evs}, '{SHARED_FOLDER}' visible {sc > 0}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    auth = ap.add_mutually_exclusive_group(required=True)
    auth.add_argument("--sa", help="service account email (keyless; uses the signed-in Google Cloud user)")
    auth.add_argument("--key", help="service account JSON key, kept outside Git")
    ap.add_argument("--owner", required=True, help="account whose Drive holds the shared folder, e.g. maria@DOMAIN")
    ap.add_argument("--users", required=True, help="comma-separated participant addresses")
    ap.add_argument("--only", default="drive,gmail,calendar")
    ap.add_argument("--apply", action="store_true", help="really write; without it nothing changes")
    ap.add_argument("--check", action="store_true", help="only report what each account contains")
    ap.add_argument("--reimport-mail", action="store_true", help="move earlier pack emails to Trash and import them again")
    args = ap.parse_args()
    users = [u.strip() for u in args.users.split(",") if u.strip()]
    if args.check:
        check(args, users)
        return
    parts = set(args.only.split(","))
    if "drive" in parts:
        seed_drive(args, users)
    for u in users:
        print(f"{u}:")
        if "gmail" in parts:
            seed_gmail(args, u)
        if "calendar" in parts:
            seed_calendar(args, u)
    if not args.apply:
        print("Dry run. Add --apply to write.")


if __name__ == "__main__":
    main()
