# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "reportlab>=4.2", "pillow>=11", "pillow-heif>=1.0", "numpy>=2", "pypdfium2>=4.30",
#   "segno>=1.6", "python-docx>=1.1", "openpyxl>=3.1", "pypdf>=5", "cryptography>=43",
# ]
# ///
"""Build the second brain pack from the story files in this folder.

Maintainer tool, not needed by participants (the generated files are committed):

    uv run --no-project --script data/second-brain-pack/generator/generate.py

It rewrites mailbox/, drive/, downloads/, notes/, records/, calendar/, telegram/,
answer-key/ and manifest.json next to this folder. README.md is hand-written and kept.
"""

import csv
import datetime as dt
import hashlib
import html as htmllib
import io
import json
import mailbox
import os
import re
import shutil
import sys
import tempfile
import zipfile
from decimal import Decimal
from email import policy
from email.message import EmailMessage
from email.utils import format_datetime, make_msgid
from pathlib import Path
from zoneinfo import ZoneInfo

GEN = Path(__file__).resolve().parent
sys.path.insert(0, str(GEN))

import openpyxl  # noqa: E402
import pillow_heif  # noqa: E402
from docx import Document  # noqa: E402
from docx.shared import Pt, RGBColor  # noqa: E402
from openpyxl.styles import Font, PatternFill  # noqa: E402
from PIL import Image  # noqa: E402
from pypdf import PdfReader, PdfWriter  # noqa: E402

import render  # noqa: E402
from documents import BUDGET_V1, BUDGET_V2, DOC, DOCS, OFFICE, OFFICE_DOC  # noqa: E402
from mail import EMAIL, EMAILS, FORWARDED  # noqa: E402
from notes import (CALENDAR, DEADLINES, IDEAS, INTERACTIONS, NOTES, PLACES, PURCHASES, TELEGRAM,  # noqa: E402
                   TRANSCRIPTS)
from questions import INBOX_SORTING, QUESTIONS  # noqa: E402
from world import BRANDS, OWNER, PEOPLE, PERSON, SCENARIO_DATE  # noqa: E402

pillow_heif.register_heif_opener()
PACK = GEN.parent
KNOWLEDGE = PACK.parent / "knowledge"
PHOTOS = GEN / "assets" / "photos"
BERLIN = ZoneInfo("Europe/Berlin")
OUT_DIRS = ["mailbox", "drive", "downloads", "notes", "records", "calendar", "telegram", "answer-key", "notion"]
FICTIONAL_LINE = "Fictional workshop data - not a real message."
PDF_PASSWORD = "15041987"  # fictional date of birth; deliberately not written anywhere in the pack

MIME = {".pdf": "application/pdf", ".jpg": "image/jpeg", ".heic": "image/heic", ".zip": "application/zip",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".ics": "text/calendar"}


def slug(text, n=48):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:n].strip("-")


def stamp(date_iso, time_hm="12:00"):
    d = dt.datetime.fromisoformat(f"{date_iso} {time_hm}").replace(tzinfo=BERLIN)
    return d.timestamp()


def write(path, data, when=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    if when:
        os.utime(path, (when, when))


# ---------------------------------------------------------------------------------- documents

def build_documents(tmp):
    """Return {doc_id: (bytes, ext)} for every document in its final variant."""
    out = {}
    base = {}
    for d in DOCS:
        if d.get("source_of"):
            continue
        p = tmp / f"{d['id']}.pdf"
        kind = d["kind"]
        if kind == "receipt":
            render.render_receipt(d, p)
        elif kind == "eticket":
            render.render_eticket(d, p)
        elif kind == "report":
            render.render_report(d, p, pages=d.get("pages", 20))
        elif kind == "contract":
            render.render_contract(d, p)
        else:
            render.render_document(d, p)
        base[d["id"]] = p
    for i, d in enumerate(DOCS):
        src = base[d.get("source_of") or d["id"]]
        spec = DOC[d.get("source_of")] if d.get("source_of") else d
        variant = d.get("variant", "clean")
        seed = 1000 + i
        if variant == "clean":
            out[d["id"]] = (src.read_bytes(), ".pdf")
        elif variant == "scan":
            dst = tmp / f"{d['id']}-scan.pdf"; render.make_scan(src, dst, seed); out[d["id"]] = (dst.read_bytes(), ".pdf")
        elif variant == "scan_big":
            dst = tmp / f"{d['id']}-big.pdf"; render.make_scan(src, dst, seed, dpi=300, color=True, quality=88)
            assert dst.stat().st_size > 5_000_000, f"big scan only {dst.stat().st_size} bytes"
            out[d["id"]] = (dst.read_bytes(), ".pdf")
        elif variant == "encrypted":
            import secrets
            rnd_bytes = __import__("random").Random(seed).randbytes
            saved = (os.urandom, secrets.token_bytes)
            os.urandom = secrets.token_bytes = lambda n=32: rnd_bytes(n)  # reproducible salts and IDs
            try:
                w = PdfWriter(clone_from=PdfReader(str(src))); w.encrypt(PDF_PASSWORD, algorithm="AES-256")
                buf = io.BytesIO(); w.write(buf)
            finally:
                os.urandom, secrets.token_bytes = saved
            out[d["id"]] = (buf.getvalue(), ".pdf")
        elif variant.startswith("photo"):
            bg = PHOTOS / f"{spec.get('photo_bg', 'desk-oak')}.jpg"
            img = render.make_photo(src, bg, seed, blur=6.0 if variant == "photo_blur" else 0.0)
            ex = render.exif_bytes(spec["date"], spec.get("time", "12:00"))
            buf = io.BytesIO()
            if variant == "photo_heic":
                img.save(buf, format="HEIF", quality=80); out[d["id"]] = (buf.getvalue(), ".heic")
            else:
                img.save(buf, format="JPEG", quality=84, exif=ex); out[d["id"]] = (buf.getvalue(), ".jpg")
        else:
            raise ValueError(variant)
    return out


def normalize_zip(data, when=(2026, 1, 1, 0, 0, 0)):
    """Rewrite a ZIP container with fixed timestamps so rebuilds are byte-identical."""
    src = zipfile.ZipFile(io.BytesIO(data))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":  # openpyxl stamps the save time here
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>2026-01-01T00:00:00Z\g<2>", data)
            z.writestr(zipfile.ZipInfo(info.filename, date_time=when), data, compress_type=zipfile.ZIP_DEFLATED)
    return out.getvalue()


def docx_bytes(build, created):
    doc = Document()
    doc.core_properties.created = created
    doc.core_properties.modified = created
    doc.core_properties.author = "Fictional workshop data"
    doc.core_properties.keywords = "fictional: true"
    build(doc)
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0]; p.text = "Fictional workshop document - not a real agreement."
    p.runs[0].font.size = Pt(8); p.runs[0].font.color.rgb = RGBColor(0x77, 0x77, 0x77)
    buf = io.BytesIO(); doc.save(buf); return normalize_zip(buf.getvalue())


