---
name: masterclass-business-data
description: Build the workshop invoice-processing agent or spreadsheet dashboard with traceable inputs, deterministic calculations, validation and reviewable exceptions.
---

# Business data prototypes

Choose **invoice workflow** or **spreadsheet dashboard**. Use synthetic files in `data/invoices/` or `data/sales.csv` unless the participant approves other inputs. Preserve source files. Use integers in minor currency units or decimal arithmetic for money, and keep currencies explicit.

## Invoice workflow

Extract supplier, invoice ID, issue/due dates, currency, line items, net/tax/gross and stated payment details. Attach each field to a source location and flag uncertain values. Never fill missing bank details from memory or another invoice. The fixture payment field is deliberately non-payable.

Validate line arithmetic, subtotal/tax/gross consistency, date order and duplicates. Detect repeated supplier + invoice ID, but retain source filenames and conflicting copies for human review. Missing currency or inconsistent totals should enter an exception queue, not be silently fixed. The fixtures include one valid invoice, one exact duplicate and one invoice with both an inconsistent total and a missing currency; `expected.json` is the answer key, not an ingestion input.

Create a local review table/CRM and draft invoices or messages only as requested. Demonstrate a review status transition and a repeat import without duplicate customer/invoice records. Creating a bank transfer, sending an invoice, contacting a customer and updating a live finance system are distinct external actions; this workflow does not authorize them. Generated invoices are workshop drafts, not verified jurisdiction-compliant documents.

Text invoices need no PDF library. For real text PDFs, project-local `pypdf` may be enough; scanned pages require OCR or a participant-provided text export. Record extraction confidence and inspect uncertain fields. Never treat successful text extraction as proof of a correct financial value.

## Spreadsheet dashboard

Profile the source before computing: sheet names, row counts, types, units, currencies, date formats, blanks, duplicates and formula cells. The CSV fixture stores amounts in EUR cents; there are 12 rows and the expected totals are documented in `data/README.md`.

Use standard-library CSV for the baseline. Add `openpyxl` for `.xlsx` or `pandas` for useful transformations; never execute workbook macros. `openpyxl` does not calculate formulas, and `data_only=True` returns the last cached result, which can be missing or stale. Recalculate an approved copy with Excel/LibreOffice when available, or reproduce the required formulas explicitly and disclose that choice.

Separate source metrics from scenario assumptions. Label sliders/inputs with units and bounds, show the calculation and preserve the baseline. Validate one ordinary scenario, zero/empty data and an extreme valid input. Guard division by zero, rounding drift and mixed currencies. Escape display content; if exporting untrusted text to CSV for spreadsheets, prevent formula injection without altering genuine numeric values.

Minimum demo: totals reconcile to source; errors are visible; changing one scenario produces a reproducible result; repeat ingestion is safe. Keep extraction records, exception CSVs and the handover in `output/business-data/`; put only a sanitized demo dashboard in `public/business-data/`. Use HTML tables/charts and CSV if Excel, a rendering tool or APIs are unavailable.
