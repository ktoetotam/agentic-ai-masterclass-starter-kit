"""Notes (sorted by PARA plus an Inbox and daily notes), meeting transcripts, calendar events,
Telegram messages and the record databases (people, interactions, deadlines, purchases,
places, ideas). The four original notes from data/knowledge/ are copied unchanged into
Project Lantern by generate.py, so their line numbers stay valid."""

# (folder, file name, created, updated, body). Front matter is added by generate.py.
NOTES = [
    # ---------------------------------------------------------------- Inbox (unsorted captures)
    ("0-Inbox", "call-noor.md", "2026-10-02", "2026-10-02",
     "# Call Noor\n\nFinal attendee number to Noor by 15 Oct.\nAlso ask about Wi-Fi for guests?\n"),
    ("0-Inbox", "video-tutorial-idea.md", "2026-09-28", "2026-09-28",
     "# Idea: video tutorial\n\nA 3-minute screen video that shows the intake form step by step. Maybe after Lantern.\n"),
    ("0-Inbox", "hdmi-adapter.md", "2026-10-02", "2026-10-02",
     "# HDMI adapter\n\nBought an HDMI adapter at Kabelkiste, 19,90 €, for the projector test with the loan laptops. Receipt is in my bag.\n"),
    ("0-Inbox", "cafe-lindgren-upstairs.md", "2026-09-30", "2026-09-30",
     "# Café Lindgren upstairs\n\nThere is a room upstairs for about 10 people. Ask whether we could rent it for small workshops.\n"),
    ("0-Inbox", "priya-team-size.md", "2026-10-01", "2026-10-01",
     "# Priya's new team\n\nPriya said her team at Moss runs 6 trainings a year, 15 to 20 people each.\n"),
    ("0-Inbox", "passport.md", "2026-09-27", "2026-09-27",
     "# Passport\n\nMy passport expires in March 2027. Renew it before any trip after Christmas.\n"),
    ("0-Inbox", "read-later-handover.md", "2026-09-15", "2026-09-15",
     "# Read later\n\nhttps://smallteams-weekly.example/handover-notes\n"),
    ("0-Inbox", "ravi-mornings.md", "2026-09-08", "2026-09-08",
     "# Ravi\n\nRavi prefers meetings before 11, London time.\n"),
    ("0-Inbox", "wifi-linden-hall.md", "2026-09-25", "2026-09-25",
     "# Wi-Fi\n\nWi-Fi at Linden Hall? Forgot to ask Noor during the walk-through.\n"),
    ("0-Inbox", "notion-formulas.md", "2026-07-22", "2026-07-22",
     "# Someday\n\nLearn basic Notion formulas (rollups!).\n"),

    # ---------------------------------------------------------------- Projects / Project Lantern (01-04 are copied in)
    ("1-Projects/Project Lantern", "05-decisions-log.md", "2026-08-15", "2026-10-06",
     "# Project Lantern: decisions log\n\n"
     "| Date | Decision | Who |\n| --- | --- | --- |\n"
     "| 2026-08-15 | Plan a customer learning day on 22 Oct, budget EUR 2,000 | Team |\n"
     "| 2026-09-05 | Budget raised to EUR 2,500 | Sam Example |\n"
     "| 2026-09-10 | Birch Room no longer available (water damage) | Linden Hall |\n"
     "| 2026-09-14 | Go for the Maple Room; quote EUR 1,150 | Alex Example |\n"
     "| 2026-10-06 | Handover guide draft moved from 9 Oct to 16 Oct | Weekly check-in |\n\n"
     "The Maple Room is not confirmed until Linden Hall has received the deposit.\n"),
    ("1-Projects/Project Lantern", "06-tasks.md", "2026-09-12", "2026-10-06",
     "# Project Lantern: tasks\n\n"
     "- [x] Ask Sam about the budget (approved 5 Sep)\n"
     "- [x] Venue walk-through (25 Sep)\n"
     "- [x] Order badges and handouts\n"
     "- [ ] Deposit for the Maple Room (Mira)\n"
     "- [ ] Vegetarian count to Lukas\n"
     "- [ ] Final attendee number to Noor\n"
     "- [ ] Handover guide draft (Alex)\n"
     "- [ ] Prepare 4 loan laptops (Theo)\n"
     "- [ ] Demo files (Jordan)\n"),
    ("1-Projects/Project Lantern", "07-venue-options.md", "2026-09-14", "2026-09-24",
     "# Venue options\n\n"
     "## Birch Room\nEUR 900 per day. Closed for repairs until mid-November after water damage. Not an option any more.\n\n"
     "## Maple Room\nEUR 1,150 including AV and cleaning. Up to 30 people. First floor.\n"
     "Step-free: yes, via the glass lift at the side entrance on Lindenplatz (Noor, 24 Sep).\n"
     "Held for us until 9 October. Terms are in the draft agreement.\n"),
    ("1-Projects/Project Lantern", "08-accessibility.md", "2026-09-23", "2026-09-29",
     "# Accessibility\n\n"
     "- One attendee uses a wheelchair. The Maple Room is step-free via the side entrance lift.\n"
     "- One attendee asked for sign language interpreting. Signwise sent an offer (two interpreters, full day). It needs confirming by 12 Oct.\n"
     "- Handouts in large print on request.\n"),
    ("1-Projects/Project Lantern", "09-handover-guide-outline.md", "2026-09-20", "2026-09-20",
     "# Handover guide: outline\n\n1. What the intake workflow is for\n2. Where requests arrive\n3. The review queue: what is missing, who supplies it\n"
     "4. Who decides the owner\n5. What happens when someone is away\n6. Where the files are\n\nTarget: a new colleague can use it without live help.\n"),

    # ---------------------------------------------------------------- Projects / London client visit
    ("1-Projects/London client visit", "trip-plan.md", "2026-09-08", "2026-09-08",
     "# London trip plan\n\n"
     "- Mon 26 Oct: flight AUR 214, Munich 07:10 to London Heathrow 08:15 (booking AUR7Q2)\n"
     "- Hotel: The Quill Hotel, 26-28 Oct, booking SP-LD4XK9, pay at the hotel\n"
     "- Tue 27 Oct 10:00: meeting with Ravi Example at Harbour Lane Consulting\n"
     "- Wed 28 Oct: flight AUR 219, London Heathrow 19:40 to Munich 22:35\n"),
    ("1-Projects/London client visit", "meeting-prep-ravi.md", "2026-09-20", "2026-10-01",
     "# Meeting prep: Ravi\n\nWhat Ravi wants: how we run intake reviews with small teams.\nBring: the review queue example, the handover guide outline.\nAsk: how many teams, which tools, who decides.\n"),

    # ---------------------------------------------------------------- Areas
    ("2-Areas/Office admin", "expense-claims-how-to.md", "2026-03-10", "2026-08-25",
     "# How to claim expenses\n\n1. Take a photo of the receipt.\n2. Write the purpose and the amount.\n"
     "3. Foreign currency: use the euro amount from the bank's card notification, not a rate from the internet.\n4. Send it to Mira by the 5th of the next month.\n"),
    ("2-Areas/Office admin", "laptop-loan-process.md", "2026-09-04", "2026-09-29",
     "# Loan laptops\n\nLabel them L1 to L4. Each loan goes on the sign-out sheet with name, date and return date. Wipe after every event.\n"),
    ("2-Areas/Office admin", "equipment-list.md", "2026-08-18", "2026-09-04",
     "# Office equipment\n\n| Item | Bought | Warranty |\n| --- | --- | --- |\n"
     "| 27-inch monitor (Bureau Bits) | 18 Aug 2026 | 3 years |\n| 3 loan laptops (Circuit & Co.) | 3 Sep 2026 | 2 years |\n"),
    ("2-Areas/Team", "1-1-jordan-2026-08-05.md", "2026-08-05", "2026-08-05",
     "# 1:1 with Jordan, 5 Aug, Café Lindgren\n\nJordan wants to run more demos. Agreed: Jordan prepares the demo files for the learning day.\n"),
    ("2-Areas/Team", "team-retro-2026-09-30.md", "2026-09-30", "2026-09-30",
     "# Team retro, 30 Sep, Café Lindgren\n\nWe sat upstairs this time.\n\nWent well: venue switch handled fast; budget approved quickly.\n"
     "Could be better: invoices land in too many inboxes; nobody owned the vegetarian count.\nNext retro: end of October.\n"),
    ("2-Areas/Team", "voice-memo-2026-09-18.md", "2026-09-18", "2026-09-18",
     "# Voice memo, 18 Sep (transcribed)\n\nSo, coming back from Salzburg. The Cedar team liked the intake form but they want the review step explained better. "
     "Note to self: the handover guide needs a page on the review queue. Also Priya isn't there any more, Elif is the new contact for the learning day.\n"),
    ("2-Areas/Team", "voice-memo-2026-10-02.md", "2026-10-02", "2026-10-02",
     "# Voice memo, 2 Oct (transcribed)\n\nIdea while walking: a short accessibility checklist for every venue we look at. Lift, toilets, quiet room, interpreters. "
     "And maybe a second brain for the whole team, so we stop asking each other where things are.\n"),
    ("2-Areas/Home and finance", "subscriptions-overview.md", "2026-05-02", "2026-08-01",
     "# Subscriptions\n\n| Service | Price | Billing |\n| --- | --- | --- |\n"
     "| NoteCloud Pro | 8.00 | monthly |\n| StreamBox Standard | 13.99 | monthly |\n| DesignKit | 119.00 | yearly, October |\n"
     "| FitPass Flex | 29.00 | monthly |\n| CloudVault 200 GB | 2.99 | monthly |\n\nAbout 54 EUR a month without DesignKit.\n"),
    ("2-Areas/Home and finance", "bills-checklist.md", "2026-01-10", "2026-07-01",
     "# Bills\n\n- Electricity (Brightwell): monthly, pay by transfer by the 15th\n- Internet (Fernleaf): monthly, direct debit\n"
     "- Mobile (Northwind): monthly, direct debit on the 20th\n- Household insurance (Harbourstone): yearly in January\n"),
    ("2-Areas/Home and finance", "insurance-notes.md", "2026-01-12", "2026-01-12",
     "# Insurance\n\nHousehold insurance with Harbourstone, renews every 1 January. Check the price in autumn and compare.\n"),

    # ---------------------------------------------------------------- Resources
    ("3-Resources/Reading", "highlights-review-queues.md", "2026-08-06", "2026-08-06",
     "---\nsource: https://smallteams-weekly.example/review-queues\nsaved: 2026-08-06\n---\n# Highlights: Five signs your review queue is too long\n\n"
     "> A review queue is only useful if every item says what is missing and who can supply it.\n\n"
     "> Keep urgent items and ideas in separate lists.\n\n"
     "My note: our queue mixes both. Split it in the handover guide.\n"),
    ("3-Resources/Reading", "highlights-intake-forms.md", "2026-09-04", "2026-09-04",
     "# Highlights: Small Team Workflows 2026 (report)\n\n"
     "> Teams with a named decider report fewer forgotten requests, but also longer waiting times when that person is away.\n\n"
     "My note: the number about shared intake forms is in the chapter on shared intake. Look it up before the London meeting.\n"),
    ("3-Resources/Reading", "book-notes-small-team-playbook.md", "2026-07-30", "2026-07-30",
     "# Book notes: The Small Team Playbook (fictional book by Jo Example)\n\n"
     "- Write every request down in one place.\n- Decide who decides.\n- A handover note is one page, not a meeting.\n"),
    ("3-Resources/Reading", "clip-handover-notes.md", "2026-09-15", "2026-09-15",
     "---\nsource: https://smallteams-weekly.example/handover-notes\nsaved: 2026-09-15\n---\n# Why handover notes beat handover meetings\n\n"
     "A handover note lists open items, who is waiting, and where the files are. Meetings are forgotten; notes can be checked.\n"),
    ("3-Resources/Reading", "clip-handover-notes (1).md", "2026-09-16", "2026-09-16",
     "---\nsource: https://smallteams-weekly.example/handover-notes\nsaved: 2026-09-16\n---\n# Why handover notes beat handover meetings\n\n"
     "A handover note lists open items, who is waiting, and where the files are. Meetings are forgotten; notes can be checked.\n"),
    ("3-Resources/How-to", "booking-train-tickets.md", "2026-09-16", "2026-09-16",
     "# Booking train tickets\n\nSüdbahn saver fares are cheapest about two weeks ahead. Book outbound and return separately if the return time is unsure.\n"),

    # ---------------------------------------------------------------- Archive
    ("4-Archive", "birch-room-request-2026-08-20.md", "2026-08-20", "2026-09-10",
     "# Birch Room request (archived)\n\nAsked Linden Hall for the Birch Room on 22 Oct. Held until 10 Sep. Released on 10 Sep after water damage.\n"),
    ("4-Archive", "early-budget-ideas.md", "2026-07-10", "2026-07-10",
     "# Early budget ideas (July)\n\nMaybe EUR 1,500 is enough if we use our own office? Too small for 25 people.\n"),

    # ---------------------------------------------------------------- Daily notes
    ("Daily", "2026-09-14.md", "2026-09-14", "2026-09-14",
     "# Mon 14 Sep\n\n- Maple Room quote arrived, EUR 1,150.\n- Asked Noor about step-free access.\n- Lunch with Mira: she will do budget v2.\n"),
    ("Daily", "2026-10-01.md", "2026-10-01", "2026-10-01",
     "# Thu 1 Oct\n\n- Call with Priya about the webinar. Promised an outline by 12 Oct.\n- Aurelian changed my flight time, check later.\n"),
    ("Daily", "2026-10-06.md", "2026-10-06", "2026-10-06",
     "# Tue 6 Oct\n\n- Check-in: handover draft now due 16 Oct.\n- Mira pays the deposit on Thursday.\n- Theo is off sick until tomorrow.\n"),
]

