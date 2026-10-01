#!/usr/bin/env python3
"""Writes seed/content.json: every page, coach, post, menu and Club setting of the approved v2 site, as ACF field values.
Run: python3 tools/build_seed.py   (rerun after editing copy here; seed/import.php reads the JSON).
Conventions in the values: "@img:key" = media library image, "@page:slug" = page, "{home}" = site address.
Links are {"title","url"}. Square-bracket text would be an open fact; v2 uses Coming soon tags instead."""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "seed" / "content.json"
EMAIL = "info@tumbleweedsvolleyball.com"
MAIL = f"mailto:{EMAIL}"
IG = "https://www.instagram.com/tumbleweedsvball/"
H = "{home}"


def L(title, url):
    return {"title": title, "url": url}


# ------------------------------------------------------------------ images
IMAGES = {
    "tw-01": ("tw-01-celebration-indoor-court.jpg", "Volleyball players celebrating a point on an indoor court"),
    "tw-04": ("tw-04-gym-spike-wide.jpg", "Players at the net in a large indoor gym"),
    "tw-09b": ("tw-09b-ready-position-crop.jpg", "Player in ready position"),
    "tw-10": ("tw-10-wood-court-sunbeam.jpg", "Players running a passing drill on a wooden court"),
    "tw-11": ("tw-11-bump-wood-floor.jpg", "Player passing on a wood court"),
    "tw-12": ("tw-12-sports-hall-wide.jpg", "Rally in an indoor sports hall"),
    "tw-13": ("tw-13-ball-on-floor-detail.jpg", "Volleyball resting on a gym floor"),
    "tw-14": ("tw-14-net-texture-detail.jpg", "Volleyball net up close"),
    "tw-15": ("tw-15-silhouette-gym-ball.jpg", "Player holding a ball in a gym"),
    "og": ("tumbleweeds-social.jpg", "Tumbleweeds Volleyball Club. Developing athletes from the ground up."),
    "pat": ("pat-hennelly-headshoulders.png", "Pat Hennelly"),
    "iuliia": ("iuliia-pakhomenko-headshoulders.png", "Iuliia Pakhomenko"),
}


# ------------------------------------------------------------------ row builders (names = ACF field names)
def fact(label, value="", note="", tag="", link=None):
    r = {"fact_label": label, "fact_value": value, "fact_note": note, "fact_tag": tag}
    if link:
        r["fact_link"] = link
    return r


def head(eyebrow="", heading="", accent="", number=True, anchor="", side=None, lede="", bg=""):
    d = {"section_anchor": anchor, "section_eyebrow": eyebrow, "show_number": 1 if number else 0,
         "section_heading": heading, "section_heading_accent": accent, "section_bg_color": bg}
    if lede:
        d["section_lede"] = lede
    if side:
        kind, val = side
        d["section_side"] = kind
        d["section_side_text" if kind == "text" else "section_side_link"] = val
    else:
        d["section_side"] = "none"
    return d


def ticker():
    return {"acf_fc_layout": "section_ticker"}


def card(colour, title, text, image=None, foot="none", tag="", link=None):
    return {"card_colour": colour, "card_image": f"@img:{image}" if image else "", "card_title": title, "card_text": text,
            "card_foot": foot, "card_foot_tag": tag, "card_foot_link": link or ""}


def cards(h, cs, numbers=True, dates=None):
    d = {"acf_fc_layout": "section_cards", **h, "show_card_numbers": 1 if numbers else 0, "cards": cs}
    if dates:
        d["cards_dates"] = 1
        d["dates"] = dates
    else:
        d["cards_dates"] = 0
    return d


def strip(photos):
    return {"acf_fc_layout": "section_strip",
            "strip_photos": [{"strip_image": f"@img:{k}", "focus_x": x, "focus_y": y} for k, x, y in photos]}


def people(h):
    return {"acf_fc_layout": "section_people", **h}


def statement(main, accent):
    return {"acf_fc_layout": "section_statement", "section_heading": main, "section_heading_accent": accent}


def info_event(side_link):
    return {"event_kind": "info_session", "event_side": "button", "event_side_link": side_link}


def event(date, title, text, side="none", tag="", link=None):
    return {"event_kind": "other", "event_date": date, "event_title": title, "event_text": text, "event_side": side,
            "event_side_tag": tag, "event_side_link": link or ""}


def events(h, rows):
    return {"acf_fc_layout": "section_events", **h, "events": rows, "events_display": "gameday"}


def faq(h, items, numbered=False, open_first=True):
    return {"acf_fc_layout": "section_faq", **h, "faq_numbered": 1 if numbered else 0, "faq_open_first": 1 if open_first else 0, "faq_items": items}


def q(question, answer, anchor=""):
    return {"faq_question": question, "faq_anchor": anchor, "answer_kind": "text", "answer_text": answer}


def qf(question, rows, anchor=""):
    return {"faq_question": question, "faq_anchor": anchor, "answer_kind": "facts", "answer_facts": rows}


def cta_banner(eyebrow, heading, button):
    return {"acf_fc_layout": "section_cta", "cta_style": "banner", "section_anchor": "", "section_eyebrow": eyebrow,
            "section_heading": heading, "section_cta": button}


