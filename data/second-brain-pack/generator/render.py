"""Renderers: PDFs with letterheads, receipts, e-tickets, a long report, a contract, and
scanned or photographed copies. Deterministic: every random choice uses a seeded Random."""

import io
import math
import random
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pypdfium2 as pdfium
import segno
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader, simpleSplit
from reportlab.pdfgen import canvas

from world import BRANDS, FOOTER_DE, FOOTER_EN

LABELS = {
    "en": dict(number="Number", date="Date", desc="Description", qty="Qty", unit="Unit price", amount="Amount",
               net="Net", vat="VAT", total="Total", total_incl="Total incl. VAT", page="Page", to="To"),
    "de": dict(number="Nummer", date="Datum", desc="Beschreibung", qty="Menge", unit="Einzelpreis", amount="Betrag",
               net="Netto", vat="MwSt.", total="Gesamt", total_incl="Gesamt inkl. MwSt.", page="Seite", to="An"),
    "it": dict(number="Numero", date="Data", desc="Descrizione", qty="Qtà", unit="Prezzo", amount="Importo",
               net="Imponibile", vat="IVA", total="Totale", total_incl="Totale", page="Pagina", to="A"),
}

D = Decimal


def money(value, lang="en"):
    q = D(value).quantize(D("0.01"), rounding=ROUND_HALF_UP)
    text = f"{q:,.2f}"
    if lang == "de":
        text = text.replace(",", "X").replace(".", ",").replace("X", ".")
    return text


def fmt_date(iso, lang):
    y, m, d = iso.split("-")
    if lang == "de":
        return f"{d}.{m}.{y}"
    if lang == "it":
        return f"{d}/{m}/{y}"
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return f"{int(d)} {months[int(m) - 1]} {y}"


def rgb(c):
    return tuple(v / 255 for v in c)


def new_canvas(path, title, brand, size=A4):
    c = canvas.Canvas(str(path), pagesize=size, invariant=1, pageCompression=1)
    c.setTitle(title)
    c.setAuthor(BRANDS[brand]["name"] + " (fictional)")
    c.setSubject("Fictional workshop document")
    c.setKeywords("fictional: true; AI Realist Agentic AI Masterclass")
    c.setCreator("second-brain-pack generator")
    return c


def draw_logo(c, brand, x, y, s):
    b = BRANDS[brand]
    c.setFillColorRGB(*rgb(b["color"]))
    c.setStrokeColorRGB(*rgb(b["color"]))
    shape = b.get("logo", "circle")
    if shape == "circle":
        c.circle(x + s / 2, y + s / 2, s / 2, stroke=0, fill=1)
    elif shape == "square":
        c.roundRect(x, y, s, s, s * 0.18, stroke=0, fill=1)
    elif shape == "diamond":
        p = c.beginPath(); p.moveTo(x + s / 2, y + s); p.lineTo(x + s, y + s / 2); p.lineTo(x + s / 2, y); p.lineTo(x, y + s / 2); p.close()
        c.drawPath(p, stroke=0, fill=1)
    elif shape == "leaf":
        p = c.beginPath(); p.moveTo(x, y); p.curveTo(x, y + s, x + s, y + s, x + s, y + s); p.curveTo(x + s, y, x, y, x, y); p.close()
        c.drawPath(p, stroke=0, fill=1)
    elif shape == "arch":
        c.rect(x, y, s, s * 0.55, stroke=0, fill=1)
        c.circle(x + s / 2, y + s * 0.55, s / 2, stroke=0, fill=1)
    elif shape == "sun":
        c.circle(x + s / 2, y + s / 2, s * 0.32, stroke=0, fill=1)
        c.setLineWidth(s * 0.07)
        for i in range(8):
            a = i * math.pi / 4
            c.line(x + s / 2 + math.cos(a) * s * 0.4, y + s / 2 + math.sin(a) * s * 0.4,
                   x + s / 2 + math.cos(a) * s * 0.5, y + s / 2 + math.sin(a) * s * 0.5)
    elif shape == "wave":
        c.setLineWidth(s * 0.12)
        for k in range(3):
            p = c.beginPath(); yy = y + s * (0.25 + 0.25 * k)
            p.moveTo(x, yy); p.curveTo(x + s * 0.3, yy + s * 0.15, x + s * 0.6, yy - s * 0.15, x + s, yy)
            c.drawPath(p, stroke=1, fill=0)
    elif shape == "wing":
        p = c.beginPath(); p.moveTo(x, y + s * 0.2); p.lineTo(x + s, y + s); p.lineTo(x + s * 0.55, y + s * 0.2); p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1)
    initials = "".join(w[0] for w in b["name"].replace("&", "").split()[:2]).upper()
    if shape not in ("wave", "sun"):
        c.setFont("Helvetica-Bold", s * 0.34)
        c.drawCentredString(x + s / 2, y + s * 0.36, initials)


