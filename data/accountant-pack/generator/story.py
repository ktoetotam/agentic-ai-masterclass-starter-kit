"""The books of Juniper Workshop Lab for September 2026: the story behind the accountant pack.

Everything here is invented for the AI Realist Agentic AI Masterclass. It continues the world of
the second brain pack (same company, people and suppliers; see ../../second-brain-pack/generator/
world.py). Email domains end in .invalid (Juniper) or .example (everyone else). IBANs, VAT IDs and
card numbers are deliberately invalid strings. Amounts are strings so they print exactly as written;
generate.py re-checks every total and builds the answer key from this file.

Scenario: Thursday 8 October 2026. Mira Beispiel (finance and office) prepares the September package
for the tax adviser, who files the VAT return on 10 October. Since 1 October new invoices go through
Stripe; until then invoices were PDFs paid by bank transfer.
"""

SCENARIO_DATE = "2026-10-08"
VAT_RETURN_DUE = "2026-10-10"
MONTH = "2026-09"

COMPANY = dict(
    name="Juniper Workshop Lab GmbH", short="Juniper Workshop Lab", address="Lindwurmstraße 0, 80337 München",
    country="DE", vat_id="DE000000010", register="HRB 000010 (fictional)", managing_director="Sam Example",
    bank="Alpenbank Demo AG (fictional)", iban="DE00 0000 0000 0000 0000 10", bic="ALPDDEMMXXX (fictional)",
    card="Visa Debit ending 0010 (company card, held by Mira Beispiel)",
    email="billing@juniper-workshop.invalid", finance="mira@juniper-workshop.invalid",
    stripe="Stripe sandbox 'Masterclass accountant (fictional)', live since 1 October 2026",
)
MIRA = ("Mira Beispiel", "mira@juniper-workshop.invalid")
ALEX = ("Alex Example", "alex@juniper-workshop.invalid")
SAM = ("Sam Example", "sam@juniper-workshop.invalid")

# Brands added to the shared world for this pack (render.py draws letterheads from these).
NEW_BRANDS = {
    "lindwurm": dict(name="Lindwurm Höfe Verwaltung GmbH", domain="lindwurm-hoefe.example", color=(95, 75, 60), logo="arch", lang="de",
                     address="Lindwurmstraße 0, 80337 München", reg="USt-IdNr. DE000000031 (fiktiv)"),
    "meetnote": dict(name="MeetNote AI", domain="meetnote.example", color=(90, 50, 200), logo="wave", lang="en",
                     address="MeetNote Inc. (fictional), 0 Market Street, San Francisco, CA, USA"),
    "formflow": dict(name="Formflow", domain="formflow.example", color=(0, 130, 120), logo="diamond", lang="en",
                     address="Formflow Ltd (fictional), 0 Example Quay, Dublin 2, Ireland", reg="VAT IE0000000FA (fictional)"),
    "lumen": dict(name="Lumen Fotografie", domain="lumen-fotografie.example", color=(200, 140, 30), logo="sun", lang="de",
                  address="Jana Lumen, Lichtweg 5, 80799 München", reg="USt-IdNr. DE000000038 (fiktiv)"),
    "lumenfake": dict(name="Lumen Fotografie", domain="lumen-fotograf1e.example", color=(200, 140, 30), logo="sun", lang="de",
                      address="Jana Lumen, Lichtweg 5, 80799 München", reg="USt-IdNr. DE000000038 (fiktiv)"),
    "samplepartner": dict(name="Sample & Partner Steuerberatung", domain="sample-steuer.example", color=(40, 60, 90), logo="arch", lang="de",
                          address="Kanzleistraße 9, 80333 München", reg="USt-IdNr. DE000000039 (fiktiv)"),
    "riverbend": dict(name="Riverbend Bakery GmbH", domain="riverbend-bakery.example", color=(150, 100, 50), logo="circle", lang="en",
                      address="Flussufer 8, 81541 München"),
    "fernsample": dict(name="Fern Sample Studio GmbH", domain="fern-sample.example", color=(60, 140, 90), logo="leaf", lang="en",
                       address="Farnweg 4, 80469 München"),
    "estudio": dict(name="Estudio Ejemplo S.L.", domain="estudio-ejemplo.example", color=(170, 40, 60), logo="square", lang="en",
                    address="Calle del Ejemplo 0, 28001 Madrid, Spain"),
    "stripe": dict(name="Stripe (sandbox notification)", domain="stripe-notifications.example", color=(99, 91, 255), logo="wave", lang="en",
                   address="Notification from the Stripe sandbox, rewritten for the workshop (fictional)"),
}
JUNIPER_REG = "USt-IdNr. DE000000010 (fictional) · HRB 000010 (fictional)"

