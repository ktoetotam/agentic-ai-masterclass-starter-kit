---
name: check
description: Check the accountant books end to end - libraries and Git safety, quotes and arithmetic, bank balances, the reconciliation, and on the fictional pack a grade against the answer key - then report what works and what the agent got wrong, ready for the demo. Use before the demo, after a change, or when someone asks whether their accountant agent works.
---

# Check the accountant books

The helper is `poetry run python output/accountant/.books/books.py`, written `books.py` below; run it from the project root. This skill reads and tests; it writes only the files the commands below write in `out/`.

1. `books.py doctor`: Python, pypdf and openpyxl, the books folder kept out of Git, the Stripe key (a sandbox key or none).
2. `books.py verify`: every quote is on its line, the arithmetic holds, no document is waiting for a record.
3. `books.py bank`: opening balance plus the lines equals the closing balance, for every statement.
4. `books.py reconcile`: every bank line is explained or listed as a question.
5. On the fictional pack only: `books.py grade` compares the review queue and the invoice status with `data/accountant-pack/answer-key/expected.json`. Do not open the answer key before this step and never copy from it into records: the test is whether the agent finds the problems itself.

## Report

| Status | Check | What it means |
| --- | --- | --- |
| Works | ... | ... |
| Fix | ... | One plain sentence and the fix |
| Missed | ... | A problem in the documents the agent did not find |

- Map the output: OK → Works; PROBLEM → Fix; MISSED and PARTLY from grade → Missed; FALSE → a correct document the agent wrongly flagged.
- Typical fixes: correct a quote or a line number in a record, add a missing record, read an email again for fraud signs.
- Write the misses into the group's `PLAN.md` under "What the agent got wrong". They are half of the demo.
- Say what the checks prove and what they do not: quotes exist where cited, sums are right, every bank line is explained or listed. They do not prove that a document was understood correctly, and they are not an audit or tax advice.

## Demo in five minutes

1. Bob's question ("another ~EUR 200?"): the answer with the email, the note, the agreement and the Stripe invoice as sources.
2. The bank statement: every line explained; the Stripe payout broken down into payments, fees and a refund.
3. The review queue: the fake bank details and the urgent payment request caught, the wrong total, the bill in a person's name.
4. The DRAFT package and one DRAFT message: a person decides and sends.
5. One thing the agent got wrong, and how you found it.