TRANSCRIPTS = [
    dict(date="2026-09-12", start="10:00", title="Project Lantern planning call", speakers=["Alex Example", "Jordan Example", "Sam Example"],
         cues=[("Alex Example", "Quick update: the learning day stays on 22 October."),
               ("Sam Example", "Good. And the room?"),
               ("Alex Example", "The Birch Room is gone, water damage. Noor suggested the Maple Room. Nothing is booked yet."),
               ("Jordan Example", "I can prepare the demo files."),
               ("Alex Example", "Great. I'll confirm attendance. Open questions: accessibility, the venue and how many loan laptops we need."),
               ("Sam Example", "Let's not send invitations until the venue is clear.")]),
    dict(date="2026-09-25", start="10:00", title="Maple Room walk-through", speakers=["Alex Example", "Jordan Example", "Noor Sample"],
         cues=[("Noor Sample", "Welcome. This is the Maple Room, up to thirty people."),
               ("Jordan Example", "A U-shape for twenty-five works, with the coffee table at the back."),
               ("Alex Example", "And the side entrance with the lift, that's the step-free way in?"),
               ("Noor Sample", "Yes, the glass lift stops right here on the first floor."),
               ("Alex Example", "So are we confirmed for the twenty-second?"),
               ("Noor Sample", "I'm holding it for you until the ninth of October. Once the three hundred euro deposit is in, it's yours. Until then it's only on hold."),
               ("Alex Example", "Understood. Mira will pay the deposit."),
               ("Jordan Example", "I'll test the projector with our laptops before the day.")]),
    dict(date="2026-10-02", start="11:00", title="Catering call with Copper Kettle", speakers=["Alex Example", "Lukas Beispiel"],
         cues=[("Lukas Beispiel", "Twenty-five people, lunch buffet and coffee all day, as in the quote."),
               ("Alex Example", "Yes. We have twenty-three confirmed and a few pending."),
               ("Lukas Beispiel", "Fine. Final numbers by the sixteenth, please."),
               ("Alex Example", "I'll also find out how many vegetarian meals we need."),
               ("Lukas Beispiel", "Perfect, by Friday next week if you can.")]),
    dict(date="2026-10-06", start="09:30", title="Weekly check-in", speakers=["Sam Example", "Alex Example", "Mira Beispiel", "Jordan Example"],
         cues=[("Sam Example", "Venue first. Where are we?"),
               ("Mira Beispiel", "I've scheduled the deposit for Thursday the eighth. It's due on the ninth."),
               ("Alex Example", "Until Noor has it, the room is only on hold."),
               ("Sam Example", "Attendees?"),
               ("Alex Example", "Twenty-three confirmed, four pending, according to Mira's list from yesterday."),
               ("Alex Example", "I'd like to move the handover guide draft from the ninth to the sixteenth. The catering and venue work comes first."),
               ("Sam Example", "Agreed, sixteenth then."),
               ("Jordan Example", "Theo is off sick, so the laptops slip to next week.")]),
]