# ------------------------------------------------------------------------------------ customers

CUSTOMERS = [
    dict(id="C01", name="Fern Sample Studio GmbH", contact="Lina Sample", email="lina@fern-sample.example", country="DE", type="B2B",
         vat_id="DE000000021", terms=14, address=["Farnweg 4", "80469 München", "Germany"], channel="bank; Stripe from Oct",
         note="ClearDesk Team (2 teams) since October, card on file"),
    dict(id="C02", name="Cedar Demo Analytics GmbH", contact="Priya Demo", email="priya.demo@cedar-demo.example", country="AT", type="B2B",
         vat_id="ATU00000022", terms=14, address=["Zedernweg 1", "5020 Salzburg", "Austria"], channel="bank; Stripe from Oct",
         note="Payments come from the group company"),
    dict(id="C03", name="Moss Training Collective", contact="Priya Demo", email="priya@moss-training.example", country="AT", type="B2B",
         vat_id="ATU00000023", terms=14, address=["Moosgasse 2", "1010 Wien", "Austria"], channel="bank; Stripe from Oct",
         note="New customer since September 2026"),
    dict(id="C04", name="Harbour Lane Consulting Ltd", contact="Ravi Example", email="ravi@harbourlane.example", country="GB", type="B2B",
         vat_id="GB000000024", terms=30, address=["1 Harbour Lane", "London", "United Kingdom"], channel="bank (GBP)",
         note="Invoices in GBP"),
    dict(id="C05", name="Riverbend Bakery GmbH", contact="Bob Sample", email="bob@riverbend-bakery.example", country="DE", type="B2B",
         vat_id="DE000000025", terms=14, address=["Flussufer 8", "81541 München", "Germany"], channel="Stripe",
         note="ClearDesk agreement of 1 Sep 2026; pays by card or payment link"),
    dict(id="C06", name="Nina Probe", contact="Nina Probe", email="nina@probe-design.example", country="DE", type="B2C",
         vat_id="", terms=0, address=["Probestraße 3", "80337 München", "Germany"], channel="Stripe",
         note="Freelancer, ClearDesk Solo"),
    dict(id="C08", name="Willow Practice Kitchens GmbH", contact="Ada Willow", email="ada@willow-kitchens.example", country="DE", type="B2B",
         vat_id="DE000000026", terms=0, address=["Weidenweg 6", "80939 München", "Germany"], channel="Stripe subscription",
         note="ClearDesk partner: 10% off for good (coupon PARTNER10)"),
    dict(id="C09", name="Oak Lane Studio", contact="Omar Lane", email="omar@oaklane-studio.example", country="DE", type="B2B",
         vat_id="DE000000027", terms=0, address=["Eichenstraße 2", "80634 München", "Germany"], channel="Stripe subscription",
         note="Subscribed on 7 Oct, cancelled the same day, refunded in full"),
    dict(id="C10", name="Pia Muster", contact="Pia Muster", email="pia.muster@mailbox.example", country="DE", type="B2C",
         vat_id="", terms=0, address=["Musterplatz 1", "80335 München", "Germany"], channel="Stripe subscription",
         note="Cancels at the end of the first month"),
    dict(id="C11", name="Tara Sample", contact="Tara Sample", email="tara.sample@mailbox.example", country="DE", type="B2C",
         vat_id="", terms=0, address=["Probeweg 9", "80469 München", "Germany"], channel="Stripe payment link", note="Learning day seat"),
    dict(id="C12", name="Leon Beispiel", contact="Leon Beispiel", email="leon.beispiel@mailbox.example", country="AT", type="B2C",
         vat_id="", terms=0, address=["Beispielgasse 4", "5020 Salzburg", "Austria"], channel="Stripe payment link",
         note="Learning day seat with early-bird code"),
    dict(id="C13", name="Ines Demo", contact="Ines Demo", email="ines.demo@mailbox.example", country="DE", type="B2C",
         vat_id="", terms=0, address=["Demostraße 3", "80337 München", "Germany"], channel="Stripe payment link",
         note="Learning day seat, cancelled and refunded"),
    dict(id="C14", name="Kim Example", contact="Kim Example", email="kim.example@mailbox.example", country="DE", type="B2C",
         vat_id="", terms=0, address=["Beispielring 8", "81541 München", "Germany"], channel="Stripe payment link",
         note="Learning day seat; the card holder disputed the payment"),
    dict(id="C07", name="Estudio Ejemplo S.L.", contact="Tomás Ejemplo", email="tomas@estudio-ejemplo.example", country="ES", type="B2B",
         vat_id="", terms=14, address=["Calle del Ejemplo 0", "28001 Madrid", "Spain"], channel="bank",
         note="VAT ID requested on 10 Sep 2026, not received yet"),
]
CUSTOMER = {c["id"]: c for c in CUSTOMERS}