def facts(h, rows, box=None):
    d = {"acf_fc_layout": "section_facts", "facts_layout": "above", **h, "facts_rows": rows, "facts_box": 0}
    if box:
        d["facts_box"] = 1
        d.update({"box_eyebrow": box[0], "box_heading": box[1], "box_text": box[2], "box_tag": box[3],
                  "box_chips": [{"chip_text": c} for c in box[4]]})
    return d


def facts_left(h, rows):
    return {"acf_fc_layout": "section_facts", "facts_layout": "left", **h, "facts_rows": rows}


def ages(h, labels, note, tag):
    return {"acf_fc_layout": "section_ages", **h, "ages": [{"age_label": a, "age_caption": "Volleyball BC"} for a in labels],
            "ages_note": note, "ages_note_tag": tag}


def helpline(eyebrow, heading, text):
    return {"acf_fc_layout": "section_helpline", "section_anchor": "", "section_eyebrow": eyebrow, "show_number": 1,
            "section_heading": heading, "section_lede": text}


def band(img, heading, accent, b1, b2, size="standard"):
    return {"acf_fc_layout": "section_band", "band_size": size, "band_image": f"@img:{img}", "band_heading": heading, "band_heading_accent": accent,
            "band_button_1": b1, "band_button_2": b2}


def hero(img, x, y, tag, heading, accent="", sub="", b1=None, b2=None, layout="page", phone=None):
    p = {"hero_phone_focus": 1, "hero_phone_x": phone[0], "hero_phone_y": phone[1]} if phone else {"hero_phone_focus": 0}
    return {**p, "hero_layout": layout, "hero_image": f"@img:{img}", "hero_focus_x": x, "hero_focus_y": y, "hero_tag": tag,
            "hero_heading": heading, "hero_heading_accent": accent, "hero_subhead": sub,
            "hero_button_1": b1 or "", "hero_button_2": b2 or ""}


EMAIL_BTN = L("Email the club", MAIL)
TRYOUT_BTN = L("Tryout details", H + "tryouts/")
INFO_BTN = L("Info session details", H + "#coming-up")

pages = []

# ------------------------------------------------------------------ HOME
pages.append({"slug": "home", "title": "Home", "front_page": True,
  "hero": hero("tw-01", 50, 35, "Kamloops youth volleyball", "Developing athletes from the", "ground up.",
               "A new Kamloops club, led by Pat Hennelly, 2024 U Sports Men's Volleyball Coach of the Year.",
               L("Tryout details", H + "tryouts/"), L("Meet the club", H + "our-coaches/"), layout="home", phone=(42, 30)),
  "flex": [
    ticker(),
    cards(head("What parents ask", "Who coaches. How they coach.", "What it costs.", side=("link", L("Read the parent questions", H + "for-parents/"))), [
        card("sage", "Who coaches your kid", "Every team will have a named coach, posted with their background before tryouts. Pat Hennelly is our President. Iuliia Pakhomenko runs operations.", "tw-15", "tag", "Coach list coming soon"),
        card("sun", "How we coach", "Fundamentals first. The basics, taught in a set order, until they're automatic. Then we build on them.", "tw-10", "link", link=L("See the programs", H + "programs/")),
        card("sand", "What you're signing up for", "The whole season on one page: the total cost with coach and travel fees, the schedule, and who to call outside the club.", "tw-13", "tag", "Posting before tryouts"),
      ], dates=[
        {"date_kind": "info_session", "date_link": L("Parent info session", H + "tryouts/")},
        {"date_kind": "custom", "date_label": "Before tryouts", "date_title": "Coaches announced", "date_line": "A named coach for every team", "date_link": L("Coaches announced", H + "tryouts/")},
        {"date_kind": "custom", "date_label": "Late November", "date_title": "Tryouts", "date_line": "In the Volleyball BC tryout window", "date_link": L("Tryouts", H + "tryouts/")},
      ]),
    strip([("tw-14", 50, 50), ("tw-11", 30, 50), ("tw-12", 50, 50), ("tw-09b", 55, 50)]),
    people(head("The club", "The people who run the club.", anchor="people", side=("text", "Coaches for each team are announced before tryouts."))),
    statement("Your kid's first club season starts", "here."),
    events(head("Coming up", "Come meet us before tryouts.", anchor="coming-up"), [
        info_event(L("Follow on Instagram", IG)),
        event("Before tryouts", "Coaches announced", "Every team's coach, with their background.", "tag", "Coming soon"),
        event("Late Nov", "Tryouts", "Held in the Volleyball BC tryout window. Dates and age groups coming soon.", "button", link=EMAIL_BTN),
      ]),
    faq(head("For parents", "The questions every parent should ask.", anchor="questions", lede="Volleyball BC tells families to ask these before choosing a club. Here's where we stand."), [
        q("Who actually coaches my kid?", "<p>Every team will have a named coach, posted with their background before tryouts. Pat Hennelly leads the club as President.</p>"),
        q("What does the season cost, all in?", "<p>We'll post one total that includes coach and travel fees, plus what's included and our refund policy, before tryouts.</p>"),
        q("How much travel is there?", "<p>The club season runs December to May, with Provincials in April and May. The tournament list for each age group will be posted with the schedule.</p>"),
        q("How do you keep kids safe?", "<p>Every adult in a position of authority completes a criminal record check, a screening disclosure and Safe Sport training, as Volleyball BC requires. Concerns can go to the Abuse-Free Sport Helpline at 1-888-837-7678.</p>"),
      ]),
    cta_banner("Sponsors", "Put your name behind Kamloops kids.", L("Become a founding sponsor", H + "sponsors/")),
    band("tw-04", "See you at", "tryouts.", L("Tryout details", H + "#coming-up"), EMAIL_BTN, "tall"),
  ]})