def header(c, brand, w, h):
    b = BRANDS[brand]
    draw_logo(c, brand, 18 * mm, h - 30 * mm, 14 * mm)
    c.setFillColorRGB(*rgb(b["color"]))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(36 * mm, h - 21 * mm, b["name"])
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.setFont("Helvetica", 8)
    c.drawString(36 * mm, h - 26 * mm, b.get("address", ""))
    c.drawRightString(w - 18 * mm, h - 21 * mm, "www." + b["domain"])
    c.drawRightString(w - 18 * mm, h - 26 * mm, "service@" + b["domain"])
    c.setStrokeColorRGB(*rgb(b["color"]))
    c.setLineWidth(1.2)
    c.line(18 * mm, h - 34 * mm, w - 18 * mm, h - 34 * mm)


def footer(c, brand, lang, page, pages, w):
    b = BRANDS[brand]
    c.setStrokeColorRGB(0.8, 0.8, 0.8); c.setLineWidth(0.5)
    c.line(18 * mm, 18 * mm, w - 18 * mm, 18 * mm)
    c.setFillColorRGB(0.45, 0.45, 0.45); c.setFont("Helvetica", 7)
    left = b["name"] + " · " + b.get("address", "")
    if b.get("reg"):
        left += " · " + b["reg"]
    c.drawString(18 * mm, 14 * mm, left[:150])
    c.drawRightString(w - 18 * mm, 14 * mm, f"{LABELS[lang]['page']} {page}/{pages}")
    c.setFont("Helvetica-Oblique", 6.5)
    c.drawString(18 * mm, 10 * mm, FOOTER_DE if lang == "de" else FOOTER_EN)


def wrap(c, text, x, y, width, font="Helvetica", size=10, leading=14):
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def qr_image(data, scale=4):
    buf = io.BytesIO()
    segno.make(data, error="m").save(buf, kind="png", scale=scale, border=1)
    buf.seek(0)
    return ImageReader(buf)


def totals_of(doc):
    lines_sum = sum((D(l["amount"]) for l in doc.get("lines", [])), D("0"))
    if doc.get("vat_rate"):
        rate = D(doc["vat_rate"]) / D(100)
        vat = (lines_sum * rate).quantize(D("0.01"), rounding=ROUND_HALF_UP)
        return dict(net=lines_sum, vat=vat, total=lines_sum + vat)
    return dict(net=None, vat=None, total=lines_sum)


