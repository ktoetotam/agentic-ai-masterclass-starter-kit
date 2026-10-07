# Bank statements pack: five kinds of account, real export formats

**Fictional workshop data.** Banks, wallets, people, IBANs (`DE00...`), ISINs (`XX...`), card numbers, wallet addresses and transaction ids are invented and deliberately invalid. Every PDF carries a "not a real bank document" footer. The providers are invented on purpose; the file layouts follow what German banks, brokers, crypto exchanges and payment wallets really export. Licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), credit "AI Realist, Agentic AI Masterclass".

It belongs to the same story as the accountant pack: Juniper Workshop Lab GmbH in München, September 2026. Use it to practise reading many statement formats, or to extend the accountant agent beyond one bank.

## The files (`files/`)

| Account | Holder | File | Format |
| --- | --- | --- | --- |
| Company current account, Alpenbank Demo | Juniper Workshop Lab GmbH | `Alpenbank_Juniper_camt053_2026-09.xml` | CAMT.053 (ISO 20022 XML), what business banking delivers today: opening and closing balance, one `Ntry` per booking, German transaction codes (GVC) |
| | | `Alpenbank_Juniper_MT940_2026-09.sta` | MT940 (SWIFT text), the older format many accounting tools still import: `:60F:` opening, `:61:` booking, `:86:` details with `?20` purpose fields, `:62F:` closing |
| Personal current account, Nordlicht Direktbank | Alex Example | `Nordlicht_Girokonto_Alex-Example_2026-09.csv` | Online banking CSV: account lines above the header, semicolons, quotes, German decimal commas |
| | | `Nordlicht_Kontoauszug_Alex-Example_2026-09.pdf` | Monthly statement (Kontoauszug) |
| Securities account, Isar Depot Demo | Sam Example | `IsarDepot_Depotauszug_Sam-Example_2026-09-30.pdf` | Holdings statement (Depotauszug) per 30 Sep |
| | | `IsarDepot_Transaktionen_Sam-Example_2026-Q3.csv` | Transactions: savings plan, distribution, sale, with fees and taxes |
| Crypto exchange, Kryptonia | Sam Example | `Kryptonia_ledger_Sam-Example_2026-09.csv` | Ledger export: UTC times, one row per asset movement (a trade is two rows with the same `refid`), fee and running balance per asset |
| | | `Kryptonia_Statement_Sam-Example_2026-09.pdf` | Account statement |
| Payment wallet, PayPort (PayPal-style) | Juniper Workshop Lab GmbH | `PayPort_Aktivitaet_Juniper_2026-09.csv` | Activity download with PayPal's German column names: gross, fee, net, transaction code, related code, balance; a USD purchase shows as three rows |
| | | `PayPort_Monatsauszug_Juniper_2026-09.pdf` | Monthly statement |

## What to notice

- **The company account agrees with the accountant pack.** CAMT.053 and MT940 carry the same 14 September lines as `accountant-pack/drive/Bank statements/`: 18,240.55 at the start, 20,506.83 at the end.
- **Alex paid company costs privately.** The flight (212.40), train (34.90), parking (6.00) and café (54.30) on the personal account are lines from Alex's expense claim; the taxi (14.80) has no card line, only a cash withdrawal in Salzburg the same day. The claim (322.40) is not reimbursed yet.
- **Revenue outside the bank.** PayPort holds EUR 424.66 that never reached the company account: three sales of checklist pads, fees, a partial refund (only the percentage part of the fee comes back), a USD image licence paid through a currency conversion, and an office supplies order without an invoice in the books.
- **Taxes in the broker statement.** The distribution shows the 30 % partial exemption for equity funds, 25 % withholding tax and 5.5 % solidarity surcharge; the sale shows tax on the gain. Private accounts are not the company's books: an agent should say so.
- **Crypto needs UTC and two-row trades.** Amounts are in the asset, fees can be in EUR or in the coin, and staking rewards are income.

## Rebuild

```sh
uv run --no-project --script data/bank-statements-pack/generator/generate.py
```

The generator reads Juniper's company lines from `accountant-pack/generator/story.py` and checks that the closing balance still matches.

## Facilitator: put it in Google Workspace

```sh
uv run --no-project --script data/bank-statements-pack/generator/seed_drive.py --sa masterclass-seed@PROJECT.iam.gserviceaccount.com --owner ADMIN@DOMAIN --users a@DOMAIN,b@DOMAIN
```

Dry run first, then `--apply`. It uploads `files/` once to the owner's Drive as "Bank statements, all formats (fictional)", shares the folder read-only without notification emails and adds a shortcut to each participant's My Drive. Same tenant and service account as the second brain pack.