def build_contract(doc):
    doc.add_heading("Room hire agreement (DRAFT)", 0)
    doc.add_paragraph("Linden Hall Events GmbH, Lindenplatz 3, 80331 München (fictional) and Juniper Workshop Lab, Lindwurmstraße 0, 80337 München (fictional)")
    clauses = [
        ("1. Room and date", "Maple Room, first floor, Thursday 22 October 2026, 08:30 to 17:30, up to 30 people."),
        ("2. Price", "EUR 1,150.00 including VAT: room hire EUR 900.00, AV package EUR 150.00, cleaning EUR 100.00 (quote LH-Q-2026-0914)."),
        ("3. Deposit and confirmation", "The booking becomes binding once Linden Hall Events has received a deposit of EUR 300.00. "
                                       "The deposit is due by 9 October 2026. Until it has been received the room is only held provisionally and may be released."),
        ("4. Numbers", "The hirer tells Linden Hall Events the final number of guests by 15 October 2026."),
        ("5. Cancellation", "After confirmation, cancellation costs 50% of the hire fee; within 7 days of the event, 100%."),
        ("6. Access", "Step-free access via the side entrance on Lindenplatz and the glass lift to the first floor. Accessible toilet on the same floor."),
        ("7. Signatures", "Linden Hall Events GmbH: ____________________      Juniper Workshop Lab: ____________________"),
    ]
    for t, body in clauses:
        doc.add_heading(t, level=2); doc.add_paragraph(body)


def build_agenda(doc):
    doc.add_heading("Learning day: agenda (draft v2)", 0)
    doc.add_paragraph("Thursday 22 October 2026 · Maple Room, Linden Hall Events · Project Lantern (fictional)")
    table = doc.add_table(rows=1, cols=3); table.style = "Light Grid Accent 1"
    table.rows[0].cells[0].text, table.rows[0].cells[1].text, table.rows[0].cells[2].text = "Time", "Session", "Who"
    for row in [("09:30", "Welcome and goals", "Alex"), ("10:00", "The intake workflow, live demo", "Jordan"),
                ("11:00", "Coffee", ""), ("11:20", "Hands-on: your own requests", "All"), ("12:30", "Lunch", ""),
                ("13:30", "The review queue: what is missing, who supplies it", "Alex"), ("14:30", "Handover: one page, not a meeting", "Jordan"),
                ("15:30", "Questions and next steps", "Alex"), ("16:30", "End", "")]:
        cells = table.add_row().cells
        for c, v in zip(cells, row):
            c.text = v
    doc.add_paragraph("Open: final attendee number; vegetarian meals; interpreter confirmation.")


def xlsx_bytes(build, created):
    wb = openpyxl.Workbook()
    wb.properties.creator = "Fictional workshop data"
    wb.properties.keywords = "fictional: true"
    wb.properties.created = created; wb.properties.modified = created
    build(wb)
    buf = io.BytesIO(); wb.save(buf); return normalize_zip(buf.getvalue())


