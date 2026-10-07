# /// script
# requires-python = ">=3.12"
# dependencies = ["google-api-python-client>=2.150", "google-auth>=2.35", "requests>=2.32"]
# ///
"""Put the bank statements pack into the workshop Google Workspace.

For the facilitator only, after the second brain pack's setup (same tenant, service account and
domain-wide delegation; see ../../second-brain-pack/README.md). Uploads files/ once to the owner's
My Drive, shares the folder read-only with the participants (no notification emails) and adds a
shortcut to each participant's My Drive. Without --apply it only prints what it would do.

  uv run --no-project --script data/bank-statements-pack/generator/seed_drive.py \\
      --sa seed@PROJECT.iam.gserviceaccount.com --owner maria@DOMAIN --users a@DOMAIN,b@DOMAIN
"""

import argparse
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PACK.parent / "second-brain-pack" / "generator"))
import seed_workspace as sw  # noqa: E402  (keyless credentials, retries and uploads)

FOLDER = "Bank statements, all formats (fictional)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    auth = ap.add_mutually_exclusive_group(required=True)
    auth.add_argument("--sa", help="service account email (keyless; uses the signed-in Google Cloud user)")
    auth.add_argument("--key", help="service account JSON key, kept outside Git")
    ap.add_argument("--owner", required=True)
    ap.add_argument("--users", required=True, help="comma-separated participant addresses")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    users = [u.strip() for u in args.users.split(",") if u.strip()]
    files = sorted(p for p in (PACK / "files").iterdir() if p.is_file())
    if not args.apply:
        print(f"Would upload {len(files)} files to '{FOLDER}' in {args.owner}'s Drive and share it read-only with {len(users)} people.")
        print("Dry run: nothing changed. Add --apply to write.")
        return
    drive = sw.api(args, args.owner, "drive", "v3")
    folder = sw.find_folder(drive, FOLDER)
    if folder:
        print(f"'{FOLDER}' already exists, upload skipped")
    else:
        folder = sw.run(drive.files().create(body={"name": FOLDER, "mimeType": sw.FOLDER,
                                                   "description": "Fictional workshop data: bank statements in real export formats."},
                                             fields="id"))["id"]
        sw.upload_tree(drive, PACK / "files", folder, FOLDER)
    existing = {p.get("emailAddress", "").lower() for p in
                sw.run(drive.permissions().list(fileId=folder, fields="permissions(emailAddress)"))["permissions"]}
    for u in users:
        if u.lower() not in existing:
            sw.run(drive.permissions().create(fileId=folder, sendNotificationEmail=False,
                                              body={"type": "user", "role": "reader", "emailAddress": u}))
    for u in users:
        udrive = sw.api(args, u, "drive", "v3")
        q = f"name = '{FOLDER}' and mimeType = 'application/vnd.google-apps.shortcut' and 'root' in parents and trashed = false"
        if not sw.run(udrive.files().list(q=q, fields="files(id)"))["files"]:
            sw.run(udrive.files().create(body={"name": FOLDER, "mimeType": "application/vnd.google-apps.shortcut",
                                               "shortcutDetails": {"targetId": folder}}, fields="id"))
    print(f"'{FOLDER}' shared read-only with {len(users)} people, shortcut in each My Drive")
    print(f"Link: https://drive.google.com/drive/folders/{folder}")


if __name__ == "__main__":
    main()
