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

Optional, for a real Gmail, Drive and Calendar per participant. Allow about an hour, at least a day before the workshop.

1. **Tenant.** Sign up for Google Workspace Business Starter with a dedicated domain. The free trial allows 10 users for 14 days; without billing it ends by itself. Cancelling during the trial switches the services off immediately, so if billing was added, cancel only after the workshop.
2. **Users.** Create one account per participant (the admin counts as one of the 10), for example `brain1@` to `brain9@`, with temporary passwords.
3. **Keep mail inside.** Admin console > Apps > Google Workspace > Gmail > Compliance > Restrict delivery: allow only the workshop domain.
4. **Service account.** In the Google Cloud console create a project, enable the Gmail, Drive and Calendar APIs, and create a service account. New organisations [block key creation by default](https://cloud.google.com/resource-manager/docs/secure-by-default-organizations): as super admin, grant yourself Organization Policy Administrator and set `iam.disableServiceAccountKeyCreation` to "not enforced" for this project only. Create a JSON key and store it in `private/` (ignored by Git). Turn the policy back on afterwards.
5. **Delegation.** Admin console > Security > Access and data control > API controls > Domain-wide delegation: add the service account's client ID with the four scopes listed at the top of `generator/seed_workspace.py`.
6. **Fill.** Dry run first, then apply:

   ```sh
   uv run --no-project --script data/second-brain-pack/generator/seed_workspace.py --key private/sa.json --users brain1@DOMAIN,brain2@DOMAIN
   uv run --no-project --script data/second-brain-pack/generator/seed_workspace.py --key private/sa.json --users brain1@DOMAIN,brain2@DOMAIN --apply
   ```

   Each account gets 84 emails with original dates and labels (nothing is sent), a Drive folder "Juniper (fictional)" with 49 files, and 16 calendar events. Alex's address in the emails becomes the account's own address.
7. **After the workshop.** Delete the key, remove the delegation, and let the trial end.

## Rebuild

The pack is generated; edit the story in `generator/*.py`, never the output:

```sh
uv run --no-project --script data/second-brain-pack/generator/generate.py
```

This is a maintainer tool; participants need nothing extra. The photos in `generator/assets/photos/` were generated with Codex image generation and show no real people, brands or text. The build checks every computed answer in the answer key against the data and stops if they disagree.
