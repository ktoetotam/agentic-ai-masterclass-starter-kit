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
  life      adds everyday life around the story (life.py): routines, focus time, home-office days,
            private appointments, pets, holidays. Different for every account; the story's events
            stay the same everywhere because the answer key depends on them.

Alex Example's address in the emails becomes the participant's own address, so everybody reads
the mailbox as Alex. Re-running is safe: work that is already done is skipped. --redo-life
replaces the life entries (they carry the private property juniper=life) with a fresh set.

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
from life import life_events  # noqa: E402
from notes import CALENDAR  # noqa: E402

ALEX = "alex@juniper-workshop.invalid"
TZ = "Europe/Berlin"
LIFE = "juniper=life"  # private extended property on every life entry
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
        print(f"  gmail: would import {len(items)} emails")
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
    for it in items:
        raw = it["path"].read_bytes().replace(ALEX.encode(), user.encode())
        labels = labels_meta[f"mailbox/eml/{it['path'].name}"]
        label_ids = [{"Inbox": "INBOX", "Sent": "SENT", "Starred": "STARRED"}.get(l, ids.get(l)) for l in labels if l != "Opened"]
        label_ids = [l for l in label_ids if l]
        if "Opened" not in labels and "Sent" not in labels:
            label_ids.append("UNREAD")
        body = {"raw": base64.urlsafe_b64encode(raw).decode(), "labelIds": label_ids}
        # Gmail groups imported replies into conversations by their References headers and subject,
        # as for received mail; importing oldest first keeps each reply after the message it answers.
        run(gmail.users().messages().import_(userId="me", body=body, internalDateSource="dateHeader",
                                             neverMarkSpam=True, processForCalendar=False, fields="id"))
    print(f"  gmail: imported {len(items)} emails")


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


def life_body(ev):
    """A life.py entry as a Calendar API event."""
    body = {"summary": ev["title"], "extendedProperties": {"private": dict([LIFE.split("=")])},
            "transparency": "opaque" if ev.get("busy", True) else "transparent"}
    if ev.get("location"):
        body["location"] = ev["location"]
    if ev.get("note"):
        body["description"] = ev["note"]
    if ev.get("allday"):
        body["start"], body["end"] = {"date": ev["start"]}, {"date": ev["end"]}
    else:
        body["start"] = {"dateTime": dt.datetime.fromisoformat(ev["start"]).isoformat(), "timeZone": TZ}
        body["end"] = {"dateTime": dt.datetime.fromisoformat(ev["end"]).isoformat(), "timeZone": TZ}
    if ev.get("rrule"):
        body["recurrence"] = [f"RRULE:{ev['rrule']}"]
        if ev.get("exdates") and ev.get("allday"):
            body["recurrence"].append("EXDATE;VALUE=DATE:" + ",".join(d.replace("-", "") for d in ev["exdates"]))
        elif ev.get("exdates"):
            body["recurrence"].append(f"EXDATE;TZID={TZ}:" + ",".join(f"{dt.datetime.fromisoformat(d):%Y%m%dT%H%M%S}" for d in ev["exdates"]))
    if ev.get("private"):
        body["visibility"] = "private"
    if ev.get("color"):
        body["colorId"] = ev["color"]
    if ev["kind"] == "focus":
        body.update(eventType="focusTime", focusTimeProperties={"chatStatus": "doNotDisturb", "autoDeclineMode": "declineNone",
                                                                "declineMessage": ev["message"]})
    elif ev["kind"] == "ooo":
        body.update(eventType="outOfOffice", outOfOfficeProperties={"autoDeclineMode": "declineNone", "declineMessage": ev["message"]})
    elif ev["kind"] in ("home", "office", "place"):
        where = {"home": {"type": "homeOffice", "homeOffice": {}},
                 "office": {"type": "officeLocation", "officeLocation": {"label": ev.get("label", "")}},
                 "place": {"type": "customLocation", "customLocation": {"label": ev.get("label", "")}}}[ev["kind"]]
        body.update(eventType="workingLocation", visibility="public", transparency="transparent", workingLocationProperties=where)
    return body


def plain_body(ev):
    """The same entry as an ordinary event, for accounts without focus time, out of office or working locations."""
    if ev["kind"] == "office":
        return None  # an all-day "Office" on most days is noise; home days and trips are enough
    body = life_body({**ev, "kind": "event"})
    if ev["kind"] == "home":
        body["summary"] = "Home office"
    return body


def life_ids(cal):
    ids, token = [], None
    while True:
        page = run(cal.events().list(calendarId="primary", privateExtendedProperty=LIFE, maxResults=250, pageToken=token,
                                     fields="items(id),nextPageToken"))
        ids += [e["id"] for e in page.get("items", [])]
        token = page.get("nextPageToken")
        if not token:
            return ids