def render_document(doc, path):
    """A4 letterhead document: bill, invoice, quote, booking, ticket, letter, statement."""
    lang = doc.get("lang", "en"); lab = LABELS[lang]; brand = doc["brand"]
    w, h = A4
    c = new_canvas(path, f"{doc['title']} {doc.get('number', '')}".strip(), brand)
    header(c, brand, w, h)
    y = h - 46 * mm
    if doc.get("to"):
        c.setFillColorRGB(0.4, 0.4, 0.4); c.setFont("Helvetica", 7)
        c.drawString(18 * mm, y + 4 * mm, BRANDS[brand]["name"] + " · " + BRANDS[brand].get("address", ""))
        c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica", 10)
        for i, line in enumerate(doc["to"]):
            c.drawString(18 * mm, y - i * 5 * mm, line)
    # meta box on the right
    meta = []
    if doc.get("number"):
        meta.append((lab["number"], doc["number"]))
    meta.append((lab["date"], fmt_date(doc["date"], lang)))
    meta += doc.get("meta", [])
    my = h - 44 * mm
    for k, v in meta:
        c.setFont("Helvetica", 8); c.setFillColorRGB(0.4, 0.4, 0.4)
        c.drawString(112 * mm, my, k)
        c.setFont("Helvetica-Bold", 8); c.setFillColorRGB(0, 0, 0)
        lines = simpleSplit(str(v), "Helvetica-Bold", 8, 52 * mm)
        for j, line in enumerate(lines):
            c.drawString(140 * mm, my - j * 3.6 * mm, line)
        my -= (len(lines) * 3.6 + 1.6) * mm
    y = min(y - 30 * mm, my - 8 * mm)
    c.setFillColorRGB(*rgb(BRANDS[brand]["color"])); c.setFont("Helvetica-Bold", 15)
    c.drawString(18 * mm, y, doc["title"])
    y -= 10 * mm
    c.setFillColorRGB(0, 0, 0)
    for para in doc.get("paragraphs", []):
        y = wrap(c, para, 18 * mm, y, w - 36 * mm) - 4
    if doc.get("lines"):
        cols = [18 * mm, 120 * mm, 140 * mm, 192 * mm]
        c.setFillColorRGB(0.94, 0.94, 0.94); c.rect(18 * mm, y - 2 * mm, w - 36 * mm, 7 * mm, stroke=0, fill=1)
        c.setFillColorRGB(0.2, 0.2, 0.2); c.setFont("Helvetica-Bold", 8.5)
        c.drawString(cols[0] + 2, y, lab["desc"]); c.drawRightString(cols[1] + 10 * mm, y, lab["qty"])
        c.drawRightString(cols[2] + 20 * mm, y, lab["unit"]); c.drawRightString(cols[3], y, lab["amount"])
        y -= 8 * mm
        c.setFont("Helvetica", 9); c.setFillColorRGB(0, 0, 0)
        for l in doc["lines"]:
            dl = simpleSplit(l["desc"], "Helvetica", 9, 95 * mm)
            for j, t in enumerate(dl):
                c.drawString(cols[0] + 2, y - j * 4 * mm, t)
            c.drawRightString(cols[1] + 10 * mm, y, l["qty"]); c.drawRightString(cols[2] + 20 * mm, y, l["unit"])
            c.drawRightString(cols[3], y, money(l["amount"], lang))
            y -= (len(dl) * 4 + 2.5) * mm
        c.setStrokeColorRGB(0.7, 0.7, 0.7); c.line(120 * mm, y + 3 * mm, 192 * mm, y + 3 * mm)
        t = totals_of(doc)
        cur = (" " + doc["currency"]) if doc.get("currency") else ""
        rows = []
        if t["net"] is not None:
            rows += [(lab["net"], money(t["net"], lang) + cur), (f"{lab['vat']} {doc['vat_rate']}%", money(t["vat"], lang) + cur)]
        total_value = doc.get("stated_total") or doc.get("total") or str(t["total"])
        rows.append((lab["total"] if doc.get("gross_only") or t["net"] is not None else lab["total_incl"], money(total_value, lang) + cur))
        for i, (k, v) in enumerate(rows):
            last = i == len(rows) - 1
            c.setFont("Helvetica-Bold" if last else "Helvetica", 10 if last else 9)
            c.drawString(122 * mm, y, k); c.drawRightString(192 * mm, y, v)
            y -= 6 * mm
        y -= 4 * mm
    for note in doc.get("notes", []):
        y = wrap(c, note, 18 * mm, y, w - 36 * mm, size=9, leading=12.5) - 3
    if doc.get("qr"):
        c.drawImage(qr_image(doc["qr"]), w - 52 * mm, 26 * mm, 32 * mm, 32 * mm)
        c.setFont("Helvetica", 6.5); c.drawRightString(w - 20 * mm, 24 * mm, "FICTIONAL - NOT VALID")
    footer(c, brand, lang, 1, 1, w)
    c.showPage(); c.save()