# Calendar of Alex Example. Times are local (Europe/Berlin unless noted).
CALENDAR = [
    dict(uid="cal-01", start="2026-09-12 10:00", end="2026-09-12 10:45", title="Project Lantern planning call", location="Online"),
    dict(uid="cal-02", start="2026-09-18 10:00", end="2026-09-18 12:00", title="Visit Cedar Demo Analytics", location="Zedernweg 1, Salzburg"),
    dict(uid="cal-03", start="2026-09-25 10:00", end="2026-09-25 10:45", title="Maple Room walk-through", location="Linden Hall Events, Lindenplatz 3, München"),
    dict(uid="cal-04", start="2026-09-30 17:00", end="2026-09-30 18:30", title="Team retro", location="Café Lindgren, Lindgrenstraße 4, München"),
    dict(uid="cal-05", start="2026-10-01 16:30", end="2026-10-01 17:00", title="Call Priya: webinar", location="Phone"),
    dict(uid="cal-06", start="2026-10-02 11:00", end="2026-10-02 11:30", title="Call Lukas: catering", location="Phone"),
    dict(uid="cal-07", start="2026-10-02 14:00", end="2026-10-02 14:20", title="Call Noor: numbers and deposit", location="Phone"),
    dict(uid="cal-08", start="2026-09-15 09:30", end="2026-09-15 10:15", title="Weekly check-in", location="Office", rrule="FREQ=WEEKLY;BYDAY=TU;COUNT=8"),
    dict(uid="cal-09", start="2026-10-09", end="2026-10-10", title="Deposit due: Maple Room (EUR 300)", allday=True),
    dict(uid="cal-10", start="2026-10-12", end="2026-10-13", title="Newsroom Daily trial ends", allday=True),
    dict(uid="cal-11", start="2026-10-22 08:30", end="2026-10-22 17:30", title="Learning day (Project Lantern)", location="Maple Room (on hold), Linden Hall Events", status="TENTATIVE"),
    dict(uid="cal-12", start="2026-10-26 07:10", end="2026-10-26 09:15", title="Flight AUR 214 Munich - London Heathrow", location="Munich Airport (MUC)",
         note="Imported from the e-ticket email on 8 Sep; not updated after the schedule change."),
    dict(uid="cal-13", start="2026-10-27 11:00", end="2026-10-27 12:30", title="Meeting Ravi Example, Harbour Lane Consulting", location="London",
         note="10:00 London time"),
    dict(uid="cal-14", start="2026-10-28 20:40", end="2026-10-28 22:35", title="Flight AUR 219 London Heathrow - Munich", location="London Heathrow (LHR)"),
    dict(uid="cal-15", start="2026-10-31 20:00", end="2026-10-31 22:30", title="Jazz im Kulturhaus (2 tickets)", location="Kulturhaus Demo, München"),
    dict(uid="cal-16", start="2026-11-13", end="2026-11-15", title="Workflow Summit Lisbon", allday=True, status="CANCELLED"),
    dict(uid="cal-17", start="2026-11-30", end="2026-12-01", title="Last day to cancel household insurance", allday=True),
]

