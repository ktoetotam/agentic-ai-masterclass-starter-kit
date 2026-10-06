# /// script
# requires-python = ">=3.12"
# dependencies = ["google-api-python-client>=2.150", "google-auth>=2.35"]
# ///
"""Fill workshop Google Workspace accounts with the fictional second brain pack.

For the facilitator only. For each account it:
  gmail     imports every email of mailbox/eml with its original date, labels, read/unread
            state and star (users.messages.import: nothing is sent)
  drive     uploads drive/ into a folder "Juniper (fictional)" in the account's My Drive
  calendar  adds the events of the story to the account's primary calendar (no invitations)

Alex Example's address in the emails is replaced by the account's own address, so every
participant reads the mailbox as Alex.

Needs a service account with domain-wide delegation for these scopes (see the README):
  https://www.googleapis.com/auth/gmail.insert
  https://www.googleapis.com/auth/gmail.labels
  https://www.googleapis.com/auth/drive
  https://www.googleapis.com/auth/calendar

Usage (keep the key file outside the repository, for example in private/):
  uv run data/second-brain-pack/generator/seed_workspace.py --key private/sa.json \\
      --users brain1@example-domain,brain2@example-domain --only gmail,drive,calendar
Without --apply it only prints what it would do.
"""

import argparse
import base64
import datetime as dt
import email
import json
import mimetypes
import sys
import time
from email import policy
from pathlib import Path
from zoneinfo import ZoneInfo

GEN = Path(__file__).resolve().parent
PACK = GEN.parent
sys.path.insert(0, str(GEN))
from notes import CALENDAR  # noqa: E402

ALEX = "alex@juniper-workshop.invalid"
BERLIN = ZoneInfo("Europe/Berlin")
SCOPES = ["https://www.googleapis.com/auth/gmail.insert", "https://www.googleapis.com/auth/gmail.labels",
          "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/calendar"]
CUSTOM_LABELS = ["Bills", "Newsletters", "Project Lantern", "Receipts", "Subscriptions", "Travel"]


def services(key, user):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(key, scopes=SCOPES).with_subject(user)
    return (build("gmail", "v1", credentials=creds, cache_discovery=False),
            build("drive", "v3", credentials=creds, cache_discovery=False),
            build("calendar", "v3", credentials=creds, cache_discovery=False))


def retry(call, tries=5):
    for k in range(tries):
        try:
            return call.execute()
        except Exception as e:  # rate limits and transient errors
            if k == tries - 1 or "429" not in str(e) and "500" not in str(e) and "503" not in str(e):
                raise
            time.sleep(2 ** k)


def seed_gmail(gmail, user, apply):
    labels_meta = json.loads((PACK / "mailbox" / "labels.json").read_text())
    existing = {l["name"]: l["id"] for l in retry(gmail.users().labels().list(userId="me"))["labels"]} if apply else {}
    ids = {}
    for name in CUSTOM_LABELS:
        if name in existing:
            ids[name] = existing[name]
        elif apply:
            ids[name] = retry(gmail.users().labels().create(userId="me", body={"name": name}))["id"]
    files = sorted((PACK / "mailbox" / "eml").glob("*.eml"))
    for f in files:
        raw = f.read_bytes().replace(ALEX.encode(), user.encode())
        labels = labels_meta[f"mailbox/eml/{f.name}"]
        label_ids = []
        for l in labels:
            if l == "Inbox":
                label_ids.append("INBOX")
            elif l == "Sent":
                label_ids.append("SENT")
            elif l == "Starred":
                label_ids.append("STARRED")
            elif l in CUSTOM_LABELS:
                label_ids.append(ids.get(l, l))
        if "Opened" not in labels and "Sent" not in labels:
            label_ids.append("UNREAD")
        body = {"raw": base64.urlsafe_b64encode(raw).decode(), "labelIds": label_ids}
        if apply:
            retry(gmail.users().messages().import_(userId="me", body=body, internalDateSource="dateHeader",
                                                   neverMarkSpam=True, processForCalendar=False))
    print(f"  gmail: {len(files)} emails {'imported' if apply else 'would be imported'}")


def seed_drive(drive, apply):
    root = None
    if apply:
        root = retry(drive.files().create(body={"name": "Juniper (fictional)", "mimeType": "application/vnd.google-apps.folder"}, fields="id"))["id"]
    folders = {Path("."): root}
    count = 0
    from googleapiclient.http import MediaFileUpload
    for p in sorted((PACK / "drive").rglob("*")):
        rel = p.relative_to(PACK / "drive")
        if p.is_dir():
            if apply:
                folders[rel] = retry(drive.files().create(body={"name": p.name, "mimeType": "application/vnd.google-apps.folder",
                                                                 "parents": [folders[rel.parent]]}, fields="id"))["id"]
            continue
        count += 1
        if apply:
            mtime = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).isoformat().replace("+00:00", "Z")
            mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            retry(drive.files().create(body={"name": p.name, "parents": [folders[rel.parent]], "modifiedTime": mtime},
                                       media_body=MediaFileUpload(str(p), mimetype=mime, resumable=False), fields="id"))
    print(f"  drive: {count} files {'uploaded' if apply else 'would be uploaded'} to 'Juniper (fictional)'")


def seed_calendar(cal, apply):
    for ev in CALENDAR:
        body = {"summary": ev["title"], "location": ev.get("location", ""), "description": (ev.get("note", "") + " Fictional workshop data.").strip(),
                "status": {"TENTATIVE": "tentative", "CANCELLED": "cancelled"}.get(ev.get("status", ""), "confirmed")}
        if ev.get("allday"):
            body["start"] = {"date": ev["start"]}; body["end"] = {"date": ev["end"]}
        else:
            body["start"] = {"dateTime": dt.datetime.fromisoformat(ev["start"]).isoformat(), "timeZone": "Europe/Berlin"}
            body["end"] = {"dateTime": dt.datetime.fromisoformat(ev["end"]).isoformat(), "timeZone": "Europe/Berlin"}
        if ev.get("rrule"):
            body["recurrence"] = [f"RRULE:{ev['rrule']}"]
        if apply and body["status"] != "cancelled":
            retry(cal.events().insert(calendarId="primary", body=body, sendUpdates="none"))
    print(f"  calendar: {len([e for e in CALENDAR if e.get('status') != 'CANCELLED'])} events {'added' if apply else 'would be added'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", required=True, help="service account JSON key (keep it outside Git)")
    ap.add_argument("--users", required=True, help="comma-separated workshop account addresses")
    ap.add_argument("--only", default="gmail,drive,calendar")
    ap.add_argument("--apply", action="store_true", help="really write; without it nothing changes")
    a = ap.parse_args()
    parts = set(a.only.split(","))
    for user in [u.strip() for u in a.users.split(",") if u.strip()]:
        print(f"{user}:")
        gmail = drive = cal = None
        if a.apply:
            gmail, drive, cal = services(a.key, user)
        if "gmail" in parts:
            seed_gmail(gmail, user, a.apply)
        if "drive" in parts:
            seed_drive(drive, a.apply)
        if "calendar" in parts:
            seed_calendar(cal, a.apply)
    if not a.apply:
        print("Dry run. Add --apply to write.")


if __name__ == "__main__":
    main()