def render_receipt(doc, path):
    """Narrow till receipt in a monospaced font."""
    lang = doc.get("lang", "de"); brand = doc["brand"]; b = BRANDS[brand]
    width = 80 * mm
    n = len(doc["lines"])
    height = (128 + n * 9 + len(doc.get("notes", [])) * 5) * mm / 1.6
    c = new_canvas(path, f"{doc['title']} {doc['number']}", brand, size=(width, height))
    y = height - 10 * mm
    draw_logo(c, brand, width / 2 - 5 * mm, y - 8 * mm, 10 * mm)
    y -= 13 * mm
    c.setFillColorRGB(0, 0, 0); c.setFont("Courier-Bold", 11); c.drawCentredString(width / 2, y, b["name"].upper()); y -= 4.5 * mm
    c.setFont("Courier", 7.5); c.drawCentredString(width / 2, y, b.get("address", "")); y -= 6 * mm
    c.drawString(5 * mm, y, f"{doc['title']} {doc['number']}"); c.drawRightString(width - 5 * mm, y, f"{fmt_date(doc['date'], lang)} {doc.get('time', '')}"); y -= 3 * mm
    c.setDash(1, 2); c.line(5 * mm, y, width - 5 * mm, y); c.setDash(); y -= 5 * mm
    c.setFont("Courier", 8)
    for l in doc["lines"]:
        c.drawString(5 * mm, y, f"{l['qty']} x {l['desc']}"[:34])
        c.drawRightString(width - 5 * mm, y, money(l["amount"], "en"))
        y -= 4.5 * mm
    c.setDash(1, 2); c.line(5 * mm, y + 2 * mm, width - 5 * mm, y + 2 * mm); c.setDash(); y -= 3 * mm
    c.setFont("Courier-Bold", 11)
    total_label = {"de": "SUMME", "it": "TOTALE", "en": "TOTAL"}[lang]
    c.drawString(5 * mm, y, f"{total_label} {doc['currency']}"); c.drawRightString(width - 5 * mm, y, money(doc["total"], "en")); y -= 6 * mm
    c.setFont("Courier", 7.5)
    c.drawString(5 * mm, y, doc.get("payment", "")); y -= 4 * mm
    for note in doc.get("notes", []):
        c.drawString(5 * mm, y, note); y -= 4 * mm
    y -= 2 * mm
    bc = code128.Code128("FICT" + doc["number"].replace("-", ""), barHeight=8 * mm, barWidth=0.32 * mm)
    bc.drawOn(c, (width - bc.width) / 2, y - 8 * mm)
    y -= 13 * mm
    c.setFont("Courier", 6.5)
    c.drawCentredString(width / 2, y, {"de": "Vielen Dank für Ihren Besuch!", "it": "Grazie e arrivederci!", "en": "Thank you!"}[lang]); y -= 3.5 * mm
    c.drawCentredString(width / 2, y, "FICTIONAL WORKSHOP RECEIPT")
    c.showPage(); c.save()