# Telegram Bot API updates, as a capture bot receives them. 100000001 is Alex; 200000002 is a stranger.
TELEGRAM = [
    ("2026-10-06 19:00", 100000001, "/start"),
    ("2026-10-06 19:02", 100000001, "bought a monitor arm 39,90 € at Bureau Bits for the second desk"),
    ("2026-10-06 21:15", 100000001, "idea: run the learning day again in spring, in German"),
    ("2026-10-07 07:40", 100000001, "remind me: call Lea about the interpreter confirmation before 12 Oct"),
    ("2026-10-07 08:05", 100000001, "[photo] parking receipt Linden Hall"),
    ("2026-10-07 08:30", 100000001, "Noor says the guest Wi-Fi password is written on the whiteboard in the Maple Room"),
    ("2026-10-07 09:10", 200000002, "Hi! You won a free trip, click here to claim it"),
]

INTERACTIONS = [
    ("IN01", "P06", "2026-08-20", "email", "Asked about the Birch Room for 22 Oct", "", ""),
    ("IN02", "P06", "2026-08-21", "email", "Birch Room held until 10 Sep, EUR 900 per day", "", ""),
    ("IN03", "P06", "2026-09-10", "email", "Birch Room closed after water damage; suggested the Maple Room", "", ""),
    ("IN04", "P06", "2026-09-14", "email", "Sent quote (EUR 1,150) and draft agreement; room held until 9 Oct", "", ""),
    ("IN05", "P06", "2026-09-24", "email", "Confirmed step-free access via the side entrance lift", "", ""),
    ("IN06", "P06", "2026-09-25", "meeting", "Walk-through of the Maple Room with Jordan", "", ""),
    ("IN07", "P06", "2026-10-02", "call", "Talked about numbers and the deposit", "Send the final attendee number", "2026-10-15"),
    ("IN08", "P07", "2026-09-16", "call", "First call; recommended by Noor", "", ""),
    ("IN09", "P07", "2026-09-21", "email", "Quote EUR 640 for 25 people", "", ""),
    ("IN10", "P07", "2026-10-02", "call", "Agreed 25 people for now, final numbers by 16 Oct", "Tell Lukas the number of vegetarian meals", "2026-10-09"),
    ("IN11", "P08", "2025-11-04", "meeting", "Met at a Cedar Demo workshop in Salzburg", "", ""),
    ("IN12", "P08", "2026-08-20", "email", "Proposed co-hosting a webinar on intake workflows", "", ""),
    ("IN13", "P08", "2026-09-02", "email", "Moved to Moss Training Collective; new email address", "", ""),
    ("IN14", "P08", "2026-10-01", "call", "Discussed the webinar", "Send a first webinar outline", "2026-10-12"),
    ("IN15", "P11", "2026-06-11", "webinar", "Met in the Q&A of a webinar", "", ""),
    ("IN16", "P11", "2026-09-07", "email", "Meeting set for Tue 27 Oct 10:00 in London; prefers mornings", "", ""),
    ("IN17", "P10", "2026-09-29", "email", "Sent offer for interpreting; asks for confirmation by 12 Oct", "Confirm or decline the interpreters", "2026-10-12"),
    ("IN18", "P12", "2026-09-28", "email", "Invoice for badges and lanyards; the total is wrong", "", ""),
    ("IN19", "P12", "2026-10-05", "email", "Asked Clara to correct the total to EUR 107.10; no reply yet", "Chase the corrected invoice", "2026-10-09"),
    ("IN20", "P13", "2026-09-25", "email", "Invoice 2026-0042 for the handouts", "", ""),
    ("IN21", "P14", "2026-09-23", "email", "Asked whether the venue is step-free", "", ""),
    ("IN22", "P09", "2026-07-18", "dinner", "Dinner at Trattoria Fittizia, Malcesine", "", ""),
    ("IN23", "P09", "2026-10-04", "email", "Lisbon is off; suggested a trip in spring", "", ""),
    ("IN24", "P03", "2026-08-05", "meeting", "1:1 at Café Lindgren", "", ""),
    ("IN25", "P02", "2026-09-05", "email", "Approved the budget increase to EUR 2,500", "", ""),
]

