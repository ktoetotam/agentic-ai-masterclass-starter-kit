# The builds

Ten build ideas plus "bring your own problem". Each card says who it suits, what to show at the 17:00 demo, what to start from, how far to push it, where agents typically fail, and which skill builds it. Sample files under `data/` are fictional; label demos that use them "Fictional workshop data". Optional tools per challenge are in `.agents/skills/masterclass-setup/references/challenge-tools.md`.

## Quick match

| If the work is mostly about... | Consider |
| --- | --- |
| Presenting a business, product or team online | 1. Company website |
| Finding customers, partners or competitors | 2. Market & lead scout |
| Finding things in your own notes, documents and meetings | 3. Second brain |
| Presentations, pitches, training material | 4. Beyond PowerPoint |
| Video, audio, images for communication or training | 5. Media studio |
| Invoices, payments, customer records | 6. Accountant agent |
| Keeping up with a topic, market or regulation | 7. News radar |
| Translating documents or websites | 8. Localisation agent |
| Excel reports, KPIs, scenarios, calculators | 9. Spreadsheet killer |
| Something else that repeats every week | 10. Bring your own problem |

## 1. A company website

- **Idea:** a polished website deployed on the web, adapted to your brand, with good design and SEO.
- **Suits:** marketing, founders, freelancers, communications, anyone who owns a business or team page.
- **Show at 17:00:** the site works on a phone and a laptop, is live at the workshop URL, and its main button gives an honest result.
- **Start from:** `data/company-brief.md`, or your own brief, approved text and images you own.
- **By lunch:** one page running in the local preview.
- **Push further:** more pages, brand adaptation, accessibility pass, SEO metadata, deployment.
- **Where agents fail, so test it:** invented testimonials, numbers or certifications; a contact form that looks like it sent something but did not; layouts that break on a phone. Check at phone width, using only the keyboard, and click every link.
- **Skill:** `masterclass-web`, then `masterclass-deploy`.

## 2. Market & lead scout

- **Idea:** research your market, competitors and likely customers; build customer profiles, score leads, draft tailored outreach and track follow-ups.
- **Suits:** sales, business development, founders, partnerships, procurement.
- **Show at 17:00:** a shortlist where every score can be explained, every fact links to its source, and outreach drafts exist that nobody has sent.
- **Start from:** `data/leads.csv` (four fictional companies), or your own target-market definition plus public websites.
- **By lunch:** the sample list scored, with the reason for each score.
- **Push further:** live research on public pages, competitor profiles, a follow-up tracker, drafts tailored to a real observation.
- **Where agents fail, so test it:** made-up email addresses or contacts; confident scores on thin evidence; outdated pages treated as current. Check that a missing email stays blank, every claim has a link, and changing a scoring rule changes the ranking as expected.
- **Skill:** `masterclass-research` (lead scout).

## 3. Build your second brain

- **Idea:** turn notes, documents, meeting transcripts and saved links into a private assistant that finds answers, connects ideas and points to the source.
- **Suits:** anyone drowning in documents: managers, consultants, researchers, project leads.
- **Show at 17:00:** ask a question and get an answer that points to the exact source passage, and see it admit when something is not in the notes.
- **Start from:** the four notes in `data/knowledge/`. `evaluation.json` there is the answer key, not a note. Use your own material only if you may send it to this AI service; a local folder does not mean the AI runs locally.
- **By lunch:** questions about the sample notes answered with sources.
- **Push further:** your own notes, links between related ideas, PDFs, meeting transcripts, a browsable view of the notes.
- **Where agents fail, so test it:** mixing an old fact with a newer one; citing a passage that does not say it; inventing an answer instead of "not found". Check: the budget is EUR 2,500, revised from EUR 2,000; the office door code is not in the notes; importing twice does not create duplicates.
- **Skill:** the `second-brain` plugin. First message: "Set up the second brain challenge: follow `.agents/plugins/plugins/second-brain/skills/setup/SKILL.md`." After setup, `second-brain-ingest`, `second-brain-ask` and `second-brain-check`. Developers who want to build their own search app use `masterclass-knowledge`.

## 4. Beyond PowerPoint

- **Idea:** a beautiful HTML deck you send as a link: animated, optionally narrated, shareable, downloadable as PDF.
- **Suits:** anyone who presents: managers, trainers, sales, consultants.
- **Show at 17:00:** the deck runs in a browser with keyboard navigation and exports to a readable PDF.
- **Start from:** `data/company-brief.md` and `data/media/storyboard.md`, or your own talk outline.
- **By lunch:** five slides running in the local preview.
- **Push further:** animation, narration, a share link through deployment, a clean PDF.
- **Where agents fail, so test it:** text that overflows or gets cut off in the PDF; facts without sources; sound that plays automatically. A password typed into the page is not real protection. Voice cloning only with the voice owner's permission. Print to PDF and look at every page.
- **Skill:** `masterclass-present-media` (HTML deck).

