# /// script
# requires-python = ">=3.10"
# dependencies = ["certifi"]
# ///
"""Fill a Stripe SANDBOX with Juniper Workshop Lab's October payments, for the accountant pack.

Facilitator tool. It creates five customers, five invoices (JWL-1041 to JWL-1045: paid, open, failed),
one card payment for JWL-1040 (the payment link), one partial refund through a credit note and one
manual payout, then writes stripe/seed-manifest.json and a CSV snapshot that generate.py and the
challenge skills use. Re-running finds what is already there (by metadata pack_ref) and skips it.

    uv run --no-project --script data/accountant-pack/generator/seed_stripe.py            # dry run: shows the plan
    uv run --no-project --script data/accountant-pack/generator/seed_stripe.py --apply    # creates the objects
    uv run --no-project --script data/accountant-pack/generator/seed_stripe.py --check    # read-only summary

The key: a sandbox secret key (sk_test_...) in STRIPE_SEED_KEY, either in the environment or in the
project's ignored .env file. Live keys are refused. The sandbox needs EUR as its currency and the payout
schedule set to Manual (Dashboard > Settings > Payouts); a new sandbox has a test bank account.
"""

import argparse
import base64
import csv
import datetime as dt
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

GEN = Path(__file__).resolve().parent
PACK = GEN.parent
ROOT = PACK.parent.parent
sys.path.insert(0, str(GEN))
import story as S  # noqa: E402

API = "https://api.stripe.com/v1"
API_VERSION = "2026-09-30.endive"  # the version these requests were checked against (stripe/openapi spec3.json)
BERLIN = ZoneInfo("Europe/Berlin")
TAG = "accountant-pack-v1"
STRIPE_CUSTOMERS = ["C01", "C02", "C03", "C05", "C06", "C08", "C09", "C10", "C11", "C12", "C13", "C14"]
FOOTER = (f"{S.COMPANY['name']} (fictional) · {S.COMPANY['address']} · USt-IdNr. {S.COMPANY['vat_id']} (fictional). "
          "Fictional workshop data: not a real invoice.")

try:
    import certifi
    CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # fall back to the system store
    CTX = ssl.create_default_context()


def cents(amount):
    return int((Decimal(amount) * 100).to_integral_value())


def euros(c):
    return f"{Decimal(c) / 100:.2f}"


def read_key():
    key = os.environ.get("STRIPE_SEED_KEY", "").strip()
    env = ROOT / ".env"
    found = False
    if not key and env.exists():
        for line in env.read_text(encoding="utf-8-sig").splitlines():
            m = re.match(r"\s*(?:export\s+)?STRIPE_SEED_KEY\s*=\s*(.*)$", line)
            if m:
                found = True
                key = m.group(1).strip().strip('"').strip("'")
    if not key and found:
        sys.exit(f"STRIPE_SEED_KEY in {env} is empty: paste the sandbox secret key (sk_test_...) after the = sign and save the file.")
    if not key:
        sys.exit(f"No key: add a line STRIPE_SEED_KEY=sk_test_... (a SANDBOX secret key) to {env}.")
    if "_live_" in key or not ("_test_" in key):
        sys.exit("Refused: this is not a sandbox (test) key. Use the secret key of the sandbox, which starts with sk_test_.")
    return key


def flatten(params, prefix=""):
    out = []
    for k, v in params.items():
        name = f"{prefix}[{k}]" if prefix else k
        if isinstance(v, dict):
            out += flatten(v, name)
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    out += flatten(item, f"{name}[{i}]")
                else:
                    out.append((f"{name}[]", str(item)))
        elif v is not None:
            out.append((name, "true" if v is True else "false" if v is False else str(v)))
    return out