# ------------------------------------------------------------------ OUR COACHES
pages.append({"slug": "our-coaches", "title": "Our coaches", "menu": "Coaches",
  "hero": hero("tw-01", 50, 35, "The club", "Who runs the club, and who", "coaches.", "Here is who leads the club now. Team coaches will be named here as the club confirms them."),
  "flex": [
    people(head("The club", "The people who run the club.", side=("text", "Club leadership today. Team coaches are named before tryouts."))),
    cards(head("Coach list", "Who coaches each team."), [
        card("sage", "A named coach for every team", "Every team will have a named coach, posted here with their background before tryouts. If you want to know who is in the gym with your athlete, this is where you will find out.", foot="tag", tag="Coach list coming soon"),
        card("sun", "Want to coach with us?", "Tell us who you are and what you coach. We read every email.", foot="button", link=EMAIL_BTN),
      ]),
    facts(head("Safe Sport", "Volleyball BC rules for every coach."), [
        fact("Criminal record check", "Volleyball BC requires one for every person in authority at a club, renewed every 3 years."),
        fact("Screening form", "Every coach and club leader files an annual Screening Disclosure."),
        fact("Safe Sport training", "Every coach and club leader completes Safe Sport training."),
        fact("Tumbleweeds", "We will confirm each coach's checks are on file before the first practice.", tag="Posting before tryouts"),
      ]),
    cta_banner("Talk to us", "Questions about who coaches? Ask us.", EMAIL_BTN),
    band("tw-12", "See you at", "tryouts.", TRYOUT_BTN, EMAIL_BTN),
  ]})

# ------------------------------------------------------------------ PROGRAMS
pages.append({"slug": "programs", "title": "Programs", "menu": "Programs",
  "hero": hero("tw-10", 50, 60, "Programs", "Programs by", "age group.", "Volleyball BC runs club teams from 12U to 18U. We will post which ones we run this season."),
  "flex": [
    ages(head("Age groups", "Programs by age group."), [f"{a}U" for a in range(12, 19)],
         "Volleyball BC runs club teams for 12U to 18U. Which of these Tumbleweeds runs this season is still being confirmed.", "Posting before tryouts"),
    strip([("tw-12", 50, 50), ("tw-10", 40, 50), ("tw-01", 50, 50), ("tw-11", 30, 50)]),
    statement("Fundamentals", "first."),
    facts_left(head("How we coach", "The basics, in a set order.", lede="We teach the basics in a set order until they are automatic. Then we build on them."), [
        fact("Coaching approach", "Fundamentals first, taught in a set order."),
        fact("Practices per week", tag="Coming soon"),
        fact("Courts and athletes per team", tag="Coming soon"),
      ]),
    facts(head("The season", "Season at a glance."), [
        fact("Season", "Volleyball BC's club season runs from December to May, with an offseason from August to November."),
        fact("Provincials", "Volleyball BC Provincials run over four weekends in April and May.", "Which Tumbleweeds teams attend is not confirmed yet.", "Coming soon"),
        fact("Practice location", tag="Coming soon"),
        fact("Tournaments and travel", "We will list every tournament and where it is before you sign.", tag="Posting before tryouts"),
        fact("Girls and boys teams", tag="Coming soon"),
      ]),
    cta_banner("Talk to us", "Questions about a team? Ask us.", EMAIL_BTN),
    band("tw-04", "See you at", "tryouts.", TRYOUT_BTN, EMAIL_BTN),
  ]})

# ------------------------------------------------------------------ TRYOUTS
pages.append({"slug": "tryouts", "title": "Tryouts", "menu": "Tryouts",
  "hero": hero("tw-04", 50, 50, "Tryouts, late November", "Tryouts,", "when and where.", "Dates, location and what to bring get posted here as we confirm them.", EMAIL_BTN, L("Meet the coaches", H + "our-coaches/")),
  "flex": [
    events(head("Dates", "What happens, and when."), [
        info_event(L("Follow on Instagram", IG)),
        event("Before tryouts", "Coaches announced", "A named coach for every team, with their background.", "tag", "Coming soon"),
        event("Late Nov", "Tryouts", "Held in the Volleyball BC tryout window. Dates and age groups coming soon.", "button", link=EMAIL_BTN),
        event("After tryouts", "Signing", "Volleyball BC sets the signing dates for each age group.", "tag", "Dates coming soon"),
      ]),
    facts_left(head("Before you come", "What to know.", lede="Nothing here is final until we say so. Each item gets posted as the club confirms it."), [
        fact("Who can try out", tag="Coming soon"), fact("Where", tag="Coming soon"), fact("What to bring", tag="Coming soon"),
        fact("Cost to try out", tag="Coming soon"),
        fact("Registration", "Registration opens before tryouts. We will post the link here and on Instagram."),
      ]),
    faq(head("Tryout questions", "Things parents ask."), [
        q("Can my athlete try out if they signed with another club early?", "<p>Volleyball BC runs an Early Signing Period from September 1 to October 15, 2026 for 15U to 18U athletes returning to their previous club. An athlete who signed early cannot try out elsewhere. Not sure? Ask Volleyball BC before you register.</p>"),
        q("Does my athlete need club experience?", f"<p>We will say how tryouts work for athletes new to club volleyball before tryouts. Questions now? <a href=\"{MAIL}\">Email the club</a>.</p>"),
        q("When will we hear back?", "<p>We will post the timeline with the tryout dates.</p>"),
      ]),
    band("tw-12", "Come meet us", "first.", INFO_BTN, EMAIL_BTN),
  ]})