def budget_builder(rows, label, with_budget):
    def build(wb):
        ws = wb.active; ws.title = "Budget"
        ws["A1"] = f"Project Lantern budget {label} (fictional)"; ws["A1"].font = Font(bold=True, size=13)
        ws.append([]); ws.append(["Item", "Amount (EUR)", "Notes"])
        for c in ws[3]:
            c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="DDEBE3")
        for item, amount in rows:
            ws.append([item, float(amount), ""])
        last = 3 + len(rows)
        ws.append(["Total", f"=SUM(B4:B{last})", "formula"])
        ws[f"A{last + 1}"].font = Font(bold=True)
        if with_budget:
            ws.append(["Approved budget", 2500, "approved 2026-09-05"])
            ws.append(["Remaining", f"=B{last + 2}-B{last + 1}", "formula"])
        ws.column_dimensions["A"].width = 42; ws.column_dimensions["B"].width = 16; ws.column_dimensions["C"].width = 24
    return build


ATTENDEE_FIRST = ["Mia", "Jonas", "Lena", "Paul", "Sofia", "Lukas", "Hannah", "Felix", "Emma", "Noah", "Lea", "Elias", "Clara", "Ben",
                  "Marie", "Leon", "Anna", "Finn", "Laura", "Tim", "Julia", "Max", "Nina", "David", "Sara", "Jan"]
ATTENDEE_LAST = ["Example", "Sample", "Demo", "Beispiel", "Muster"]
ATTENDEE_ORG = ["Cedar Demo Analytics", "Moss Training Collective", "Fern Sample Studio", "Willow Practice Kitchens", "Harbour Lane Consulting"]


def attendees_rows():
    rows = [("Elif Example", "Cedar Demo Analytics", "confirmed", "vegetarian", "wheelchair: step-free access")]
    statuses = ["confirmed"] * 22 + ["pending"] * 4
    diets = ["none", "vegetarian", "none", "vegan", "none", "none", "vegetarian"]
    for i in range(26):
        name = f"{ATTENDEE_FIRST[i]} {ATTENDEE_LAST[i % 5]}"
        access = "sign language interpreting" if i == 9 else ""
        rows.append((name, ATTENDEE_ORG[i % 5], statuses[i], diets[i % 7], access))
    return rows