## 5. Media studio

- **Idea:** videos, podcasts, music and images for training, communications and marketing.
- **Suits:** communications, marketing, HR and training teams.
- **Show at 17:00:** a 15–30 second piece with captions, or a narrated storyboard, that plays.
- **Start from:** `data/media/storyboard.md`, or your own script and images you own.
- **By lunch:** the storyboard and script, with a first playable sequence.
- **Push further:** generated images, audio or video, music, several formats.
- **Where agents fail, so test it:** costs grow quickly with retries; characters and style drift between shots; text inside generated images comes out garbled; unclear image rights. Agree a spending limit before any paid generation; ChatGPT Plus does not include API credits. Keep a list of every asset and its source.
- **Skill:** `masterclass-present-media` (media studio).

## 6. Accountant agent

- **Idea:** process invoices, extract payment details, create invoices, build a customer CRM and track communication.
- **Suits:** finance, accounting, office management, small business owners.
- **Show at 17:00:** invoices go in, fields come out with their source, and duplicates and wrong totals land in a review list for a human.
- **Start from:** the three text invoices in `data/invoices/`. `expected.json` is the answer key, not an invoice.
- **By lunch:** fields extracted from the sample invoices into a table.
- **Push further:** PDF invoices, invoice drafts, a small customer table, a status history.
- **Where agents fail, so test it:** arithmetic done by the AI instead of by code; guessed currency or bank details; scanned PDFs it cannot read. Check: three files become two invoices because one is a duplicate; the wrong total and the missing currency are flagged; nothing is paid or sent.
- **Skill:** `masterclass-business-data` (invoice workflow).

## 7. News radar

- **Idea:** an analytics dashboard for the latest news on your topic, with executive briefings, audio summaries or another feature you want to test.
- **Suits:** strategy, communications, market intelligence, regulatory affairs, anyone tracking a field.
- **Show at 17:00:** a dashboard where duplicates are removed, each item links to its source, and a "last updated" time is visible.
- **Start from:** `data/news/feed.xml` and `data/news/source-notes.md` (fictional), or public RSS feeds on your topic.
- **By lunch:** the sample feed shown as a deduplicated list.
- **Push further:** live feeds, an executive briefing, an audio summary, filters by topic.
- **Where agents fail, so test it:** summaries written from the headline only; publication date confused with the date of the event; old items called "latest". Check: five sample items become four; the undated story is flagged; every summary links to its source.
- **Skill:** `masterclass-research` (news radar).

## 8. Localisation agent

- **Idea:** translate documents and localise websites, check facts and terminology, keep content aligned with your brand and relevant standards.
- **Suits:** localisation, marketing, documentation, international teams.
- **Show at 17:00:** translated content with the glossary applied, placeholders intact and a QA report listing open questions.
- **Start from:** `data/localisation/` (`en.json`, `glossary.csv`, `brief.md`), or your own text and glossary.
- **By lunch:** the seven sample strings translated with placeholders preserved.
- **Push further:** whole pages or documents, Word files, terminology and fact checks, a human review queue.
- **Where agents fail, so test it:** broken placeholders such as `{count}`; wrong plural forms; terminology that drifts; claims of standards compliance. Automated checks are not linguistic sign-off or certification.
- **Skill:** `masterclass-localise`.

## 9. The spreadsheet killer

- **Idea:** turn an Excel file into an interactive dashboard or calculator, with scenarios, financial impact and an agent that explains what changed.
- **Suits:** controlling, finance, operations, sales operations, anyone who rebuilds the same report every month.
- **Show at 17:00:** a dashboard whose totals match the source, and a scenario that changes the numbers predictably.
- **Start from:** `data/sales.csv` (12 rows), or a copy of your own spreadsheet without confidential figures.
- **By lunch:** totals and one chart from the sample.
- **Push further:** Excel files, scenarios with clear assumptions, an explanation of what changed between versions.
- **Where agents fail, so test it:** totals calculated by the AI instead of by code; stale formula values read from Excel; mixed currencies. Check: 110 units and EUR 13,250.00 revenue; raising revenue by 10% gives EUR 14,575.00 revenue and EUR 7,950.00 gross profit.
- **Skill:** `masterclass-business-data` (spreadsheet dashboard).

## 10. Bring your own problem

- **Idea:** the thing at work that eats your Friday afternoon, often the best build in the room.
- **Suits:** everyone with a recurring task that takes an input and produces something a person checks.
- **Show at 17:00:** one real task from your week: input goes in, a useful output comes out, and you show how you check it.
- **Start from:** your own example, or the request-triage example in `data/problem-brief.md`.
- **By lunch:** one input turned into one output.
- **Push further:** a review step, a change log, more input types, a shareable page.
- **Where agents fail, so test it:** scope that grows all day; dependence on systems you cannot connect today; "fully automatic" with no human check. Write the success criteria first and check that a second run does not create duplicates.
- **Skill:** `masterclass-build`.