# ------------------------------------------------------------------ FEES
def kf(*rows):
    return [fact(*r) if isinstance(r, tuple) else r for r in rows]

pages.append({"slug": "fees-and-registration", "title": "Fees and registration", "menu": "Fees", "footer_menu": "Fees and registration",
  "hero": hero("tw-13", 50, 60, "Fees and registration", "What the season costs,", "in total.", "Club fee, coach and travel fees, what is included, and the refund policy, all in one place.", EMAIL_BTN),
  "flex": [
    facts(head("Fees and registration", "Every cost, line by line.", anchor="fees"), [
        fact("Club fee", tag="Coming soon"),
        fact("Coach and travel fees", "Shown here with the rest, so the total is not a surprise.", tag="Coming soon"),
        fact("Estimated season total", tag="Coming soon"),
        fact("Payment plan", tag="Coming soon"),
        fact("What the fee includes", "Coaching, tournament entry, uniform, hotels and transportation. We will say which are in and which are out.", tag="Posting before tryouts"),
        fact("Refund policy", "Volleyball BC requires every club to publish one.", tag="Posting before tryouts"),
        fact("Fundraising and volunteering", "What families are asked to do.", tag="Coming soon"),
      ], box=("Season total", "One total, with everything in it.", "We will post one number that includes coach and travel fees, so the total is not a surprise.", "Posting before tryouts",
              ["Club fee", "Coach and travel fees", "What is included", "Payment plan", "Refund policy"])),
    faq(head("The rest of the answers", "Who coaches, who runs the club, how we keep kids safe.", lede="The five things Volleyball BC tells families to ask any club. Ours, in one place."), [
        qf("Training", [fact("Coaching approach", "Fundamentals first, taught in a set order."), fact("Who coaches each team", "A named coach for every team, posted with their background before tryouts."), fact("Practices per week", tag="Coming soon"), fact("Courts and athletes per team", tag="Coming soon"), fact("Sport science and strength", tag="Coming soon")], "training"),
        qf("Culture", [fact("Values", tag="Coming soon"), fact("Athletes who come back", "This is the club's first season, so there are no returning athletes yet."), fact("Playing time", "How playing time works for each age group.", tag="Posting before tryouts")], "culture"),
        qf("Organisation", [fact("Status", "Registered non-profit. Volleyball BC member club, in good standing (new club), Zone 2 Thompson-Okanagan."), fact("Year started", "2026. New Volleyball BC clubs serve a one-year probation."), fact("Board", tag="Coming soon"), fact("Policies", "Codes of conduct for parents, athletes and coaches, a complaint and dispute process, and a conflict of interest policy. Volleyball BC requires every club to publish them.", tag="Links coming soon"), fact("Complaints contact", "A named person outside the club.", tag="Coming soon")], "organisation"),
        qf("Safe Sport", [fact("Screening", "Volleyball BC requires every person in authority to pass a criminal record check every 3 years, file an annual Screening Disclosure, and complete Safe Sport training."), fact("Open and Observable", tag="Coming soon"), fact("Boundaries", "One-on-one time and boundaries policy.", tag="Coming soon"), fact("Overnight travel", tag="Coming soon"), fact("Helpline", "Abuse-Free Sport Helpline: 1-888-83SPORT (77678)")], "safe-sport"),
      ], numbered=True),
    {"acf_fc_layout": "section_cta", "cta_style": "highlight", "section_anchor": "registration", "section_eyebrow": "Registration", "show_number": 1,
     "section_heading": "Register for tryouts.", "section_lede": "Registration opens before tryouts. We will post the link and opening date here.", "cta_tag": "Coming soon", "section_cta": EMAIL_BTN, "cta_use_registration": 1},
    band("tw-10", "Questions before you", "register?", EMAIL_BTN, L("For parents", H + "for-parents/")),
  ]})