DEADLINES = [
    ("DL01", "Pay the Maple Room deposit (EUR 300)", "2026-10-09", "scheduled", "Project Lantern", "", "Mira scheduled the payment for 8 Oct"),
    ("DL02", "Tell Lukas the number of vegetarian meals", "2026-10-09", "open", "Project Lantern", "", ""),
    ("DL03", "Chase the corrected PrintWorks invoice", "2026-10-09", "open", "Project Lantern", "", ""),
    ("DL04", "Newsroom Daily trial ends: keep or cancel", "2026-10-12", "open", "Home and finance", "", "EUR 9.99 a month after the trial"),
    ("DL05", "Send the webinar outline to Priya", "2026-10-12", "open", "Ideas", "", ""),
    ("DL06", "Confirm the interpreters with Signwise", "2026-10-12", "open", "Project Lantern", "", ""),
    ("DL07", "Send the final attendee number to Noor", "2026-10-15", "open", "Project Lantern", "", ""),
    ("DL08", "Final catering numbers to Lukas", "2026-10-16", "open", "Project Lantern", "", ""),
    ("DL09", "Handover guide draft", "2026-10-16", "open", "Project Lantern", "2026-10-09", "Moved in the weekly check-in on 6 Oct"),
    ("DL10", "Learning day", "2026-10-22", "scheduled", "Project Lantern", "", ""),
    ("DL11", "Last day for free cancellation, The Quill Hotel", "2026-10-24", "info", "Travel", "", "18:00 London time"),
    ("DL12", "DesignKit renews (EUR 119)", "2026-10-30", "info", "Home and finance", "", ""),
    ("DL13", "Last day to cancel the household insurance", "2026-11-30", "open", "Home and finance", "", "New premium EUR 168 from 2027"),
]