def attendees_builder(wb):
    ws = wb.active; ws.title = "Attendees"
    ws.append(["Name", "Organisation", "Status", "Dietary", "Access needs"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for r in attendees_rows():
        ws.append(list(r))
    ws.append([]); ws.append(["Fictional workshop data. Updated 2026-10-05 by Mira Beispiel."])
    for col, w in zip("ABCDE", (22, 28, 12, 12, 30)):
        ws.column_dimensions[col].width = w


def build_office(tmp):
    created = lambda iso: dt.datetime.fromisoformat(iso + " 09:00")
    out = {
        "LH-CONTRACT": (docx_bytes(build_contract, created("2026-09-14")), ".docx"),
        "AGENDA": (docx_bytes(build_agenda, created("2026-10-01")), ".docx"),
        "BUDGET-V1": (xlsx_bytes(budget_builder(BUDGET_V1, "v1", False), created("2026-09-01")), ".xlsx"),
        "BUDGET-V2": (xlsx_bytes(budget_builder(BUDGET_V2, "v2", True), created("2026-09-22")), ".xlsx"),
        "ATTENDEES": (xlsx_bytes(attendees_builder, created("2026-10-05")), ".xlsx"),
    }
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for k, name in enumerate(["maple-room-1", "maple-room-2", "maple-room-3"]):
            img = Image.open(PHOTOS / f"{name}.jpg")
            b = io.BytesIO(); img.save(b, format="JPEG", quality=84, exif=render.exif_bytes("2026-09-25", f"10:{12 + k * 7:02d}"))
            info = zipfile.ZipInfo(f"IMG_47{70 + k}.jpg", date_time=(2026, 9, 25, 10, 12 + k * 7, 0))
            z.writestr(info, b.getvalue())
    out["VENUE-ZIP"] = (buf.getvalue(), ".zip")
    return out


# ---------------------------------------------------------------------------------- calendar

def ics_dt(s):
    d = dt.datetime.fromisoformat(s).replace(tzinfo=BERLIN).astimezone(dt.timezone.utc)
    return d.strftime("%Y%m%dT%H%M%SZ")


def vevent(ev, method_attendees=None, dtstamp="20261007T060000Z"):
    lines = ["BEGIN:VEVENT", f"UID:{ev['uid']}@juniper-workshop.invalid", f"DTSTAMP:{dtstamp}"]
    if ev.get("allday"):
        lines += [f"DTSTART;VALUE=DATE:{ev['start'].replace('-', '')}", f"DTEND;VALUE=DATE:{ev['end'].replace('-', '')}"]
    else:
        lines += [f"DTSTART:{ics_dt(ev['start'])}", f"DTEND:{ics_dt(ev['end'])}"]
    lines.append(f"SUMMARY:{ev['title']}")
    if ev.get("location"):
        lines.append(f"LOCATION:{ev['location'].replace(',', chr(92) + ',')}")
    desc = (ev.get("note", "") + " " if ev.get("note") else "") + "Fictional workshop data."
    lines.append(f"DESCRIPTION:{desc.replace(',', chr(92) + ',')}")
    if ev.get("rrule"):
        lines.append(f"RRULE:{ev['rrule']}")
    if ev.get("status"):
        lines.append(f"STATUS:{ev['status']}")
    if method_attendees:
        org, atts = method_attendees
        lines.append(f"ORGANIZER;CN={org[0]}:mailto:{org[1]}")
        for a in atts:
            lines.append(f"ATTENDEE;CN={a[0]};ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE:mailto:{a[1]}")
    lines.append("END:VEVENT")
    return lines


def calendar_text(events, method=None, attendees=None, name="Alex Example (fictional)"):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//AI Realist//second-brain-pack//EN", "CALSCALE:GREGORIAN",
             f"X-WR-CALNAME:{name}"]
    if method:
        lines.append(f"METHOD:{method}")
    for ev in events:
        lines += vevent(ev, attendees)
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def build_ics():
    alex = (OWNER["name"], OWNER["email"])
    return {
        "ICS-FLIGHT": (calendar_text([dict(uid="aur7q2-1", start="2026-10-26 07:10", end="2026-10-26 09:15", title="Flight AUR 214 Munich - London Heathrow",
                                            location="Munich Airport (MUC) Terminal 2", note="Booking AUR7Q2"),
                                       dict(uid="aur7q2-2", start="2026-10-28 20:40", end="2026-10-28 22:35", title="Flight AUR 219 London Heathrow - Munich",
                                            location="London Heathrow (LHR) Terminal 5", note="Booking AUR7Q2")], method="PUBLISH", name="Aurelian Air").encode(), ".ics"),
        "ICS-WALK": (calendar_text([dict(uid="walk-0925", start="2026-09-25 10:00", end="2026-09-25 10:45", title="Maple Room walk-through",
                                          location="Linden Hall Events, Lindenplatz 3, München")], method="REQUEST",
                                    attendees=((PERSON["P06"]["name"], PERSON["P06"]["email"]), [alex, (PERSON["P03"]["name"], PERSON["P03"]["email"])]),
                                    name="Invitation").encode(), ".ics"),
        "ICS-CHECKIN": (calendar_text([dict(uid="checkin-1006", start="2026-10-06 09:30", end="2026-10-06 10:15", title="Weekly check-in",
                                             location="Office")], method="REQUEST",
                                       attendees=((PERSON["P02"]["name"], PERSON["P02"]["email"]),
                                                  [alex] + [(PERSON[p]["name"], PERSON[p]["email"]) for p in ("P03", "P04", "P05")]),
                                       name="Invitation").encode(), ".ics"),
    }


# ---------------------------------------------------------------------------------- email

def to_html(email, brand_key, fake=False):
    b = BRANDS[brand_key]
    color = "#%02x%02x%02x" % b["color"]
    if fake:
        color = "#1b4f9c"
    name = ("StayPiIot" if fake else b["name"])
    paras = "".join(f"<p style=\"margin:0 0 14px\">{htmllib.escape(p).replace(chr(10), '<br>')}</p>"
                    for p in email["body"].split("\n\n"))
    paras = re.sub(r"(https://[^\s<]+)", r'<a href="\1">\1</a>', paras)
    inline = ""
    if email.get("inline"):
        inline = '<tr><td><img src="cid:inline-image" width="600" alt="" style="display:block;width:100%;height:auto"></td></tr>'
    unsub = ""
    if email.get("newsletter"):
        unsub = f' · <a href="https://{b["domain"]}/unsubscribe">Unsubscribe</a>'
    jsonld = ""
    if email.get("jsonld"):
        jsonld = f'<script type="application/ld+json">{json.dumps(reservation_jsonld(email["jsonld"]), ensure_ascii=False)}</script>'
    return f"""<!doctype html><html><head><meta charset="utf-8">{jsonld}</head>
<body style="margin:0;background:#f2f2f2;font-family:Arial,Helvetica,sans-serif">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:20px 8px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff;max-width:600px">
<tr><td style="background:{color};padding:16px 24px;color:#ffffff;font-size:20px;font-weight:bold">{htmllib.escape(name)}</td></tr>
{inline}
<tr><td style="padding:24px;font-size:14px;line-height:1.5;color:#222222">{paras}</td></tr>
<tr><td style="padding:14px 24px;font-size:11px;color:#777777;border-top:1px solid #eeeeee">{htmllib.escape(b.get('address', ''))} · {b['domain']}{unsub}<br>{FICTIONAL_LINE}</td></tr>
</table></td></tr></table></body></html>"""


def reservation_jsonld(ref):
    kind, doc_id = ref.split(":")
    d = DOC[doc_id]
    if kind == "flight":
        return [{"@context": "https://schema.org", "@type": "FlightReservation", "reservationNumber": d["number"],
                 "reservationStatus": "https://schema.org/ReservationConfirmed", "underName": {"@type": "Person", "name": "Alex Example"},
                 "reservationFor": {"@type": "Flight", "flightNumber": f["flight"].split()[1], "airline": {"@type": "Airline", "name": "Aurelian Air"},
                                    "departureAirport": {"@type": "Airport", "name": f["dep"]}, "arrivalAirport": {"@type": "Airport", "name": f["arr"]},
                                    "departureTime": f["date"] + " " + f["dep_time"]}} for f in d["flights"]]
    meta = dict(d["meta"])
    return {"@context": "https://schema.org", "@type": "LodgingReservation", "reservationNumber": d["number"],
            "reservationStatus": "https://schema.org/ReservationConfirmed", "underName": {"@type": "Person", "name": "Alex Example"},
            "reservationFor": {"@type": "LodgingBusiness", "name": meta["Property"].split(",")[0]},
            "checkinTime": meta.get("Check-in"), "checkoutTime": meta.get("Check-out"), "totalPrice": d.get("total"), "priceCurrency": "EUR"}


def brand_of(address):
    domain = address.split("@")[1]
    for k, b in BRANDS.items():
        if b["domain"] == domain:
            return k
    return None


def attachment_name(att_id, files):
    if att_id in DOC or att_id in OFFICE_DOC:
        spec = DOC.get(att_id) or OFFICE_DOC.get(att_id)
        dl = spec.get("downloads")
        if isinstance(dl, list):
            dl = dl[0]
        name = dl or Path(spec["drive"]).name
        ext = files[att_id][1]
        return Path(name).stem + ext
    return {"ICS-FLIGHT": "AUR7Q2.ics", "ICS-WALK": "invite.ics", "ICS-CHECKIN": "invite.ics"}[att_id]


def build_message(e, files, threads, by_id, extra_attachments=None):
    msg = EmailMessage(policy=policy.SMTP)
    msg["From"] = f"{e['frm'][0]} <{e['frm'][1]}>"
    msg["To"] = ", ".join(f"{n} <{a}>" for n, a in e["to"])
    if e.get("cc"):
        msg["Cc"] = ", ".join(f"{n} <{a}>" for n, a in e["cc"])
    msg["Subject"] = e["subject"]
    when = dt.datetime.fromisoformat(e["date"]).replace(tzinfo=BERLIN)
    msg["Date"] = format_datetime(when)
    msg["Message-ID"] = f"<{e['id'].lower()}.{slug(e['subject'], 24)}@{e['frm'][1].split('@')[1]}>"
    if e.get("thread"):
        prev = threads.get(e["thread"], [])
        if prev:
            msg["In-Reply-To"] = by_id[prev[-1]]["Message-ID"]
            msg["References"] = " ".join(by_id[p]["Message-ID"] for p in prev)
        threads.setdefault(e["thread"], []).append(e["id"])
    msg["X-Fictional"] = "true"
    if e.get("newsletter"):
        msg["List-Unsubscribe"] = f"<https://{e['frm'][1].split('@')[1]}/unsubscribe>"
    body = e["body"]
    if e.get("quote") and e.get("thread") and len(threads[e["thread"]]) > 1:
        prev_id = threads[e["thread"]][-2]
        prev = EMAIL.get(prev_id)
        prev_when = dt.datetime.fromisoformat(prev["date"]).strftime("%a, %d %b %Y at %H:%M")
        quoted = "\n".join("> " + line if line else ">" for line in quoted_text(prev_id, threads).splitlines())
        body = body + f"\n\nOn {prev_when}, {prev['frm'][0]} <{prev['frm'][1]}> wrote:\n" + quoted
    body = body + "\n\n" + FICTIONAL_LINE + "\n"
    QUOTED[e["id"]] = body.rsplit("\n\n" + FICTIONAL_LINE, 1)[0]
    brand = brand_of(e["frm"][1])
    html_mode = e.get("html")
    if html_mode == "only":
        msg.set_content(to_html(e, brand), subtype="html")
    elif html_mode in ("brand", "brand_fake"):
        msg.set_content(body)
        msg.add_alternative(to_html(e, "staypilot" if html_mode == "brand_fake" else brand, fake=html_mode == "brand_fake"), subtype="html")
    else:
        msg.set_content(body)
    if e.get("inline") and html_mode:
        img = Image.open(PHOTOS / f"{e['inline']}.jpg"); img.thumbnail((1200, 800))
        b = io.BytesIO(); img.save(b, format="JPEG", quality=78)
        html_part = msg.get_body(("html",))
        html_part.add_related(b.getvalue(), maintype="image", subtype="jpeg", cid="<inline-image>", filename=f"{e['inline']}.jpg")
    for att in e.get("attach", []):
        data, ext = files[att]
        maintype, subtype = MIME[ext].split("/")
        params = {"method": "REQUEST"} if att in ("ICS-WALK", "ICS-CHECKIN") else {}
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=attachment_name(att, files), params=params)
    for m in extra_attachments or []:
        msg.add_attachment(m)
    for n, part in enumerate(p for p in msg.walk() if p.is_multipart()):
        part.set_boundary(f"=_juniper_{e['id']}_{n}")
    return msg