def render_eticket(doc, path):
    brand = doc["brand"]; w, h = A4; b = BRANDS[brand]
    c = new_canvas(path, f"E-ticket {doc['number']}", brand)
    header(c, brand, w, h)
    y = h - 48 * mm
    c.setFont("Helvetica-Bold", 16); c.setFillColorRGB(*rgb(b["color"])); c.drawString(18 * mm, y, doc["title"]); y -= 10 * mm
    c.setFillColorRGB(0, 0, 0)
    boxes = [("Passenger", doc["passenger"]), ("Booking reference", doc["number"]), ("Ticket number", doc["ticket"]),
             ("Issued", fmt_date(doc["date"], "en"))]
    for i, (k, v) in enumerate(boxes):
        x = 18 * mm + i * 44 * mm
        c.setFillColorRGB(0.95, 0.95, 0.95); c.rect(x, y - 12 * mm, 42 * mm, 14 * mm, stroke=0, fill=1)
        c.setFillColorRGB(0.4, 0.4, 0.4); c.setFont("Helvetica", 7); c.drawString(x + 2 * mm, y - 1 * mm, k)
        c.setFillColorRGB(0, 0, 0); c.setFont("Helvetica-Bold", 10); c.drawString(x + 2 * mm, y - 7 * mm, v)
    y -= 24 * mm
    for f in doc["flights"]:
        c.setStrokeColorRGB(*rgb(b["color"])); c.setLineWidth(0.8); c.rect(18 * mm, y - 30 * mm, w - 36 * mm, 34 * mm, stroke=1, fill=0)
        c.setFont("Helvetica-Bold", 11); c.drawString(22 * mm, y - 3 * mm, f"{f['date']}   {f['flight']}")
        c.setFont("Helvetica", 9)
        c.drawString(22 * mm, y - 11 * mm, "Departure"); c.drawString(22 * mm, y - 16 * mm, f["dep"])
        c.setFont("Helvetica-Bold", 14); c.drawString(22 * mm, y - 23 * mm, f["dep_time"])
        c.setFont("Helvetica", 9)
        c.drawString(100 * mm, y - 11 * mm, "Arrival"); c.drawString(100 * mm, y - 16 * mm, f["arr"])
        c.setFont("Helvetica-Bold", 14); c.drawString(100 * mm, y - 23 * mm, f["arr_time"])
        c.setFont("Helvetica", 8.5)
        c.drawRightString(w - 22 * mm, y - 11 * mm, f"Seat {f['seat']} · {f['cls']}")
        c.drawRightString(w - 22 * mm, y - 16 * mm, f"Baggage {f['bag']}")
        y -= 40 * mm
    c.setFont("Helvetica-Bold", 10); c.drawString(18 * mm, y, "Fare"); y -= 6 * mm
    c.setFont("Helvetica", 9)
    for k, v in doc["fare"]:
        c.drawString(18 * mm, y, k); c.drawRightString(110 * mm, y, f"{money(v)} {doc['currency']}"); y -= 5 * mm
    y -= 4 * mm
    for note in ["Check-in closes 45 minutes before departure. Bag drop closes 40 minutes before departure.",
                 "Times are local. Please check your booking before travelling; schedules can change."]:
        y = wrap(c, note, 18 * mm, y, w - 80 * mm, size=8.5, leading=11)
    c.drawImage(qr_image(f"FICTIONAL ETICKET {doc['number']} {doc['ticket']} NOT VALID"), w - 52 * mm, 26 * mm, 32 * mm, 32 * mm)
    footer(c, brand, "en", 1, 1, w)
    c.showPage(); c.save()


REPORT_SECTIONS = [
    ("About this report", ["Small Teams Weekly surveyed 412 fictional teams of 5 to 50 people in Germany, Austria and Switzerland between May and July 2026. "
                           "Respondents were team leads, operations staff and founders. All figures in this report are invented for a training exercise.",
                           "The survey asked how requests arrive, who decides what happens next, and how work is handed over when someone is away."]),
    ("How requests arrive", ["Most teams receive requests through more than one channel. The median team uses three: email, a chat tool and conversations in person.",
                             "Requests that arrive by chat are the least likely to be written down. Teams said they 'remember' them, until they do not."]),
    ("Who decides", ["In two thirds of teams, one person decides the owner of each new request. In the rest, whoever sees the request first takes it.",
                     "Teams with a named decider report fewer forgotten requests, but also longer waiting times when that person is away."]),
    ("Missing information", ["Almost every team said that requests often arrive incomplete. The most common missing details are deadlines, budget and the person to contact.",
                             "Asking for missing details takes, by the teams' own estimate, between 10 and 30 minutes per request."]),
    ("Review queues", ["A review queue is a list of requests that a person must look at before anything happens. Teams that use one say it makes problems visible early.",
                       "The most useful review queues are short. Teams recommend that each item says what is missing and who can supply it."]),
    ("Handover", ["When someone is away, their open requests are the most likely to stall. Only a minority of teams keep a written handover note.",
                  "Teams that keep one describe it as a short page: open items, who is waiting, and where the files are."]),
    ("Tools", ["Spreadsheets remain the most common tool for tracking requests. Dedicated ticket tools are used mainly by teams above 30 people.",
               "Several teams use a notes app as a database: one page per request with a status field."]),
    ("Shared intake", []),
    ("Automation", ["Few teams automate more than reminders. The most common automation is a weekly summary email.",
                    "Teams were cautious about tools that send messages on their own. Most want a person to approve anything that leaves the team."]),
    ("Recommendations", ["Write every request down in one place. Name who decides. Show what is missing. Keep a short handover note.",
                         "Start small: one form, one list and one weekly review are enough for most teams."]),
]
INTAKE_FACT = ("41% of small teams use a shared intake form, such as a web form or a shared spreadsheet that everyone fills in the same way. "
               "23% rely on email alone. The remaining teams mix chat, email and in-person requests without a single place to collect them.")


