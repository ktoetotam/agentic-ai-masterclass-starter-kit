---
name: package
description: Prepare the month-end package for the tax adviser from the reconciled accountant books - a DRAFT Excel workbook and summary, plus DRAFT messages (payment reminder, payment link, request for a corrected invoice or a VAT ID) that a person reviews and sends. Use after reconcile, when someone says prepare the package for the accountant, month-end close, write the reminder or send Bob the payment link.
---

# Prepare the month-end package and drafts

The helper is `poetry run python output/accountant/.books/books.py`, written `books.py` below; run it from the project root. You write only in `output/accountant/out/`.

## 1. The workbook

Run `books.py package`. It writes `out/month-end-2026-09.xlsx` (Summary, Status, Register, Bank, Stripe, Review notes) and `out/summary.md`, both marked DRAFT. Check the tax adviser's request in the mailbox (subject "Unterlagen September / September package") and say which of the seven requested items the package covers and which it does not.

## 2. Questions for the tax adviser

Add to `out/summary.md` a short section "Questions for the tax adviser" in plain words: bills from abroad without VAT, bills addressed to a person, the reverse-charge invoice without a VAT ID, anything else in the review queue a person cannot decide alone. Do not calculate the VAT payable; the tax adviser does that.

## 3. Drafts, never sent

Write each draft as its own file in `out/drafts/`, starting with the line `DRAFT - not sent. A person checks and sends it.`:

- a friendly payment reminder for an overdue invoice (no fees, no threats);
- an answer to Bob with the amount, what it covers, and the Stripe payment link: the `hosted_invoice_url` of his invoice in `out/stripe/invoices.csv` (a sandbox link: only test cards work);
- a request for a corrected invoice, or for a customer's VAT ID, or for billing to the company.

Each draft states the facts with their source (invoice number, date, amount). Only if the participant asks and a Gmail or Outlook connector is connected, create the draft in their mailbox, one at a time, after they say yes to each; never send.

## 4. Report

Say where the files are, what a person must check before anything leaves (the review queue, every draft, the open payments), and the next message: "Use $accountant-agent-check. Check the books and prepare our demo."

## Boundaries

- Nothing is sent, paid, approved, uploaded or shared. A person does that, after reading the draft.
- No tax advice: the house rules are this exercise's rules. Say so when someone asks for a tax decision.
- Keep real names, bank details and documents of your own company out of `public/`, Git and screenshots.
