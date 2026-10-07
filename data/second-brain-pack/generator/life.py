"""Everyday life around the story, different in every Workspace account.

The story's events (notes.CALENDAR) are the same in every account because the questions in
answer-key/ depend on them. life_events(seed) adds what else fills a real calendar: team routines,
focus time, home-office days, private appointments, a pet at the vet, holidays. The seed is any
text, for example the account's address: the same seed always gives the same life, two seeds give
two different ones. No question depends on these entries, none names a contact from the story,
and none is planned on top of a story event or trip.

Each entry is a dict. kind is "event", "focus" (focus time), "ooo" (out of office) or a working
location ("home", "office", "place"). Times are Europe/Berlin; "rrule" and "exdates" describe
repeats. seed_workspace.py turns the entries into Google Calendar events.
"""

import calendar
import datetime as dt
import hashlib
import random

from notes import CALENDAR

FIRST = dt.date(2026, 9, 1)   # routines start here ...
LAST = dt.date(2026, 12, 18)  # ... and end before the Christmas break
DAYS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]
WORK = DAYS[:5]
# Story days without routines (trips and the learning day), with the working location to show.
AWAY = {"2026-09-18": "Salzburg", "2026-10-22": None, "2026-10-26": "London", "2026-10-27": "London", "2026-10-28": "London"}
OFFICE = "Juniper office, Lindwurmstraße"

FRIENDS = ["Hanna", "Felix", "Sophie", "Jakob", "Lisa", "Tobias", "Katrin", "Markus", "Anna", "Daniel", "Julia", "Nina",
           "Moritz", "Carla", "Paula", "Simon", "Ines", "Yusuf", "Selin", "Marek", "Fabian", "Leonie", "Charlotte", "Florian",
           "Theresa", "Valentin", "Johanna", "Kai", "Aylin", "Dominik"]
PARTNERS = ["Robin", "Kim", "Sascha", "Toni", "Mika", "Luca", "Jo", "Andrea", "Noah", "Mattia", "Elena", "Jana", "Tom", "Sarah"]
KIDS = ["Ida", "Emil", "Mila", "Anton", "Frida", "Leo", "Greta", "Paul", "Lina", "Finn", "Ella", "Henri", "Matilda", "Karl", "Rosa"]
CATS = ["Mochi", "Krümel", "Luna", "Pixel", "Socke", "Minka", "Tiger", "Pünktchen", "Merlin", "Lilly", "Simba", "Nala", "Kiwi",
        "Mimi", "Zorro", "Muffin", "Pepper", "Tofu", "Kasimir", "Momo"]
DOGS = ["Bruno", "Balu", "Frieda", "Lotte", "Rocky", "Emma", "Charlie", "Hugo", "Wilma", "Bello"]
HOMETOWNS = ["Augsburg", "Regensburg", "Rosenheim", "Landshut", "Ingolstadt", "Nürnberg", "Würzburg", "Passau"]
MONTHS_DE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
WEEKDAYS_DE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

# (title, German title, outward, German, return, German, minutes on the way)
TRIPS = [
    ("Vacation: Sardinia", "Urlaub Sardinien", "Flight to Cagliari", "Flug nach Cagliari", "Flight back from Cagliari", "Rückflug aus Cagliari", 105),
    ("Vacation: Madeira", "Urlaub Madeira", "Flight to Funchal", "Flug nach Funchal", "Flight back from Funchal", "Rückflug aus Funchal", 245),
    ("Vacation: Crete", "Urlaub Kreta", "Flight to Heraklion", "Flug nach Heraklion", "Flight back from Heraklion", "Rückflug aus Heraklion", 160),
    ("Vacation: Tenerife", "Urlaub Teneriffa", "Flight to Tenerife South", "Flug nach Teneriffa Süd", "Flight back from Tenerife South",
     "Rückflug aus Teneriffa Süd", 300),
    ("Hiking in South Tyrol", "Wandern in Südtirol", "Drive to South Tyrol", "Fahrt nach Südtirol", "Drive back from South Tyrol",
     "Rückfahrt aus Südtirol", 240),
    ("Lake Constance", "Bodensee", "Train to Lindau", "Zug nach Lindau", "Train back from Lindau", "Zug zurück aus Lindau", 150),
    ("Amsterdam trip", "Amsterdam-Reise", "Train to Amsterdam", "Zug nach Amsterdam", "Train back from Amsterdam", "Zug zurück aus Amsterdam", 480),
    ("Vacation: Sicily", "Urlaub Sizilien", "Flight to Palermo", "Flug nach Palermo", "Flight back from Palermo", "Rückflug aus Palermo", 120),
]
WINTER_TRIPS = [
    ("Skiing in the Zillertal", "Skiurlaub Zillertal", "Drive to the Zillertal", "Fahrt ins Zillertal", "Drive back from the Zillertal",
     "Rückfahrt aus dem Zillertal", 150),
    ("Vienna trip", "Wien-Reise", "Train to Vienna", "Zug nach Wien", "Train back from Vienna", "Zug zurück aus Wien", 240),
    ("Copenhagen trip", "Kopenhagen-Reise", "Flight to Copenhagen", "Flug nach Kopenhagen", "Flight back from Copenhagen", "Rückflug aus Kopenhagen", 95),
]
WEEKEND_CITIES = [("Prague", "Prag"), ("Venice", "Venedig"), ("Berlin", "Berlin"), ("Ljubljana", "Ljubljana"), ("Strasbourg", "Straßburg"),
                  ("Hamburg", "Hamburg"), ("Bologna", "Bologna"), ("Basel", "Basel"), ("Leipzig", "Leipzig"), ("Trieste", "Triest"),
                  ("Budapest", "Budapest")]