# ------------------------------------------------------------------ FOR PARENTS
FEES = H + "fees-and-registration/"
pages.append({"slug": "for-parents", "title": "For parents", "menu": "For parents",
  "hero": hero("tw-11", 40, 60, "For parents", "Straight answers,", "including the hard ones.", "We are a new club. Here is what you are probably wondering, answered plainly."),
  "flex": [
    faq(head("Before you sign up", "Questions parents ask.", lede="We are a new club. Here is what you are probably wondering, answered plainly."), [
        q("Pat coaches the university team. Is he coaching my kid?", "<p>We will state Pat's exact role plainly here before tryouts, so you know who is in the gym with your athlete.</p>"),
        q("You are brand new. Why risk a season?", "<p>You are right, this is our first season. As the club confirms them, we will post who coaches, what the season costs, and how Safe Sport works, so you can decide with everything in front of you. New clubs also serve a one-year probation with Volleyball BC.</p>"),
        q("What does it cost, really?", "<p>We will show the club fee, coach and travel fees, and the season total, plus what is included and what is not, and the refund policy. All of it before tryouts.</p>"),
        q("How much travel is there?", "<p>The club season runs December to May, with Provincials in April and May. We will list every tournament, where it is, and whether hotels are included before you sign.</p>"),
        q("Will my kid play?", "<p>We will write down how playing time works for each age group before tryouts.</p>"),
        q("Who do I call if something goes wrong?", "<p>Talk to your coach first. If you need someone outside the club, we will post a named contact before tryouts. For concerns about abuse or maltreatment, anyone in Canada can call the Abuse-Free Sport Helpline at 1-888-83SPORT (77678).</p>"),
      ]),
    cards(head("What Volleyball BC tells parents to ask", "What to ask any club, ours included."), [
        card("sage", "Culture", "What are the club's values, and do actions match?", foot="link", link=L("Our answers", FEES + "#culture")),
        card("sun", "Organisation", "How long established, who is on the board, which policies are posted?", foot="link", link=L("Our answers", FEES + "#organisation")),
        card("sand", "Training", "Who coaches, what is the approach, how many practices a week?", foot="link", link=L("Our answers", FEES + "#training")),
        card("sage", "Fees", "What is included, and what is the refund policy?", foot="link", link=L("Our answers", FEES + "#fees")),
        card("sun", "Safe Sport", "How are coaches screened, and what are the rules on one-on-one time and travel?", foot="link", link=L("Our answers", FEES + "#safe-sport")),
      ]),
    helpline("Safe Sport", "If something feels wrong, call.", "For concerns about abuse or maltreatment, anyone in Canada can call the Abuse-Free Sport Helpline. It is free and confidential."),
    band("tw-12", "Still have a", "question?", EMAIL_BTN, L("Info session", H + "#coming-up")),
  ]})

# ------------------------------------------------------------------ SPONSORS
pages.append({"slug": "sponsors", "title": "Sponsors", "menu": "Sponsors",
  "hero": hero("tw-12", 50, 50, "Sponsors", "Put your name behind", "Kamloops kids.", "Tumbleweeds is a Kamloops club for Kamloops families. Sponsors put their name in front of those families.", L("Become a sponsor", MAIL)),
  "flex": [
    cards(head("Where you show up", "Your name, where families look."), [
        card("sage", "On the jersey", "Your name on the uniform families see every weekend.", foot="tag", tag="Placement coming soon"),
        card("sun", "On the website", "Your name and a link on the page parents check before they sign.", foot="tag", tag="Placement coming soon"),
        card("sand", "In the gym", "Your banner where athletes and families are in the room.", foot="tag", tag="Placement coming soon"),
      ]),
    facts(head("", "", number=False), [], box=("Sponsor levels", "What each level includes.", "Email the club and we will send the sponsor details when they are final.", "Levels coming soon", ["Levels", "Amounts", "What each includes"])),
    facts(head("Who you would back", "The families behind the logo."), [
        fact("Athletes and families", "Known after tryouts."),
        fact("Where we play", "Kamloops, BC. Practice location posted before tryouts."),
      ]),
    band("tw-10", "Talk to", "us.", EMAIL_BTN, L("Meet the club", H + "our-coaches/")),
  ]})

# ------------------------------------------------------------------ NEWS (the posts page)
pages.append({"slug": "news", "title": "News", "posts_page": True, "footer_menu": "News",
  "hero": hero("tw-11", 40, 60, "News", "Club news, dates and", "announcements."),
  "flex": [
    {"acf_fc_layout": "section_news", **head("Latest", "From the club.", side=("link", L("Follow on Instagram", IG))), "news_count": 12},
    cta_banner("Talk to us", "Want updates in your inbox?", EMAIL_BTN),
    band("tw-04", "See you at", "tryouts.", TRYOUT_BTN, EMAIL_BTN),
  ]})

# ------------------------------------------------------------------ CONTACT
pages.append({"slug": "contact", "title": "Contact", "menu": "Contact", "footer_menu": "",
  "hero": hero("tw-14", 50, 50, "Contact", "Questions?", "Ask us.", "Coaches, fees, tryouts or sponsoring. Email us."),
  "flex": [
    {"acf_fc_layout": "section_contact", **head("Reach the club", "How to find us.", lede="Questions about coaches, fees, tryouts or sponsoring? Email us and we will point you to the right person."),
     "contact_rows": [
        fact("Email", link=L(EMAIL, MAIL)),
        fact("Instagram", link=L("@tumbleweedsvball", IG)),
        fact("Info session", "Sunday, October 4, 7:00 to 8:30 pm, TRU Science Building S337"),
        fact("Practice location", tag="Coming soon"),
        fact("Club complaints contact", tag="Coming soon"),
        fact("Abuse-Free Sport Helpline", link=L("1-888-83SPORT (77678)", "tel:+18888377678")),
     ],
     "form_heading": "Send a message.",
     "form_topics": [{"topic_text": t} for t in ("Coaches", "Fees", "Tryouts", "Sponsoring", "Something else")],
     "form_note": "This opens your email app with the message ready to send to the club."},
    band("tw-12", "See you at", "tryouts.", TRYOUT_BTN, EMAIL_BTN),
  ]})


