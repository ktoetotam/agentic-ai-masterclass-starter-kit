# Accountant pack: Juniper Workshop Lab's September books

**Fictional workshop data.** Everything here is invented for the AI Realist Agentic AI Masterclass: the company, its customers and suppliers, invoices, bank lines and payments. Email domains end in `.invalid` or `.example`, which can never receive mail. IBANs, VAT IDs and card numbers are deliberately invalid. Every document carries a "fictional" footer. The house rules are this exercise's rules, not tax advice. Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), credit "AI Realist, Agentic AI Masterclass".

**The story.** It continues the second brain pack: same company, people and suppliers. Mira Beispiel (finance and office) closes September 2026 for Juniper Workshop Lab GmbH in München. The tax adviser files the VAT return on 10 October and wants the package by Thursday 8 October. Until September, invoices were PDFs paid by bank transfer; since 1 October they go through Stripe. **Scenario date: Thursday 8 October 2026.**

## What is in it

| Folder | What |
| --- | --- |
| `drive/` | The shared accounting folder: outgoing invoices JWL-1031 to JWL-1040, incoming invoices (one a scan of the wrong month), September bank statement as PDF and CSV, October so far as CSV, the office lease, the ClearDesk agreement with Riverbend Bakery, a call note, the customer and supplier lists and the house rules |
| `mailbox/eml/` | Mira's mailbox from September to 7 October: bills by email (one only as HTML), forwards, the expense claim with receipts, a fake "new bank details" invoice, an urgent payment request in the boss's name, Bob's question, the tax adviser's request |
| `mailbox/mira-beispiel.mbox` | The same mailbox as one file (Google Takeout format, with labels) |
| `stripe/` | `seed-manifest.json` and `snapshot/` (invoices, charges, balance transactions, payouts, balance) of the seeded Stripe sandbox |
| `answer-key/` | `expected.json`: every invoice, bill, bank line and status, 24 planted problems with what to do, 6 things that must not be flagged, and test questions. **Never give this folder to the agent.** |
| `generator/` | The scripts that build the pack, seed the Stripe sandbox and fill Google Workspace accounts |

## Deliberate traps

- **Arithmetic:** a supplier invoice whose total is EUR 10 too high; an expense claim whose total is a formula without a stored value.
- **Payments:** a Stripe payout that is charges minus fees minus a refund; an invoice paid through a Stripe payment link (count it once); an invoice Stripe shows as failed and open that was paid by bank; a payment from a group company; one paid two days after month end; GBP converted to EUR with a separate bank fee; a supplier paid through a payment provider; a card payment without any document.
- **Documents:** a reverse-charge invoice without the customer's VAT ID; a receipt billed to a person with foreign VAT; a US supplier without VAT; a scan without text from August filed in September; the same receipt as PDF and as HTML email; an e-ticket attached twice; a blurred parking receipt; a taxi ride without a receipt.
- **The online shop in Stripe:** a ClearDesk subscription with a 10% partner coupon, one cancelled the same day and refunded through a credit note, one ending at period end; learning-day seats sold through a payment link, one with an early-bird code, one refunded, one disputed (amount and fee taken back while its payment is still pending); two payouts that only add up together with the pending balance.
- **Fraud:** the same invoice sent again from a look-alike domain with a new IBAN; an urgent, secret payment request in the managing director's name.
- **Must not be flagged:** rent by direct debit (the lease is the invoice), bank fees, a cancelled invoice and its cancellation, small German receipts without the company's name, a bill that is open but not yet due.
- **The question from the intro slides:** "How much does Bob owe for the extra pads?" EUR 197.83, answered from his email, the call note, the agreement and the Stripe invoice.

## How participants use it

The `accountant-agent` challenge plugin does the work: `books.py collect` reads `drive/` and every email with its attachments, the agent writes one record per document, and `books.py` checks quotes and sums, reads the bank CSVs and Stripe, reconciles and writes a DRAFT package. `books.py grade` compares the result with the answer key. Stripe is read with a read-only sandbox key from the facilitator, or from `stripe/snapshot/` without one.

## Facilitator: seed the Stripe sandbox

About 10 minutes, the evening before. Without it the pack still works offline, but the October statement has no Stripe payout.

1. In a Stripe account with EUR as currency, open the account picker, then **Sandboxes → Create**: "Masterclass accountant (fictional)". A sandbox is isolated from live data.
2. In the sandbox: **Settings → Business → Public details**, name "Juniper Workshop Lab (fictional)". **Settings → Payouts → Payout schedule: Manual** (a script can only create a payout on a manual schedule).
3. Copy the sandbox's secret key (`sk_test_...`) and add `STRIPE_SEED_KEY=sk_test_...` to the project's `.env` (ignored by Git). Never paste it anywhere else.
4. Dry run, then create:

   ```sh
   uv run --no-project --script data/accountant-pack/generator/seed_stripe.py
   uv run --no-project --script data/accountant-pack/generator/seed_stripe.py --apply
   uv run --no-project --script data/accountant-pack/generator/generate.py
   ```

   The seed creates 12 customers, invoices JWL-1041 to JWL-1045 (paid, open, failed), a catalogue, coupons, a promotion code, two payment links, three subscriptions, four learning-day seat sales (one refunded, one disputed), the payment-link payment for JWL-1040 and manual payouts of what is available, then writes `stripe/`. The second command puts the payout into the October bank statement, the Stripe notification into the mailbox and the fees into the answer key. Re-running finds what exists and skips it. Commit the result.
5. **For participants:** in the sandbox, **Developers → API keys → Create restricted key**, mark it for agent access, and give it **Read** on balance, balance transactions, charges and refunds, disputes, customers, invoices, credit notes, payment intents, payouts, products and prices, coupons and promotion codes, subscriptions and payment links, nothing else (no Account or Settings). Hand it over in the room; participants add it as `STRIPE_API_KEY=` to their own `.env`. After the workshop, expire it.
6. Remove `STRIPE_SEED_KEY` from `.env`.

## Facilitator: fill Google Workspace accounts

After the second brain pack's Workspace setup (same tenant, service account and delegation; see its README), for the accountant group only:

```sh
uv run --no-project --script data/accountant-pack/generator/seed_workspace.py --sa masterclass-seed@PROJECT.iam.gserviceaccount.com --owner ADMIN@DOMAIN --users a@DOMAIN,b@DOMAIN
```

Dry run first, then `--apply`, then `--check`. The owner's Drive gets "Juniper accounting (fictional)" (shared read-only, no notification emails) and "Accountant pack (facilitator only)" (not shared). Each participant gets Mira's emails under the Gmail label "Juniper accounting", out of the inbox so they do not mix with Alex's second brain mail; add `--inbox` for an account without it. Mira's address in the emails becomes the account's own.

## Rebuild

The pack is generated; edit the story in `generator/story.py`, never the output:

```sh
uv run --no-project --script data/accountant-pack/generator/generate.py
```

It reuses the second brain pack's renderer and copies several of its September documents byte for byte, so both packs agree. The build checks every total and builds the answer key from the same story.