class Stripe:
    def __init__(self, key):
        self.auth = "Basic " + base64.b64encode(f"{key}:".encode()).decode()

    def call(self, method, path, params=None, idem=None):
        data = None
        url = API + path
        if params and method == "GET":
            url += "?" + urllib.parse.urlencode(flatten(params))
        elif params:
            data = urllib.parse.urlencode(flatten(params)).encode()
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self.auth)
        req.add_header("Stripe-Version", API_VERSION)
        if idem:
            req.add_header("Idempotency-Key", f"{TAG}-{idem}")
        try:
            with urllib.request.urlopen(req, context=CTX, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            body = json.loads(e.read() or b"{}")
            err = body.get("error", {})
            raise StripeError(e.code, err.get("code") or err.get("type"), err.get("message", str(e)), err.get("param"))

    def get(self, path, **params):
        return self.call("GET", path, params)

    def post(self, path, params=None, idem=None):
        return self.call("POST", path, params or {}, idem)

    def all(self, path, **params):
        items, params = [], dict(params, limit=100)
        while True:
            page = self.get(path, **params)
            items += page["data"]
            if not page.get("has_more"):
                return items
            params["starting_after"] = page["data"][-1]["id"]


class StripeError(Exception):
    def __init__(self, status, code, message, param=None):
        super().__init__(f"{status} {code}: {message}" + (f" (parameter: {param})" if param else ""))
        self.status, self.code, self.message, self.param = status, code, message, param


def ts(date_iso, hm="10:00"):
    return int(dt.datetime.fromisoformat(f"{date_iso} {hm}").replace(tzinfo=BERLIN).timestamp())


def day(epoch):
    return dt.datetime.fromtimestamp(epoch, BERLIN).strftime("%Y-%m-%d")


def plan():
    print("Plan (sandbox only):")
    for cid in STRIPE_CUSTOMERS:
        c = S.CUSTOMER[cid]
        print(f"  customer {cid} {c['name']} ({c['country']}, {c['type']}{', reverse charge' if c['country'] != 'DE' else ''})")
    for inv in S.STRIPE_INVOICES:
        extra = f", credit note EUR {inv['credit_note']} refunded" if inv.get("credit_note") else ""
        print(f"  invoice {inv['number']} EUR {inv['gross']} for {S.CUSTOMER[inv['customer']]['name']}: {inv['outcome']}{extra}")
    p = S.PAYMENT_LINK_PAYMENT
    print(f"  card payment EUR {p['amount']} for {p['invoice']} (the payment link), {S.CUSTOMER[p['customer']]['name']}")
    print(f"  manual payout of the available balance: EUR {S.STRIPE_GROSS_CHARGED} charged - EUR {S.STRIPE_REFUNDED} refund - Stripe fees")


def find_by_tag(objects, ref):
    for o in objects:
        if (o.get("metadata") or {}).get("pack_ref") == ref:
            return o
    return None


def seed(st):
    manifest = {"tag": TAG, "fictional": True, "seeded_at": dt.datetime.now(BERLIN).isoformat(timespec="seconds"),
                "customers": {}, "invoices": {}}
    acct = st.get("/account")
    name = ((acct.get("settings") or {}).get("dashboard") or {}).get("display_name") or (acct.get("business_profile") or {}).get("name") or ""
    print(f"Sandbox account: {acct['id']} ({name or 'no display name'}), default currency {acct.get('default_currency')}")
    if acct.get("default_currency") not in (None, "eur"):
        sys.exit("This sandbox settles in " + str(acct.get("default_currency")) + ", not EUR. Create the sandbox in a European account.")
    if "juniper" not in name.lower():
        print("  Note: set the sandbox's public business name to 'Juniper Workshop Lab (fictional)' so invoices do not show your company.")

    rates = st.all("/tax_rates", active="true")
    rate = find_by_tag(rates, "MWST-19") or st.post("/tax_rates", dict(
        display_name="MwSt.", percentage="19", inclusive=False, country="DE", jurisdiction="DE", description="German VAT 19% (workshop)",
        metadata=dict(pack_ref="MWST-19", fictional="true")), idem="taxrate")
    print(f"  tax rate {rate['id']} (19%)")

    existing = st.all("/customers")
    customers = {}
    for cid in STRIPE_CUSTOMERS:
        c = S.CUSTOMER[cid]
        cus = find_by_tag(existing, cid)
        if not cus:
            city = c["address"][1].split(" ", 1)
            params = dict(name=c["name"], email=c["email"], preferred_locales=["en"],
                          address=dict(line1=c["address"][0], postal_code=city[0], city=city[1], country=c["country"]),
                          metadata=dict(pack_ref=cid, fictional="true"), description=c["note"])
            if c["country"] != "DE":
                params["tax_exempt"] = "reverse"
            if c["vat_id"]:
                params["tax_id_data"] = [dict(type="eu_vat", value=c["vat_id"])]
            cus = st.post("/customers", params, idem=f"customer-{cid}")
            print(f"  created customer {cid} {cus['id']}")
        else:
            print(f"  customer {cid} exists: {cus['id']}")
        customers[cid] = cus["id"]
    manifest["customers"] = customers

    pm_cache = {}

    def card(cid, token):
        if (cid, token) not in pm_cache:
            pm = st.post(f"/payment_methods/{token}/attach", dict(customer=customers[cid]), idem=f"attach-{cid}-{token}")
            pm_cache[(cid, token)] = pm["id"]
        return pm_cache[(cid, token)]

    invoices = st.all("/invoices")
    for inv in S.STRIPE_INVOICES:
        found = find_by_tag(invoices, inv["number"])
        if found and found["status"] != "draft":
            print(f"  invoice {inv['number']} exists: {found['id']} ({found['status']})")
            manifest["invoices"][inv["number"]] = summarize_invoice(found)
            continue
        send = inv["outcome"] == "open"
        params = dict(customer=customers[inv["customer"]], currency="eur", number=inv["number"], auto_advance=False,
                      collection_method="send_invoice" if send else "charge_automatically", footer=FOOTER,
                      metadata=dict(pack_ref=inv["number"], fictional="true"), effective_at=ts(inv["effective"]),
                      custom_fields=[dict(name="Service", value="October 2026")])
        if send:
            params["days_until_due"] = inv.get("days_until_due", 14)
        if inv["vat"] == "19":
            params["default_tax_rates"] = [rate["id"]]
        if found:
            draft = found
        else:
            try:
                draft = st.post("/invoices", params, idem=f"invoice-{inv['number']}")
            except StripeError as e:
                if e.param != "effective_at" and "effective_at" not in e.message:
                    raise
                params.pop("effective_at")  # the API did not accept a past issue date: use today's
                print(f"  note: issue date not backdated for {inv['number']} ({e.message})")
                draft = st.post("/invoices", params, idem=f"invoice-{inv['number']}-now")
            for i, line in enumerate(inv["lines"]):
                st.post("/invoiceitems", dict(customer=customers[inv["customer"]], invoice=draft["id"], currency="eur",
                                              description=line["desc"], quantity=int(line["qty"]),
                                              unit_amount_decimal=str(cents(line["unit"])),
                                              metadata=dict(pack_ref=f"{inv['number']}-{i + 1}")), idem=f"item-{inv['number']}-{i}")
        final = st.post(f"/invoices/{draft['id']}/finalize", dict(auto_advance=False), idem=f"finalize-{inv['number']}")
        if final["total"] != cents(inv["gross"]):
            sys.exit(f"Stop: {inv['number']} totals {euros(final['total'])} in Stripe, the story says {inv['gross']}.")
        if inv["outcome"] in ("paid", "failed"):
            try:
                final = st.post(f"/invoices/{final['id']}/pay", dict(payment_method=card(inv["customer"], inv["card"])),
                                idem=f"pay-{inv['number']}")
            except StripeError as e:
                if inv["outcome"] != "failed":
                    raise
                print(f"  {inv['number']}: card payment failed as planned ({e.code})")
                final = st.get(f"/invoices/{final['id']}")
        if inv.get("credit_note"):
            cn = st.post("/credit_notes", dict(invoice=final["id"], amount=cents(inv["credit_note"]), refund_amount=cents(inv["credit_note"]),
                                              reason="order_change", memo="One ClearDesk team cancelled for October.", email_type="none",
                                              metadata=dict(pack_ref=f"CN-{inv['number']}")), idem=f"creditnote-{inv['number']}")
            print(f"  credit note {cn['id']} EUR {inv['credit_note']} refunded on {inv['number']}")
            final = st.get(f"/invoices/{final['id']}")
        manifest["invoices"][inv["number"]] = summarize_invoice(final)
        print(f"  invoice {inv['number']} {final['id']}: {final['status']}, EUR {euros(final['total'])}")

    seed_shop(st, customers, card, rate, manifest)

    p = S.PAYMENT_LINK_PAYMENT
    intents = st.all("/payment_intents")
    pi = find_by_tag(intents, p["invoice"])
    if not pi:
        pi = st.post("/payment_intents", dict(amount=cents(p["amount"]), currency="eur", customer=customers[p["customer"]],
                                              payment_method=card(p["customer"], p["card"]), confirm=True, off_session=True,
                                              automatic_payment_methods=dict(enabled=True, allow_redirects="never"), description=p["description"],
                                              metadata=dict(pack_ref=p["invoice"], invoice_number=p["invoice"], channel="payment_link",
                                                            fictional="true")), idem=f"pi-{p['invoice']}")
    print(f"  card payment for {p['invoice']}: {pi['id']} ({pi['status']})")
    manifest["payment_link_payment"] = dict(invoice=p["invoice"], payment_intent=pi["id"], status=pi["status"], amount=p["amount"])

    pos = sorted([p for p in st.all("/payouts") if (p.get("metadata") or {}).get("pack_ref", "").startswith("PAYOUT-")], key=lambda p: p["created"])
    for _ in range(10):  # pay out what is available; a charge can take a moment to become available
        bal = st.get("/balance")
        available = next((b["amount"] for b in bal["available"] if b["currency"] == "eur"), 0)
        if available <= 0 or len(pos) >= 2:
            break
        ref = f"PAYOUT-{len(pos) + 1}"
        try:
            pos.append(st.post("/payouts", dict(amount=available, currency="eur", description="Juniper Workshop Lab payout (workshop)",
                                                statement_descriptor="JUNIPER STRIPE", metadata=dict(pack_ref=ref, fictional="true")), idem=ref.lower()))
        except StripeError as e:
            sys.exit(f"The payout failed: {e.message}\nSet Dashboard > Settings > Payouts > Payout schedule to Manual, check that the "
                     "sandbox has a test bank account in EUR, then run this script again.")
        time.sleep(5)
    if not pos:
        sys.exit("No available EUR balance to pay out.")
    for po in pos:
        print(f"  payout {po['id']}: EUR {euros(po['amount'])}, {po['status']}, arrives {day(po['arrival_date'])}")
    write_outputs(st, manifest, pos)


def seed_shop(st, customers, card, rate, manifest):
    """Catalogue, discounts, payment links, subscriptions with cancellations, seat sales with a refund and a dispute."""
    shop = manifest.setdefault("shop", {})
    products = {p["metadata"].get("pack_ref"): p for p in st.all("/products") if p.get("metadata")}
    prices = {}
    for pr in S.STRIPE_PRODUCTS:
        prod = products.get(pr["ref"]) or st.post("/products", dict(name=pr["name"], description=pr["desc"],
                                                                   metadata=dict(pack_ref=pr["ref"], fictional="true")), idem=f"product-{pr['ref']}")
        existing = [x for x in st.all("/prices", product=prod["id"]) if x.get("active")]
        price = existing[0] if existing else st.post("/prices", dict(
            product=prod["id"], currency="eur", unit_amount=cents(pr["price"]), tax_behavior=pr["tax_behavior"],
            recurring=dict(interval=pr["recurring"]) if pr["recurring"] else None, metadata=dict(pack_ref=pr["ref"])), idem=f"price-{pr['ref']}")
        prices[pr["ref"]] = price["id"]
    shop["prices"] = prices
    have = {c["id"] for c in st.all("/coupons")}
    for c in S.STRIPE_COUPONS:
        if c["id"] not in have:
            st.post("/coupons", dict(id=c["id"], name=c["name"], percent_off=c["percent_off"], duration=c["duration"],
                                     metadata=dict(fictional="true")), idem=f"coupon-{c['id']}")
        if c.get("promotion_code") and not st.all("/promotion_codes", code=c["promotion_code"]):
            st.post("/promotion_codes", dict(code=c["promotion_code"], promotion=dict(type="coupon", coupon=c["id"]),
                                             metadata=dict(fictional="true")), idem=f"promo-{c['id']}")
    links = {l["metadata"].get("pack_ref"): l for l in st.all("/payment_links") if l.get("metadata")}
    shop["payment_links"] = {}
    for l in S.STRIPE_PAYMENT_LINKS:
        link = links.get(l["ref"]) or st.post("/payment_links", dict(
            line_items=[dict(price=prices[l["product"]], quantity=1)], allow_promotion_codes=l["promotion_codes"],
            metadata=dict(pack_ref=l["ref"], fictional="true")), idem=f"link-{l['ref']}")
        shop["payment_links"][l["ref"]] = dict(id=link["id"], url=link.get("url"))
    subs = {x["metadata"].get("pack_ref"): x for x in st.all("/subscriptions", status="all") if x.get("metadata")}
    shop["subscriptions"] = {}
    for sub in S.STRIPE_SUBSCRIPTIONS:
        x = subs.get(sub["ref"])
        if not x:
            params = dict(customer=customers[sub["customer"]], items=[dict(price=prices["P-CLEARDESK"])],
                          default_payment_method=card(sub["customer"], "pm_card_bypassPending"), default_tax_rates=[rate["id"]],
                          metadata=dict(pack_ref=sub["ref"], fictional="true"), off_session=True)
            if sub["coupon"]:
                params["discounts"] = [dict(coupon=sub["coupon"])]
            x = st.post("/subscriptions", params, idem=f"sub-{sub['ref']}")
            if sub["then"] == "cancel_and_refund":
                inv = st.get(f"/invoices/{x['latest_invoice']}")
                st.post("/credit_notes", dict(invoice=inv["id"], amount=inv["total"], refund_amount=inv["total"], reason="order_change",
                                              memo="Cancelled within 14 days: full refund.", email_type="none"), idem=f"cn-{sub['ref']}")
                x = st.call("DELETE", f"/subscriptions/{x['id']}", dict(prorate=False))
            elif sub["then"] == "cancel_at_period_end":
                x = st.post(f"/subscriptions/{x['id']}", dict(cancel_at_period_end=True), idem=f"cape-{sub['ref']}")
        shop["subscriptions"][sub["ref"]] = dict(id=x["id"], status=x["status"], cancel_at_period_end=x.get("cancel_at_period_end"))
        print(f"  subscription {sub['ref']}: {x['status']}{' (cancels at period end)' if x.get('cancel_at_period_end') else ''}")
    intents = {i["metadata"].get("pack_ref"): i for i in st.all("/payment_intents") if i.get("metadata")}
    shop["seats"] = {}
    for seat in S.STRIPE_SEAT_SALES:
        pi = intents.get(seat["ref"])
        if not pi:
            c = S.CUSTOMER[seat["customer"]]
            pi = st.post("/payment_intents", dict(
                amount=cents(seat["amount"]), currency="eur", customer=customers[seat["customer"]],
                payment_method=card(seat["customer"], seat["card"]), confirm=True, off_session=True,
                automatic_payment_methods=dict(enabled=True, allow_redirects="never"),
                description=f"Learning day seat, {c['name']} (payment link)" + (f", code {seat['code']}" if seat["code"] else ""),
                metadata=dict(pack_ref=seat["ref"], channel="payment_link", payment_link=shop["payment_links"]["LINK-SEAT"]["id"],
                              promotion_code=seat["code"] or "", fictional="true")), idem=f"seat-{seat['ref']}")
            if seat["then"] == "refund":
                st.post("/refunds", dict(payment_intent=pi["id"], reason="requested_by_customer",
                                         metadata=dict(pack_ref=f"RF-{seat['ref']}")), idem=f"refund-{seat['ref']}")
        shop["seats"][seat["ref"]] = dict(payment_intent=pi["id"], status=pi["status"], amount=seat["amount"], then=seat["then"])
        print(f"  seat {seat['ref']}: EUR {seat['amount']} {pi['status']}{', ' + seat['then'] if seat['then'] else ''}")
    if any(s_["then"] == "dispute" for s_ in S.STRIPE_SEAT_SALES):
        for _ in range(20):  # the test card opens the dispute a moment after the payment
            if st.all("/disputes"):
                break
            time.sleep(2)


def summarize_invoice(inv):
    return dict(id=inv["id"], status=inv["status"], total=euros(inv["total"]), amount_paid=euros(inv.get("amount_paid", 0)),
                amount_remaining=euros(inv.get("amount_remaining", 0)), hosted_invoice_url=inv.get("hosted_invoice_url"),
                due_date=day(inv["due_date"]) if inv.get("due_date") else None, attempt_count=inv.get("attempt_count", 0))


def write_outputs(st, manifest, pos):
    txns = [t for t in st.all("/balance_transactions") if t["currency"] == "eur"]
    ours = [t for t in txns if t["type"] != "payout"]
    fees = sum(t["fee"] for t in ours if t["type"] in ("charge", "payment"))
    gross = sum(t["amount"] for t in ours if t["type"] in ("charge", "payment"))
    refunds = -sum(t["amount"] for t in ours if t["type"] in ("refund", "payment_refund"))
    disputes = -sum(t["net"] for t in ours if t["type"] == "adjustment")
    other = [t for t in ours if t["type"] not in ("charge", "payment", "refund", "payment_refund", "adjustment")]
    net = sum(t["net"] for t in ours)
    if other:
        print(f"  WARNING: unexpected balance transactions: {sorted({t['type'] for t in other})}")
    bal = st.get("/balance")
    pending = sum(b["amount"] for b in bal["pending"] if b["currency"] == "eur")
    available = sum(b["amount"] for b in bal["available"] if b["currency"] == "eur")
    paid_out = sum(p["amount"] for p in pos)
    if net != paid_out + pending + available:
        print(f"  WARNING: payouts {euros(paid_out)} + pending {euros(pending)} + available {euros(available)} differ from the net {euros(net)}.")
    manifest.update(pending=euros(pending), available=euros(available))
    manifest.update(gross=euros(gross), refunds=euros(refunds), disputes=euros(disputes))
    manifest["fees"] = euros(fees)
    manifest["payouts"] = [dict(id=po["id"], amount=euros(po["amount"]), status=po["status"], created_date=day(po["created"]),
                                arrival_date=day(po["arrival_date"])) for po in pos]
    manifest["payout"] = manifest["payouts"][0]
    out = PACK / "stripe"
    out.mkdir(exist_ok=True)
    (out / "seed-manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    snap = out / "snapshot"
    snap.mkdir(exist_ok=True)
    rows = [[day(t["created"]), t["id"], t["type"], euros(t["amount"]), euros(t["fee"]), euros(t["net"]), t.get("description") or "",
             t.get("source") or "", day(t["available_on"])] for t in sorted(txns, key=lambda t: t["created"])]
    write_csv(snap / "balance_transactions.csv",
              ["date", "id", "type", "amount_eur", "fee_eur", "net_eur", "description", "source", "available_on"], rows)
    invs = [i for i in st.all("/invoices") if (i.get("metadata") or {}).get("pack_ref")]
    write_csv(snap / "invoices.csv", ["number", "id", "customer_name", "status", "total_eur", "amount_paid_eur", "amount_remaining_eur",
                                      "due_date", "attempt_count", "hosted_invoice_url"],
              [[i.get("number"), i["id"], i.get("customer_name"), i["status"], euros(i["total"]), euros(i.get("amount_paid", 0)),
                euros(i.get("amount_remaining", 0)), day(i["due_date"]) if i.get("due_date") else "", i.get("attempt_count", 0),
                i.get("hosted_invoice_url") or ""] for i in sorted(invs, key=lambda i: i.get("number") or "")])
    charges = st.all("/charges")
    link_pi = (manifest.get("payment_link_payment") or {}).get("payment_intent")
    for c in charges:  # a charge does not copy the payment's metadata: add the invoice number for the payment link
        if c.get("payment_intent") == link_pi:
            c.setdefault("metadata", {})["invoice_number"] = S.PAYMENT_LINK_PAYMENT["invoice"]
    write_csv(snap / "charges.csv", ["date", "id", "status", "amount_eur", "amount_refunded_eur", "description", "customer",
                                     "payment_intent", "failure_code", "invoice_number"],
              [[day(c["created"]), c["id"], c["status"], euros(c["amount"]), euros(c.get("amount_refunded", 0)), c.get("description") or "",
                c.get("customer") or "", c.get("payment_intent") or "", c.get("failure_code") or "",
                (c.get("metadata") or {}).get("invoice_number", "")] for c in sorted(charges, key=lambda c: c["created"])])
    write_csv(snap / "payouts.csv", ["created", "id", "amount_eur", "status", "arrival_date", "statement_descriptor"],
              [[day(p["created"]), p["id"], euros(p["amount"]), p["status"], day(p["arrival_date"]), p.get("statement_descriptor") or ""]
               for p in st.all("/payouts")])
    write_csv(snap / "balance.csv", ["available_eur", "pending_eur"], [[manifest["available"], manifest["pending"]]])
    print(f"Wrote {out / 'seed-manifest.json'} and stripe/snapshot/. Fees EUR {manifest['fees']}, payouts EUR "
          f"{' + '.join(p['amount'] for p in manifest['payouts'])}, pending EUR {manifest['pending']}.")
    print("Next: run generate.py again, so the October bank statement shows the payout.")


def write_csv(path, header, rows):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def check(st):
    acct = st.get("/account")
    print(f"Sandbox {acct['id']}, currency {acct.get('default_currency')}")
    for i in st.all("/invoices"):
        if (i.get("metadata") or {}).get("pack_ref"):
            print(f"  {i.get('number')}: {i['status']}, EUR {euros(i['total'])}, paid {euros(i.get('amount_paid', 0))}")
    bal = st.get("/balance")
    print("  balance:", {b["currency"]: euros(b["amount"]) for b in bal["available"]}, "available")
    for p in st.all("/payouts"):
        print(f"  payout {p['id']}: EUR {euros(p['amount'])}, {p['status']}, arrives {day(p['arrival_date'])}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="create the objects (otherwise a dry run)")
    ap.add_argument("--check", action="store_true", help="read-only summary of what is in the sandbox")
    a = ap.parse_args()
    if not a.apply and not a.check:
        plan()
        print("\nDry run: nothing was sent to Stripe. Add --apply to create these objects in the sandbox.")
        return
    st = Stripe(read_key())
    try:
        check(st) if a.check else seed(st)
    except StripeError as e:
        sys.exit(f"Stripe said: {e}")


if __name__ == "__main__":
    main()