# ------------------------------------------------------------------ PRIVACY POLICY (draft, the club reviews it)
PRIVACY = """<p><strong>Club to review.</strong> This is a plain-language draft written from what the website does today. Someone on the club's board should read it, fix anything that is not true for the club, and then remove this paragraph.</p>
<p>Last updated: October 2026.</p>
<h2>Who we are</h2>
<p>Tumbleweeds Volleyball Club is a registered non-profit volleyball club in Kamloops, BC, and a Volleyball BC member club. This page explains what this website collects and what we do with it. Questions about it go to <a href="mailto:info@tumbleweedsvolleyball.com">info@tumbleweedsvolleyball.com</a>.</p>
<h2>What the website collects</h2>
<ul>
<li><strong>The contact form.</strong> Your name, your email address, the topic you pick and your message. It is emailed to the club so we can answer you. It is not stored on the website.</li>
<li><strong>The sign-up form in the footer.</strong> Your email address, so we can send club news such as tryout dates and coach announcements.</li>
<li><strong>Visit counts (only if the club turns analytics on).</strong> Google Analytics counts visits: which pages are opened, what kind of device and an approximate location. By default it runs without cookies and does not identify you.</li>
<li><strong>Technical logs.</strong> Like every website, our web host keeps basic logs (your IP address, the page asked for, the time) for security and to keep the site running.</li>
</ul>
<h2>What we do with it</h2>
<ul>
<li>Answer your message.</li>
<li>Send club news to people who signed up. Every email has an unsubscribe link, and you can also ask us to remove you.</li>
<li>Understand which pages families use, so we can improve the site.</li>
</ul>
<p>We do not sell or rent your information, and we do not show ads.</p>
<h2>Who else sees it</h2>
<p>Club volunteers who answer email and send news. Our email service (club to confirm which one, for example Mailchimp or Flodesk) holds the sign-up list. Google receives visit counts if analytics is on. Our web host stores the website itself.</p>
<h2>Registration and children</h2>
<p>This website is written for parents and guardians. We do not ask children for personal information on it. Registering an athlete happens on a separate registration service (club to confirm: TeamSnap or Volleyball BC), which has its own privacy policy.</p>
<h2>How long we keep it</h2>
<p>We keep messages as long as we need to answer them and follow up. We keep the sign-up list until you unsubscribe. (Club to confirm these.)</p>
<h2>Your choices</h2>
<p>You can ask what we have about you, ask us to correct it, or ask us to delete it. Email us at the address above. In British Columbia, privacy in non-profit organizations is covered by the Personal Information Protection Act, and you can also contact the Office of the Information and Privacy Commissioner for BC.</p>
<h2>Changes</h2>
<p>If we change what the website collects, we will update this page and the date at the top.</p>"""

pages.append({"slug": "privacy-policy", "title": "Privacy policy", "menu": "", "footer_menu": "",
  "hero": hero("tw-14", 50, 50, "Club to review", "Privacy", "policy.", "What this website collects, why, and your choices."),
  "flex": [
    {"acf_fc_layout": "section_text", **head("The short version", "We collect only what we need to answer you.", number=False, anchor="policy"), "section_text": PRIVACY},
  ]})

# ------------------------------------------------------------------ COACHES (CPT)
def coach_band(img):
    return {"band_image": f"@img:{img}", "band_heading": "Come meet us", "band_heading_accent": "before tryouts.",
            "band_button_1": INFO_BTN, "band_button_2": EMAIL_BTN}