QUOTED = {}


def quoted_text(email_id, threads):
    return QUOTED.get(email_id, EMAIL[email_id]["body"])


def build_mail(files):
    threads, by_id = {}, {}
    fwd = EmailMessage(policy=policy.SMTP)
    fwd["From"] = f"{FORWARDED['frm'][0]} <{FORWARDED['frm'][1]}>"
    fwd["To"] = f"{OWNER['name']} <{OWNER['email']}>"
    fwd["Subject"] = FORWARDED["subject"]
    fwd["Date"] = format_datetime(dt.datetime.fromisoformat(FORWARDED["date"]).replace(tzinfo=BERLIN))
    fwd["Message-ID"] = "<fwd-noor.payment@lindenhall-events.example>"
    fwd.set_content(FORWARDED["body"] + "\n\n" + FICTIONAL_LINE + "\n")
    messages = []
    for e in sorted(EMAILS, key=lambda x: x["date"]):
        extra = [fwd] if "FWD-NOOR" in e.get("attach", []) else None
        e2 = dict(e); e2["attach"] = [a for a in e.get("attach", []) if a != "FWD-NOOR"]
        msg = build_message(e2, files, threads, by_id, extra)
        by_id[e["id"]] = msg
        messages.append((e, msg))
    return messages


def labels_for(e):
    sent = e["frm"][1] == OWNER["email"]
    labels = ["Sent"] if sent else ["Inbox"]
    if not sent and e.get("seen", True):
        labels.append("Opened")
    if e.get("starred"):
        labels.append("Starred")
    labels += e.get("labels", [])
    return labels