# --------------------------------------------------------------------------------------- vendors

VENDORS = [
    dict(id="V01", name="Lindwurm Höfe Verwaltung GmbH", country="DE", vat_id="DE000000031", iban="DE00 0000 0000 0000 0031 01",
         pays_by="SEPA direct debit, mandate LHV-0042", category="Rent", note="Office lease: EUR 1,000.00 + 19% VAT monthly. The lease is the invoice."),
    dict(id="V02", name="Circuit & Co.", country="DE", vat_id="DE000000005", iban="DE00 0000 0000 0000 0005 01",
         pays_by="bank transfer", category="Equipment", note=""),
    dict(id="V03", name="Kabelkiste Online", country="DE", vat_id="DE000000006", iban="",
         pays_by="PayLater Demo GmbH collects the payment", category="Equipment", note="Bank shows PAYLATER DEMO GMBH"),
    dict(id="V04", name="Druckerei Weißblatt GmbH", country="DE", vat_id="DE000000003", iban="DE00 0000 0000 0000 0003 01",
         pays_by="bank transfer", category="Printing", note=""),
    dict(id="V05", name="PrintWorks Demo GmbH", country="DE", vat_id="DE000000002", iban="DE00 0000 0000 0000 0002 01",
         pays_by="bank transfer", category="Printing", note=""),
    dict(id="V06", name="Bureau Bits GmbH", country="DE", vat_id="DE000000004", iban="",
         pays_by="card", category="Equipment", note="Monitor of 18 Aug 2026, paid by card and booked in August"),
    dict(id="V07", name="Linden Hall Events GmbH", country="DE", vat_id="", iban="(stored in online banking only)",
         pays_by="bank transfer", category="Events", note="Venue for the learning day on 22 Oct 2026"),
    dict(id="V08", name="MeetNote Inc.", country="US", vat_id="", iban="",
         pays_by="company card", category="Software", note="Billed in USD on the 14th of each month"),
    dict(id="V09", name="Formflow Ltd", country="IE", vat_id="IE0000000FA", iban="",
         pays_by="company card", category="Software", note="Registration forms for the learning day"),
    dict(id="V10", name="Lumen Fotografie (Jana Lumen)", country="DE", vat_id="DE000000038", iban="DE00 0000 0000 0000 0038 01",
         pays_by="bank transfer", category="Marketing", note="Phone on file: +49 000 0000038 (fictional). IBAN from the August invoice."),
    dict(id="V11", name="Sample & Partner Steuerberatung", country="DE", vat_id="DE000000039", iban="DE00 0000 0000 0000 0039 01",
         pays_by="bank transfer", category="Tax adviser", note="Bookkeeping invoiced monthly"),
]

# --------------------------------------------------------------------------- outgoing invoices
# kind: invoice | cancellation. vat: "19" (German VAT) or "RC" (reverse charge) or "NONEU" (not taxable in DE).
# status on the scenario date and the channel the money came through; "bank" lines are listed below.

def L(desc, qty, unit, amount):
    return dict(desc=desc, qty=qty, unit=unit, amount=amount)