def render_report(doc, path, pages=20):
    brand = doc["brand"]; w, h = A4; b = BRANDS[brand]
    c = new_canvas(path, doc["title"], brand)
    # title page
    c.setFillColorRGB(*rgb(b["color"])); c.rect(0, 0, w, h, stroke=0, fill=1)
    c.setFillColorRGB(1, 1, 1); c.setFont("Helvetica-Bold", 34); c.drawString(22 * mm, h - 90 * mm, "Small Team")
    c.drawString(22 * mm, h - 104 * mm, "Workflows 2026"); c.setFont("Helvetica", 13)
    c.drawString(22 * mm, h - 118 * mm, "How 412 small teams collect, decide and hand over work")
    c.setFont("Helvetica", 9); c.drawString(22 * mm, 30 * mm, "Small Teams Weekly · August 2026 · fictional report for a training exercise")
    c.showPage()
    rnd = random.Random(7)
    sec_index = 0
    for page in range(2, pages + 1):
        header(c, brand, w, h)
        y = h - 46 * mm
        if page == 2:
            c.setFont("Helvetica-Bold", 16); c.drawString(18 * mm, y, "Contents"); y -= 10 * mm
            c.setFont("Helvetica", 10)
            for i, (t, _) in enumerate(REPORT_SECTIONS):
                c.drawString(18 * mm, y, f"{i + 1}. {t}"); c.drawRightString(w - 18 * mm, y, str(3 + i * 2 if t != "Shared intake" else 17)); y -= 7 * mm
        elif page == 17:
            c.setFont("Helvetica-Bold", 16); c.drawString(18 * mm, y, "8. Shared intake"); y -= 10 * mm
            y = wrap(c, INTAKE_FACT, 18 * mm, y, w - 36 * mm, size=10.5, leading=15) - 6
            for label, value in [("Shared intake form", 41), ("Email only", 23), ("Mixed, no single place", 36)]:
                c.setFont("Helvetica", 9); c.drawString(18 * mm, y, label)
                c.setFillColorRGB(*rgb(b["color"])); c.rect(70 * mm, y - 1, value * 1.6 * mm, 4 * mm, stroke=0, fill=1)
                c.setFillColorRGB(0, 0, 0); c.drawString(72 * mm + value * 1.6 * mm, y, f"{value}%"); y -= 9 * mm
            y -= 4 * mm
            y = wrap(c, "Teams with a shared intake form reported that fewer requests were lost, but said the form only works if everyone uses it, including the team lead.",
                     18 * mm, y, w - 36 * mm)
        else:
            title, paras = REPORT_SECTIONS[sec_index % len(REPORT_SECTIONS)]
            if title == "Shared intake":
                sec_index += 1; title, paras = REPORT_SECTIONS[sec_index % len(REPORT_SECTIONS)]
            part = "" if page % 2 else " (continued)"
            c.setFont("Helvetica-Bold", 16); c.drawString(18 * mm, y, f"{(sec_index % len(REPORT_SECTIONS)) + 1}. {title}{part}"); y -= 10 * mm
            for p in paras:
                y = wrap(c, p, 18 * mm, y, w - 36 * mm, size=10.5, leading=15) - 6
            # a small chart with invented numbers
            vals = [rnd.randint(8, 70) for _ in range(4)]
            c.setFont("Helvetica-Oblique", 8.5); c.drawString(18 * mm, y, f"Figure {page}: responses by team size (illustrative, fictional)"); y -= 8 * mm
            for i, v in enumerate(vals):
                c.setFont("Helvetica", 8.5); c.drawString(18 * mm, y, ["5-9 people", "10-19 people", "20-34 people", "35-50 people"][i])
                c.setFillColorRGB(*rgb(b["color"])); c.rect(55 * mm, y - 1, v * 1.8 * mm, 3.6 * mm, stroke=0, fill=1)
                c.setFillColorRGB(0, 0, 0); c.drawString(57 * mm + v * 1.8 * mm, y, f"{v}%"); y -= 7 * mm
            if not page % 2:
                sec_index += 1
        footer(c, brand, "en", page, pages, w)
        c.showPage()
    c.save()