coaches = [
  {"slug": "pat-hennelly", "title": "Pat Hennelly", "menu_order": 1,
   "fields": {"coach_role": "President",
              "coach_summary": "TRU WolfPack men's head coach since 2005. 2024 U Sports Men's Volleyball Coach of the Year.",
              "coach_photo": "@img:pat",
              "coach_bio": "<p>Pat Hennelly is the President of Tumbleweeds Volleyball Club.</p><p>He has coached university volleyball since 1995: at UBC, as an assistant at Northern Arizona University, and as head coach of the TRU WolfPack men's team since 2005.</p><p>He was named the 2024 U Sports Men's Volleyball Coach of the Year. He was also named 2024 Canada West Men's Volleyball Coach of the Year.</p>",
              "coach_facts": [
                  {"fact_label": "Experience", "fact_value": "University coach since 1995", "fact_tag": ""},
                  {"fact_label": "Current post", "fact_value": "TRU WolfPack men's volleyball head coach since 2005", "fact_tag": ""},
                  {"fact_label": "Award", "fact_value": "2024 U Sports Men's Volleyball Coach of the Year", "fact_tag": ""},
                  {"fact_label": "Coaching role with Tumbleweeds teams", "fact_value": "Team assignments are named before tryouts.", "fact_tag": "Coming soon"}],
              "coach_hero_image": "@img:tw-12", "hero_focus_x": 50, "hero_focus_y": 40,
              **coach_band("tw-10")}},
  {"slug": "iuliia-pakhomenko", "title": "Iuliia Pakhomenko", "menu_order": 2,
   "fields": {"coach_role": "Manager of Operations",
              "coach_summary": "Played professionally in Ukraine, then played and coached for the TRU WolfPack.",
              "coach_photo": "@img:iuliia",
              "coach_bio": "<p>Iuliia Pakhomenko is the club's Manager of Operations.</p><p>She played professionally in Ukraine, then played and coached for the TRU WolfPack.</p><p>She is the club's contact on the Volleyball BC registry, so questions about the club's status and paperwork come to her.</p>",
              "coach_facts": [
                  {"fact_label": "Playing", "fact_value": "Former professional player in Ukraine", "fact_tag": ""},
                  {"fact_label": "Coaching", "fact_value": "Former TRU WolfPack athlete and coach", "fact_tag": ""},
                  {"fact_label": "Coaching role with Tumbleweeds teams", "fact_value": "Team assignments are named before tryouts.", "fact_tag": "Coming soon"}],
              "coach_hero_image": "@img:tw-15", "hero_focus_x": 50, "hero_focus_y": 40,
              **coach_band("tw-04")}},
]

# ------------------------------------------------------------------ NEWS POSTS
def post_band():
    return {"band_image": "@img:tw-10", "band_heading": "Come meet us", "band_heading_accent": "before tryouts.",
            "band_button_1": INFO_BTN, "band_button_2": EMAIL_BTN}

posts = [
  {"slug": "info-session", "title": "Info session for new families", "date": "2026-09-30 09:00:00",
   "excerpt": "Come meet Pat Hennelly and Iuliia Pakhomenko, and ask anything about coaches, fees, and Safe Sport.",
   "thumb": "tw-12",
   "content": "<p>Come meet Pat Hennelly and Iuliia Pakhomenko, and ask anything about coaches, fees, and Safe Sport.</p>\n\n<p><strong>When:</strong> Sunday, October 4, 7:00 to 8:30 pm.<br><strong>Where:</strong> TRU Science Building, room S337. Free parking in S Lot.</p>\n\n<p>Can't make it? A Teams link goes up on our Instagram story that day, <a href=\"" + IG + "\">@tumbleweedsvball</a>.</p>",
   "fields": {"hero_focus_x": 50, "hero_focus_y": 55, **post_band()}},
  {"slug": "what-we-will-publish-before-tryouts", "title": "What we will publish before tryouts", "date": "2026-10-01 09:00:00",
   "excerpt": "A new club owes parents straight answers. Here is what we will post, and when.",
   "thumb": "tw-13",
   "content": "<p>A new club owes parents straight answers. As the club confirms them, we will post:</p>\n\n<p>Who coaches each team, with their background.<br>The full fee list, and what it includes.<br>Practice nights and location.<br>The refund policy.<br>Who to call if something goes wrong.</p>\n\n<p>Each item goes on this site as soon as it is confirmed, and we will say so on Instagram.</p>",
   "fields": {"hero_focus_x": 50, "hero_focus_y": 55, **post_band()}},
]

# ------------------------------------------------------------------ CLUB SETTINGS
settings = {
  "announcement_show": 1,
  "announcement_text": "Info session for parents: Sunday, October 4, 7:00 to 8:30 pm, TRU Science Building S337.",
  "announcement_link": L("Details", H + "#coming-up"),
  "announcement_until": "20261004",
  "logo_text": "Tumbleweeds",
  "header_cta": L("Tryouts", H + "tryouts/"),
  "phone_menu_link": L("News", H + "news/"),
  "coaches_page": "@page:our-coaches",
  "info_title": "Parent info session",
  "info_date": "20261004",
  "info_time": "7:00 to 8:30 pm",
  "info_place": "TRU Science Building S337",
  "info_details": "Free parking in S Lot. Can't make it? A Teams link goes up on our Instagram story that day.",
  "ticker_phrases": [{"ticker_phrase": t} for t in ("Developing athletes from the ground up", "Kamloops, BC", "Tryouts late November", "Info session Sun, Oct 4", "Est. 2026")],
  "badge_text": "Tumbleweeds · Kamloops, BC · Est. 2026 · Volleyball club ·",
  "contact_email": EMAIL,
  "club_location": "Kamloops, BC",
  "footer_contact_link": L("Contact page", H + "contact/"),
  "socials": [{"social_network": "instagram", "social_label": "@tumbleweedsvball", "social_url": IG}],
  "helpline_name": "Abuse-Free Sport Helpline",
  "helpline_phone": "1-888-83SPORT (77678)",
  "complaints_contact": "coming soon",
  "footer_blurb": "Kamloops youth volleyball. Developing athletes from the ground up.",
  "footer_signup_title": "Stay in the loop.",
  "footer_signup_code": "",
  "footer_status_line": "A Volleyball BC member club (new club), Zone 2 Thompson-Okanagan.",
  "footer_small_print": "Placeholder photography: Unsplash. Club photo day to come.",
  "footer_privacy_label": "Privacy policy",
  "footer_title_club": "The club", "footer_title_contact": "Contact", "footer_title_help": "If something goes wrong",
  "label_news": "News", "label_club": "The club", "label_complaints": "Club complaints contact",
  "header_register": 1, "registration_url": "", "registration_label": "Register now",
  "contact_form": "@form:contact", "footer_signup_form": "@form:signup",
  "social_image": "@img:og", "ga4_id": "", "ga4_cookies": 0,
}