def mins(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m


def day(s):
    return dt.date.fromisoformat(s)


class Diary:
    """Booked time per day, so new entries avoid the story's events and each other."""

    def __init__(self):
        self.booked, self.away = {}, set()

    def empty(self, *days):
        return all(d not in self.away and not self.booked.get(d) for d in days)

    def free(self, d, start, end):
        return d not in self.away and all(end <= s or start >= e for s, e in self.booked.get(d, []))

    def book(self, d, start, end):
        self.booked.setdefault(d, []).append((start, end))

    def block(self, first, last):
        for k in range((last - first).days + 1):
            self.away.add(first + dt.timedelta(days=k))


def story_diary():
    diary = Diary()
    for ev in CALENDAR:
        if ev.get("status") == "CANCELLED" or ev.get("allday"):
            continue
        s, e = dt.datetime.fromisoformat(ev["start"]), dt.datetime.fromisoformat(ev["end"])
        weeks = int(ev["rrule"].split("COUNT=")[1]) if ev.get("rrule") else 1  # the story only repeats weekly
        for k in range(weeks):
            diary.book(s.date() + dt.timedelta(weeks=k), s.hour * 60 + s.minute - 30, e.hour * 60 + e.minute + 30)
    diary.away |= {day(d) for d in AWAY}
    return diary


def weekly(days, first, last, interval=1):
    monday, out = first - dt.timedelta(days=first.weekday()), []
    while monday <= last:
        out += [monday + dt.timedelta(days=DAYS.index(d)) for d in days]
        monday += dt.timedelta(weeks=interval)
    return sorted(d for d in out if first <= d <= last)


def monthly(nth, weekday, first, last):
    """The nth weekday of every month; nth -1 is the last one."""
    out, y, m = [], first.year, first.month
    while dt.date(y, m, 1) <= last:
        hits = [dt.date(y, m, k) for k in range(1, calendar.monthrange(y, m)[1] + 1) if dt.date(y, m, k).weekday() == DAYS.index(weekday)]
        out.append(hits[nth - 1] if nth > 0 else hits[nth])
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return [d for d in out if first <= d <= last]


def timed(title, d, start, minutes, **kw):
    s = dt.datetime.combine(d, dt.time()) + dt.timedelta(minutes=mins(start))
    return {"kind": "event", "title": title, "start": f"{s:%Y-%m-%d %H:%M}",
            "end": f"{s + dt.timedelta(minutes=minutes):%Y-%m-%d %H:%M}", **kw}


def allday(title, first, last=None, **kw):
    return {"kind": "event", "title": title, "start": str(first), "end": str((last or first) + dt.timedelta(days=1)),
            "allday": True, "busy": False, **kw}


def series(rng, diary, title, options, minutes, first=FIRST, last=LAST, interval=1, tolerance=0.25, **kw):
    """A repeating entry at the first option (pattern, time) that seldom clashes; clashing dates are left out.
    "MO,TH" repeats weekly (every `interval` weeks); "2TH" is the second Thursday of each month."""
    for pattern, start in rng.sample(options, len(options)):
        if pattern[0].isdigit() or pattern[0] == "-":
            dates, rule = monthly(int(pattern[:-2]), pattern[-2:], first, last), f"FREQ=MONTHLY;BYDAY={pattern}"
        else:
            dates = weekly(pattern.split(","), first, last, interval)
            rule = f"FREQ=WEEKLY;{f'INTERVAL={interval};' if interval > 1 else ''}BYDAY={pattern}"
        s = mins(start)
        clash = [d for d in dates if not diary.free(d, s, s + minutes)]
        keep = [d for d in dates if d not in clash]
        if not keep or len(clash) > tolerance * len(dates):
            continue
        for d in keep:
            diary.book(d, s, s + minutes)
        until = f"{last + dt.timedelta(days=1):%Y%m%d}T000000Z"
        return timed(title, keep[0], start, minutes, rrule=f"{rule};UNTIL={until}",
                     exdates=[f"{d} {start}" for d in clash if d > keep[0]], **kw)
    return None


def weekly_allday(title, days, diary, **kw):
    dates = weekly(days, FIRST, LAST)
    keep = [d for d in dates if d not in diary.away]
    return {**allday(title, keep[0], **kw), "rrule": f"FREQ=WEEKLY;BYDAY={','.join(days)};UNTIL={LAST:%Y%m%d}",
            "exdates": [str(d) for d in dates if d in diary.away and d > keep[0]]}


def once(rng, diary, title, minutes, window, days=WORK, times=("17:30",), **kw):
    """One appointment on a free slot: a random date in window whose weekday is in days, at one of times."""
    first, last = day(window[0]), day(window[1])
    for _ in range(80):
        d = first + dt.timedelta(days=rng.randint(0, (last - first).days))
        start = rng.choice(times)
        s = mins(start)
        if DAYS[d.weekday()] in days and diary.free(d, s, s + minutes):
            diary.book(d, s, s + minutes)
            return timed(title, d, start, minutes, **kw)
    return None


def free_day(rng, diary, window, days=WORK):
    first, last = day(window[0]), day(window[1])
    for _ in range(80):
        d = first + dt.timedelta(days=rng.randint(0, (last - first).days))
        if DAYS[d.weekday()] in days and d not in diary.away:
            return d
    return None


def out_of_office(diary, title, first, last, message):
    diary.block(first, last)
    return {**timed(title, first, "00:00", ((last - first).days + 1) * 1440), "kind": "ooo", "message": message}


def life_events(seed):
    """The calendar entries for one account, and a one-line description of that life."""
    rng = random.Random(int.from_bytes(hashlib.sha256(seed.strip().lower().encode()).digest()[:8], "big"))
    de = rng.random() < 0.4  # writes private entries in German

    def t(en, german):
        return german if de else en

    def date_de(d):
        return f"{d.day}. {MONTHS_DE[d.month - 1]}"

    diary, out = story_diary(), []
    hue = {k: rng.choice(v.split()) for k, v in {"health": "4 11 3", "sport": "10 2", "family": "5 6", "home": "8 7",
                                                  "social": "9 6 3", "trip": "7 9"}.items()} if rng.random() < 0.65 else {}
    kids = rng.choices(["none", "kita", "school"], [55, 25, 20])[0]
    kid = rng.choice(KIDS)
    pet = rng.choices(["cat", "dog", "none"], [50, 20, 30])[0]
    pet_name = rng.choice(CATS if pet == "cat" else DOGS)
    partner = rng.choice(PARTNERS) if rng.random() < 0.5 else None
    friends = rng.sample(FRIENDS, 8)
    town = rng.choice(HOMETOWNS)
    uses_location = rng.random() < 0.8
    home_days = rng.choice([["FR"], ["MO", "FR"], ["WE"], ["TH", "FR"], ["MO"], ["WE", "FR"], ["MO", "TH"], []])
    about = []

    # Holidays first: everything else is planned around them.
    if kids == "school":
        first, last = day("2026-11-04"), day("2026-11-06")  # with the school's autumn break
        trip = (f"Autumn break with {kid}", f"Herbstferien mit {kid}", "Drive to the North Sea", "Fahrt an die Nordsee",
                "Drive back from the North Sea", "Rückfahrt von der Nordsee", 480)
    else:
        first, last = map(day, rng.choice([("2026-08-31", "2026-09-03"), ("2026-11-04", "2026-11-06"), ("2026-11-09", "2026-11-13"),
                                           ("2026-11-11", "2026-11-13"), ("2026-11-16", "2026-11-20"), ("2026-11-23", "2026-11-27"),
                                           ("2026-12-01", "2026-12-04"), ("2026-12-07", "2026-12-11"), ("2026-12-14", "2026-12-18")]))
        trip = rng.choice(WINTER_TRIPS if first.month == 12 else TRIPS)
    leave = first - dt.timedelta(days=2) if first.weekday() == 0 else first
    back = last + dt.timedelta(days=2) if last.weekday() == 4 else last
    workday_back = back + dt.timedelta(days=1)
    while workday_back.weekday() > 4:
        workday_back += dt.timedelta(days=1)
    out.append(out_of_office(diary, t(trip[0], trip[1]), leave, back,
                             t(f"I'm on holiday until {back.day} {back:%B}. Back on {workday_back:%A} {workday_back.day} {workday_back:%B}.",
                               f"Ich bin bis {date_de(back)} im Urlaub, ab {WEEKDAYS_DE[workday_back.weekday()]}, {date_de(workday_back)} wieder da.")))
    out.append(timed(t(trip[2], trip[3]), leave, rng.choice(["07:05", "08:40", "09:55", "11:20"]), trip[6], color=hue.get("trip")))
    out.append(timed(t(trip[4], trip[5]), back, rng.choice(["14:30", "16:10", "17:45"]), trip[6], color=hue.get("trip")))
    about.append(f"holiday {leave:%d %b}-{back:%d %b}")

    xmas_first = rng.choice([day("2026-12-21"), day("2026-12-23"), day("2026-12-24")])
    xmas_last = rng.choice([day("2027-01-01"), day("2027-01-06")])
    out.append(out_of_office(diary, t("Christmas break", "Weihnachtsurlaub"), xmas_first, xmas_last,
                             t(f"Away until {xmas_last.day} January. Happy holidays!", f"Bis {date_de(xmas_last)} nicht da. Frohe Feiertage!")))
    if rng.random() < 0.6:
        out.append(allday(t(f"Christmas at my parents' in {town}", f"Weihnachten bei den Eltern in {town}"),
                          day("2026-12-24"), day("2026-12-26"), color=hue.get("family")))
    if rng.random() < 0.5:
        off = day(rng.choice(["2026-09-11", "2026-09-28"]))
        out.append(out_of_office(diary, t("Day off", "Freier Tag"), off, off, t("Day off, back tomorrow.", "Heute frei, morgen wieder da.")))
    if rng.random() < 0.35:
        fridays = [d for d in map(day, ["2026-10-23", "2026-11-06", "2026-11-13", "2026-11-20", "2026-11-27", "2026-12-04", "2026-12-11"])
                   if not {d, d + dt.timedelta(days=1), d + dt.timedelta(days=2)} & diary.away]
        if fridays:
            fri = rng.choice(fridays)
            city = rng.choice(WEEKEND_CITIES)
            out.append(out_of_office(diary, t(f"Long weekend: {city[0]}", f"Langes Wochenende: {city[1]}"), fri, fri + dt.timedelta(days=2),
                                     t("Long weekend, back on Monday.", "Langes Wochenende, ab Montag wieder da.")))
            about.append(f"long weekend {city[0]}")

    # Family, children, pets.
    if kids == "kita":
        pick = rng.choice(["MO,WE,FR", "TU,TH", "MO,TU,TH"])
        out.append(series(rng, diary, t("Kita pick-up", "Kita abholen"), [(pick, "16:00"), (pick, "16:15")], 30, color=hue.get("family")))
        closed = free_day(rng, diary, ("2026-10-12", "2026-11-27")) if rng.random() < 0.6 else None
        if closed:
            out.append(allday(t("Kita closed (team day)", "Kita geschlossen (Teamtag)"), closed, color=hue.get("family")))
        if rng.random() < 0.6:
            out.append(once(rng, diary, t("Kita parents' evening", "Elternabend Kita"), 90, ("2026-09-14", "2026-10-16"), times=("19:30",),
                            location="Kita Sonnenblume", color=hue.get("family")))
        if rng.random() < 0.6:
            out.append(once(rng, diary, t(f"Paediatrician: {kid}'s check-up", f"Kinderarzt: U-Untersuchung {kid}"), 45, ("2026-10-12", "2026-11-27"),
                            times=("08:30", "15:00"), location="Kinderarztpraxis Kleine Riesen", private=True, color=hue.get("health")))
        if rng.random() < 0.7 and diary.free(day("2026-11-11"), mins("17:00"), mins("18:30")):
            diary.book(day("2026-11-11"), mins("17:00"), mins("18:30"))
            out.append(timed(t("St. Martin's procession (Kita)", "Sankt-Martins-Umzug (Kita)"), day("2026-11-11"), "17:00", 90,
                             location="Kita Sonnenblume", color=hue.get("family")))
        about.append(f"child {kid} in Kita")
    elif kids == "school":
        out.append(series(rng, diary, t(f"{kid}: swimming lesson", f"{kid}: Schwimmkurs"), [("MO", "16:30"), ("WE", "16:30"), ("TH", "16:00")], 60,
                          first=day("2026-09-21"), location="Hallenbad", color=hue.get("family")))
        out.append(once(rng, diary, t(f"Parent-teacher meeting ({kid})", f"Elterngespräch Klassenlehrerin ({kid})"), 20, ("2026-11-16", "2026-12-04"),
                        times=("16:40", "17:00", "17:20"), location="Grundschule an der Kastanienallee", color=hue.get("family")))
        out.append(allday(t("No school: autumn break", "Herbstferien"), day("2026-11-02"), day("2026-11-06"), color=hue.get("family")))
        out.append(allday(t("No school (Buß- und Bettag)", "Schulfrei (Buß- und Bettag)"), day("2026-11-18"), color=hue.get("family")))
        about.append(f"school child {kid}")

    vet = "Tierarztpraxis Pfotenweg, Pfotenweg 4, München"
    if pet == "cat":
        when = rng.choice([(WORK, ("17:00", "17:30", "18:00")), (["SA"], ("09:30", "10:15"))])
        out.append(once(rng, diary, t(f"Cat vet: {pet_name}'s vaccination", f"Tierarzt: {pet_name} impfen"), 30, ("2026-10-07", "2026-10-23"),
                        days=when[0], times=when[1], location=vet, color=hue.get("family"),
                        note=t("Bring the vaccination record and the carrier.", "Impfpass und Transportbox mitnehmen.")))
        if rng.random() < 0.5:
            out.append(once(rng, diary, t(f"Cat vet: {pet_name}'s teeth", f"Tierarzt: Zahnkontrolle {pet_name}"), 30, ("2026-09-07", "2026-09-30"),
                            times=("17:30", "18:00"), location=vet, color=hue.get("family")))
        sitter = t("Cat sitter: hand over keys and feeding plan", "Katzensitterin: Schlüssel und Futterplan übergeben")
        about.append(f"cat {pet_name}")
    elif pet == "dog":
        out.append(series(rng, diary, t(f"Dog school with {pet_name}", f"Hundeschule mit {pet_name}"), [("SA", "10:00"), ("SA", "09:00"), ("SU", "10:30")], 60,
                          last=day("2026-11-28"), location="Hundeplatz am Isarufer", color=hue.get("family")))
        out.append(once(rng, diary, t(f"Vet: {pet_name}'s vaccination", f"Tierarzt: {pet_name} impfen"), 30, ("2026-10-07", "2026-10-30"),
                        times=("17:00", "17:30", "18:00"), location=vet, color=hue.get("family")))
        sitter = t(f"Drop {pet_name} at the dog sitter's", f"{pet_name} zur Hundesitterin bringen")
        about.append(f"dog {pet_name}")
    if pet != "none":
        eve = leave - dt.timedelta(days=1)
        if diary.free(eve, mins("19:00"), mins("19:30")):
            diary.book(eve, mins("19:00"), mins("19:30"))
            out.append(timed(sitter, eve, "19:00", 30, color=hue.get("family")))

    if partner:
        for window in [("2026-09-04", "2026-10-03"), ("2026-10-29", "2026-12-12")]:
            out.append(once(rng, diary, t(f"Date night with {partner}", f"Date Night mit {partner}"), 150, window, days=["FR", "SA"],
                            times=("19:30", "20:00"), color=hue.get("social")))
        out.append(allday(t(f"{partner}'s birthday", f"{partner} hat Geburtstag"), free_day(rng, Diary(), ("2026-09-01", "2026-12-20"), DAYS),
                          rrule="FREQ=YEARLY", color=hue.get("family")))
        if rng.random() < 0.5:
            out.append(once(rng, diary, t(f"Lunch with {partner}'s parents", f"Mittagessen bei {partner}s Eltern"), 180, ("2026-09-06", "2026-12-13"),
                            days=["SU"], times=("12:30",), color=hue.get("family")))
        about.append(f"partner {partner}")
    if rng.random() < 0.8:
        out.append(allday(t("Mum's birthday", "Geburtstag Mama"), free_day(rng, Diary(), ("2026-09-01", "2026-12-20"), DAYS),
                          rrule="FREQ=YEARLY", color=hue.get("family")))
    if rng.random() < 0.3:
        out.append(series(rng, diary, t("Call Mum", "Mama anrufen"), [("SU", "18:00"), ("SU", "17:30")], 30, color=hue.get("family")))
    weekends = [d for d in weekly(["SA"], day("2026-09-05"), day("2026-12-12")) if diary.empty(d, d + dt.timedelta(days=1))]
    if weekends and rng.random() < 0.4:
        sat = rng.choice(weekends)
        if diary.empty(sat, sat + dt.timedelta(days=1)):
            diary.block(sat, sat + dt.timedelta(days=1))
            out.append(allday(t(f"Visiting my parents in {town}", f"Bei den Eltern in {town}"), sat, sat + dt.timedelta(days=1), color=hue.get("family")))

    # Work routines. The story's weekly check-in is on Tuesdays at 09:30.
    early = rng.random() < 0.5
    if rng.random() < 0.6:
        pattern = rng.choice(["MO,WE,TH,FR", "MO,TH", "MO,WE,FR"])
        out.append(series(rng, diary, rng.choice(["Team stand-up", "Stand-up", "Morning sync"]),
                          [(pattern, s) for s in (["08:45", "09:00"] if early else ["09:15", "10:00"])], 15))
    if rng.random() < 0.85:
        out.append(series(rng, diary, rng.choice(["1:1 Sam", "Sam / Alex 1:1", "1:1 with Sam"]),
                          [("MO", "11:00"), ("WE", "14:00"), ("TH", "15:30"), ("FR", "11:00")], 45, interval=2,
                          location=rng.choice(["Sam's office", "Walk and talk", ""])))
    team_lunch = rng.random() < 0.45
    if team_lunch:
        out.append(series(rng, diary, "Team lunch", [("TH", "12:30"), ("WE", "12:30")], 60))
    if rng.random() < 0.35:
        out.append(series(rng, diary, t("Lunch", "Mittagspause"), [("MO,TU,WE,FR" if team_lunch else "MO,TU,WE,TH,FR", "12:00"),
                                                                    ("MO,TU,WE,FR" if team_lunch else "MO,TU,WE,TH,FR", "12:30")], 45))
    if rng.random() < 0.5:
        name, pattern, start, minutes = rng.choice([("Inbox zero and expenses", "FR", "14:00", 60), ("Plan the week", "MO", "08:30", 30),
                                                    ("Week review", "FR", "15:30", 30)])
        out.append(series(rng, diary, name, [(pattern, start)], minutes))
    focus = [("MO", "09:30", 120), ("WE", "09:30", 150), ("TH", "13:30", 120), ("FR", "09:00", 120), ("WE", "14:00", 120),
             ("MO", "14:00", 90), ("TH", "08:30", 90)]
    if rng.random() < 0.9:
        title = t(rng.choice(["Focus time", "Deep work", "Writing time", "No meetings, please"]), "Fokuszeit")
        wanted = rng.choice([1, 2, 2])
        for pattern, start, minutes in rng.sample(focus, len(focus)):
            block = series(rng, diary, title, [(pattern, start)], minutes)
            if block:
                out.append({**block, "kind": "focus", "message": t("In focus time. I'll get back to you later.", "Fokuszeit, ich melde mich später.")})
                about.append(f"focus {pattern} {start}")
                wanted -= 1
            if not wanted:
                break
    for _ in range(rng.choice([0, 1, 1, 2])):
        name, minutes, start, days = rng.choice([("Webinar: accessible events", 60, "14:00", WORK), ("Online course: Notion databases (module 2)", 90, "18:00", WORK),
                                                 ("Facilitation meetup", 120, "18:30", ["TU", "WE", "TH"]), ("Lunch and learn: AI tools", 45, "12:30", WORK)])
        out.append(once(rng, diary, name, minutes, ("2026-09-14", "2026-12-11"), days=days, times=(start,)))
    if rng.random() < 0.7:
        out.append(once(rng, diary, t("Team Christmas dinner", "Weihnachtsfeier Team"), 210, ("2026-12-09", "2026-12-17"), days=["WE", "TH", "FR"],
                        times=("18:30", "19:00"), location="Wirtshaus am Anger", color=hue.get("social")))

    # Sport and hobbies.
    sports = [
        ("gym", t("Gym", "Fitnessstudio"), [("MO,TH", "07:00"), ("MO,TH", "18:30"), ("TU,FR", "07:00")], 60, "FitPass Studio Westend"),
        ("running", t("Running club", "Lauftreff"), [("WE", "18:30"), ("TU", "18:30")], 75, "Meeting point: Wittelsbacherbrücke"),
        ("yoga", "Yoga", [("TU", "19:00"), ("TH", "19:30"), ("WE", "07:30")], 75, "Yoga Loft Schwabing"),
        ("swimming", t("Swimming", "Schwimmen"), [("FR", "07:00"), ("WE", "07:00")], 60, "Westbad"),
        ("bouldering", "Bouldering", [("WE", "19:00"), ("TH", "19:00")], 120, "Boulderhalle Nord"),
        ("football", t("Football", "Fußball"), [("MO", "20:00")], 90, "Soccerhalle Ost"),
        ("pilates", "Pilates", [("WE", "12:15"), ("FR", "12:15")], 45, "Studio Kern"),
        ("tennis", "Tennis", [("SU", "10:00"), ("SA", "11:00")], 90, "Tennisclub Ost"),
    ]
    for key, name, options, minutes, place in rng.sample(sports, rng.choice([1, 2, 2])):
        # The story's gym membership ends on 31 October, so the gym stops there and a trial session follows.
        until = day("2026-10-30") if key == "gym" else LAST
        out.append(series(rng, diary, name, options, minutes, last=until, location=place, color=hue.get("sport")))
        if key == "gym":
            out.append(once(rng, diary, t("Bouldering: trial session", "Bouldern: Probetraining"), 120, ("2026-11-02", "2026-11-13"),
                            days=["TU", "WE", "TH"], times=("19:00",), location="Boulderhalle Nord", color=hue.get("sport")))
        about.append(key)
    hobbies = [
        (t("Choir rehearsal", "Chorprobe"), [("MO", "19:30"), ("TH", "19:30")], 120, "Gemeindesaal", FIRST, LAST, 1),
        (t("Italian A2 (evening class)", "Italienisch A2 (VHS)"), [("WE", "18:30"), ("TU", "18:30")], 90, "Volkshochschule, room 2.14",
         day("2026-09-21"), day("2026-12-16"), 1),
        (t("Pottery course", "Töpferkurs"), [("TH", "18:00"), ("MO", "18:00")], 150, "Töpferwerkstatt Tonart", day("2026-10-01"), day("2026-11-26"), 1),
        (t("Book club", "Buchclub"), [("2TH", "19:30"), ("1WE", "19:30")], 120, "", FIRST, LAST, 1),
        (t("Board game night", "Spieleabend"), [("-1FR", "19:00")], 180, "", FIRST, LAST, 1),
        (t("Guitar lesson", "Gitarrenunterricht"), [("WE", "17:30"), ("MO", "17:30")], 45, "Musikschule am Bach", FIRST, LAST, 1),
        (t("Volunteering: food bank", "Ehrenamt: Tafel"), [("SA", "09:30")], 180, "", FIRST, LAST, 2),
    ]
    if rng.random() < 0.65:
        name, options, minutes, place, start, until, interval = rng.choice(hobbies)
        out.append(series(rng, diary, name, options, minutes, first=start, last=until, interval=interval, location=place, color=hue.get("social")))
        about.append(name.lower())

    # Doctors, home, errands.
    private_health = rng.random() < 0.6
    dentist = "Zahnarztpraxis Rosengarten, Rosengasse 2, München"
    gp = "Hausarztpraxis am Kirchplatz, München"
    health = [
        (t("Dentist: check-up", "Zahnarzt: Kontrolle"), 30, ("08:00", "08:30", "17:00", "17:30"), dentist, ""),
        (t("Teeth cleaning", "Professionelle Zahnreinigung"), 60, ("08:00", "16:30", "17:00"), dentist, ""),
        (t("Flu shot", "Grippeimpfung"), 15, ("08:15", "12:30", "17:45"), gp, t("Bring the vaccination record.", "Impfpass mitnehmen.")),
        (t("Eye doctor", "Augenarzt"), 45, ("08:30", "15:30", "16:00"), "Augenpraxis Weitblick, München",
         t("Pupils get dilated: don't cycle home.", "Pupillen werden erweitert: nicht mit dem Rad fahren.")),
        (t("Skin check", "Hautarzt: Hautscreening"), 30, ("09:00", "16:15"), "Hautarztpraxis am Markt, München", ""),
        (t("Blood test (fasting!)", "Blutabnahme (nüchtern!)"), 15, ("07:45", "08:00"), gp,
         t("Nothing to eat after 22:00 the evening before.", "Ab 22 Uhr am Vorabend nichts mehr essen.")),
        (t("Massage", "Massage"), 60, ("18:00", "18:30"), "Praxis Ruhepol", ""),
    ]
    for name, minutes, times, place, note in rng.sample(health, rng.choice([2, 3, 3, 4])):
        out.append(once(rng, diary, name, minutes, ("2026-09-07", "2026-12-11"), times=times, location=place, note=note,
                        private=private_health, color=hue.get("health")))
    if rng.random() < 0.3:
        monday = rng.choice(weekly(["MO"], day("2026-10-05"), day("2026-10-26")))
        out.append(series(rng, diary, t("Physio (back)", "Physiotherapie (Rücken)"), [("MO", "18:00"), ("WE", "18:00"), ("TH", "07:30")], 30,
                          first=monday, last=monday + dt.timedelta(weeks=6), tolerance=0.4, location="Physio am Bach",
                          note=t("Prescription for 6 sessions.", "Rezept über 6 Einheiten."), private=private_health, color=hue.get("health")))
    if rng.random() < 0.75:
        when = rng.choice([(["SA"], ("09:30", "10:00", "11:00")), (["TU", "WE", "TH"], ("18:00", "18:30"))])
        for window in [("2026-09-07", "2026-09-26"), ("2026-10-19", "2026-11-07"), ("2026-12-01", "2026-12-19")]:
            out.append(once(rng, diary, t("Haircut", "Friseur"), 60, window, days=when[0], times=when[1], location="Salon Schnittpunkt",
                            color=hue.get("health")))

    home = [
        (t("Chimney sweep (between 8 and 12)", "Schornsteinfeger (zwischen 8 und 12 Uhr)"), 240, ("08:00",),
         t("Notice in the stairwell. Someone has to be at home.", "Aushang im Treppenhaus. Jemand muss zu Hause sein."), True),
        (t("Heating maintenance", "Heizungswartung"), 120, ("07:30", "13:00"), "", True),
        (t("Plumber: dripping kitchen tap", "Installateur: Wasserhahn Küche tropft"), 60, ("08:00", "15:00", "16:00"), "", True),
        (t("Fibre technician (window 8-12)", "Techniker Glasfaser (8-12 Uhr)"), 240, ("08:00",),
         t("They call 30 minutes before.", "Ruft 30 Minuten vorher an."), True),
        (t("Sofa delivery (window 8-14)", "Lieferung Sofa (8-14 Uhr)"), 360, ("08:00",), "", True),
        (t("Window cleaner", "Fensterputzer"), 120, ("09:00",), "", True),
        (t("Smoke detector check (landlord)", "Rauchmelderprüfung (Hausverwaltung)"), 120, ("10:00",), "", True),
        (t("Tenants' meeting", "Mieterversammlung"), 90, ("19:00",), "", False),
        (t("Bulky waste: put the old shelf out", "Sperrmüll: altes Regal rausstellen"), 15, ("06:45",), "", False),
    ]
    for name, minutes, times, note, at_home in rng.sample(home, rng.choice([2, 2, 3])):
        days = home_days if at_home and home_days and uses_location else WORK
        out.append(once(rng, diary, name, minutes, ("2026-09-14", "2026-12-11"), days=days, times=times, note=note, color=hue.get("home")))
    if rng.random() < 0.3:
        out.append(series(rng, diary, t("Cleaner", "Putzhilfe"), [("FR", "09:00"), ("TH", "13:00")], 180, interval=2, busy=False, color=hue.get("home")))

    if rng.random() < 0.6:  # the passport expires in March 2027 (see notes/0-Inbox/passport.md)
        out.append(once(rng, diary, t("Bürgeramt: apply for a new passport", "Bürgerbüro: neuen Reisepass beantragen"), 30, ("2026-10-19", "2026-11-27"),
                        times=("08:10", "10:40", "11:20", "14:15"), location="Bürgerbüro, Ruppertstraße 19, München",
                        note=t("Bring the old passport and a biometric photo.", "Alten Pass und biometrisches Foto mitnehmen.")))
    if rng.random() < 0.3:
        out.append(once(rng, diary, t("Tax advisor: 2025 tax return", "Steuerberaterin: Steuererklärung 2025"), 60, ("2026-10-05", "2026-11-20"),
                        times=("16:00", "17:00"), location="Kanzlei Zahlwerk, München",
                        note=t("Bring the receipts folder.", "Belege-Ordner mitnehmen.")))
    if rng.random() < 0.35:
        out.append(once(rng, diary, t("Winter tyres (garage)", "Reifenwechsel (Werkstatt)"), 60, ("2026-10-10", "2026-11-14"), days=WORK + ["SA"],
                        times=("07:30", "08:00", "09:00"), location="Autowerkstatt Kolben, München", color=hue.get("home")))
        if rng.random() < 0.5:
            out.append(once(rng, diary, t("Car inspection (TÜV)", "TÜV-Termin"), 60, ("2026-09-07", "2026-12-11"), times=("07:30", "16:00"),
                            location="Prüfstelle Nord", color=hue.get("home")))
        about.append("car")
    if rng.random() < 0.3:
        out.append(once(rng, diary, t("Bike service: drop off", "Fahrrad zur Inspektion bringen"), 15, ("2026-09-07", "2026-10-16"),
                        times=("08:00", "18:00"), location="Radladen Speiche"))
    if rng.random() < 0.35:
        out.append(once(rng, diary, t("Pick up parcel (post office)", "Paket abholen (Post)"), 15, ("2026-10-05", "2026-10-23"),
                        times=("12:30", "18:15"), location="Postfiliale"))

    # Private time and friends.
    if rng.random() < 0.75:
        for _ in range(rng.choice([1, 2])):
            out.append(once(rng, diary, rng.choice([t("Private", "Privat"), t("Personal appointment", "Privater Termin"), t("Blocked", "Geblockt")]),
                            rng.choice([60, 90]), ("2026-09-07", "2026-12-11"), times=("15:00", "16:00", "16:30"), private=True))
    if rng.random() < 0.3:
        out.append(series(rng, diary, t("Private", "Privat"), [("WE", "17:30"), ("TH", "17:00")], 60, interval=2, private=True))
    f = friends
    social = [
        lambda: once(rng, diary, t(f"Birthday dinner: {f[0]}", f"Geburtstagsessen {f[0]}"), 150, ("2026-09-07", "2026-12-12"), days=["FR", "SA"],
                     times=("19:00", "19:30"), color=hue.get("social")),
        lambda: once(rng, diary, t(f"{f[1]}'s birthday party", f"Geburtstagsparty {f[1]}"), 240, ("2026-09-07", "2026-12-12"), days=["SA"],
                     times=("19:00", "20:00"), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Brunch with {f[2]}", f"Brunch mit {f[2]}"), 150, ("2026-09-06", "2026-12-13"), days=["SU"],
                     times=("10:30", "11:00"), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Cinema with {f[3]}", f"Kino mit {f[3]}"), 150, ("2026-09-07", "2026-12-17"), days=["TU", "WE", "TH"],
                     times=("20:00", "20:15"), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Game night at {f[4]}'s", f"Spieleabend bei {f[4]}"), 210, ("2026-09-07", "2026-12-12"), days=["FR"],
                     times=("19:00",), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Concert with {f[5]}", f"Konzert mit {f[5]}"), 180, ("2026-09-07", "2026-12-12"), days=["FR", "SA"],
                     times=("20:00",), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Oktoberfest with {f[6]} and {f[7]}", f"Wiesn mit {f[6]} und {f[7]}"), 360, ("2026-09-19", "2026-10-04"),
                     days=["SA", "SU"], times=("11:00", "12:00", "13:00"), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Christmas market with {f[3]}", f"Christkindlmarkt mit {f[3]}"), 150, ("2026-11-25", "2026-12-18"),
                     days=WORK, times=("18:00", "18:30"), color=hue.get("social")),
        lambda: once(rng, diary, t(f"Dinner at {f[4]}'s", f"Abendessen bei {f[4]}"), 180, ("2026-09-07", "2026-12-12"), days=["SA"],
                     times=("19:00",), color=hue.get("social")),
    ]
    for make in rng.sample(social, rng.choice([3, 4, 5])):
        out.append(make())
    if rng.random() < 0.3:
        sat = rng.choice([day("2026-09-05"), day("2026-09-19")])
        if diary.empty(sat):
            diary.block(sat, sat)
            out.append(allday(t(f"Wedding: {f[1]} & {f[2]}", f"Hochzeit {f[1]} & {f[2]}"), sat, busy=True, color=hue.get("social")))
    for name in f[:rng.choice([1, 2])]:
        out.append(allday(t(f"{name}'s birthday", f"Geburtstag {name}"), free_day(rng, Diary(), ("2026-09-01", "2026-12-20"), DAYS),
                          rrule="FREQ=YEARLY", color=hue.get("social")))

    # Working location last: home and office days skip holidays and trips.
    if uses_location:
        office_days = [d for d in WORK if d not in home_days]
        # Google repeats an all-day working location on one weekday only, so each day gets its own series.
        for d in home_days:
            out.append({**weekly_allday(t("Home", "Zuhause"), [d], diary), "kind": "home"})
        for d in office_days:
            out.append({**weekly_allday("Office", [d], diary), "kind": "office", "label": OFFICE})
        for d, label in AWAY.items():
            if label and day(d) not in diary.away - {day(x) for x in AWAY}:
                out.append({**allday(label, day(d)), "kind": "place", "label": label})
        about.append("home on " + "+".join(home_days) if home_days else "always in the office")
    if de:
        about.append("writes in German")
    return [e for e in out if e and e.get("title")], ", ".join(about)