CONTRACT_DE = [
    ("§ 1 Mietsache", "Vermietet wird die Wohnung im 2. Obergeschoss links, Beispielweg 7, 80331 München (fiktiv), bestehend aus zwei Zimmern, Küche, Bad und Flur."),
    ("§ 2 Mietzeit", "Das Mietverhältnis beginnt am 01.04.2023 und läuft auf unbestimmte Zeit. Die Kündigungsfrist beträgt für den Mieter drei Monate zum Monatsende."),
    ("§ 3 Miete", "Die monatliche Grundmiete beträgt 980,00 EUR. Hinzu kommt eine Vorauszahlung auf die Betriebskosten von 180,00 EUR monatlich."),
    ("§ 4 Kaution", "Der Mieter leistet eine Kaution in Höhe von drei Monatsgrundmieten, also 2.940,00 EUR."),
    ("§ 5 Schönheitsreparaturen", "Schönheitsreparaturen übernimmt der Mieter nach Bedarf. Die Wohnung wurde renoviert übergeben."),
    ("§ 6 Haustiere", "Kleintierhaltung ist erlaubt. Für Hunde und Katzen ist die vorherige Zustimmung des Vermieters erforderlich."),
    ("§ 7 Hausordnung", "Die Hausordnung in der Anlage ist Bestandteil dieses Vertrags. Ruhezeiten gelten von 22 bis 6 Uhr."),
    ("§ 8 Sonstiges", "Änderungen dieses Vertrags bedürfen der Textform. Vermieterin: Eigentümergemeinschaft Beispielweg 7, vertreten durch Hausverwaltung Muster."),
]


def render_contract(doc, path):
    brand = doc["brand"]; w, h = A4
    c = new_canvas(path, doc["title"], brand)
    pages = 6
    per = math.ceil(len(CONTRACT_DE) / (pages - 1))
    for page in range(1, pages + 1):
        header(c, brand, w, h)
        y = h - 48 * mm
        if page == 1:
            c.setFont("Helvetica-Bold", 18); c.drawString(18 * mm, y, doc["title"]); y -= 12 * mm
            y = wrap(c, "zwischen der Eigentümergemeinschaft Beispielweg 7, vertreten durch die Hausverwaltung Muster (Vermieterin), "
                        "und Alex Example (Mieter). Vertragsnummer HV-M-2023-0401. Fiktives Workshop-Dokument.", 18 * mm, y, w - 36 * mm)
        chunk = CONTRACT_DE[(page - 1) * per: page * per]
        for title, text in chunk:
            y -= 6 * mm
            c.setFont("Helvetica-Bold", 11); c.drawString(18 * mm, y, title); y -= 7 * mm
            y = wrap(c, text, 18 * mm, y, w - 36 * mm, size=10.5, leading=15)
        if page == pages:
            y -= 20 * mm
            c.line(18 * mm, y, 80 * mm, y); c.line(110 * mm, y, 180 * mm, y)
            c.setFont("Helvetica", 8); c.drawString(18 * mm, y - 5 * mm, "München, 15.03.2023 - Vermieterin")
            c.drawString(110 * mm, y - 5 * mm, "München, 15.03.2023 - Mieter")
        footer(c, brand, "de", page, pages, w)
        c.showPage()
    c.save()


# ---------------------------------------------------------------- scans and photos

def rasterize(pdf_path, dpi):
    pdf = pdfium.PdfDocument(str(pdf_path))
    images = [pdf[i].render(scale=dpi / 72).to_pil().convert("RGB") for i in range(len(pdf))]
    pdf.close()
    return images


def scan_look(img, rnd, color=False):
    if not color:
        img = img.convert("L").convert("RGB")
    angle = rnd.uniform(-1.6, 1.6)
    img = img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(246, 244, 240))
    arr = np.asarray(img).astype(np.int16)
    noise = np.random.default_rng(rnd.randint(0, 10**6)).normal(0, 9, arr.shape)
    arr = np.clip(arr * 0.96 + 6 + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    # darker edges, like a flatbed lid
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rectangle([w * 0.03, h * 0.03, w * 0.97, h * 0.97], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w * 0.03))
    dark = ImageEnhance.Brightness(img).enhance(0.82)
    img = Image.composite(img, dark, mask)
    d = ImageDraw.Draw(img)
    for _ in range(rnd.randint(8, 20)):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h); r = rnd.uniform(0.6, 2.2)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(60, 60, 60))
    return img.filter(ImageFilter.GaussianBlur(0.5))