# ---------------------------------------------------------------------------------- records

def doc_path(doc_id):
    spec = DOC.get(doc_id) or OFFICE_DOC.get(doc_id)
    return f"drive/{spec['drive']}" if spec and spec.get("drive") else ""


def write_csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header); w.writerows(rows)
    write(path, buf.getvalue())


def md_table(title, header, rows):
    out = ["---", "fictional: true", "type: records", f"updated: {SCENARIO_DATE}", "---", f"# {title}", "",
           "| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    out.append("")
    out.append("Fictional workshop data.")
    return "\n".join(out) + "\n"


def build_records():
    tables = {}
    tables["people"] = (["id", "name", "aliases", "role", "organisation", "email", "how_met", "first_met", "last_contact"],
                        [(p["id"], p["name"], "; ".join(p["aliases"]), p["role"], p["org"], p["email"], p["how_met"], p["first_met"],
                          max((i[2] for i in INTERACTIONS if i[1] == p["id"]), default="")) for p in PEOPLE if p["id"] != "P01"])
    tables["interactions"] = (["id", "person_id", "person", "date", "channel", "summary", "promise", "follow_up_due"],
                              [(i[0], i[1], PERSON[i[1]]["name"], i[2], i[3], i[4], i[5], i[6]) for i in INTERACTIONS])
    tables["deadlines"] = (["id", "title", "due", "status", "area", "changed_from", "notes"], DEADLINES)
    tables["purchases"] = (["id", "date", "item", "vendor", "category", "amount", "currency", "warranty_until", "receipt", "duplicate_of"],
                           [(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], doc_path(p[8]), p[9]) for p in PURCHASES])
    tables["places"] = (["id", "name", "city", "country", "type", "visited", "with", "rating", "status", "notes"], PLACES)
    tables["ideas"] = (["id", "captured", "idea", "status", "related_people", "related"],
                       [(i[0], i[1], i[2], i[3], "; ".join(PERSON[x.strip()]["name"] for x in i[4].split(";") if x.strip()), i[5]) for i in IDEAS])
    titles = dict(people="People", interactions="Interactions", deadlines="Deadlines", purchases="Purchases", places="Places", ideas="Someday ideas")
    for name, (header, rows) in tables.items():
        write_csv(PACK / "records" / f"{name}.csv", header, rows)
        write(PACK / "records" / "markdown" / f"{name}.md", md_table(titles[name], header, rows))
    return tables


# ---------------------------------------------------------------------------------- notes, transcripts, telegram

def front_matter(folder, created, updated):
    para = folder.split("/")[0]
    return f"---\nfictional: true\ntype: note\npara: {para}\ncreated: {created}\nupdated: {updated}\n---\n"


def build_notes():
    for folder, name, created, updated, body in NOTES:
        if body.startswith("---\n"):
            fm, rest = body[4:].split("\n---\n", 1)
            text = f"---\nfictional: true\ntype: clip\npara: {folder.split('/')[0]}\ncreated: {created}\nupdated: {updated}\n{fm}\n---\n{rest}"
        else:
            text = front_matter(folder, created, updated) + body
        write(PACK / "notes" / folder / name, text, stamp(updated, "18:00"))
    for src in sorted(KNOWLEDGE.glob("0*.md")):
        dst = PACK / "notes" / "1-Projects" / "Project Lantern" / src.name
        write(dst, src.read_bytes())


def vtt(t):
    lines = ["WEBVTT", f"NOTE {t['title']}, {t['date']}. Fictional workshop transcript.", ""]
    sec = 0
    for i, (who, text) in enumerate(t["cues"], 1):
        a = sec; sec += 4 + len(text) // 14
        f = lambda s: f"00:{s // 60:02d}:{s % 60:02d}.000"
        lines += [str(i), f"{f(a)} --> {f(sec)}", f"<v {who}>{text}", ""]
    return "\n".join(lines)


def build_transcripts():
    for t in TRANSCRIPTS:
        name = f"{t['date']} {t['title']}.vtt"
        write(PACK / "drive" / "Meetings" / name, vtt(t), stamp(t["date"], "11:00"))
    write(PACK / "downloads" / "transcript (2).vtt", vtt(TRANSCRIPTS[1]), stamp("2026-09-25", "12:05"))


