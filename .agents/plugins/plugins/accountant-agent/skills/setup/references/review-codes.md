# Review codes

Every finding in `out/review-queue.csv` has a code. **Script** codes are found by `books.py` from the records, the bank and Stripe; **agent** codes need judgement and go into a record's `flags` or `books.py flag`. A finding is a question for a person, not a decision. The house rules in `BOOKS.md` say what the company wants; they are this exercise's rules, not tax advice.

## Documents

| Code | By | Means | A person should |
| --- | --- | --- | --- |
| `TOTAL_MISMATCH` | script | The printed total is not net plus VAT | Not pay it; ask for a corrected document |
| `LINE_MISMATCH`, `NET_MISMATCH`, `VAT_MISMATCH` | script | A line, the net or the VAT does not add up | Check the document |
| `MISSING_CURRENCY` | script | No currency on the document | Ask; never assume EUR |
| `DUPLICATE` | script | The same file twice in one place, or the same supplier and number twice | Count it once; keep both files |
| `NOT_TEXT` | script | A PDF without a text layer (a scan) | Have it read as an image; check the values |
| `OUT_OF_PERIOD` | script | A bill dated before the month being closed | Check whether it was booked already |
| `FORMULA_WITHOUT_VALUE` | script | A spreadsheet total is a formula with no stored result | Let `books.py` calculate it |
| `BILLED_TO_PERSON` | script | A bill addressed to a person, not the company (abroad, or above EUR 250) | Ask the supplier to correct it; tell the tax adviser |
| `FOREIGN_NO_VAT` | script | A supplier abroad without German or EU VAT on the bill | List it for the tax adviser (reverse charge) |
| `IBAN_CHANGED` | script | The bill asks for payment to a different account than the one on file | Not pay; call the supplier on the number on file |
| `RC_WITHOUT_VAT_ID` | script | Our reverse-charge invoice to an EU business shows no customer VAT ID | Ask the customer for the VAT ID; tell the tax adviser |
| `NO_RECEIPT` | script | An expense claim line without a receipt | Ask for the receipt or a written note |
| `UNREADABLE` | agent | A value on a scan or photo cannot be read with certainty | Read it by hand |
| `CEO_FRAUD` | agent | An urgent or secret payment request, a new payee, a sender address that is almost right | Do nothing; check through a known channel |
| `CONTACT_OUTDATED` | agent | The customer or supplier list is out of date | Update it after asking |

## Bank and Stripe

| Code | By | Means | A person should |
| --- | --- | --- | --- |
| `NO_DOCUMENT` | script | A bank line nothing explains | Ask who paid and for the receipt |
| `AMOUNT_DIFFERS` | script | The bank amount differs from the invoice | Check for a partial payment or a fee |
| `CURRENCY` | script | Invoiced in another currency, paid in EUR | Record the EUR amount; fees separately |
| `PAYER_DIFFERS` | script | Someone else paid the invoice (a group company, a founder) | Note the payer |
| `PAID_AFTER_MONTH_END` | script | Paid after the month being closed | Paid, but not in this month |
| `OVERDUE` | script | A customer invoice past its due date | Approve a reminder |
| `PAYABLE_OVERDUE` | script | A bill past its due date | Pay after approval |
| `PAID_VIA_STRIPE` | script | A PDF invoice paid by card through Stripe | Count it once, inside the payout |
| `PAID_BY_BANK_NOT_STRIPE` | script | Stripe shows an invoice open, the bank shows it paid | Mark it paid outside Stripe after approval |
| `PAYOUT_IS_NOT_REVENUE` | script | A Stripe payout: payments minus fees minus refunds | Book the parts separately |
| `PAYOUT_MISMATCH` | script | The payout does not equal the payments in Stripe | Look for payments from another period |

Add your own codes when you need them: short, in capitals, and explained in `BOOKS.md`.
