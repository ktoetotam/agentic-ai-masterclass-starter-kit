# The record format

One JSON file per document: `output/accountant/records/<id>.json`, where `<id>` is the document's id from `inventory.csv`. `books.py template <id>` prints an empty one. Amounts are strings with a dot for decimals (`"1606.50"`), dates `YYYY-MM-DD`. Leave a field empty (`""`) when the document does not show it.

| Field | What to write |
| --- | --- |
| `doc_id` | The document's id |
| `type` | `sales_invoice` (we invoice a customer), `cancellation` (cancels one of ours), `bill` (a supplier invoices us), `receipt` (shop, taxi, ticket, online receipt), `expense_claim`, `email`, `note`, `contract`, `other` |
| `party` | The other side: the supplier for a bill, the customer for a sales invoice, as written on the document |
| `number` | The invoice or receipt number, exactly as printed |
| `date`, `due` | Issue date and due date as printed (converted to `YYYY-MM-DD`) |
| `currency` | As printed: `EUR`, `GBP`, `USD`. Empty if the document shows none |
| `lines` | Each line: `desc`, `qty`, `unit` (unit price), `amount`, as printed |
| `net`, `vat_rate`, `vat` | As printed. `vat_rate` is the percentage (`"19"`); for reverse charge or no VAT write `"0"` |
| `gross`, `stated_gross` | `stated_gross` is the total printed on the document. `gross` too, unless you see it is wrong: the script compares both with net plus VAT |
| `billed_to` | The name and address the document is addressed to |
| `customer_vat_id` | Sales invoices: the customer's VAT ID if printed |
| `iban` | The bank account the document asks to pay to, if printed |
| `refers_to` | A cancellation or credit note: the number of the invoice it refers to |
| `read_from_image` | `true` for scans and photos you read as images |
| `rows` | Expense claims only: each row's `date`, `desc`, `amount`, `receipt` (the receipt's file name, empty if missing) |
| `sources` | For each important field: `[line, "exact words from that line"]`, at least `number` and `stated_gross` |
| `flags` | Findings: `{"code": "...", "item": "...", "finding": "...", "what_to_do": "..."}`, codes in `review-codes.md` |
| `notes` | Anything a person should know, in plain words |

## Example

From the warm-up fixture `data/invoices/invoice-001.txt`, where line 4 reads `Invoice ID: DEMO-001` and line 14 `Gross total: 300.00`:

```json
{
 "doc_id": "a1b2c3d4e5",
 "type": "sales_invoice",
 "party": "Fern Sample Studio",
 "number": "DEMO-001",
 "date": "2026-09-01",
 "due": "2026-09-15",
 "currency": "EUR",
 "lines": [
  {"desc": "Workflow session", "qty": "2", "unit": "100.00", "amount": "200.00"},
  {"desc": "Setup notes", "qty": "1", "unit": "50.00", "amount": "50.00"}
 ],
 "net": "250.00", "vat_rate": "20", "vat": "50.00", "gross": "300.00", "stated_gross": "300.00",
 "billed_to": "Fern Sample Studio", "customer_vat_id": "", "iban": "", "refers_to": "", "read_from_image": false,
 "sources": {"number": [4, "Invoice ID: DEMO-001"], "stated_gross": [14, "Gross total: 300.00"]},
 "flags": [],
 "notes": ""
}
```

The line numbers are those that `books.py lines <id>` prints, not the original file's.