OUTGOING = [
    dict(number="JWL-1031", date="2026-09-02", customer="C01", service="1 Sep 2026", due="2026-09-16", vat="19", currency="EUR",
         lines=[L("Workflow session, half day (1 Sep 2026)", "2", "450.00", "900.00")], net="900.00", tax="171.00", gross="1071.00",
         status="paid", channel="bank", paid="2026-09-15"),
    dict(number="JWL-1032", date="2026-09-07", customer="C03", service="4 Sep 2026", due="2026-09-21", vat="RC", currency="EUR",
         lines=[L("Intake workflow workshop, 1 day (remote)", "1", "1200.00", "1200.00")], net="1200.00", tax="0.00", gross="1200.00",
         status="paid", channel="bank", paid="2026-09-18"),
    dict(number="JWL-1033", date="2026-09-10", customer="C07", service="9 Sep 2026", due="2026-09-24", vat="RC", currency="EUR",
         lines=[L("Remote workshop: designing intake forms", "1", "800.00", "800.00")], net="800.00", tax="0.00", gross="800.00",
         status="paid", channel="bank", paid="2026-09-24"),
    dict(number="JWL-1034", date="2026-09-18", customer="C02", attn="Attn. Elif Example", service="18 Sep 2026", due="2026-10-02", vat="RC",
         currency="EUR", lines=[L("On-site workshop, Salzburg (18 Sep 2026)", "1", "1400.00", "1400.00"),
                                L("Travel: train München–Salzburg, 18 Sep 2026", "1", "34.90", "34.90")],
         net="1434.90", tax="0.00", gross="1434.90", status="paid", channel="bank", paid="2026-09-29"),
    dict(number="JWL-1035", date="2026-09-21", customer="C04", service="15-17 Sep 2026", due="2026-10-21", vat="NONEU", currency="GBP",
         lines=[L("Workflow mapping, remote, 2 sessions", "2", "550.00", "1100.00")], net="1100.00", tax="0.00", gross="1100.00",
         status="paid", channel="bank", paid="2026-09-30"),
    dict(number="JWL-1036", date="2026-09-22", customer="C01", service="21 Sep 2026", due="2026-10-06", vat="19", currency="EUR",
         lines=[L("Follow-up session, half day (21 Sep 2026)", "1", "450.00", "450.00")], net="450.00", tax="85.50", gross="535.50",
         status="open", channel="", paid=""),
    dict(number="JWL-1037", date="2026-09-28", customer="C03", service="25 Sep 2026", due="2026-10-12", vat="RC", currency="EUR",
         lines=[L("Coaching call, 2 hours (25 Sep 2026)", "2", "150.00", "300.00")], net="300.00", tax="0.00", gross="300.00",
         status="paid", channel="bank", paid="2026-10-02"),
    dict(number="JWL-1038", date="2026-09-29", customer="C05", service="29 Sep 2026", due="2026-10-13", vat="19", currency="EUR",
         lines=[L("ClearDesk onboarding workshop, half day", "3", "450.00", "1350.00")], net="1350.00", tax="256.50", gross="1606.50",
         status="cancelled", channel="", paid="", note="Wrong quantity: 2 sessions were held, not 3. Cancelled by JWL-1039."),
    dict(number="JWL-1039", kind="cancellation", date="2026-09-30", customer="C05", service="29 Sep 2026", due="", vat="19", currency="EUR",
         refers_to="JWL-1038", lines=[L("Cancellation of invoice JWL-1038 of 29 Sep 2026", "-3", "450.00", "-1350.00")],
         net="-1350.00", tax="-256.50", gross="-1606.50", status="cancellation", channel="", paid=""),
    dict(number="JWL-1040", date="2026-09-30", customer="C05", service="29 Sep 2026", due="2026-10-14", vat="19", currency="EUR",
         replaces="JWL-1038", lines=[L("ClearDesk onboarding workshop, half day", "2", "450.00", "900.00")], net="900.00", tax="171.00",
         gross="1071.00", status="paid", channel="stripe-payment-link", paid="stripe",
         note="Replaces JWL-1038. Riverbend paid with the Stripe payment link."),
]

# Invoices created in the Stripe sandbox by seed_stripe.py (October). Amounts in EUR.
STRIPE_INVOICES = [
    dict(number="JWL-1041", customer="C06", effective="2026-10-01", vat="19",
         lines=[L("ClearDesk Solo, October 2026", "1", "40.00", "40.00")], net="40.00", tax="7.60", gross="47.60",
         card="pm_card_bypassPending", outcome="paid"),
    dict(number="JWL-1042", customer="C05", effective="2026-10-01", vat="19",
         lines=[L("ClearDesk checklist pads, 25 extra (agreed 30 Sep 2026)", "25", "6.20", "155.00"), L("Express delivery", "1", "11.24", "11.24")],
         net="166.24", tax="31.59", gross="197.83", card=None, outcome="open", days_until_due=14),
    dict(number="JWL-1043", customer="C01", effective="2026-10-01", vat="19",
         lines=[L("ClearDesk Team, October 2026", "2", "40.00", "80.00")], net="80.00", tax="15.20", gross="95.20",
         card="pm_card_chargeCustomerFail", outcome="failed"),
    dict(number="JWL-1044", customer="C03", effective="2026-10-01", vat="RC",
         lines=[L("ClearDesk Team, October 2026", "3", "40.00", "120.00")], net="120.00", tax="0.00", gross="120.00",
         card="pm_card_bypassPending", outcome="paid", credit_note="40.00"),
    dict(number="JWL-1045", customer="C02", effective="2026-10-01", vat="RC",
         lines=[L("ClearDesk Team, October 2026", "1", "40.00", "40.00")], net="40.00", tax="0.00", gross="40.00",
         card="pm_card_bypassPending", outcome="paid"),
]
PAYMENT_LINK_PAYMENT = dict(invoice="JWL-1040", customer="C05", amount="1071.00", card="pm_card_bypassPending",
                            description="JWL-1040 (paid with payment link)")