def build_telegram():
    result = []
    for k, (when, uid, text) in enumerate(TELEGRAM):
        ts = int(dt.datetime.fromisoformat(when).replace(tzinfo=BERLIN).timestamp())
        user = {"id": uid, "is_bot": False, "first_name": "Alex" if uid == 100000001 else "Promo", "language_code": "en"}
        message = {"message_id": 10 + k, "from": user, "chat": {"id": uid, "type": "private", "first_name": user["first_name"]}, "date": ts}
        if text.startswith("[photo]"):
            message["photo"] = [{"file_id": "FICTIONAL-PHOTO-0001", "file_unique_id": "FICT0001", "width": 1280, "height": 960, "file_size": 182000}]
            message["caption"] = text.replace("[photo] ", "")
        else:
            message["text"] = text
            if text.startswith("/"):
                message["entities"] = [{"offset": 0, "length": len(text), "type": "bot_command"}]
        result.append({"update_id": 500000 + k, "message": message})
    doc = {"ok": True, "result": result, "_note": "Fictional workshop data in the shape of the Telegram Bot API getUpdates response."}
    write(PACK / "telegram" / "updates.json", json.dumps(doc, ensure_ascii=False, indent=2) + "\n")


# ---------------------------------------------------------------------------------- answer key

def check_computed(tables):
    D = Decimal
    checks = {}
    v1 = sum(D(a) for _, a in BUDGET_V1); v2 = sum(D(a) for _, a in BUDGET_V2)
    checks["budget"] = (v1 == D("2000") and v2 == D("2430") and D("2500") - v2 == D("70"), f"v1 {v1}, v2 {v2}")
    rows = attendees_rows()
    conf = sum(1 for r in rows if r[2] == "confirmed"); pend = sum(1 for r in rows if r[2] == "pending")
    checks["attendees"] = (conf == 23 and pend == 4, f"{conf} confirmed, {pend} pending")
    monthly = {"NoteCloud": D("8.00"), "StreamBox": D("15.99"), "Newsroom Daily": D("9.99"), "CloudVault": D("2.99")}
    checks["subscriptions"] = (sum(monthly.values()) == D("36.97"), str(sum(monthly.values())))
    eq = sum(D(p[5]) for p in PURCHASES if p[4] == "equipment" and not p[9] and "2026-07-01" <= p[1] <= "2026-09-30")
    checks["equipment"] = (eq == D("2135.90"), str(eq))
    noor = max((i for i in INTERACTIONS if i[1] == "P06"), key=lambda i: i[2])
    checks["noor"] = (noor[2] == "2026-10-02" and noor[6] == "2026-10-15", f"{noor[2]} {noor[5]} {noor[6]}")
    pi = sorted(i[0] for i in IDEAS if "P08" in i[4])
    checks["priya_ideas"] = (pi == ["I07", "I09"], str(pi))
    fu = sorted(PERSON[i[1]]["name"] for i in INTERACTIONS if i[6] and "2026-10-07" <= i[6] <= "2026-10-11")
    checks["followups"] = (fu == ["Clara Sample", "Lukas Beispiel"], str(fu))
    nw = sorted(d[0] for d in DEADLINES if "2026-10-12" <= d[2] <= "2026-10-18")
    checks["next_week"] = (nw == ["DL04", "DL05", "DL06", "DL07", "DL08", "DL09"], str(nw))
    bad = {k: v[1] for k, v in checks.items() if not v[0]}
    if bad:
        raise SystemExit(f"Computed answers disagree with the data: {bad}")
    return {k: v[1] for k, v in checks.items()}


def resolve(source, email_files):
    kind, _, rest = source.partition(":")
    if kind == "email":
        return email_files[rest]
    if kind in ("doc", "office"):
        return doc_path(rest) or f"downloads/{(DOC.get(rest) or OFFICE_DOC.get(rest))['downloads']}"
    if kind == "note":
        return f"notes/{rest}"
    if kind == "transcript":
        t = next(t for t in TRANSCRIPTS if t["date"] == rest)
        return f"drive/Meetings/{t['date']} {t['title']}.vtt"
    if kind == "record":
        table, _, rid = rest.partition(":")
        return f"records/{table}.csv" + (f" ({rid})" if rid else "")
    if kind == "calendar":
        return f"calendar/alex-example.ics ({rest})"
    if kind == "telegram":
        return "telegram/updates.json" + (f" ({rest})" if rest else "")
    return source


