---
name: reconcile
description: Reconcile the accountant books - read the bank statement files and Stripe (read-only sandbox key or snapshot), match every bank line to an invoice, bill, fee, contract or Stripe payout, find what is open, overdue or paid twice, and answer questions about payments with their sources. Use after extract, when someone says reconcile, match the bank statement, check Stripe or asks whether an invoice is paid.
---

# Reconcile bank, Stripe and documents

The helper is `poetry run python output/accountant/.books/books.py`, written `books.py` below; run it from the project root. If `out/register.csv` is missing, run the extract skill first (`books.py verify` writes it).

## Run

1. `books.py bank` reads every bank statement CSV in the pack and checks that opening balance plus the lines equals the closing balance. A PROBLEM here means a line was misread: stop and look before going on.
2. `books.py stripe` reads the Stripe sandbox with the read-only key in `.env`, or `books.py stripe --snapshot` without one.
3. `books.py verify` once more, so the review queue starts fresh.
4. `books.py reconcile` writes `out/matches.csv` (each bank line and what explains it), `out/status.csv` (each invoice and bill: paid, open, cancelled, in an expense claim, blocked, on hold) and adds its findings to `out/review-queue.csv`.

## Explain the result

Open `out/matches.csv` and `out/status.csv` and say in plain words:

- how many bank lines are explained and which are not (each one without a document is a question for a person);
- the Stripe payout broken down: what was charged, the fees, the refund, and the amount that reached the bank. A payout is not revenue;
- invoices paid through Stripe are counted once, inside the payout, never again as bank payments;
- which customer invoices are open or overdue, and which bills are open, on hold or blocked, and why.

If Stripe's own `stripe-docs` and `stripe-best-practices` skills are installed (see `../setup/references/connectors.md`), use them to check how Stripe treats refunds, disputes, dispute fees and payouts, and name the Stripe page. They explain Stripe; the amounts still come from `books.py`.

Read `out/review-queue.csv` with the participant. For each item: what it is, why it matters, what a person should do. Use `../setup/references/review-codes.md` for the meaning of each code.

## Answer questions with sources

When someone asks "Is X paid?", "How much does Bob owe?" or "Why is the payout smaller?":

1. Find the answer in `out/status.csv`, `out/matches.csv` and the Stripe files in `out/stripe/`, not from memory.
2. Read the documents behind it (`books.py lines <id>`): the invoice, the email, the note, the contract.
3. Answer with the amount, the date and the source of each fact (file and line, or the Stripe id). Say what you could not confirm.

Example: "How much does Bob owe for the extra pads?" needs the email, the call note, the agreement (VAT) and the Stripe invoice.

## Boundaries

- Read only. Never mark an invoice paid, refund, void or create anything in Stripe, even with a key that allows it. Say what a person should do in the Stripe Dashboard instead.
- A payment you cannot explain is a question for a person, not a guess.
- Never treat money from a payer with a different name as unexplained when the invoice number matches; note the payer instead.