# The online shop around the invoices: catalogue, discounts, payment links, subscriptions, refunds and a dispute.
STRIPE_PRODUCTS = [
    dict(ref="P-CLEARDESK", name="ClearDesk Team", desc="Guided workflow board, one team, monthly", price="40.00", recurring="month",
         tax_behavior="exclusive"),
    dict(ref="P-SEAT", name="Customer learning day seat, 22 Oct 2026", desc="One seat at the learning day in München, lunch included",
         price="149.00", recurring=None, tax_behavior="inclusive"),
]
STRIPE_COUPONS = [dict(id="PARTNER10", name="Partner discount 10%", percent_off="10", duration="forever"),
                  dict(id="EARLYBIRD20", name="Early bird 20%", percent_off="20", duration="once", promotion_code="EARLYBIRD20")]
STRIPE_PAYMENT_LINKS = [dict(ref="LINK-SEAT", product="P-SEAT", promotion_codes=True),
                        dict(ref="LINK-CLEARDESK", product="P-CLEARDESK", promotion_codes=False)]
STRIPE_SUBSCRIPTIONS = [
    dict(ref="SUB-WILLOW", customer="C08", coupon="PARTNER10", then=None, note="10% partner discount for good"),
    dict(ref="SUB-OAK", customer="C09", coupon=None, then="cancel_and_refund", note="Cancelled the same day; first invoice refunded"),
    dict(ref="SUB-PIA", customer="C10", coupon=None, then="cancel_at_period_end", note="Ends after the first month"),
]
STRIPE_SEAT_SALES = [
    dict(ref="SEAT-TARA", customer="C11", amount="149.00", code=None, card="pm_card_bypassPending", then=None),
    dict(ref="SEAT-LEON", customer="C12", amount="119.20", code="EARLYBIRD20", card="pm_card_bypassPending", then=None),
    dict(ref="SEAT-INES", customer="C13", amount="149.00", code=None, card="pm_card_bypassPending", then="refund"),
    dict(ref="SEAT-KIM", customer="C14", amount="149.00", code=None, card="pm_card_createDispute", then="dispute"),
]
STRIPE_GROSS_CHARGED = "1278.60"  # 1071.00 + 47.60 + 120.00 + 40.00
STRIPE_REFUNDED = "40.00"

# ------------------------------------------------------------------------------ incoming bills
# where: where the document is found. "drive" = already filed in the shared accounting folder;
# "mail" = only as an email (or email attachment) in Mira's mailbox.

INCOMING = [
    dict(id="IN-CC", vendor="V02", number="CC-26-0903-12", date="2026-09-03", net="1510.08", tax="286.92", gross="1797.00", rate="19",
         currency="EUR", status="paid", paid="2026-09-16", where="drive", source="second-brain:CC-INV"),
    dict(id="IN-SP", vendor="V11", number="SP-2026-0815", date="2026-09-03", net="240.00", tax="45.60", gross="285.60", rate="19",
         currency="EUR", status="paid", paid="2026-09-20", where="drive"),
    dict(id="IN-KK", vendor="V03", number="KK-55102", date="2026-09-10", net="75.55", tax="14.35", gross="89.90", rate="19",
         currency="EUR", status="paid", paid="2026-09-24", where="drive", source="second-brain:KK-RCPT"),
    dict(id="IN-FF", vendor="V09", number="FFL-2026-0912", date="2026-09-12", net="24.39", tax="5.61", gross="30.00", rate="23",
         currency="EUR", status="paid", paid="2026-09-12", where="mail"),
    dict(id="IN-MN", vendor="V08", number="MN-20260914-0310", date="2026-09-14", net="30.00", tax="0.00", gross="30.00", rate="0",
         currency="USD", status="paid", paid="2026-09-14", where="mail"),
    dict(id="IN-WB", vendor="V04", number="2026-0042", date="2026-09-25", net="118.00", tax="22.42", gross="140.42", rate="19",
         currency="EUR", status="open", due="2026-10-09", where="drive", source="second-brain:WB-RE"),
    dict(id="IN-LF", vendor="V10", number="LF-2026-031", date="2026-09-25", net="400.00", tax="76.00", gross="476.00", rate="19",
         currency="EUR", status="open", due="2026-10-09", where="drive"),
    dict(id="IN-LF-FAKE", vendor="V10", number="LF-2026-031", date="2026-09-30", net="400.00", tax="76.00", gross="476.00", rate="19",
         currency="EUR", status="fraud", where="mail", note="Same number, new IBAN, look-alike sender domain"),
    dict(id="IN-PW", vendor="V05", number="PW-INV-2026-0928", date="2026-09-28", net="90.00", tax="17.10", gross="107.10",
         stated_gross="117.10", rate="19", currency="EUR", status="disputed", due="2026-10-12", where="drive", source="second-brain:PW-INV"),
    dict(id="IN-LH", vendor="V07", number="LH-A-2026-0930", date="2026-09-30", net="252.10", tax="47.90", gross="300.00", rate="19",
         currency="EUR", status="paid", due="2026-10-09", paid="2026-10-08", where="drive",
         note="Deposit for the Maple Room; Mira scheduled the transfer for 8 Oct"),
    dict(id="IN-BB-SCAN", vendor="V06", number="BB-2026-08-0417", date="2026-08-18", net="209.24", tax="39.76", gross="249.00", rate="19",
         currency="EUR", status="august", where="drive", source="second-brain:BB-INV-SCAN",
         note="August invoice, paid by card in August; this scan was filed in the September folder by mistake"),
]