PURCHASES = [
    ("PU01", "2026-07-16", "Car rental, Verona airport, 4 days", "Pebble Rent", "travel", "236.80", "EUR", "", "PEB-INV", ""),
    ("PU02", "2026-08-18", "27-inch monitor", "Bureau Bits GmbH", "equipment", "249.00", "EUR", "2029-08-18", "BB-INV", ""),
    ("PU03", "2026-08-18", "27-inch monitor (from the scanned invoice)", "Bureau Bits GmbH", "equipment", "249.00", "EUR", "2029-08-18", "BB-INV-SCAN", "PU02"),
    ("PU04", "2026-09-03", "3 loan laptops", "Circuit & Co.", "equipment", "1797.00", "EUR", "2028-09-03", "CC-INV", ""),
    ("PU05", "2026-09-10", "USB-C docking station", "Kabelkiste Online", "equipment", "89.90", "EUR", "", "KK-RCPT", ""),
    ("PU06", "2026-09-08", "Flights Munich - London return", "Aurelian Air", "travel", "212.40", "EUR", "", "AUR-ETKT", ""),
    ("PU07", "2026-09-16", "Train ticket Munich - Salzburg (outbound)", "Südbahn Regio", "travel", "34.90", "EUR", "", "SUED-TKT", ""),
    ("PU08", "2026-09-12", "2 concert tickets", "TicketNest", "leisure", "64.00", "EUR", "", "TN-TKT", ""),
    ("PU09", "2026-09-25", "Handout printing", "Druckerei Weißblatt GmbH", "project", "140.42", "EUR", "", "WB-RE", ""),
    ("PU10", "2026-09-28", "Badges and lanyards (invoice states 117.10)", "PrintWorks Demo GmbH", "project", "107.10", "EUR", "", "PW-INV", ""),
    ("PU11", "2026-07-18", "Dinner", "Trattoria Fittizia", "meals", "72.50", "EUR", "", "R-TRAT", ""),
    ("PU12", "2026-08-22", "Lunch (EUR 49.71 charged by the bank)", "Bistro Limmatblick", "meals", "46.50", "CHF", "", "R-ZRH", ""),
    ("PU13", "2026-09-30", "Team retro", "Café Lindgren", "meals", "54.30", "EUR", "", "R-CAFE2", ""),
]

