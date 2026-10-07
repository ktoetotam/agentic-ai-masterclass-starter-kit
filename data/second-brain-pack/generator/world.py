"""The fictional world of the second brain pack: one owner, colleagues, contacts and companies.

Everything here is invented for the AI Realist Agentic AI Masterclass. Company names, people,
addresses, numbers and codes are fictional. Email domains end in .invalid (Juniper) or
.example (everyone else), which are reserved and can never receive mail. Bank details are
deliberately invalid strings.
"""

SCENARIO_DATE = "2026-10-07"  # "today" inside the story; questions about "next week" use it
TZ_SUMMER = "+0200"  # Europe/Berlin until 2026-10-25
FOOTER_EN = "Fictional workshop document - not a real invoice, booking or message."
FOOTER_DE = "Fiktives Workshop-Dokument - keine echte Rechnung, Buchung oder Nachricht."

OWNER = {
    "name": "Alex Example",
    "email": "alex@juniper-workshop.invalid",
    "role": "Coordinator, Juniper Workshop Lab",
    "home": "Beispielweg 7, 80331 München",
}

# Companies. "logo" picks a simple drawn mark; colours are RGB 0-255.
BRANDS = {
    "juniper": dict(name="Juniper Workshop Lab", domain="juniper-workshop.invalid", color=(31, 77, 58), logo="leaf",
                    address="Lindwurmstraße 0, 80337 München", lang="en"),
    "lindenhall": dict(name="Linden Hall Events GmbH", domain="lindenhall-events.example", color=(46, 94, 62), logo="arch",
                       address="Lindenplatz 3, 80331 München", lang="en", reg="HRB 000001 (fictional)"),
    "copperkettle": dict(name="Copper Kettle Catering", domain="copperkettle-catering.example", color=(176, 92, 42), logo="circle",
                         address="Kupfergasse 12, 81369 München", lang="en", reg="VAT DE000000001 (fictional)"),
    "printworks": dict(name="PrintWorks Demo GmbH", domain="printworks.example", color=(40, 60, 140), logo="square",
                       address="Druckweg 5, 80995 München", lang="en", reg="VAT DE000000002 (fictional)"),
    "weissblatt": dict(name="Druckerei Weißblatt GmbH", domain="weissblatt-druck.example", color=(90, 90, 90), logo="square",
                       address="Papiermühlstraße 8, 85748 Garching", lang="de", reg="USt-IdNr. DE000000003 (fiktiv)"),
    "signwise": dict(name="Signwise Interpreting", domain="signwise.example", color=(120, 60, 140), logo="wave",
                     address="Handzeichenweg 2, 80469 München", lang="en"),
    "bureaubits": dict(name="Bureau Bits GmbH", domain="bureaubits.example", color=(20, 120, 140), logo="diamond",
                       address="Monitorstraße 27, 80339 München", lang="en", reg="VAT DE000000004 (fictional)"),
    "circuitco": dict(name="Circuit & Co.", domain="circuitco.example", color=(200, 60, 50), logo="circle",
                      address="Platinenring 9, 80807 München", lang="en", reg="VAT DE000000005 (fictional)"),
    "kabelkiste": dict(name="Kabelkiste Online", domain="kabelkiste.example", color=(240, 160, 30), logo="square",
                       address="Steckerweg 1, 90402 Nürnberg", lang="de", reg="USt-IdNr. DE000000006 (fiktiv)"),
    "brightwell": dict(name="Brightwell Energie GmbH", domain="brightwell-energie.example", color=(230, 170, 20), logo="sun",
                       address="Sonnenallee 100, 80335 München", lang="de", reg="USt-IdNr. DE000000007 (fiktiv)"),
    "northwind": dict(name="Northwind Mobile", domain="northwind-mobile.example", color=(0, 110, 200), logo="wave",
                      address="Funkturmstraße 4, 80636 München", lang="en"),
    "fernleaf": dict(name="Fernleaf Fibre", domain="fernleaf-fibre.example", color=(60, 150, 70), logo="leaf",
                     address="Glasfaserweg 11, 81677 München", lang="en"),
    "harbourstone": dict(name="Harbourstone Versicherung AG", domain="harbourstone.example", color=(30, 50, 90), logo="arch",
                         address="Hafensteinplatz 1, 20457 Hamburg", lang="de"),
    "staypilot": dict(name="StayPilot", domain="staypilot.example", color=(0, 90, 160), logo="diamond",
                      address="StayPilot B.V. (fictional), Keizersgracht 0, Amsterdam", lang="en"),
    "aurelian": dict(name="Aurelian Air", domain="aurelian-air.example", color=(120, 20, 40), logo="wing",
                     address="Aurelian Air (fictional), Flughafen München", lang="en"),
    "suedbahn": dict(name="Südbahn Regio", domain="suedbahn-regio.example", color=(200, 30, 40), logo="square",
                     address="Bahnhofplatz 0, 80335 München", lang="de"),
    "pebble": dict(name="Pebble Rent", domain="pebblerent.example", color=(100, 100, 100), logo="circle",
                   address="Pebble Rent (fictional), Aeroporto di Verona", lang="en"),
    "ticketnest": dict(name="TicketNest", domain="ticketnest.example", color=(230, 80, 120), logo="diamond",
                       address="TicketNest (fictional), Berlin", lang="en"),
    "notecloud": dict(name="NoteCloud Pro", domain="notecloud.example", color=(80, 80, 200), logo="circle", lang="en",
                      address="NoteCloud Inc. (fictional)"),
    "streambox": dict(name="StreamBox", domain="streambox.example", color=(200, 20, 20), logo="square", lang="en",
                      address="StreamBox Media (fictional)"),
    "designkit": dict(name="DesignKit", domain="designkit.example", color=(250, 100, 60), logo="diamond", lang="en",
                      address="DesignKit Ltd (fictional)"),
    "newsroom": dict(name="Newsroom Daily", domain="newsroom-daily.example", color=(20, 20, 20), logo="square", lang="en",
                     address="Newsroom Daily (fictional)"),
    "fitpass": dict(name="FitPass", domain="fitpass.example", color=(0, 160, 120), logo="circle", lang="de",
                    address="FitPass Studios GmbH (fiktiv), Westendstraße 0, 80339 München"),
    "cloudvault": dict(name="CloudVault Backup", domain="cloudvault.example", color=(60, 130, 200), logo="wave", lang="en",
                       address="CloudVault (fictional)"),
    "alpenbank": dict(name="Alpenbank Demo", domain="alpenbank-demo.example", color=(10, 70, 60), logo="arch", lang="de",
                      address="Alpenbank Demo AG (fiktiv), Bankplatz 0, 80333 München"),
    "trattoria": dict(name="Trattoria Fittizia", domain="trattoria-fittizia.example", color=(150, 40, 30), logo="circle", lang="it",
                      address="Via del Lago 0, Malcesine (VR)"),
    "limmatblick": dict(name="Bistro Limmatblick", domain="limmatblick.example", color=(40, 90, 120), logo="circle", lang="de",
                        address="Uferweg 0, 8001 Zürich"),
    "cafelindgren": dict(name="Café Lindgren", domain="cafe-lindgren.example", color=(110, 70, 40), logo="circle", lang="de",
                         address="Lindgrenstraße 4, 80469 München"),
    "parkpoint": dict(name="ParkPoint", domain="parkpoint.example", color=(0, 80, 180), logo="square", lang="de",
                      address="Parkhaus Lindenplatz, 80331 München"),
    "meetnote": dict(name="MeetNote AI", domain="meetnote.example", color=(90, 50, 200), logo="wave", lang="en",
                     address="MeetNote (fictional)"),
    "smallteams": dict(name="Small Teams Weekly", domain="smallteams-weekly.example", color=(31, 77, 58), logo="leaf", lang="en",
                       address="Small Teams Weekly (fictional newsletter)"),
    "hausverwaltung": dict(name="Hausverwaltung Muster", domain="hv-muster.example", color=(70, 70, 70), logo="arch", lang="de",
                           address="Verwalterstraße 3, 80333 München"),
    "cedar": dict(name="Cedar Demo Analytics", domain="cedar-demo.example", color=(110, 80, 50), logo="leaf", lang="en",
                  address="Zedernweg 1, 5020 Salzburg"),
    "moss": dict(name="Moss Training Collective", domain="moss-training.example", color=(70, 120, 60), logo="leaf", lang="en",
                 address="Moosgasse 2, 1010 Wien"),
    "harbourlane": dict(name="Harbour Lane Consulting", domain="harbourlane.example", color=(20, 40, 80), logo="arch", lang="en",
                        address="1 Harbour Lane (fictional), London"),
}


