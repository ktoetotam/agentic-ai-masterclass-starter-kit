# /// script
# requires-python = ">=3.12"
# dependencies = ["reportlab>=4.2"]
# ///
"""Build the bank statements pack: one fictional statement per kind of account, each in the format
that kind of provider really exports.

Maintainer tool, not needed by participants (the generated files are committed):

    uv run --no-project --script data/bank-statements-pack/generator/generate.py

Everything is fictional workshop data: banks, people, IBANs (DE00...), ISINs (XX...), wallet
addresses and transaction ids are invented and deliberately invalid. The company account reuses
Juniper Workshop Lab's September lines from the accountant pack, so both packs agree.
"""

import csv
import io
import sys
from datetime import date, datetime
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

GEN = Path(__file__).resolve().parent
PACK = GEN.parent
sys.path.insert(0, str(PACK.parent / "accountant-pack" / "generator"))
import story  # noqa: E402  (Juniper's company account, September 2026)

FICTIONAL = "Fictional workshop data · AI Realist Agentic AI Masterclass · not a real bank document"
CENT = D("0.01")


def q(x, places=CENT):
    return D(x).quantize(places, rounding=ROUND_HALF_UP)


def de(x, places=2):
    """German number format: 1.234,56"""
    s = f"{q(x, D(1).scaleb(-places)):,.{places}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def de_date(iso):
    return date.fromisoformat(iso).strftime("%d.%m.%Y")


# ------------------------------------------------------------------------------------------ PDF
STYLES = {
    "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=15, leading=19),
    "b": ParagraphStyle("b", fontName="Helvetica", fontSize=9, leading=12),
    "r": ParagraphStyle("r", fontName="Helvetica", fontSize=9, leading=12, alignment=2),
    "s": ParagraphStyle("s", fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor("#666666")),
}


def pdf(path, bank, colour, title, meta, columns, rows, widths, totals, notes=()):
    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm,
                            bottomMargin=18 * mm, title=title, author=bank, subject=FICTIONAL)
    band = Table([[Paragraph(f'<font color="white"><b>{escape(bank)}</b></font>', STYLES["h"])]], colWidths=[178 * mm])
    band.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(colour)),
                              ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story_ = [band, Spacer(1, 8), Paragraph(f"<b>{escape(title)}</b>", STYLES["h"]), Spacer(1, 6)]
    m = Table([[Paragraph(f"<b>{escape(k)}</b>", STYLES["b"]), Paragraph(escape(v), STYLES["b"])] for k, v in meta],
              colWidths=[45 * mm, 133 * mm])
    m.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    story_ += [m, Spacer(1, 10)]
    last = len(columns) - 1
    body = [[Paragraph(f"<b>{escape(c)}</b>", STYLES["r" if i == last else "b"]) for i, c in enumerate(columns)]]
    body += [[Paragraph(escape(str(c)), STYLES["r" if i == last else "b"]) for i, c in enumerate(r)] for r in rows]
    t = Table(body, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#cccccc")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f6f6")])]))
    story_ += [t, Spacer(1, 10)]
    tt = Table([[Paragraph(f"<b>{escape(k)}</b>", STYLES["b"]), Paragraph(f"<b>{escape(v)}</b>", STYLES["b"])] for k, v in totals],
               colWidths=[120 * mm, 58 * mm])
    tt.setStyle(TableStyle([("ALIGN", (1, 0), (1, -1), "RIGHT"), ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black)]))
    story_ += [tt, Spacer(1, 10)] + [Paragraph(escape(n), STYLES["s"]) for n in notes]

    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#888888"))
        canvas.drawString(16 * mm, 10 * mm, FICTIONAL)
        canvas.drawRightString(194 * mm, 10 * mm, f"Seite {d.page}")
        canvas.restoreState()

    doc.build(story_, onFirstPage=foot, onLaterPages=foot)