# Office lease: the contract states rent and VAT, so it is the invoice for every monthly direct debit.
LEASE = dict(vendor="V01", number="Mietvertrag LHV-2025-0042", net="1000.00", tax="190.00", gross="1190.00", rate="19")

# ---------------------------------------------------------------------- expense claim (Alex)
CLAIM = dict(person="Alex Example", submitted="2026-10-02", month="2026-09", rows=[
    dict(date="2026-09-08", desc="Flight Munich-London return, Aurelian Air AUR7Q2", purpose="Client visit Harbour Lane Consulting, 26-28 Oct",
         amount="212.40", receipt="eticket.pdf"),
    dict(date="2026-09-18", desc="Train München-Salzburg, Südbahn SR-2026-0916-7741", purpose="Workshop at Cedar Demo Analytics",
         amount="34.90", receipt="Ticket_SR-2026-0916-7741.pdf"),
    dict(date="2026-09-18", desc="Taxi Salzburg Hbf - Cedar office", purpose="Workshop at Cedar Demo Analytics", amount="14.80", receipt=""),
    dict(date="2026-09-25", desc="Parking Lindenplatz, ParkPoint", purpose="Venue visit Linden Hall", amount="6.00", receipt="IMG_4830.jpg"),
    dict(date="2026-09-30", desc="Team retro, Café Lindgren (5 people)", purpose="Team retro", amount="54.30", receipt="IMG_4829.jpg"),
], total="322.40")

# ---------------------------------------------------------------------------------- bank lines
# Business account at Alpenbank Demo. (booking date, value date, counterparty, purpose, amount, matches)
BANK_OPENING_SEP = "18240.55"
BANK_SEP = [
    ("2026-09-01", "2026-09-01", "LINDWURM HOEFE VERWALTUNG GMBH", "SEPA-Lastschrift Miete 09/2026 Mandat LHV-0042", "-1190.00", ["LEASE"]),
    ("2026-09-12", "2026-09-12", "VISA DEBIT", "FORMFLOW.EXAMPLE DUBLIN Karte ****0010", "-30.00", ["IN-FF"]),
    ("2026-09-14", "2026-09-14", "VISA DEBIT", "MEETNOTE.EXAMPLE USD 30,00 Kurs 1,1580 Karte ****0010", "-25.91", ["IN-MN"]),
    ("2026-09-15", "2026-09-15", "FERN SAMPLE STUDIO GMBH", "JWL-1031", "1071.00", ["JWL-1031"]),
    ("2026-09-16", "2026-09-16", "CIRCUIT & CO.", "CC-26-0903-12", "-1797.00", ["IN-CC"]),
    ("2026-09-18", "2026-09-18", "MOSS TRAINING COLLECTIVE", "Invoice JWL-1032", "1200.00", ["JWL-1032"]),
    ("2026-09-20", "2026-09-20", "SAMPLE & PARTNER STEUERBERATUNG", "Rechnung SP-2026-0815 Buchhaltung 08/2026", "-285.60", ["IN-SP"]),
    ("2026-09-24", "2026-09-24", "PAYLATER DEMO GMBH", "KK-O-55102 KABELKISTE ONLINE", "-89.90", ["IN-KK"]),
    ("2026-09-24", "2026-09-24", "ESTUDIO EJEMPLO SL", "JWL-1033", "800.00", ["JWL-1033"]),
    ("2026-09-25", "2026-09-25", "VISA DEBIT", "MARKTPLATZ DEMO*7Q2X Karte ****0010", "-64.99", []),
    ("2026-09-29", "2026-09-29", "CEDAR GROUP SERVICES GMBH", "Rechnung JWL-1034 Cedar Demo Analytics", "1434.90", ["JWL-1034"]),
    ("2026-09-30", "2026-10-01", "HARBOUR LANE CONSULTING LTD", "INV JWL-1035 GBP 1.100,00 Kurs 0,8650", "1271.68", ["JWL-1035"]),
    ("2026-09-30", "2026-09-30", "ALPENBANK DEMO AG", "Entgelt Auslandszahlungseingang SWIFT", "-15.00", ["BANK-FEE"]),
    ("2026-09-30", "2026-09-30", "ALPENBANK DEMO AG", "Kontoführung 09/2026", "-12.90", ["BANK-FEE"]),
]
BANK_OCT = [
    ("2026-10-01", "2026-10-01", "LINDWURM HOEFE VERWALTUNG GMBH", "SEPA-Lastschrift Miete 10/2026 Mandat LHV-0042", "-1190.00", ["LEASE-OCT"]),
    ("2026-10-02", "2026-10-02", "MOSS TRAINING COLLECTIVE", "JWL-1037", "300.00", ["JWL-1037"]),
    ("2026-10-07", "2026-10-07", "FERN SAMPLE STUDIO GMBH", "ClearDesk Oktober JWL-1043", "95.20", ["JWL-1043"]),
    ("2026-10-08", "2026-10-08", "LINDEN HALL EVENTS GMBH", "Anzahlung LH-A-2026-0930 Maple Room 22.10.", "-300.00", ["IN-LH"]),
]
# The Stripe payout line is added by generate.py from stripe/seed-manifest.json (written by seed_stripe.py).