# Contact Form 7 forms the import creates (when the plugin is active). Tags are CF7 syntax: [text* name].
FORMS = {
  "contact": {"title": "Contact form", "to": EMAIL, "subject": "[your-topic] from [your-name]",
    "body": "From: [your-name] <[your-email]>\nTopic: [your-topic]\n\n[your-message]\n\n-- \nSent from the contact form on [_site_url]",
    "form": '<label>Your name [text* your-name autocomplete:name]</label>\n<label>Your email [email* your-email autocomplete:email]</label>\n<label>What is it about [select your-topic "Coaches" "Fees" "Tryouts" "Sponsoring" "Something else"]</label>\n<label>Message [textarea* your-message]</label>\n[submit class:btn class:btn--dark "Send message"]'},
  "signup": {"title": "Newsletter sign-up", "to": EMAIL, "subject": "Add me to club updates",
    "body": "Please add [your-email] to club updates.\n\n-- \nSent from the footer sign-up on [_site_url]",
    "form": '<label class="screen-reader-text" for="signup-email">Your email</label>[email* your-email id:signup-email autocomplete:email placeholder "Your email"][submit class:btn class:btn--light "Sign up"]'},
}

# Search results text for every page, coach and post (Yoast SEO reads these as the page's own title and description)
SEO = {
  "home": ("Tumbleweeds Volleyball Club | Kamloops youth volleyball", "A new Kamloops youth volleyball club led by Pat Hennelly, 2024 U Sports Men's Volleyball Coach of the Year. Developing athletes from the ground up."),
  "our-coaches": ("Our coaches | Tumbleweeds Volleyball Club", "Who runs Tumbleweeds Volleyball Club in Kamloops, and who coaches. Team coaches are named before tryouts."),
  "programs": ("Programs | Tumbleweeds Volleyball Club", "Club volleyball programs by age group in Kamloops, built on fundamentals taught in a set order."),
  "tryouts": ("Tryouts | Tumbleweeds Volleyball Club", "Tryout dates, location and what to bring for Tumbleweeds Volleyball Club, posted as the club confirms them."),
  "fees-and-registration": ("Fees and registration | Tumbleweeds Volleyball Club", "Every cost of the club season, line by line, plus what is included and the refund policy."),
  "for-parents": ("For parents | Tumbleweeds Volleyball Club", "The questions every parent should ask a club, answered: coaches, cost, travel and safety."),
  "sponsors": ("Sponsors | Tumbleweeds Volleyball Club", "Put your name behind Kamloops kids. Become a founding sponsor of Tumbleweeds Volleyball Club."),
  "news": ("News | Tumbleweeds Volleyball Club", "News from Tumbleweeds Volleyball Club: info sessions, coach announcements and tryout updates."),
  "contact": ("Contact | Tumbleweeds Volleyball Club", "Email the club about coaches, fees, tryouts or sponsoring. Tumbleweeds Volleyball Club, Kamloops, BC."),
  "privacy-policy": ("Privacy policy | Tumbleweeds Volleyball Club", "What the Tumbleweeds Volleyball Club website collects, why, and your choices."),
  "pat-hennelly": ("Pat Hennelly | Tumbleweeds Volleyball Club", "Pat Hennelly, President of Tumbleweeds Volleyball Club and TRU WolfPack men's head coach since 2005."),
  "iuliia-pakhomenko": ("Iuliia Pakhomenko | Tumbleweeds Volleyball Club", "Iuliia Pakhomenko, Manager of Operations at Tumbleweeds Volleyball Club."),
  "info-session": ("Info session for new families | Tumbleweeds Volleyball Club", "Come meet Pat Hennelly and Iuliia Pakhomenko, and ask anything about coaches, fees and Safe Sport."),
  "what-we-will-publish-before-tryouts": ("What we will publish before tryouts | Tumbleweeds Volleyball Club", "A new club owes parents straight answers. Here is what we will post, and when."),
}
for _item in pages + coaches + posts:
    if _item["slug"] in SEO:
        _item["seo"] = {"title": SEO[_item["slug"]][0], "desc": SEO[_item["slug"]][1]}
for _pg in pages:
    if _pg["slug"] == "tryouts":
        _pg["hero"]["hero_register"] = 1

data = {"images": {k: {"file": ("assets/img/" if k == "og" else "seed/img/") + f, "alt": a} for k, (f, a) in IMAGES.items()},
        "pages": pages, "coaches": coaches, "posts": posts, "settings": settings, "forms": FORMS,
        "header_menu": ["coaches", "programs", "tryouts", "fees", "parents", "sponsors", "contact"]}
OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
print("seed written:", len(pages), "pages,", len(coaches), "coaches,", len(posts), "posts")