def build_answer_key(email_files, computed):
    qs = []
    for q in QUESTIONS:
        qs.append({"id": q["id"], "type": q["type"], "question": q["question"] if "question" in q else q["q"], "expected": q["a"],
                   "sources": [resolve(s, email_files) for s in q["sources"]],
                   **({"computed_check": computed[q["computed"]]} if q.get("computed") else {})})
    key = {"fixture_only": True, "exclude_from_index": True, "scenario_date": SCENARIO_DATE,
           "note": "Answer key for the fictional second brain pack. Do not import it into a brain; it would invalidate the test.",
           "questions": qs}
    write(PACK / "answer-key" / "questions.json", json.dumps(key, ensure_ascii=False, indent=2) + "\n")
    sorting = {"fixture_only": True, "exclude_from_index": True,
               "items": [{"item": resolve(i, email_files) if not i.startswith("telegram:") else f"telegram/updates.json ({i[9:]})",
                          "belongs_in": b, "why": w} for i, b, w in INBOX_SORTING]}
    write(PACK / "answer-key" / "inbox-sorting.json", json.dumps(sorting, ensure_ascii=False, indent=2) + "\n")
    template = {"note": "Your own test questions. Keep this file in output/, never in Git.", "scenario_date": "YYYY-MM-DD",
                "questions": [{"id": f"MY{n}", "question": "", "expected": "", "type": t, "sources": []}
                              for n, t in enumerate(["fact", "fact", "fact", "fact", "fact", "not_found", "not_found"], 1)]}
    write(PACK / "answer-key" / "my-questions.template.json", json.dumps(template, ensure_ascii=False, indent=2) + "\n")


# ---------------------------------------------------------------------------------- main

def main():
    for d in OUT_DIRS:
        shutil.rmtree(PACK / d, ignore_errors=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        files = build_documents(tmp)
        files.update(build_office(tmp))
        files.update(build_ics())

    # drive/ and downloads/
    for spec in DOCS + OFFICE:
        data, ext = files[spec["id"]]
        when = stamp(spec.get("date") or DOC[spec["source_of"]]["date"], "17:30")
        if spec.get("drive"):
            p = PACK / "drive" / spec["drive"]
            assert p.suffix.lower() == ext, (spec["id"], p.suffix, ext)
            write(p, data, when)
        dls = spec.get("downloads")
        for k, name in enumerate([dls] if isinstance(dls, str) else (dls or [])):
            fname = name if Path(name).suffix.lower() == ext else Path(name).stem + ext
            write(PACK / "downloads" / fname, data, when + 60 * k)
    write(PACK / "downloads" / "AUR7Q2.ics", files["ICS-FLIGHT"][0], stamp("2026-09-08", "21:50"))
    write(PACK / "downloads" / "invite.ics", files["ICS-WALK"][0], stamp("2026-09-22", "09:05"))
    report = files["REPORT"][0]
    write(PACK / "downloads" / "Unconfirmed 482913.crdownload", report[: len(report) // 3], stamp("2026-09-03", "07:20"))

    # mail
    messages = build_mail(files)
    email_files = {}
    mb_path = PACK / "mailbox" / "alex-example.mbox"
    mb_path.parent.mkdir(parents=True, exist_ok=True)
    mbox = mailbox.mbox(str(mb_path), create=True)
    mbox.lock()
    for e, msg in messages:
        name = f"{e['id']}-{slug(e['subject'])}.eml"
        when = dt.datetime.fromisoformat(e["date"]).replace(tzinfo=BERLIN)
        write(PACK / "mailbox" / "eml" / name, msg.as_bytes(), when.timestamp())
        email_files[e["id"]] = f"mailbox/eml/{name}"
        m = mailbox.mboxMessage(msg.as_bytes())
        m["X-Gmail-Labels"] = ",".join(labels_for(e))
        m.set_from(e["frm"][1], when.astimezone(dt.timezone.utc).timetuple())
        if e.get("seen", True):
            m.set_flags("RO")
        mbox.add(m)
    mbox.flush(); mbox.unlock(); mbox.close()
    labels = {e["id"]: labels_for(e) for e, _ in messages}
    write(PACK / "mailbox" / "labels.json", json.dumps({email_files[k]: v for k, v in labels.items()}, indent=2) + "\n")

    build_notes()
    zbuf = io.BytesIO()
    with zipfile.ZipFile(zbuf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted((PACK / "notes").rglob("*.md")):
            z.writestr(zipfile.ZipInfo(str(p.relative_to(PACK / "notes")), date_time=(2026, 10, 7, 9, 0, 0)), p.read_bytes(),
                       compress_type=zipfile.ZIP_DEFLATED)
    write(PACK / "notion" / "notes-for-notion-import.zip", zbuf.getvalue())
    build_transcripts()
    tables = build_records()
    write(PACK / "calendar" / "alex-example.ics", calendar_text(CALENDAR))
    build_telegram()
    computed = check_computed(tables)
    build_answer_key(email_files, computed)

    manifest = []
    for p in sorted(PACK.rglob("*")):
        if p.is_file() and p.relative_to(PACK).parts[0] in OUT_DIRS:
            data = p.read_bytes()
            manifest.append({"path": str(p.relative_to(PACK)), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "fictional": True})
    write(PACK / "manifest.json", json.dumps({"scenario_date": SCENARIO_DATE, "fictional": True, "files": manifest}, indent=1) + "\n")
    total = sum(f["bytes"] for f in manifest)
    print(f"Wrote {len(manifest)} files, {total / 1e6:.1f} MB. Emails: {len(messages)}. Documents: {len(DOCS)}. Notes: {len(NOTES) + 4}.")
    print("Computed checks:", computed)


if __name__ == "__main__":
    main()