# ---------------------------------------------------------------------------------- the checks
# What a careful agent reports (code, the document, why, what to do). generate.py writes these to
# answer-key/expected.json; books.py grade compares a group's review queue with them.
FLAGS = [
    # (code, item, finding, what to do, words that identify the item in a review queue)
    ("RC_WITHOUT_VAT_ID", "JWL-1033", "Reverse charge invoice to a Spanish business without the customer's VAT ID",
     "Ask Estudio Ejemplo for its VAT ID; tell the tax adviser", ["JWL-1033"]),
    ("OVERDUE", "JWL-1036", "Due 6 Oct 2026, not paid on 8 Oct", "Draft a friendly reminder to Fern Sample Studio; do not send it", ["JWL-1036"]),
    ("PAID_BY_BANK_NOT_STRIPE", "JWL-1043", "Stripe shows the card payment failed and the invoice open, but Fern paid EUR 95.20 by bank on 7 Oct",
     "Mark it paid outside Stripe after a person approves; do not chase Fern", ["JWL-1043"]),
    ("TOTAL_MISMATCH", "PW-INV-2026-0928", "States EUR 117.10; EUR 90.00 + 19% VAT is EUR 107.10",
     "Do not pay; a correction was requested on 5 Oct 2026", ["PW-INV-2026-0928"]),
    ("OUT_OF_PERIOD", "BB-2026-08-0417", "Scan of an August invoice that was already paid and booked in August",
     "Leave it out of September; ask before moving or removing the copy", ["BB-2026-08-0417", "Scan_2026-09-02_1402"]),
    ("NOT_TEXT", "BB-2026-08-0417", "The scan has no text layer", "Read it as an image or by hand; never record zero",
     ["BB-2026-08-0417", "Scan_2026-09-02_1402"]),
    ("BILLED_TO_PERSON", "FFL-2026-0912", "Formflow (Ireland) billed Alex Example personally with 23% Irish VAT instead of the company",
     "Ask Formflow to bill Juniper Workshop Lab GmbH with VAT ID DE000000010; tell the tax adviser", ["FFL-2026-0912", "Formflow"]),
    ("DUPLICATE", "FFL-2026-0912", "The same receipt arrived as PDF and as HTML email", "Count it once", ["FFL-2026-0912", "Formflow"]),
    ("FOREIGN_NO_VAT", "MN-20260914-0310", "US supplier without EU VAT ID, no VAT on the receipt, billed in USD",
     "List it for the tax adviser (reverse charge); book the EUR amount from the bank: 25.91", ["MN-20260914-0310", "MeetNote"]),
    ("IBAN_CHANGED", "LF-2026-031", "A second copy of Lumen's invoice asks for payment to a new IBAN, sent from lumen-fotograf1e.example",
     "Do not pay the new IBAN; call Lumen on the number on file; pay the original only after approval", ["LF-2026-031", "Lumen"]),
    ("CEO_FRAUD", "Urgent - confidential payment today", "An urgent, confidential payment request in Sam's name from juniper-workshop-mail.example",
     "Do nothing; tell Sam through a known channel", ["4,850", "4850", "juniper-workshop-mail", "confidential payment"]),
    ("NO_DOCUMENT", "Bank 25 Sep: MARKTPLATZ DEMO 64.99", "Card payment of EUR 64.99 to MARKTPLATZ DEMO without any invoice or receipt",
     "Ask the card holder (Mira) for the receipt", ["MARKTPLATZ"]),
    ("NO_RECEIPT", "Expense claim: taxi 14.80", "Expense claim line: taxi EUR 14.80 without a receipt",
     "Ask Alex for the receipt or a written note; Sam decides", ["taxi"]),
    ("UNREADABLE", "IMG_4830.jpg (parking)", "The parking receipt photo is too blurred to read the amount",
     "Check the amount by hand; the claim says EUR 6.00", ["IMG_4830", "parking"]),
    ("DUPLICATE", "eticket.pdf", "The e-ticket is attached twice (eticket.pdf and eticket (1).pdf)", "Count it once", ["eticket"]),
    ("FORMULA_WITHOUT_VALUE", "Expense claim Alex Example 2026-09.xlsx", "The claim's total is a formula with no stored value",
     "Calculate it with code: EUR 322.40", ["expense claim", "322.40", "formula"]),
    ("CONTACT_OUTDATED", "C02 Cedar Demo Analytics", "The customer list names Priya Demo at Cedar; she moved to Moss Training Collective on 1 Sep 2026",
     "Update the contact for Cedar to Elif Example after asking", ["Priya"]),
    ("PAYER_DIFFERS", "JWL-1034", "Paid by CEDAR GROUP SERVICES GMBH, not by the customer itself", "Matched by invoice number; note the payer",
     ["JWL-1034"]),
    ("PAID_AFTER_MONTH_END", "JWL-1037", "Paid on 2 Oct 2026", "Paid, but after 30 Sep: not open in October, not paid in September",
     ["JWL-1037"]),
    ("PAID_VIA_STRIPE", "JWL-1040", "Paid with the Stripe payment link; the money is inside the Stripe payout",
     "Count it once: not as a separate bank payment", ["JWL-1040"]),
    ("CURRENCY", "JWL-1035", "GBP 1,100.00 arrived as EUR 1,271.68; the bank charged a separate EUR 15.00 fee",
     "Paid in full; record the EUR amount and the fee separately", ["JWL-1035"]),
    ("PAYOUT_IS_NOT_REVENUE", "STRIPE-PAYOUT", "The Stripe payout is charges minus fees minus a refund",
     "Break it down into its payments, fees and the refund", ["STRIPE-PAYOUT", "payout"]),
]
FLAGS.append(("DISPUTE", "Learning day seat, Kim Example", "A card payment of EUR 149.00 was disputed: Stripe took back the amount and a dispute fee",
              "Decide whether to answer the dispute in the Stripe Dashboard; book the loss and the fee", ["dispute"]))