def make_scan(src_pdf, dst_pdf, seed, dpi=130, color=False, quality=60):
    rnd = random.Random(seed)
    pages = [scan_look(p, rnd, color=color) for p in rasterize(src_pdf, dpi)]
    fixed = __import__("time").gmtime(1767225600)  # 2026-01-01, so rebuilds are identical
    pages[0].save(dst_pdf, save_all=True, append_images=pages[1:], resolution=dpi, quality=quality,
                  title="Scan", author="Scanner (fictional)", subject="Fictional workshop document",
                  creationDate=fixed, modDate=fixed)


def _coeffs(dst, src):
    a = []
    for (x, y), (u, v) in zip(dst, src):
        a.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        a.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(a, dtype=float); B = np.array(src, dtype=float).reshape(8)
    return np.linalg.solve(A, B).tolist()


def make_photo(src_pdf, background, seed, blur=0.0):
    """Place page 1 of a PDF on a background photo with a slight perspective, shadow and warm light."""
    rnd = random.Random(seed)
    doc = rasterize(src_pdf, 170)[0]
    bg = Image.open(background).convert("RGB")
    W, H = 1200, 1600  # portrait phone photo
    bw, bh = bg.size
    scale = max(W / bw, H / bh)
    bg = bg.resize((int(bw * scale) + 1, int(bh * scale) + 1), Image.LANCZOS)
    left = (bg.width - W) // 2; top = (bg.height - H) // 2
    bg = bg.crop((left, top, left + W, top + H))
    dw, dh = doc.size
    target_h = H * rnd.uniform(0.72, 0.84)
    target_w = target_h * dw / dh
    if target_w > W * 0.82:
        target_w = W * 0.82; target_h = target_w * dh / dw
    cx, cy = W / 2 + rnd.uniform(-40, 40), H / 2 + rnd.uniform(-30, 30)
    j = lambda: rnd.uniform(-0.035, 0.035) * target_w
    quad = [(cx - target_w / 2 + j(), cy - target_h / 2 + j()), (cx + target_w / 2 + j(), cy - target_h / 2 + j()),
            (cx + target_w / 2 + j() * 1.6, cy + target_h / 2 + j()), (cx - target_w / 2 + j() * 1.6, cy + target_h / 2 + j())]
    coeffs = _coeffs(quad, [(0, 0), (dw, 0), (dw, dh), (0, dh)])
    warped = doc.transform((W, H), Image.PERSPECTIVE, coeffs, Image.BICUBIC, fillcolor=(0, 0, 0))
    mask = Image.new("L", (W, H), 0); ImageDraw.Draw(mask).polygon(quad, fill=255)
    shadow = Image.new("L", (W, H), 0); ImageDraw.Draw(shadow).polygon([(x + 14, y + 18) for x, y in quad], fill=150)
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    bg = Image.composite(Image.new("RGB", (W, H), (25, 20, 15)), bg, shadow.point(lambda v: int(v * 0.55)))
    # paper is never pure white in a photo: warm it and add a light gradient
    paper = ImageEnhance.Brightness(warped).enhance(0.93)
    grad = Image.linear_gradient("L").resize((W, H)).rotate(rnd.uniform(20, 70))
    paper = Image.composite(paper, ImageEnhance.Brightness(paper).enhance(0.86), grad)
    out = Image.composite(paper, bg, mask)
    out = ImageEnhance.Color(out).enhance(0.92)
    r, g, b = out.split(); out = Image.merge("RGB", (r.point(lambda v: min(255, v + 6)), g, b.point(lambda v: max(0, v - 6))))
    out = out.filter(ImageFilter.GaussianBlur(0.6 + blur))
    return out


def exif_bytes(date_iso, time_hm="12:00"):
    ex = Image.Exif()
    stamp = date_iso.replace("-", ":") + " " + time_hm + ":00"
    ex[0x0132] = stamp            # DateTime
    ex[0x010F] = "Fictional"      # Make
    ex[0x0110] = "Workshop Phone"  # Model
    ex.get_ifd(0x8769)[0x9003] = stamp  # DateTimeOriginal
    return ex