PLACES = [
    ("PL01", "Linden Hall Events (Maple Room)", "München", "Germany", "venue", "2026-09-25", "Jordan Example, Noor Sample", "", "visited",
     "Step-free via the glass lift at the side entrance on Lindenplatz"),
    ("PL02", "Trattoria Fittizia", "Malcesine, Lake Garda", "Italy", "restaurant", "2026-07-18", "Ben Sample", "5", "visited", "Dinner EUR 72.50"),
    ("PL03", "Bistro Limmatblick", "Zürich", "Switzerland", "restaurant", "2026-08-22", "", "4", "visited", "Lunch CHF 46.50"),
    ("PL04", "Café Lindgren", "München", "Germany", "café", "2026-08-05; 2026-09-30", "Jordan Example; the team", "4", "visited",
     "Room upstairs for about 10 people"),
    ("PL05", "Cedar Demo Analytics office", "Salzburg", "Austria", "client office", "2026-09-18", "", "", "visited", "Train from München Hbf at 07:28"),
    ("PL06", "Lake Garda trip", "Malcesine", "Italy", "trip", "2026-07-16 to 2026-07-20", "Ben Sample", "5", "visited", "Rental car from Verona airport"),
    ("PL07", "Casa Azulejo", "Lisbon", "Portugal", "hotel", "2026-11-13 to 2026-11-15", "", "", "cancelled", "Cancelled on 2026-10-03; refund pending"),
    ("PL08", "The Quill Hotel", "London", "United Kingdom", "hotel", "2026-10-26 to 2026-10-28", "", "", "booked", "Pay at the hotel; free cancellation until 24 Oct 18:00"),
]

