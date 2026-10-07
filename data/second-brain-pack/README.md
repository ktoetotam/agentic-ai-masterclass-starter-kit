# Second brain pack: Alex Example's fictional working life

**Fictional workshop data.** Everything here is invented for the AI Realist Agentic AI Masterclass: people, companies, addresses, prices, booking codes and bank details. Email domains end in `.invalid` or `.example`, which are reserved and can never receive mail. Bank details and ticket numbers are deliberately invalid. Every document carries a small "fictional" footer; the brands imitate no real company. Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), credit "AI Realist, Agentic AI Masterclass".

**The story.** Alex Example coordinates Project Lantern at Juniper Workshop Lab in München: a customer learning day on 22 October 2026. It continues the four notes in `data/knowledge/`. Alongside the project there is ordinary life: bills, subscriptions, a cancelled Lisbon trip, a London client visit, receipts, a rental contract. **Scenario date: Wednesday 7 October 2026.** Questions about "this week" or "next week" count from that date.

## What is in it

| Folder | What | Size |
| --- | --- | --- |
| `mailbox/eml/` | 84 emails from July to 6 October 2026, one `.eml` file each: threads with quoted replies, HTML newsletters, PDFs, photos, Word, Excel, ZIP, calendar invites, a forwarded email inside an email | 2.8 MB |
| `mailbox/alex-example.mbox` | The same mailbox as one file, in the format Google Takeout exports, with Gmail labels | |
| `drive/` | An organised Google Drive: Finance, Travel, Projects, Subscriptions, Meetings, Reading, Home | 9 MB |
| `downloads/` | A messy Downloads folder: duplicate copies with "(1)", phone photos named `IMG_....`, scans, an unfinished download | 9 MB |
| `notes/` | 42 Markdown notes sorted by PARA (Inbox, Projects, Areas, Resources, Archive) plus daily notes | |
| `records/` | Six small databases as CSV (for Notion) and Markdown: people, interactions, deadlines, purchases, places, someday ideas | |
| `calendar/alex-example.ics` | Alex's calendar | |
| `telegram/updates.json` | Messages to a capture bot, in the Telegram Bot API format | |
| `notion/` | A ready-made import for Notion: the notes as a ZIP; import the CSVs from `records/` as databases | |
| `answer-key/` | 40 questions with expected answers and sources, the inbox sorting key, and a template for your own questions. **Never import this folder into a brain.** | |
| `manifest.json` | Every file with size and checksum | |
| `generator/` | The scripts that build the pack, and the script that fills Google Workspace accounts | |

## Deliberate traps

Each one tests something a second brain must handle:

- **Formats** that need converting before import: `.eml`, `.docx`, `.xlsx`, `.vtt`, `.ics`, `.json`, PDF.
- **Scans and photos** without a text layer: an insurance letter, a scanned invoice, receipts photographed on a table, a 7.7 MB rental contract scan (above Notion's 5 MB free-plan upload limit).
- **Files that cannot be read as they are:** a blurred parking receipt, a password-protected bank statement (the password is not in the pack), a ZIP, a HEIC photo, an unfinished `.crdownload`.
- **Duplicates:** the same invoice as PDF and scan, files saved twice, an electricity bill paid twice, an article clipped twice.
- **Facts that changed:** budget EUR 2,000 to 2,500; a flight moved from 07:10 to 08:25 (the calendar and the trip plan still say 07:10); a hotel booking changed, then cancelled; a deadline moved; a contact changed company; prices went up.
- **Conflicts:** an AI meeting summary says "Maple Room confirmed"; the transcript says it is only on hold.
- **Arithmetic:** an invoice with a wrong total; an offer without a currency; spreadsheet totals stored as formulas without a calculated value; sums and date questions that must be calculated by code.
- **Facts only in attachments:** the deposit terms (Word file), the terminal and seat (e-ticket PDF), the intake statistic on page 17 of a 20-page report.
- **Safety:** an email with instructions to an AI assistant, a look-alike phishing email, a Telegram message from a stranger.
- **Privacy:** a colleague's sick note and forwarded bank details that should not be stored.
- **Not in the notes:** the office door code, the guest Wi-Fi password, the return train from Salzburg.

## How participants look at it (Windows)

| Data | Where to look | How the agent reads it |
| --- | --- | --- |
| Mail | Mailpit, a local inbox in the browser (below), or the Workspace Gmail if the facilitator set it up | `.eml` files, Mailpit's API, or the Gmail connector |
| Documents | The Workspace Drive folder "Juniper (fictional)", or `drive/` and `downloads/` in File Explorer | The Drive connector, or the files |
| Notes and records | Notion (import below) or Obsidian (open `notes/` as a vault) | Notion MCP, or the files |
| Calendar | The Workspace calendar, or Outlook: Add calendar > Upload from file `calendar/alex-example.ics` into a separate calendar | The `.ics` file, or a read-only calendar connector |

**Mailpit** ([download](https://github.com/axllent/mailpit/releases), Windows builds for Intel/AMD and ARM; unpack `mailpit.exe` into `output\mailpit\`). In one PowerShell window:

```powershell
output\mailpit\mailpit.exe --use-message-dates --database output\mailpit\mail.db
```

In a second window, load the mailbox once:

```powershell
output\mailpit\mailpit.exe ingest data\second-brain-pack\mailbox\eml
```

Open `http://localhost:8025`. `--use-message-dates` sorts the inbox by each email's own date. Anything sent to Mailpit's SMTP port stays on the laptop. Windows may ask once whether Mailpit may use the network: allowing private networks is enough.

**Notion.** In a separate free workspace (Notion MCP can see everything the signed-in person can see): Settings > Import > Text & Markdown, choose `notion/notes-for-notion-import.zip`; then Import > CSV for each file in `records/`. Or duplicate the facilitator's published template.

## Facilitator: fill Google Workspace accounts

Optional, for a real Gmail, Drive and Calendar per participant. About 15 minutes, at least a few hours before the workshop. Tested on 7 October 2026 with a Business Starter trial.

1. **Tenant and users.** Sign up for Google Workspace Business Starter with a dedicated domain and create one account per participant. The free trial allows 10 users including the admin. Cancelling during the trial switches the services off immediately; without billing the trial simply ends after 14 days.
2. **Google Cloud CLI** in your user folder, no shell changes ([official download](https://cloud.google.com/sdk/docs/install)); then sign in twice as the admin:

   ```sh
   CLOUDSDK_PYTHON="$(uv python find 3.13)" ~/google-cloud-sdk/bin/gcloud auth login ADMIN@DOMAIN
   CLOUDSDK_PYTHON="$(uv python find 3.13)" ~/google-cloud-sdk/bin/gcloud auth application-default login
   ```

3. **Project and service account.** Accept the Google Cloud terms once in the console if `projects create` asks for it. Service account names must be 6 to 30 characters. No key file is created: the script borrows the service account's identity through your own sign-in (role Service Account Token Creator), so the organisation's default ban on service account keys stays on.

   ```sh
   g(){ CLOUDSDK_PYTHON="$(uv python find 3.13)" "$HOME/google-cloud-sdk/bin/gcloud" "$@"; }; P=YOUR-PROJECT-ID; S=masterclass-seed@$P.iam.gserviceaccount.com
   g projects create $P && g config set project $P && g services enable gmail.googleapis.com drive.googleapis.com calendar-json.googleapis.com iamcredentials.googleapis.com
   g iam service-accounts create masterclass-seed && sleep 15 && g iam service-accounts add-iam-policy-binding $S --member user:ADMIN@DOMAIN --role roles/iam.serviceAccountTokenCreator
   g auth application-default set-quota-project $P && g iam service-accounts describe $S --format "value(oauth2ClientId)"
   ```

4. **Domain-wide delegation.** Admin console > Security > Access and data control > API controls > Domain-wide delegation > Add new: the client ID from step 3 and the scopes `https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/drive,https://www.googleapis.com/auth/calendar`.
5. **Keep mail inside (recommended).** Admin console > Apps > Google Workspace > Gmail > Compliance > Restrict delivery: allow only the workshop domain.
6. **Fill.** Dry run first, then `--apply`, then `--check`:

   ```sh
   uv run --no-project --script data/second-brain-pack/generator/seed_workspace.py --sa masterclass-seed@PROJECT.iam.gserviceaccount.com --owner ADMIN@DOMAIN --users a@DOMAIN,b@DOMAIN
   ```

   The owner's My Drive gets "Juniper (fictional)" (Alex's 49 Drive files), shared read-only with the participants without notification emails, and "Second brain pack (facilitator only)" with the answer key, not shared. Each participant gets 84 emails with original dates, labels and read state (imported, nothing is sent), the story's 16 calendar events and a "Juniper (fictional)" shortcut in My Drive. Alex's address in the emails becomes the account's own. Re-running skips what is already there.

   The calendar also gets 35 to 50 entries of everyday life, different in every account (`generator/life.py`): team routines, focus time, home and office days, an out-of-office holiday and Christmas break, doctors, a pet at the vet, children, friends, private blocks. They are built from the account's address, so the same account always gets the same life. The story's events stay identical everywhere because the answer key depends on them, and the everyday entries never sit on top of them. `--redo-life` replaces the everyday entries (marked with the private property `juniper=life`) after `life.py` changes.

   Optional: `--share-calendars-with ADMIN@DOMAIN` gives the facilitator read access to every participant's calendar, without notification emails. New accounts can start with their calendar in UTC, which shows the story's Munich times two hours early; `--calendar-timezone Europe/Berlin --apply` sets every account's calendar time zone.
7. **After the workshop.** Remove the delegation, delete the service account or the project, and let the trial end or cancel it.

## Rebuild

The pack is generated; edit the story in `generator/*.py`, never the output:

```sh
uv run --no-project --script data/second-brain-pack/generator/generate.py
```

This is a maintainer tool; participants need nothing extra. The photos in `generator/assets/photos/` were generated with Codex image generation and show no real people, brands or text. The build checks every computed answer in the answer key against the data and stops if they disagree.