def addr(local, brand):
    return f"{local}@{BRANDS[brand]['domain']}"


# People. "aliases" are other ways the same person is written in the sources.
PEOPLE = [
    dict(id="P01", name="Alex Example", aliases=["A. Example", "Alex"], role="Coordinator", org="Juniper Workshop Lab",
         email=OWNER["email"], how_met="(owner of this second brain)", first_met=""),
    dict(id="P02", name="Sam Example", aliases=["S. Example", "Sam"], role="Managing director", org="Juniper Workshop Lab",
         email="sam@juniper-workshop.invalid", how_met="Colleague", first_met="2024-03-01"),
    dict(id="P03", name="Jordan Example", aliases=["J. Example", "Jordan"], role="Facilitator", org="Juniper Workshop Lab",
         email="jordan@juniper-workshop.invalid", how_met="Colleague", first_met="2025-01-15"),
    dict(id="P04", name="Mira Beispiel", aliases=["M. Beispiel", "Mira"], role="Finance and office", org="Juniper Workshop Lab",
         email="mira@juniper-workshop.invalid", how_met="Colleague", first_met="2024-03-01"),
    dict(id="P05", name="Theo Muster", aliases=["T. Muster", "Theo"], role="IT and equipment", org="Juniper Workshop Lab",
         email="theo@juniper-workshop.invalid", how_met="Colleague", first_met="2025-06-01"),
    dict(id="P06", name="Noor Sample", aliases=["N. Sample", "Noor"], role="Events manager", org="Linden Hall Events",
         email=addr("noor.sample", "lindenhall"), how_met="Venue search for Project Lantern", first_met="2026-08-20"),
    dict(id="P07", name="Lukas Beispiel", aliases=["L. Beispiel", "Lukas"], role="Owner", org="Copper Kettle Catering",
         email=addr("lukas", "copperkettle"), how_met="Recommended by Noor Sample", first_met="2026-09-16"),
    dict(id="P08", name="Priya Demo", aliases=["P. Demo", "Priya"], role="Head of Programmes", org="Moss Training Collective",
         email=addr("priya", "moss"), how_met="Customer at Cedar Demo Analytics; moved to Moss Training Collective on 2026-09-01",
         first_met="2025-11-04"),
    dict(id="P09", name="Ben Sample", aliases=["Ben"], role="Friend", org="",
         email="ben.sample@mailbox.example", how_met="University friend", first_met="2015-10-01"),
    dict(id="P10", name="Lea Muster", aliases=["L. Muster"], role="Interpreter coordinator", org="Signwise Interpreting",
         email=addr("lea", "signwise"), how_met="Accessibility request for the learning day", first_met="2026-09-22"),
    dict(id="P11", name="Ravi Example", aliases=["R. Example", "Ravi"], role="Head of Operations", org="Harbour Lane Consulting",
         email=addr("ravi", "harbourlane"), how_met="Webinar Q&A in June", first_met="2026-06-11"),
    dict(id="P12", name="Clara Sample", aliases=["C. Sample"], role="Account manager", org="PrintWorks Demo GmbH",
         email=addr("clara.sample", "printworks"), how_met="Badge printing order", first_met="2026-09-24"),
    dict(id="P13", name="Jonas Demo", aliases=["J. Demo"], role="Customer service", org="Druckerei Weißblatt GmbH",
         email=addr("jonas.demo", "weissblatt"), how_met="Handout printing order", first_met="2026-09-19"),
    dict(id="P14", name="Elif Example", aliases=["E. Example"], role="Analyst", org="Cedar Demo Analytics",
         email=addr("elif", "cedar"), how_met="Learning day registration", first_met="2026-09-23"),
    dict(id="P15", name="Max Muster", aliases=["M. Muster"], role="Property manager", org="Hausverwaltung Muster",
         email=addr("max.muster", "hausverwaltung"), how_met="Landlord's property manager", first_met="2023-04-01"),
]

PERSON = {p["id"]: p for p in PEOPLE}