IDEAS = [
    ("I01", "2026-06-20", "Run a customer learning day", "became a project", "P02", "Project Lantern (planned 2026-08-15)"),
    ("I02", "2026-06-28", "Short video tutorial for the intake form", "open", "", ""),
    ("I03", "2026-07-05", "Monthly office hours for customers", "open", "", ""),
    ("I04", "2026-07-12", "Template library with three examples", "open", "P03", ""),
    ("I05", "2026-07-22", "Learn basic Notion formulas", "someday", "", ""),
    ("I06", "2026-07-30", "Blog post about review queues", "open", "", "highlights-review-queues.md"),
    ("I07", "2026-08-20", "Co-host a webinar on intake workflows", "open", "P08", "Outline due 2026-10-12"),
    ("I08", "2026-08-25", "Go to the Workflow Summit in Lisbon", "dropped", "", "Summit moved online; hotel cancelled 2026-10-03"),
    ("I09", "2026-08-28", "Case study with Cedar Demo Analytics", "dropped", "P08", "Dropped on 2026-09-02 after Priya moved to Moss"),
    ("I10", "2026-09-06", "Offer the learning day in German", "someday", "", ""),
    ("I11", "2026-09-14", "Booking calendar for the loan laptops", "open", "P05", ""),
    ("I12", "2026-09-19", "Spring trip with Ben", "someday", "P09", ""),
    ("I13", "2026-10-02", "Accessibility checklist for every venue", "open", "P10; P06", "voice-memo-2026-10-02.md"),
    ("I14", "2026-10-02", "A second brain for the whole team", "open", "", "voice-memo-2026-10-02.md"),
    ("I15", "2026-09-30", "Rent the room upstairs at Café Lindgren for small workshops", "open", "", "cafe-lindgren-upstairs.md"),
]