def seed_life(args, user):
    from googleapiclient.errors import HttpError
    entries, about = life_events(user)
    if not args.apply:
        print(f"  life: would add {len(entries)} entries: {about}")
        return
    cal = api(args, user, "calendar", "v3")
    old = life_ids(cal)
    if old and not args.redo_life:
        print("  life: already added, skipped")
        return
    for event_id in old:
        run(cal.events().delete(calendarId="primary", eventId=event_id, sendUpdates="none"))
    plain = {}
    for ev in entries:
        try:
            run(cal.events().insert(calendarId="primary", body=life_body(ev), sendUpdates="none"))
        except HttpError as e:
            if ev["kind"] == "event":
                raise
            plain.setdefault(ev["kind"], getattr(e, "reason", str(e)))
            body = plain_body(ev)
            if body:
                run(cal.events().insert(calendarId="primary", body=body, sendUpdates="none"))
    replaced = f"replaced {len(old)} earlier entries, " if old else ""
    print(f"  life: {replaced}added {len(entries)} entries: {about}")
    for kind, reason in plain.items():
        print(f"  life: {kind} entries added as ordinary events ({reason})")


def set_timezone(args, users, tz):
    """Show every account's calendar in this time zone (the story's times are Europe/Berlin)."""
    if not args.apply:
        print(f"  calendar: would set the time zone of {len(users)} calendars to {tz}")
        return
    for u in users:
        cal = api(args, u, "calendar", "v3")
        before = run(cal.calendars().get(calendarId="primary", fields="timeZone"))["timeZone"]
        if before != tz:
            run(cal.calendars().patch(calendarId="primary", body={"timeZone": tz}, fields="timeZone"))
        print(f"{u}: calendar time zone {before} -> {tz}" if before != tz else f"{u}: calendar time zone already {tz}")


def share_calendars(args, users, viewer):
    """Let the facilitator see each participant's primary calendar (read-only, no notification emails)."""
    if not args.apply:
        print(f"  calendar: would share {len(users)} calendars read-only with {viewer}")
        return
    for u in users:
        cal = api(args, u, "calendar", "v3")
        run(cal.acl().insert(calendarId="primary", sendNotifications=False,
                             body={"role": "reader", "scope": {"type": "user", "value": viewer}}))
    vcal = api(args, viewer, "calendar", "v3")
    listed = {c["id"] for c in run(vcal.calendarList().list(maxResults=250)).get("items", [])}
    for u in users:
        if u not in listed:
            run(vcal.calendarList().insert(body={"id": u, "selected": True}))
    print(f"  calendar: {len(users)} calendars shared read-only with {viewer} and added to its calendar list")


# ---------------------------------------------------------------------------------- check

def check(args, users):
    first = first_message_id()
    for u in users:
        gmail = api(args, u, "gmail", "v1")
        n = run(gmail.users().messages().list(userId="me", q="-in:chats", maxResults=500)).get("resultSizeEstimate", 0)
        has = bool(run(gmail.users().messages().list(userId="me", q=f"rfc822msgid:{first}"))["resultSizeEstimate"])
        cal = api(args, u, "calendar", "v3")
        items, token = [], None
        while True:
            page = run(cal.events().list(calendarId="primary", timeMin="2026-08-01T00:00:00Z", timeMax="2027-02-01T00:00:00Z",
                                         maxResults=250, pageToken=token, fields="items(extendedProperties),nextPageToken"))
            items += page.get("items", [])
            token = page.get("nextPageToken")
            if not token:
                break
        life = sum(1 for e in items if e.get("extendedProperties", {}).get("private", {}).get("juniper") == "life")
        tz = run(cal.calendars().get(calendarId="primary", fields="timeZone"))["timeZone"]
        drive = api(args, u, "drive", "v3")
        sc = len(run(drive.files().list(q=f"name = '{SHARED_FOLDER}' and trashed = false", fields="files(id)"))["files"])
        print(f"{u}: mail {n} (pack {'yes' if has else 'no'}), calendar {len(items) - life} story + {life} life entries ({tz}), "
              f"'{SHARED_FOLDER}' visible {sc > 0}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    auth = ap.add_mutually_exclusive_group(required=True)
    auth.add_argument("--sa", help="service account email (keyless; uses the signed-in Google Cloud user)")
    auth.add_argument("--key", help="service account JSON key, kept outside Git")
    ap.add_argument("--owner", required=True, help="account whose Drive holds the shared folder, e.g. maria@DOMAIN")
    ap.add_argument("--users", required=True, help="comma-separated participant addresses")
    ap.add_argument("--only", default="drive,gmail,calendar,life")
    ap.add_argument("--apply", action="store_true", help="really write; without it nothing changes")
    ap.add_argument("--check", action="store_true", help="only report what each account contains")
    ap.add_argument("--reimport-mail", action="store_true", help="move earlier pack emails to Trash and import them again")
    ap.add_argument("--redo-life", action="store_true", help="replace the life entries with a fresh set")
    ap.add_argument("--share-calendars-with", help="give this account read access to every participant's calendar")
    ap.add_argument("--calendar-timezone", help="set every account's calendar time zone, e.g. Europe/Berlin")
    args = ap.parse_args()
    users = [u.strip() for u in args.users.split(",") if u.strip()]
    if args.check:
        check(args, users)
        return
    if args.share_calendars_with:
        share_calendars(args, users, args.share_calendars_with)
        return
    if args.calendar_timezone:
        set_timezone(args, users, args.calendar_timezone)
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
        if "life" in parts:
            seed_life(args, u)
    if not args.apply:
        print("Dry run. Add --apply to write.")


if __name__ == "__main__":
    main()