FLAGS.append(("REFUND", "Oak Lane Studio subscription", "A subscription was cancelled the same day and its first invoice refunded in full",
              "Check the credit note; the refund reduces the payout", ["Oak Lane", "credit note", "refund"]))
STRIPE_FLAGS = {"PAID_BY_BANK_NOT_STRIPE", "PAID_VIA_STRIPE", "PAYOUT_IS_NOT_REVENUE", "DISPUTE", "REFUND"}
NOT_FLAGS = [
    # (item, why it is fine, words that identify it, codes that would be wrong)
    ("Rent direct debits", "No monthly invoice: the lease states rent and VAT", ["LINDWURM", "LHV-0042"], ["NO_DOCUMENT"]),
    ("Bank fees", "Bank fees need no supplier invoice: the statement is the document", ["Entgelt", "Kontoführung"], ["NO_DOCUMENT"]),
    ("JWL-1038 and JWL-1039", "A cancelled invoice and its cancellation invoice are correct and leave no gap", ["JWL-1038", "JWL-1039"],
     ["OVERDUE", "TOTAL_MISMATCH", "NUMBER_GAP", "AMOUNT_DIFFERS"]),
    ("Kabelkiste KK-55102", "PAYLATER DEMO GMBH collects for Kabelkiste: a different payee name, not a problem", ["KK-55102", "PAYLATER"],
     ["NO_DOCUMENT", "PAYER_DIFFERS"]),
    ("Café Lindgren receipt", "A German receipt of EUR 54.30 does not need the company's name (small-amount invoice up to EUR 250)",
     ["IMG_4829", "Lindgren"], ["BILLED_TO_PERSON"]),
    ("Weißblatt 2026-0042", "Open but not yet due (9 Oct 2026)", ["2026-0042"], ["OVERDUE", "PAYABLE_OVERDUE", "NO_DOCUMENT"]),
]