def write_csv(path, header, rows, delimiter=";", quoting=csv.QUOTE_MINIMAL, encoding="utf-8", preamble=()):
    with open(path, "w", newline="", encoding=encoding) as f:
        for line in preamble:
            f.write(line + "\r\n")
        w = csv.writer(f, delimiter=delimiter, quoting=quoting, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


# ------------------------------------------------------- 1. Company account: CAMT.053 and MT940
def company(out):
    c = story.COMPANY
    iban = c["iban"].replace(" ", "")
    lines = story.BANK_SEP
    opening = D(story.BANK_OPENING_SEP)
    closing = opening + sum(D(l[4]) for l in lines)
    credits = [D(l[4]) for l in lines if D(l[4]) > 0]
    debits = [-D(l[4]) for l in lines if D(l[4]) < 0]

    def code(l):
        purpose = l[3]
        if "Lastschrift" in purpose:
            return "PMNT", "IDDT", "ESDD", "105"
        if l[2] == "VISA DEBIT":
            return "PMNT", "CCRD", "POSD", "106"
        if l[2].startswith("ALPENBANK"):
            return "ACMT", "MDOP", "CHRG", "805"
        return ("PMNT", "RCDT", "ESCT", "166") if D(l[4]) > 0 else ("PMNT", "ICDT", "ESCT", "116")

    entries = []
    for i, l in enumerate(lines, 1):
        amt = D(l[4])
        dom, fam, sub, gvc = code(l)
        party = "Dbtr" if amt > 0 else "Cdtr"
        entries.append(f"""      <Ntry>
        <NtryRef>{i:04d}</NtryRef>
        <Amt Ccy="EUR">{abs(amt):.2f}</Amt>
        <CdtDbtInd>{"CRDT" if amt > 0 else "DBIT"}</CdtDbtInd>
        <Sts><Cd>BOOK</Cd></Sts>
        <BookgDt><Dt>{l[0]}</Dt></BookgDt>
        <ValDt><Dt>{l[1]}</Dt></ValDt>
        <AcctSvcrRef>ALPD-2609-{i:05d}</AcctSvcrRef>
        <BkTxCd>
          <Domn><Cd>{dom}</Cd><Fmly><Cd>{fam}</Cd><SubFmlyCd>{sub}</SubFmlyCd></Fmly></Domn>
          <Prtry><Cd>NTRF+{gvc}</Cd><Issr>DK</Issr></Prtry>
        </BkTxCd>
        <NtryDtls>
          <TxDtls>
            <Refs><EndToEndId>NOTPROVIDED</EndToEndId></Refs>
            <RltdPties><{party}><Pty><Nm>{escape(l[2])}</Nm></Pty></{party}></RltdPties>
            <RmtInf><Ustrd>{escape(l[3])}</Ustrd></RmtInf>
          </TxDtls>
        </NtryDtls>
      </Ntry>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!-- {FICTIONAL}. IBAN and BIC are invalid on purpose. -->
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.08">
  <BkToCstmrStmt>
    <GrpHdr>
      <MsgId>ALPD-CAMT053-20260930-0001</MsgId>
      <CreDtTm>2026-10-01T06:12:44+02:00</CreDtTm>
    </GrpHdr>
    <Stmt>
      <Id>ALPD-2026-09-0010</Id>
      <ElctrncSeqNb>9</ElctrncSeqNb>
      <CreDtTm>2026-10-01T06:12:44+02:00</CreDtTm>
      <FrToDt><FrDtTm>2026-09-01T00:00:00+02:00</FrDtTm><ToDtTm>2026-09-30T23:59:59+02:00</ToDtTm></FrToDt>
      <Acct>
        <Id><IBAN>{iban}</IBAN></Id>
        <Ccy>EUR</Ccy>
        <Ownr><Nm>{escape(c["name"])}</Nm></Ownr>
        <Svcr><FinInstnId><BICFI>ALPDDEMMXXX</BICFI><Nm>Alpenbank Demo AG</Nm></FinInstnId></Svcr>
      </Acct>
      <Bal><Tp><CdOrPrtry><Cd>OPBD</Cd></CdOrPrtry></Tp><Amt Ccy="EUR">{opening:.2f}</Amt><CdtDbtInd>CRDT</CdtDbtInd><Dt><Dt>2026-08-31</Dt></Dt></Bal>
      <Bal><Tp><CdOrPrtry><Cd>CLBD</Cd></CdOrPrtry></Tp><Amt Ccy="EUR">{closing:.2f}</Amt><CdtDbtInd>CRDT</CdtDbtInd><Dt><Dt>2026-09-30</Dt></Dt></Bal>
      <TxsSummry>
        <TtlNtries><NbOfNtries>{len(lines)}</NbOfNtries></TtlNtries>
        <TtlCdtNtries><NbOfNtries>{len(credits)}</NbOfNtries><Sum>{sum(credits):.2f}</Sum></TtlCdtNtries>
        <TtlDbtNtries><NbOfNtries>{len(debits)}</NbOfNtries><Sum>{sum(debits):.2f}</Sum></TtlDbtNtries>
      </TxsSummry>
{chr(10).join(entries)}
    </Stmt>
  </BkToCstmrStmt>
</Document>
"""
    (out / "Alpenbank_Juniper_camt053_2026-09.xml").write_text(xml, encoding="utf-8")

    def mt_amount(x):
        return f"{abs(x):.2f}".replace(".", ",")

    mt = [":20:STARTUMSE", ":25:00000000/0000000010", ":28C:00009/001",
          f":60F:C260831EUR{mt_amount(opening)}"]
    for l in lines:
        amt = D(l[4])
        b, v = date.fromisoformat(l[0]), date.fromisoformat(l[1])
        dom, fam, sub, gvc = code(l)
        mt.append(f":61:{v:%y%m%d}{b:%m%d}{'C' if amt > 0 else 'D'}{mt_amount(amt)}NTRFNONREF")
        purpose = l[3].replace("&", "+")
        party = l[2].replace("&", "+")
        sv = [purpose[i:i + 27] for i in range(0, len(purpose), 27)][:7]
        field = f":86:{gvc}?00{'GUTSCHRIFT' if amt > 0 else 'LASTSCHRIFT' if 'Lastschrift' in l[3] else 'UEBERWEISUNG'}"
        field += "".join(f"?{20 + i}{s}" for i, s in enumerate(sv)) + f"?32{party[:27]}"
        mt.append(field)
    mt += [f":62F:C260930EUR{mt_amount(closing)}", "-"]
    (out / "Alpenbank_Juniper_MT940_2026-09.sta").write_text("\r\n".join(mt) + "\r\n", encoding="latin-1")
    return opening, closing


# --------------------------------------------- 2. Personal current account (direct bank, CSV+PDF)
ALEX_OPEN = D("3912.40")
ALEX = [  # booking, value, type, counterparty, purpose, amount
    ("2026-09-01", "2026-09-01", "Lastschrift", "Hausverwaltung Example GmbH", "Miete 09/2026 Wohnung 3 OG links", "-980.00"),
    ("2026-09-03", "2026-09-03", "Kartenzahlung", "FRISCHMARKT DEMO MUENCHEN", "Visa Debit 4000********0071", "-46.18"),
    ("2026-09-05", "2026-09-05", "Lastschrift", "Flimmer Demo Streaming", "Abo 09/2026 Kunde 0071", "-12.99"),
    ("2026-09-08", "2026-09-08", "Kartenzahlung", "AURELIAN AIR AUR7Q2", "Visa Debit 4000********0071 Flug MUC-LHR-MUC", "-212.40"),
    ("2026-09-12", "2026-09-12", "Kartenzahlung", "FRISCHMARKT DEMO MUENCHEN", "Visa Debit 4000********0071", "-38.72"),
    ("2026-09-15", "2026-09-15", "Lastschrift", "Sportverein Demo e.V.", "Mitgliedsbeitrag Q3/2026", "-24.00"),
    ("2026-09-18", "2026-09-18", "Kartenzahlung", "SUEDBAHN SR-2026-0916-7741", "Visa Debit 4000********0071 Online-Ticket", "-34.90"),
    ("2026-09-18", "2026-09-18", "Bargeldauszahlung", "GA SALZBURG HBF", "Geldautomat Fremdbank, EUR 50,00", "-50.00"),
    ("2026-09-20", "2026-09-20", "Gutschrift", "Robin Example", "Konzertkarten Kulturhaus danke", "35.00"),
    ("2026-09-25", "2026-09-25", "Kartenzahlung", "PARKPOINT LINDENPLATZ", "Visa Debit 4000********0071", "-6.00"),
    ("2026-09-26", "2026-09-26", "Kartenzahlung", "FRISCHMARKT DEMO MUENCHEN", "Visa Debit 4000********0071", "-51.40"),
    ("2026-09-30", "2026-09-30", "Kartenzahlung", "CAFE LINDGREN", "Visa Debit 4000********0071", "-54.30"),
]


def personal(out):
    bal = ALEX_OPEN
    rows = []
    for b, v, typ, party, purpose, amt in ALEX:
        a = D(amt)
        bal += a
        payer, payee = ("Alex Example", party) if a < 0 else (party, "Alex Example")
        rows.append([de_date(b), de_date(v), "Gebucht", payer, payee, purpose, "Ausgang" if a < 0 else "Eingang",
                     "DE00000000000000000099" if typ in ("Lastschrift", "Gutschrift") else "", de(a), "", "", ""])
    pre = ['"Konto:";"Girokonto DE00000000000000000071"', f'"Kontostand vom {de_date("2026-09-30")}:";"{de(bal)} €"', '""']
    write_csv(out / "Nordlicht_Girokonto_Alex-Example_2026-09.csv",
              ["Buchungsdatum", "Wertstellung", "Status", "Zahlungspflichtige*r", "Zahlungsempfänger*in", "Verwendungszweck",
               "Umsatztyp", "IBAN", "Betrag (€)", "Gläubiger-ID", "Mandatsreferenz", "Kundenreferenz"],
              rows, quoting=csv.QUOTE_ALL, preamble=pre)
    pdf(out / "Nordlicht_Kontoauszug_Alex-Example_2026-09.pdf", "Nordlicht Direktbank (fictional)", "#1d4e6b",
        "Kontoauszug Nr. 9/2026",
        [("Kontoinhaber", "Alex Example, Farnweg 0, 80469 München"), ("Konto", "Girokonto · IBAN DE00 0000 0000 0000 0000 71 · BIC NRDLDEDEMO"),
         ("Zeitraum", "01.09.2026 – 30.09.2026"), ("Alter Kontostand", f"{de(ALEX_OPEN)} EUR")],
        ["Datum", "Wert", "Vorgang", "Empfänger / Auftraggeber · Verwendungszweck", "Betrag EUR"],
        [[de_date(b)[:6], de_date(v)[:6], t, f"{p} · {u}", de(a)] for b, v, t, p, u, a in ALEX],
        [16, 16, 26, 92, 28],
        [("Summe Eingänge", de(sum(D(r[5]) for r in ALEX if D(r[5]) > 0))),
         ("Summe Ausgänge", de(sum(D(r[5]) for r in ALEX if D(r[5]) < 0))),
         ("Neuer Kontostand 30.09.2026", f"{de(bal)} EUR")],
        ["Bitte prüfen Sie diesen Auszug. Einwendungen gegen Lastschriften sind innerhalb von acht Wochen möglich."])
    return bal


# ----------------------------------------------------- 3. Broker: securities account (PDF + CSV)
ETF = ("Welt Aktien ETF (fictional)", "XX0000000001")
BOND = ("Euro Staatsanleihen ETF (fictional)", "XX0000000002")
TECH = ("Demo Tech AG (fictional)", "XX0000000003")


def broker(out):
    tx = []  # date, type, name, isin, qty, price, gross, fee, tax, net (net is cash effect)
    for d_, price in (("2026-07-01", "142.36"), ("2026-08-03", "143.35"), ("2026-09-01", "139.70")):
        qty = q(D("500.00") / D(price), D("0.001"))  # fractional shares: the plan buys for exactly 500.00
        gross = D("500.00")
        tx.append((d_, "Sparplan Kauf", *ETF, qty, D(price), gross, D("0.00"), D("0.00"), -gross))
    # Dividend on 214.732 shares: 30 % partial exemption for an equity fund, 25 % withholding tax + 5.5 % Soli
    shares = D("214.732")
    div = q(shares * D("0.42"))
    taxable = q(div * D("0.70"))
    kest = q(taxable * D("0.25"))
    soli = q(kest * D("0.055"))
    tx.append(("2026-09-15", "Ausschüttung", *ETF, shares, D("0.42"), div, D("0.00"), kest + soli, div - kest - soli))
    # Sale of 20 shares, cost basis 900.00
    gross = q(20 * D("61.20"))
    gain = gross - D("900.00") - D("1.00")
    kest = q(gain * D("0.25"))
    soli = q(kest * D("0.055"))
    tx.append(("2026-09-22", "Verkauf", *TECH, D(20), D("61.20"), gross, D("1.00"), kest + soli, gross - D("1.00") - kest - soli))
    write_csv(out / "IsarDepot_Transaktionen_Sam-Example_2026-Q3.csv",
              ["Datum", "Typ", "Wertpapier", "ISIN", "Stück", "Kurs (EUR)", "Kurswert (EUR)", "Gebühren (EUR)",
               "Steuern (EUR)", "Betrag Verrechnungskonto (EUR)"],
              [[de_date(t[0]), t[1], t[2], t[3], de(t[4], 3), de(t[5]), de(t[6]), de(t[7]), de(t[8]), de(t[9])] for t in tx])
    holdings = [(*ETF, shares + sum(t[4] for t in tx if t[1] == "Sparplan Kauf" and t[0] > "2026-09-15"), D("141.10")),
                (*BOND, D("120"), D("48.20"))]
    hold_rows = [[n, i, de(s, 3), de(p), de(q(s * p))] for n, i, s, p in holdings]
    total = sum(q(s * p) for _, _, s, p in holdings)
    cash = D("2311.10")
    pdf(out / "IsarDepot_Depotauszug_Sam-Example_2026-09-30.pdf", "Isar Depot Demo (fictional)", "#3a5a40",
        "Depotauszug per 30.09.2026",
        [("Depotinhaber", "Sam Example"), ("Depot", "Nr. 0000000081 · Verrechnungskonto DE00 0000 0000 0000 0000 81"),
         ("Bewertung", "Schlusskurse vom 30.09.2026")],
        ["Wertpapier", "ISIN", "Stück", "Kurs EUR", "Kurswert EUR"], hold_rows, [70, 30, 24, 24, 30],
        [("Depotwert", f"{de(total)} EUR"), ("Verrechnungskonto", f"{de(cash)} EUR"), ("Gesamtvermögen", f"{de(total + cash)} EUR")],
        ["Steuerliche Angaben ohne Gewähr. Teilfreistellung für Aktienfonds 30 % (§ 20 InvStG). Kapitalertragsteuer 25 % zzgl. "
         "Solidaritätszuschlag 5,5 %; kein Freistellungsauftrag erteilt.",
         "Die Transaktionen des Quartals stehen in der CSV-Datei IsarDepot_Transaktionen_Sam-Example_2026-Q3.csv."])
    return tx


# ------------------------------------------------------------ 4. Crypto exchange: ledger export
def crypto(out):
    rows = []
    bal = {"EUR": D(0), "BTC": D(0), "ETH": D(0)}
    n = 0

    def add(t, refid, typ, sub, asset, amount, fee):
        nonlocal n
        n += 1
        amount, fee = D(amount), D(fee)
        bal[asset] += amount - fee
        places = 2 if asset == "EUR" else 8
        rows.append([f"LDG{n:04d}-DEMO-{asset}", refid, t, typ, sub, "currency", asset, "spot / main",
                     f"{amount:.{places}f}", f"{fee:.{places}f}", f"{bal[asset]:.{places}f}"])

    add("2026-09-02 06:14:22", "QDEP-0001-DEMO", "deposit", "", "EUR", "1000.00", "0.00")
    add("2026-09-02 06:20:05", "TRD-0001-DEMO", "trade", "tradespot", "EUR", "-500.00", "1.30")
    add("2026-09-02 06:20:05", "TRD-0001-DEMO", "trade", "tradespot", "BTC", "0.00816327", "0")
    add("2026-09-02 06:21:40", "TRD-0002-DEMO", "trade", "tradespot", "EUR", "-300.00", "0.78")
    add("2026-09-02 06:21:40", "TRD-0002-DEMO", "trade", "tradespot", "ETH", "0.13043478", "0")
    for d_, r in (("2026-09-09", "0.00012345"), ("2026-09-16", "0.00012400"), ("2026-09-23", "0.00012388"), ("2026-09-30", "0.00012420")):
        add(f"{d_} 01:00:00", f"STK-{d_[5:7]}{d_[8:]}-DEMO", "staking", "reward", "ETH", r, "0")
    add("2026-09-20 14:02:11", "WDR-0001-DEMO", "withdrawal", "", "BTC", "-0.00500000", "0.00002000")
    write_csv(out / "Kryptonia_ledger_Sam-Example_2026-09.csv",
              ["txid", "refid", "time", "type", "subtype", "aclass", "asset", "wallet", "amount", "fee", "balance"],
              rows, delimiter=",", quoting=csv.QUOTE_ALL)
    pdf(out / "Kryptonia_Statement_Sam-Example_2026-09.pdf", "Kryptonia Exchange (fictional)", "#4b3a6b",
        "Account statement · September 2026 (all times UTC)",
        [("Account holder", "Sam Example"), ("Account", "KRY-0000-0081 (verified)"),
         ("Withdrawal address", "bc1q-demo-0000-0000-0000-fictional (not a real address)")],
        ["Time (UTC)", "Type", "Asset", "Amount", "Fee", "Balance"],
        [[r[2], r[3] + (f"/{r[4]}" if r[4] else ""), r[6], r[8], r[9], r[10]] for r in rows], [36, 30, 16, 32, 30, 34],
        [(f"Balance {a} 30.09.2026", f"{bal[a]:.{2 if a == 'EUR' else 8}f}") for a in ("EUR", "BTC", "ETH")],
        ["Trade prices: BTC 61,250.00 EUR, ETH 2,300.00 EUR (fictional). Staking rewards are credited weekly.",
         "This statement is not a tax report. Keep the ledger export for your records."])
    return bal


# ---------------------------------------------- 5. PayPal-style wallet: activity export (CSV + PDF)
def wallet(out):
    cols = ["Datum", "Uhrzeit", "Zeitzone", "Name", "Typ", "Status", "Währung", "Brutto", "Entgelt", "Netto",
            "Absender E-Mail-Adresse", "Empfänger E-Mail-Adresse", "Transaktionscode", "Zugehöriger Transaktionscode",
            "Guthaben", "Hinweis"]
    me = "shop@juniper-workshop.invalid"
    bal = {"EUR": D("212.35"), "USD": D("0.00")}
    rows = []
    n = 0

    def fee_for(gross):
        return -q(gross * D("0.0249") + D("0.35"))

    def add(d_, t, name, typ, cur, gross, fee, sender, receiver, related="", note=""):
        nonlocal n
        n += 1
        gross, fee = D(gross), D(fee)
        net = gross + fee
        bal[cur] += net
        code = f"0DEMO{n:03d}{d_.replace('-', '')[2:]}X"
        rows.append([de_date(d_), t, "Europe/Berlin", name, typ, "Abgeschlossen", cur, de(gross), de(fee), de(net),
                     sender, receiver, code, related, de(bal[cur]), note])
        return code

    g = D("49.00"); first = add("2026-09-03", "10:42:13", "Lena Muster", "Handyzahlung", "EUR", g, fee_for(g), "lena.muster@mailbox.example", me, note="Checklisten-Pads 5er Set")
    g = D("98.00"); add("2026-09-07", "18:05:51", "Tom Beispiel", "Handyzahlung", "EUR", g, fee_for(g), "tom.beispiel@mailbox.example", me, note="Checklisten-Pads 2 Sets")
    usd = add("2026-09-10", "09:12:30", "PixStock Inc.", "Zahlung im Einzugsverfahren", "USD", "-19.00", "0.00", me, "billing@pixstock.example", note="Bildlizenz Monatsabo")
    add("2026-09-10", "09:12:30", "", "Allgemeine Währungsumrechnung", "USD", "19.00", "0.00", "", "", usd)
    add("2026-09-10", "09:12:30", "", "Allgemeine Währungsumrechnung", "EUR", "-16.53", "0.00", "", "", usd)
    add("2026-09-14", "15:30:02", "Lena Muster", "Rückzahlung", "EUR", "-24.50", "0.61", me, "lena.muster@mailbox.example", first,
        "Teilerstattung: ein Pad beschädigt")
    g = D("147.00"); add("2026-09-21", "11:48:09", "Café Lindgren", "Zahlung erhalten", "EUR", g, fee_for(g), "hallo@cafe-lindgren.example", me, note="Checklisten-Pads 3 Sets")
    add("2026-09-28", "16:20:44", "Bürobedarf Demo", "Website-Zahlung", "EUR", "-32.90", "0.00", me, "shop@buerobedarf.example", note="Bestellung 0928-DEMO")
    write_csv(out / "PayPort_Aktivitaet_Juniper_2026-09.csv", cols, rows, delimiter=",", quoting=csv.QUOTE_ALL,
              encoding="utf-8-sig")
    eur = [r for r in rows if r[6] == "EUR"]
    pdf(out / "PayPort_Monatsauszug_Juniper_2026-09.pdf", "PayPort (fictional payment wallet)", "#7a3e2b",
        "Monatsauszug September 2026",
        [("Konto", f"Geschäftskonto · {me}"), ("Kontoinhaber", "Juniper Workshop Lab GmbH"),
         ("Anfangsguthaben 01.09.2026", f"{de(D('212.35'))} EUR")],
        ["Datum", "Name", "Typ", "Brutto", "Entgelt", "Netto"],
        [[r[0][:6], r[3] or "–", r[4], r[7], r[8], r[9]] for r in eur], [16, 40, 52, 24, 22, 24],
        [("Endguthaben 30.09.2026", f"{de(bal['EUR'])} EUR"), ("USD-Guthaben 30.09.2026", f"{de(bal['USD'])} USD")],
        ["Im September wurde kein Guthaben auf ein Bankkonto übertragen. Entgelte: 2,49 % + 0,35 EUR je erhaltene Zahlung "
         "(fiktive Konditionen). Bei Rückzahlungen wird nur der prozentuale Teil des Entgelts erstattet."])
    return bal


def main():
    out = PACK / "files"
    out.mkdir(exist_ok=True)
    for f in out.iterdir():
        f.unlink()
    o, c = company(out)
    a = personal(out)
    tx = broker(out)
    k = crypto(out)
    w = wallet(out)
    assert c == D("20506.83"), c  # agrees with the accountant pack's September statement
    print(f"company   Alpenbank   {o} -> {c}")
    print(f"personal  Nordlicht   {ALEX_OPEN} -> {a}")
    print(f"broker    Isar Depot  {len(tx)} transactions")
    print(f"crypto    Kryptonia   " + ", ".join(f"{x} {v}" for x, v in k.items()))
    print(f"wallet    PayPort     EUR {w['EUR']}, USD {w['USD']}")
    for f in sorted(out.iterdir()):
        print("  ", f.name, f.stat().st_size)


if __name__ == "__main__":
    main()
