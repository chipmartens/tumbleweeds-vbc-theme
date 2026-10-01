#!/usr/bin/env python3
"""Generates every v2 static page from one shared shell (nav, mobile sheet, footer, closing band).
Run: python3 _build.py   (from website/v2). Relative links, works on file:// and GitHub Pages."""
import os, re, html
ROOT = os.path.dirname(os.path.abspath(__file__))
EMAIL = "info@tumbleweedsvolleyball.com"
IG = "https://www.instagram.com/tumbleweedsvball/"
ARR = '<svg class="arrow" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
PLUS = '<span class="plus"><svg width="14" height="14" viewBox="0 0 14 14" stroke="currentColor" stroke-width="1.5"><path d="M7 1v12M1 7h12"/></svg></span>'
NAV = [("coaches", "Coaches", "our-coaches/"), ("programs", "Programs", "programs/"), ("tryouts", "Tryouts", "tryouts/"),
       ("fees", "Fees", "fees-and-registration/"), ("parents", "For parents", "for-parents/"), ("sponsors", "Sponsors", "sponsors/"),
       ("contact", "Contact", "contact/")]

def soon(t="Coming soon"): return f'<span class="tag tag--soon">{t}</span>'
def link(href, label): return f'<a class="link" href="{href}">{label} {ARR}</a>'

def shell(page):
    r = "../" * page["depth"]
    u = lambda p: r + (p + "index.html" if p else "index.html")
    active = page.get("active")
    def navlinks(extra=""):
        return "".join(f'<a href="{u(p)}"{" aria-current=\"page\"" if k == active else ""}>{l}</a>' for k, l, p in NAV)
    ann_href = ("#coming-up" if page["depth"] == 0 else u("") + "#coming-up")
    head = f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page["title"])}</title>
<meta name="description" content="{html.escape(page["desc"])}">
<link rel="icon" type="image/svg+xml" href="{r}img/tumbleweeds-mark-small.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600&family=Figtree:wght@300;400;500;600&family=Instrument+Serif:ital@1&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/site.css">
</head>
<body>

<div class="ann">Info session for parents: Sunday, October 4, 7:00 to 8:30 pm, TRU Science Building S337. <a href="{ann_href}">Details</a></div>

<nav class="nav" aria-label="Main">
  <a class="nav__logo" href="{u("")}" aria-label="Tumbleweeds Volleyball Club home"><img src="{r}img/tumbleweeds-mark-small.svg" alt=""><span>Tumbleweeds</span></a>
  <div class="nav__links">{navlinks()}</div>
  <a class="btn btn--sun btn--sm" href="{u("tryouts/")}">Tryouts</a>
  <button class="nav__menu" aria-label="Open menu" aria-expanded="false"><svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M2 6h14M2 12h14"/></svg></button>
</nav>
<div class="sheetmenu" id="menu" aria-hidden="true">
  <div class="sheetmenu__top"><span class="nav__logo"><img src="{r}img/tumbleweeds-mark-small-reverse.svg" alt=""><span>Tumbleweeds</span></span><button class="nav__menu" style="display:flex" aria-label="Close menu" data-close><svg width="16" height="16" viewBox="0 0 16 16" stroke="currentColor" stroke-width="1.5"><path d="M2 2l12 12M14 2L2 14"/></svg></button></div>
  <nav aria-label="Mobile">{navlinks()}<a href="{u("news/")}"{" aria-current=\"page\"" if active=="news" else ""}>News</a></nav>
  <a class="btn btn--sun" href="{u("tryouts/")}">Tryout details</a>
</div>
'''
    footer = f'''
<footer class="footer{" footer--flat" if not page.get("band") else ""}">
  <img class="footer__wreath" src="{r}img/tumbleweeds-mark-reverse.svg" alt="">
  <div class="footer__news">
    <h2 class="h3">Stay in the loop.</h2>
    <!-- Preview only: no backend. Opens the visitor's email app addressed to the club. -->
    <form onsubmit="location.href='mailto:{EMAIL}?subject='+encodeURIComponent('Add me to club updates')+'&amp;body='+encodeURIComponent('Please add '+this.email.value+' to club updates.');return false"><label class="sr" for="em" hidden>Email</label><input id="em" name="email" type="email" placeholder="Your email" required><button class="btn btn--light" type="submit">Sign up</button></form>
  </div>
  <div class="footer__cols">
    <div><a href="{u("")}" style="display:flex;align-items:center;gap:12px;font:600 20px/24px Figtree;color:var(--sand-100)"><img src="{r}img/tumbleweeds-mark-reverse.svg" alt="" style="height:48px;width:48px">Tumbleweeds<br>Volleyball Club</a><p style="margin:16px 0 0;font-size:14px;line-height:22px;color:rgba(243,235,223,.75);max-width:30ch">Kamloops youth volleyball. Developing athletes from the ground up.</p></div>
    <div><h5>The club</h5><ul><li><a href="{u("our-coaches/")}">Coaches</a></li><li><a href="{u("programs/")}">Programs</a></li><li><a href="{u("tryouts/")}">Tryouts</a></li><li><a href="{u("fees-and-registration/")}">Fees and registration</a></li><li><a href="{u("for-parents/")}">For parents</a></li><li><a href="{u("sponsors/")}">Sponsors</a></li><li><a href="{u("news/")}">News</a></li></ul></div>
    <div><h5>Contact</h5><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{IG}">@tumbleweedsvball</a></li><li><a href="{u("contact/")}">Contact page</a></li><li>Kamloops, BC</li></ul></div>
    <div><h5>If something goes wrong</h5><ul><li>Abuse-Free Sport Helpline</li><li><a href="tel:18888377678">1-888-83SPORT (77678)</a></li><li>Club complaints contact: coming soon</li></ul></div>
  </div>
  <div class="footer__base">
    <span>© 2026 Tumbleweeds Volleyball Club. A Volleyball BC member club (new club), Zone 2 Thompson-Okanagan.</span>
    <span>Placeholder photography: Unsplash. Club photo day to come.</span>
  </div>
</footer>

<script src="{r}assets/site.js" defer></script>
</body>
</html>
'''
    return head, footer, u

def phero(page, u):
    r = "../" * page["depth"]
    h = page["hero"]
    lead = f'<p class="hero__lead">{h["lead"]}</p>' if h.get("lead") else ""
    ctas = ""
    if h.get("ctas"):
        ctas = '<div class="hero__ctas">' + "".join(
            f'<a class="btn {c[2]}" href="{c[1]}">{c[0]}{(" " + ARR) if c[2]=="btn--light" else ""}</a>' for c in h["ctas"]) + "</div>"
    return f'''
<header class="phero">
  <img class="hero__img" src="{r}img/{h["img"]}" alt="{h["alt"]}"{(' style="object-position:' + h["pos"] + '"') if h.get("pos") else ""} fetchpriority="high">
  <div class="phero__inner">
    <span class="hero__tag"><span class="dot"></span>{h["tag"]}</span>
    <h1>{h["h1"]}</h1>
    {lead}
    {ctas}
  </div>
</header>
'''

def band(page, u):
    b = page.get("band")
    if not b: return ""
    r = "../" * page["depth"]
    return f'''
<section class="band band--compact">
  <img src="{r}img/{b["img"]}" alt="" loading="lazy">
  <div class="band__inner">
    <h2 class="h2">{b["h2"]}</h2>
    <div class="ctas">
      <a class="btn btn--sun" href="{b["cta"][1]}">{b["cta"][0]}</a>
      <a class="btn btn--ghost" href="{b["cta2"][1]}">{b["cta2"][0]}</a>
    </div>
  </div>
</section>
'''

def render(page, body):
    head, footer, u = shell(page)
    out = head + phero(page, u) + "\n<main>\n" + body(u, "../" * page["depth"]) + "\n</main>\n" + band(page, u) + footer
    path = os.path.join(ROOT, page["path"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(out)

def sheet(num, eyebrow, h2, inner, head_extra="", tint="", id_=""):
    t = f" sheet--tint-{tint}" if tint else ""
    i = f' id="{id_}"' if id_ else ""
    return f'''<section class="sheet{t}"{i}>
  <div class="wrap">
    <div class="sheet__head reveal">
      <div>
        <p class="eyebrow"><b>{num}</b>{eyebrow}</p>
        <h2 class="h2">{h2}</h2>
      </div>
      {head_extra}
    </div>
    {inner}
  </div>
</section>'''

def facts(rows):
    out = '<div class="facts reveal">'
    for k, v, note, tag in rows:
        n = f"<small>{note}</small>" if note else ""
        t = soon(tag) if tag else "<span></span>"
        out += f'<div class="fact"><span class="fact__k">{k}</span><div class="fact__v">{v}{n}</div>{t}</div>'
    return out + "</div>"

def cta_block(h3, label, href, tint="sun"):
    return f'''<section class="sponsor-wrap"><div><div class="sponsor reveal"><div><p class="eyebrow" style="margin-bottom:8px">Talk to us</p><h2 class="h3">{h3}</h2></div><a class="btn btn--dark" href="{href}">{label}</a></div></div></section>'''

def person_card(u, r, slug, name, role, blurb, img):
    return f'''<article class="person reveal">
        <div class="person__img"><img src="{r}img/{img}" alt="{name}" loading="lazy"></div>
        <div class="person__body">
          <h3 class="h4">{name}</h3>
          <span class="role">{role}</span>
          <p>{blurb}</p>
          {link(u("coaches/" + slug + "/"), "Read the bio")}
        </div>
      </article>'''

PAT = ("pat-hennelly", "Pat Hennelly", "President", "TRU WolfPack men's head coach since 2005. 2024 U Sports Men's Volleyball Coach of the Year.", "pat-hennelly-headshoulders.png")
IUL = ("iuliia-pakhomenko", "Iuliia Pakhomenko", "Manager of Operations", "Played professionally in Ukraine, then played and coached for the TRU WolfPack.", "iuliia-pakhomenko-headshoulders.png")

pages = []

# ---------------- HOME (body kept in _src/home.body.html) ----------------
def home():
    head, footer, u = shell({"depth": 0, "title": "Tumbleweeds Volleyball Club | Kamloops youth volleyball",
                             "desc": "A new youth volleyball club in Kamloops. Developing athletes from the ground up.", "active": None})
    b = open(os.path.join(ROOT, "_src/home.body.html")).read()
    rep = [
        ('<a class="btn btn--light" href="#coming-up">Tryout details', f'<a class="btn btn--light" href="{u("tryouts/")}">Tryout details'),
        ('<a class="btn btn--ghost" href="#people">Meet the club</a>', f'<a class="btn btn--ghost" href="{u("our-coaches/")}">Meet the club</a>'),
        ('<a class="link" href="#questions">Read the parent questions', f'<a class="link" href="{u("for-parents/")}">Read the parent questions'),
        ('<a class="link" href="#">See the programs', f'<a class="link" href="{u("programs/")}">See the programs'),
        ('<a class="btn btn--sun" href="#coming-up">Tryout details</a>', f'<a class="btn btn--sun" href="{u("tryouts/")}">Tryout details</a>'),
        ('<a class="btn btn--dark" href="mailto:info@tumbleweedsvolleyball.com">Become a founding sponsor', f'<a class="btn btn--dark" href="{u("sponsors/")}">Become a founding sponsor'),
        ("The club season runs January to May", "The club season runs December to May"),
    ]
    for a, c in rep:
        assert a in b, a
        b = b.replace(a, c)
    # upnext rail links -> tryouts page
    b = re.sub(r'(<div class="upnext[^>]*>)(.*?)(</div>)', lambda m: m.group(1) + m.group(2).replace('href="#coming-up"', f'href="{u("tryouts/")}"') + m.group(3), b, flags=re.S)
    # two bio links
    b = b.replace('<a class="link" href="#">Read the bio', f'<a class="link" href="{u("coaches/pat-hennelly/")}">Read the bio', 1)
    b = b.replace('<a class="link" href="#">Read the bio', f'<a class="link" href="{u("coaches/iuliia-pakhomenko/")}">Read the bio', 1)
    out = head + b.replace("\n<main>", "\n<main>", 1) + footer
    open(os.path.join(ROOT, "index.html"), "w").write(out)
home()

# ---------------- OUR COACHES ----------------
def coaches_body(u, r):
    ppl = '<div class="people">' + person_card(u, r, *PAT) + person_card(u, r, *IUL) + '</div>'
    s1 = sheet("01", "The club", "The people who run the club.", ppl,
               '<p class="lead" style="margin:0">Club leadership today. Team coaches are named before tryouts.</p>')
    coachlist = f'''<div class="cards cards--2">
      <article class="card card--sage reveal"><div class="card__body"><span class="card__num">01</span><h3 class="h4">A named coach for every team</h3><p>Every team will have a named coach, posted here with their background before tryouts. If you want to know who is in the gym with your athlete, this is where you will find out.</p><div class="card__foot">{soon("Coach list coming soon")}</div></div></article>
      <article class="card card--sun reveal"><div class="card__body"><span class="card__num">02</span><h3 class="h4">Want to coach with us?</h3><p>Tell us who you are and what you coach. We read every email.</p><div class="card__foot"><a class="btn btn--outline btn--sm" href="mailto:{EMAIL}">Email the club</a></div></div></article>
    </div>'''
    s2 = sheet("02", "Coach list", "Who coaches each team.", coachlist)
    ss = facts([
        ("Criminal record check", "Volleyball BC requires one for every person in authority at a club, renewed every 3 years.", "", ""),
        ("Screening form", "Every coach and club leader files an annual Screening Disclosure.", "", ""),
        ("Safe Sport training", "Every coach and club leader completes Safe Sport training.", "", ""),
        ("Tumbleweeds", "We will confirm each coach's checks are on file before the first practice.", "", "Posting before tryouts"),
    ])
    s3 = sheet("03", "Safe Sport", "Volleyball BC rules for every coach.", ss)
    return s1 + "\n" + s2 + "\n" + s3 + "\n" + cta_block("Questions about who coaches? Ask us.", "Email the club", f"mailto:{EMAIL}")

pages.append(({"depth": 1, "path": "our-coaches/index.html", "active": "coaches", "title": "Our coaches | Tumbleweeds Volleyball Club",
  "desc": "Who runs Tumbleweeds Volleyball Club in Kamloops, and how team coaches will be named.",
  "hero": {"img": "tw-01-celebration-indoor-court.jpg", "alt": "Players celebrating a point on an indoor court", "pos": "50% 35%", "tag": "The club",
           "h1": "Who runs the club, and who <span class=\"accent\">coaches.</span>",
           "lead": "Here is who leads the club now. Team coaches will be named here as the club confirms them."},
  "band": {"img": "tw-12-sports-hall-wide.jpg", "h2": "See you at <span class=\"accent\">tryouts.</span>", "cta": ("Tryout details", "../tryouts/index.html"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, coaches_body))

# ---------------- COACH PAGES ----------------
def coach_page(slug, name, role, summary, img, hero_img, hero_alt, bio, creds, other, hero_pos=None):
    def body(u, r):
        cred_rows = facts([(k, c, "", "") for k, c in creds] + [("Coaching role with Tumbleweeds teams", "Team assignments are named before tryouts.", "", "Coming soon")])
        inner = f'''<div class="bio">
      <div class="bio__img reveal"><img src="{r}img/{img}" alt="{name}" loading="lazy"></div>
      <div class="reveal">
        <p class="eyebrow"><b>01</b>{role}</p>
        <h2 class="h2">{name}</h2>
        <span class="role">{role}, Tumbleweeds Volleyball Club</span>
        <div class="prose">{bio}</div>
        {cred_rows}
      </div>
    </div>'''
        s = f'<section class="sheet"><div class="wrap">{inner}</div></section>'
        on = other
        pager = f'''<section class="sheet" style="padding-top:48px;padding-bottom:48px"><div class="wrap"><div class="pager reveal">
      <a href="{u("our-coaches/")}"><span><span class="data">The club</span><strong>All coaches</strong></span>{ARR}</a>
      <a href="{u("coaches/" + on[0] + "/")}"><span><span class="data">Next</span><strong>{on[1]}</strong></span>{ARR}</a>
    </div></div></section>'''
        return s + "\n" + pager
    return ({"depth": 2, "path": f"coaches/{slug}/index.html", "active": "coaches", "title": f"{name} | Tumbleweeds Volleyball Club",
             "desc": f"{name}, {role} of Tumbleweeds Volleyball Club in Kamloops. {summary}",
             "hero": {"img": hero_img, "alt": hero_alt, "pos": hero_pos, "tag": "Our coaches", "h1": name, "lead": f"{role}, Tumbleweeds Volleyball Club."},
             "band": {"img": "tw-04-gym-spike-wide.jpg" if slug == "iuliia-pakhomenko" else "tw-10-wood-court-sunbeam.jpg", "h2": "Come meet us <span class=\"accent\">before tryouts.</span>", "cta": ("Info session details", "../../index.html#coming-up"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, body)

pages.append(coach_page("pat-hennelly", "Pat Hennelly", "President", PAT[3], "pat-hennelly-headshoulders.png", "tw-12-sports-hall-wide.jpg", "Rally in an indoor sports hall",
  "<p>Pat Hennelly is the President of Tumbleweeds Volleyball Club.</p><p>He has coached university volleyball since 1995: at UBC, as an assistant at Northern Arizona University, and as head coach of the TRU WolfPack men's team since 2005.</p><p>In 2024 he was named U Sports Men's Volleyball Coach of the Year. He was also named 2024 Canada West Men's Volleyball Coach of the Year.</p>",
  [("Experience", "University coach since 1995"), ("Current post", "TRU WolfPack men's volleyball head coach since 2005"), ("Award", "2024 U Sports Men's Volleyball Coach of the Year")],
  ("iuliia-pakhomenko", "Iuliia Pakhomenko")))
pages.append(coach_page("iuliia-pakhomenko", "Iuliia Pakhomenko", "Manager of Operations", IUL[3], "iuliia-pakhomenko-headshoulders.png", "tw-15-silhouette-gym-ball.jpg", "Player holding a volleyball in a dim gym",
  "<p>Iuliia Pakhomenko is the club's Manager of Operations.</p><p>She played professionally in Ukraine, then played and coached for the TRU WolfPack.</p><p>She is the club's contact on the Volleyball BC registry, so questions about the club's status and paperwork come to her.</p>",
  [("Playing", "Former professional player in Ukraine"), ("Coaching", "Former TRU WolfPack athlete and coach")],
  ("pat-hennelly", "Pat Hennelly"), "50% 40%"))

# ---------------- PROGRAMS ----------------
def programs_body(u, r):
    ages = '<div class="ages reveal">' + "".join(f'<div class="age"><b>{a}U</b><span>Volleyball BC</span></div>' for a in range(12, 19)) + '</div>'
    ages += f'<p class="ages-note reveal">Volleyball BC runs club teams for 12U to 18U. Which of these Tumbleweeds runs this season is still being confirmed. {soon("Posting before tryouts")}</p>'
    s1 = sheet("01", "Age groups", "Programs by age group.", ages)
    strip = f'''<div class="strip" aria-label="Photos">
  <figure class="reveal"><img src="{r}img/tw-12-sports-hall-wide.jpg" alt="Rally in an indoor sports hall" loading="lazy"></figure>
  <figure class="reveal"><img src="{r}img/tw-10-wood-court-sunbeam.jpg" alt="Players on a wooden court" loading="lazy" style="object-position:40% 50%"></figure>
  <figure class="reveal"><img src="{r}img/tw-01-celebration-indoor-court.jpg" alt="Players celebrating a point" loading="lazy"></figure>
  <figure class="reveal"><img src="{r}img/tw-11-bump-wood-floor.jpg" alt="Player passing on a wood court" loading="lazy" style="object-position:30% 50%"></figure>
</div>'''
    st = '<section class="statement reveal"><img class="statement__mark" src="' + r + 'img/tumbleweeds-mark.svg" alt=""><p>Fundamentals <span class="accent">first.</span></p></section>'
    how = f'''<div class="split">
      <div class="reveal"><p class="eyebrow"><b>02</b>How we coach</p><h2 class="h2">The basics, in a set order.</h2><p class="lead" style="margin-top:20px">We teach the basics in a set order until they are automatic. Then we build on them.</p></div>
      <div class="reveal">{facts([("Coaching approach", "Fundamentals first, taught in a set order.", "", ""), ("Practices per week", "", "", "Coming soon"), ("Courts and athletes per team", "", "", "Coming soon")])}</div></div>'''
    s2 = f'<section class="sheet"><div class="wrap">{how}</div></section>'
    season = facts([
        ("Season", "Volleyball BC's club season runs from December to May, with an offseason from August to November.", "", ""),
        ("Provincials", "Volleyball BC Provincials run over four weekends in April and May.", "Which Tumbleweeds teams attend is not confirmed yet.", "Coming soon"),
        ("Practice location", "", "", "Coming soon"),
        ("Tournaments and travel", "We will list every tournament and where it is before you sign.", "", "Posting before tryouts"),
        ("Girls and boys teams", "", "", "Coming soon"),
    ])
    s3 = sheet("03", "The season", "Season at a glance.", season)
    return s1 + "\n" + strip + "\n" + st + "\n" + s2 + "\n" + s3 + "\n" + cta_block("Questions about a team? Ask us.", "Email the club", f"mailto:{EMAIL}")

pages.append(({"depth": 1, "path": "programs/index.html", "active": "programs", "title": "Programs | Tumbleweeds Volleyball Club",
  "desc": "Programs by age group, and the club season at a glance, from Tumbleweeds Volleyball Club in Kamloops.",
  "hero": {"img": "tw-10-wood-court-sunbeam.jpg", "alt": "Players running a drill on a wooden court", "pos": "50% 60%", "tag": "Programs",
           "h1": "Programs by <span class=\"accent\">age group.</span>",
           "lead": "Volleyball BC runs club teams from 12U to 18U. We will post which ones we run this season."},
  "band": {"img": "tw-04-gym-spike-wide.jpg", "h2": "See you at <span class=\"accent\">tryouts.</span>", "cta": ("Tryout details", "../tryouts/index.html"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, programs_body))

# ---------------- TRYOUTS ----------------
def faq(items, open_first=False, n=False):
    out = '<div class="faq reveal' + (' faq--n' if n else '') + '">'
    for i, it in enumerate(items):
        q, a = it[0], it[1]
        id_ = f' id="{it[2]}"' if len(it) > 2 else ""
        o = " open" if (open_first and i == 0) else ""
        num = f'<b class="faq__n">{i+1:02d}</b>' if n else ""
        out += f'<details{id_}{o}><summary>{num}<span>{q}</span> {PLUS}</summary><div class="ans">{a}</div></details>'
    return out + "</div>"

def tryouts_body(u, r):
    ev = f'''<div class="events">
      <div class="event reveal"><span class="date">Sun, Oct 4</span><div><h3 class="h4">Parent info session</h3><p class="meta" style="margin:4px 0 0">7:00 to 8:30 pm, TRU Science Building, room S337. Free parking in S Lot. Can't make it? A Teams link goes up on our Instagram story that day.</p></div><a class="btn btn--outline btn--sm" href="{IG}">Follow on Instagram</a></div>
      <div class="event reveal"><span class="date">Before tryouts</span><div><h3 class="h4">Coaches announced</h3><p class="meta" style="margin:4px 0 0">A named coach for every team, with their background.</p></div>{soon()}</div>
      <div class="event reveal"><span class="date">Late Nov</span><div><h3 class="h4">Tryouts</h3><p class="meta" style="margin:4px 0 0">Held in the Volleyball BC tryout window. Dates and age groups coming soon.</p></div><a class="btn btn--outline btn--sm" href="mailto:{EMAIL}">Email the club</a></div>
      <div class="event reveal"><span class="date">After tryouts</span><div><h3 class="h4">Signing</h3><p class="meta" style="margin:4px 0 0">Volleyball BC sets the signing dates for each age group.</p></div>{soon("Dates coming soon")}</div>
    </div>'''
    s1 = sheet("01", "Dates", "What happens, and when.", ev)
    know = facts([("Who can try out", "", "", "Coming soon"), ("Where", "", "", "Coming soon"), ("What to bring", "", "", "Coming soon"),
                  ("Cost to try out", "", "", "Coming soon"), ("Registration", "Registration opens before tryouts. We will post the link here and on Instagram.", "", "")])
    s2 = f'''<section class="sheet"><div class="wrap split">
      <div class="reveal"><p class="eyebrow"><b>02</b>Before you come</p><h2 class="h2">What to know.</h2><p class="lead" style="margin-top:20px">Nothing here is final until we say so. Each item gets posted as the club confirms it.</p></div>
      <div>{know}</div></div></section>'''
    qs = faq([
        ("Can my athlete try out if they signed with another club early?", "<p>Volleyball BC runs an Early Signing Period from September 1 to October 15, 2026 for 15U to 18U athletes returning to their previous club. An athlete who signed early cannot try out elsewhere. Not sure? Ask Volleyball BC before you register.</p>"),
        ("Does my athlete need club experience?", f"<p>We will say how tryouts work for athletes new to club volleyball before tryouts. Questions now? <a class='link' href='mailto:{EMAIL}'>Email the club</a>.</p>"),
        ("When will we hear back?", "<p>We will post the timeline with the tryout dates.</p>"),
    ], open_first=True)
    s3 = f'''<section class="sheet"><div class="wrap split">
      <div class="reveal"><p class="eyebrow"><b>03</b>Tryout questions</p><h2 class="h2">Things parents ask.</h2></div>{qs}</div></section>'''
    return s1 + "\n" + s2 + "\n" + s3

pages.append(({"depth": 1, "path": "tryouts/index.html", "active": "tryouts", "title": "Tryouts | Tumbleweeds Volleyball Club",
  "desc": "Tryout timing, what to know before you come, and common questions from Tumbleweeds Volleyball Club in Kamloops.",
  "hero": {"img": "tw-04-gym-spike-wide.jpg", "alt": "Players at the net in a large indoor gym", "pos": "50% 50%", "tag": "Tryouts, late November",
           "h1": "Tryouts, <span class=\"accent\">when and where.</span>",
           "lead": "Dates, location and what to bring get posted here as we confirm them.",
           "ctas": [("Email the club", f"mailto:{EMAIL}", "btn--light"), ("Meet the coaches", "../our-coaches/index.html", "btn--ghost")]},
  "band": {"img": "tw-12-sports-hall-wide.jpg", "h2": "Come meet us <span class=\"accent\">first.</span>", "cta": ("Info session details", "../index.html#coming-up"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, tryouts_body))

# ---------------- FEES ----------------
def fees_body(u, r):
    price = f'''<div class="pricecard reveal">
      <div><p class="eyebrow" style="margin-bottom:16px">Season total</p><h3 class="h3">One total, with everything in it.</h3><p>We will post one number that includes coach and travel fees, so the total is not a surprise. {soon("Posting before tryouts")}</p></div>
      <div class="chips"><span class="chip">Club fee</span><span class="chip">Coach and travel fees</span><span class="chip">What is included</span><span class="chip">Payment plan</span><span class="chip">Refund policy</span></div>
    </div>'''
    fees = facts([
        ("Club fee", "", "", "Coming soon"),
        ("Coach and travel fees", "Shown here with the rest, so the total is not a surprise.", "", "Coming soon"),
        ("Estimated season total", "", "", "Coming soon"),
        ("Payment plan", "", "", "Coming soon"),
        ("What the fee includes", "Coaching, tournament entry, uniform, hotels and transportation. We will say which are in and which are out.", "", "Posting before tryouts"),
        ("Refund policy", "Volleyball BC requires every club to publish one.", "", "Posting before tryouts"),
        ("Fundraising and volunteering", "What families are asked to do.", "", "Coming soon"),
    ])
    s1 = sheet("01", "Fees and registration", "What the season costs, in total.", price + fees, id_="fees")
    acc = faq([
        ("Training", facts([("Coaching approach", "Fundamentals first, taught in a set order.", "", ""), ("Who coaches each team", "A named coach for every team, posted with their background before tryouts.", "", ""), ("Practices per week", "", "", "Coming soon"), ("Courts and athletes per team", "", "", "Coming soon"), ("Sport science and strength", "", "", "Coming soon")]), "training"),
        ("Culture", facts([("Values", "", "", "Coming soon"), ("Athletes who come back", "This is the club's first season, so there are no returning athletes yet.", "", ""), ("Playing time", "How playing time works for each age group.", "", "Posting before tryouts")]), "culture"),
        ("Organisation", facts([("Status", "Registered non-profit. Volleyball BC member club, in good standing (new club), Zone 2 Thompson-Okanagan.", "", ""), ("Year started", "2026. New Volleyball BC clubs serve a one-year probation.", "", ""), ("Board", "", "", "Coming soon"), ("Policies", "Codes of conduct for parents, athletes and coaches, a complaint and dispute process, and a conflict of interest policy. Volleyball BC requires every club to publish them.", "", "Links coming soon"), ("Complaints contact", "A named person outside the club.", "", "Coming soon")]), "organisation"),
        ("Safe Sport", facts([("Screening", "Volleyball BC requires every person in authority to pass a criminal record check every 3 years, file an annual Screening Disclosure, and complete Safe Sport training.", "", ""), ("Open and Observable", "", "", "Coming soon"), ("Boundaries", "One-on-one time and boundaries policy.", "", "Coming soon"), ("Overnight travel", "", "", "Coming soon"), ("Helpline", "Abuse-Free Sport Helpline: 1-888-83SPORT (77678)", "", "")]), "safe-sport"),
    ], open_first=True, n=True)
    s2 = f'''<section class="sheet"><div class="wrap split">
      <div class="reveal"><p class="eyebrow"><b>02</b>The rest of the answers</p><h2 class="h2">Who coaches, who runs the club, how we keep kids safe.</h2><p class="lead" style="margin-top:20px">The five things Volleyball BC tells families to ask any club. Ours, in one place.</p></div>{acc}</div></section>'''
    s3 = f'''<section class="sheet sheet--tint-sun" id="registration"><div class="wrap sheet__head" style="margin:0;align-items:center">
      <div class="reveal"><p class="eyebrow"><b>03</b>Registration</p><h2 class="h3">Register for tryouts.</h2><p class="lead" style="margin-top:12px">Registration opens before tryouts. We will post the link and opening date here. {soon("Coming soon")}</p></div>
      <a class="btn btn--dark reveal" href="mailto:{EMAIL}">Email the club</a></div></section>'''
    return s1 + "\n" + s2 + "\n" + s3

pages.append(({"depth": 1, "path": "fees-and-registration/index.html", "active": "fees", "title": "Fees and registration | Tumbleweeds Volleyball Club",
  "desc": "What the season costs in total, what is included, and how the club answers the questions Volleyball BC tells parents to ask.",
  "hero": {"img": "tw-13-ball-on-floor-detail.jpg", "alt": "Volleyball resting on a gym floor", "pos": "50% 60%", "tag": "Fees and registration",
           "h1": "What the season costs, <span class=\"accent\">in total.</span>",
           "lead": "Club fee, coach and travel fees, what is included, and the refund policy, all in one place.",
           "ctas": [("Email the club", f"mailto:{EMAIL}", "btn--light")]},
  "band": {"img": "tw-10-wood-court-sunbeam.jpg", "h2": "Questions before you <span class=\"accent\">register?</span>", "cta": ("Email the club", f"mailto:{EMAIL}"), "cta2": ("For parents", "../for-parents/index.html")}}, fees_body))

# ---------------- FOR PARENTS ----------------
def parents_body(u, r):
    qs = faq([
        ("Pat coaches the university team. Is he coaching my kid?", "<p>We will state Pat's exact role plainly here before tryouts, so you know who is in the gym with your athlete.</p>"),
        ("You are brand new. Why risk a season?", "<p>You are right, this is our first season. As the club confirms them, we will post who coaches, what the season costs, and how Safe Sport works, so you can decide with everything in front of you. New clubs also serve a one-year probation with Volleyball BC.</p>"),
        ("What does it cost, really?", "<p>We will show the club fee, coach and travel fees, and the season total, plus what is included and what is not, and the refund policy. All of it before tryouts.</p>"),
        ("How much travel is there?", "<p>The club season runs December to May, with Provincials in April and May. We will list every tournament, where it is, and whether hotels are included before you sign.</p>"),
        ("Will my kid play?", "<p>We will write down how playing time works for each age group before tryouts.</p>"),
        ("Who do I call if something goes wrong?", "<p>Talk to your coach first. If you need someone outside the club, we will post a named contact before tryouts. For concerns about abuse or maltreatment, anyone in Canada can call the Abuse-Free Sport Helpline at 1-888-83SPORT (77678).</p>"),
    ], open_first=True)
    s1 = f'''<section class="sheet"><div class="wrap split">
      <div class="reveal"><p class="eyebrow"><b>01</b>Before you sign up</p><h2 class="h2">Questions parents ask.</h2><p class="lead" style="margin-top:20px">We are a new club. Here is what you are probably wondering, answered plainly.</p></div>{qs}</div></section>'''
    f = u("fees-and-registration/")
    items = [("01", "Culture", "What are the club's values, and do actions match?", "culture"), ("02", "Organisation", "How long established, who is on the board, which policies are posted?", "organisation"),
             ("03", "Training", "Who coaches, what is the approach, how many practices a week?", "training"), ("04", "Fees", "What is included, and what is the refund policy?", "fees"),
             ("05", "Safe Sport", "How are coaches screened, and what are the rules on one-on-one time and travel?", "safe-sport")]
    tints = ["sage", "sun", "sand", "sage", "sun"]
    cards = '<div class="cards cards--5">' + "".join(
        f'<article class="card card--{tints[i]} reveal"><div class="card__body"><span class="card__num">{n}</span><h3 class="h4">{t}</h3><p>{p}</p><div class="card__foot">{link(f + "#" + a, "Our answers")}</div></div></article>'
        for i, (n, t, p, a) in enumerate(items)) + '</div>'
    s2 = sheet("02", "What Volleyball BC tells parents to ask", "What to ask any club, ours included.", cards)
    helpline = '''<section class="helpline reveal"><p class="eyebrow"><b>03</b>Safe Sport</p><h2 class="h2">If something feels wrong, call.</h2><p>For concerns about abuse or maltreatment, anyone in Canada can call the Abuse-Free Sport Helpline. It is free and confidential.</p><a class="helpline__num" href="tel:18888377678">1-888-83SPORT<small>(77678)</small></a></section>'''
    return s1 + "\n" + s2 + "\n" + helpline

pages.append(({"depth": 1, "path": "for-parents/index.html", "active": "parents", "title": "For parents | Tumbleweeds Volleyball Club",
  "desc": "Straight answers for parents considering a new club: coaches, cost, travel, playing time, and who to call.",
  "hero": {"img": "tw-11-bump-wood-floor.jpg", "alt": "Player passing on a wood court", "pos": "40% 60%", "tag": "For parents",
           "h1": "Straight answers, <span class=\"accent\">including the hard ones.</span>",
           "lead": "We are a new club. Here is what you are probably wondering, answered plainly."},
  "band": {"img": "tw-12-sports-hall-wide.jpg", "h2": "Still have a <span class=\"accent\">question?</span>", "cta": ("Email the club", f"mailto:{EMAIL}"), "cta2": ("Info session", "../index.html#coming-up")}}, parents_body))

# ---------------- SPONSORS ----------------
def sponsors_body(u, r):
    cards = f'''<div class="cards">
      <article class="card card--sage reveal"><div class="card__body"><span class="card__num">01</span><h3 class="h4">On the jersey</h3><p>Your name on the uniform families see every weekend.</p><div class="card__foot">{soon("Placement coming soon")}</div></div></article>
      <article class="card card--sun reveal"><div class="card__body"><span class="card__num">02</span><h3 class="h4">On the website</h3><p>Your name and a link on the page parents check before they sign.</p><div class="card__foot">{soon("Placement coming soon")}</div></div></article>
      <article class="card card--sand reveal"><div class="card__body"><span class="card__num">03</span><h3 class="h4">In the gym</h3><p>Your banner where athletes and families are in the room.</p><div class="card__foot">{soon("Placement coming soon")}</div></div></article>
    </div>'''
    s1 = sheet("01", "Where you show up", "Your name, where families look.", cards)
    levels = f'''<div class="pricecard reveal" style="margin-bottom:0"><div><p class="eyebrow" style="margin-bottom:16px">Sponsor levels</p><h3 class="h3">What each level includes.</h3><p>Email the club and we will send the sponsor details when they are final. {soon("Levels coming soon")}</p></div><div class="chips"><span class="chip">Levels</span><span class="chip">Amounts</span><span class="chip">What each includes</span></div></div>'''
    s2 = f'<section class="sheet"><div class="wrap">{levels}</div></section>'
    who = facts([("Athletes and families", "Known after tryouts.", "", ""), ("Where we play", "Kamloops, BC. Practice location posted before tryouts.", "", "")])
    s3 = sheet("02", "Who you would back", "The families behind the logo.", who)
    return s1 + "\n" + s2 + "\n" + s3

pages.append(({"depth": 1, "path": "sponsors/index.html", "active": "sponsors", "title": "Sponsors | Tumbleweeds Volleyball Club",
  "desc": "Put your name behind Kamloops kids. Sponsor Tumbleweeds Volleyball Club.",
  "hero": {"img": "tw-12-sports-hall-wide.jpg", "alt": "Rally in an indoor sports hall", "pos": "50% 50%", "tag": "Sponsors",
           "h1": "Put your name behind <span class=\"accent\">Kamloops kids.</span>",
           "lead": "Tumbleweeds is a Kamloops club for Kamloops families. Sponsors put their name in front of those families.",
           "ctas": [("Become a sponsor", f"mailto:{EMAIL}", "btn--light")]},
  "band": {"img": "tw-10-wood-court-sunbeam.jpg", "h2": "Talk to <span class=\"accent\">us.</span>", "cta": ("Email the club", f"mailto:{EMAIL}"), "cta2": ("Meet the club", "../our-coaches/index.html")}}, sponsors_body))

# ---------------- NEWS ----------------
POSTS = [
 ("info-session", "Sep 30, 2026", "Info session for new families", "Come meet Pat Hennelly and Iuliia Pakhomenko, and ask anything about coaches, fees, and Safe Sport.", "tw-12-sports-hall-wide.jpg", "sage",
  "<p>Come meet Pat Hennelly and Iuliia Pakhomenko, and ask anything about coaches, fees, and Safe Sport.</p><p><strong>When:</strong> Sunday, October 4, 7:00 to 8:30 pm.<br><strong>Where:</strong> TRU Science Building, room S337. Free parking in S Lot.</p><p>Can't make it? A Teams link goes up on our Instagram story that day, <a class=\"link\" href=\"" + IG + "\">@tumbleweedsvball</a>.</p>"),
 ("what-we-will-publish-before-tryouts", "Oct 1, 2026", "What we will publish before tryouts", "A new club owes parents straight answers. Here is what we will post, and when.", "tw-13-ball-on-floor-detail.jpg", "sun",
  "<p>A new club owes parents straight answers. As the club confirms them, we will post:</p><p>Who coaches each team, with their background.<br>The full fee list, and what it includes.<br>Practice nights and location.<br>The refund policy.<br>Who to call if something goes wrong.</p><p>Each item goes on this site as soon as it is confirmed, and we will say so on Instagram.</p>"),
]
def news_body(u, r):
    cards = '<div class="cards cards--2">' + "".join(
        f'<a class="card card--{t} card--link reveal" href="{u("news/" + s + "/")}"><div class="card__img"><img src="{r}img/{img}" alt="" loading="lazy"></div><div class="card__body"><span class="card__meta">{d}</span><h3 class="h4">{ti}</h3><p>{ex}</p><div class="card__foot"><span class="link">Read more {ARR}</span></div></div></a>'
        for s, d, ti, ex, img, t, _ in POSTS) + '</div>'
    return sheet("01", "Latest", "From the club.", cards, f'<a class="link" href="{IG}">Follow on Instagram {ARR}</a>') + "\n" + cta_block("Want updates in your inbox?", "Email the club", f"mailto:{EMAIL}")
pages.append(({"depth": 1, "path": "news/index.html", "active": "news", "title": "News | Tumbleweeds Volleyball Club",
  "desc": "Club news, dates, and announcements from Tumbleweeds Volleyball Club in Kamloops.",
  "hero": {"img": "tw-11-bump-wood-floor.jpg", "alt": "Player passing on a wood court", "pos": "40% 60%", "tag": "News", "h1": "Club news, dates and <span class=\"accent\">announcements.</span>"},
  "band": {"img": "tw-04-gym-spike-wide.jpg", "h2": "See you at <span class=\"accent\">tryouts.</span>", "cta": ("Tryout details", "../tryouts/index.html"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, news_body))
for s, d, ti, ex, img, t, content in POSTS:
    def mk(s=s, d=d, ti=ti, content=content):
        def body(u, r):
            nxt = [p for p in POSTS if p[0] != s][0]
            return f'''<section class="sheet"><div class="article">
      <div class="article__meta reveal"><span class="data">{d}</span><p class="eyebrow"><b>01</b>News</p>{link(u("news/"), "All news")}</div>
      <div class="prose reveal">{content}</div></div></section>
<section class="sheet" style="padding-top:48px;padding-bottom:48px"><div class="wrap"><div class="pager reveal">
      <a href="{u("news/")}"><span><span class="data">News</span><strong>All news</strong></span>{ARR}</a>
      <a href="{u("news/" + nxt[0] + "/")}"><span><span class="data">Next</span><strong>{nxt[2]}</strong></span>{ARR}</a></div></div></section>'''
        return body
    pages.append(({"depth": 2, "path": f"news/{s}/index.html", "active": "news", "title": f"{ti} | Tumbleweeds Volleyball Club", "desc": ex,
      "hero": {"img": img, "alt": "", "pos": "50% 55%", "tag": f"News, {d}", "h1": ti},
      "band": {"img": "tw-10-wood-court-sunbeam.jpg", "h2": "Come meet us <span class=\"accent\">before tryouts.</span>", "cta": ("Info session details", "../../index.html#coming-up"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, mk()))

# ---------------- CONTACT ----------------
def contact_body(u, r):
    info = facts([
        ("Email", f'<a class="link" href="mailto:{EMAIL}">{EMAIL}</a>', "", ""),
        ("Instagram", f'<a class="link" href="{IG}">@tumbleweedsvball</a>', "", ""),
        ("Info session", "Sunday, October 4, 7:00 to 8:30 pm, TRU Science Building S337", "", ""),
        ("Practice location", "", "", "Coming soon"),
        ("Club complaints contact", "", "", "Coming soon"),
        ("Abuse-Free Sport Helpline", '<a class="link" href="tel:18888377678">1-888-83SPORT (77678)</a>', "", ""),
    ])
    # Visual only: no backend. Submit opens the visitor's email app with the message filled in.
    form = f'''<div class="panel reveal"><form class="form" onsubmit="var f=this;location.href='mailto:{EMAIL}?subject='+encodeURIComponent(f.topic.value+' (from '+f.name.value+')')+'&amp;body='+encodeURIComponent(f.message.value+'\\n\\n'+f.name.value+'\\n'+f.email.value);return false">
      <h3 class="h3" style="margin-bottom:8px">Send a message.</h3>
      <label>Your name<input name="name" type="text" autocomplete="name" required></label>
      <label>Your email<input name="email" type="email" autocomplete="email" required></label>
      <label>What is it about<select name="topic"><option>Coaches</option><option>Fees</option><option>Tryouts</option><option>Sponsoring</option><option>Something else</option></select></label>
      <label>Message<textarea name="message" required></textarea></label>
      <button class="btn btn--dark" type="submit">Send message</button>
      <p class="form__note">This opens your email app with the message ready to send to the club.</p>
    </form></div>'''
    s1 = f'''<section class="sheet"><div class="wrap split">
      <div><div class="reveal"><p class="eyebrow"><b>01</b>Reach the club</p><h2 class="h2">How to find us.</h2><p class="lead" style="margin:20px 0 32px">Questions about coaches, fees, tryouts or sponsoring? Email us and we will point you to the right person.</p></div>{info}</div>
      {form}</div></section>'''
    return s1
pages.append(({"depth": 1, "path": "contact/index.html", "active": "contact", "title": "Contact | Tumbleweeds Volleyball Club",
  "desc": "Contact Tumbleweeds Volleyball Club in Kamloops about coaches, fees, tryouts or sponsoring.",
  "hero": {"img": "tw-14-net-texture-detail.jpg", "alt": "Volleyball net close up", "pos": "50% 50%", "tag": "Contact", "h1": "Questions? <span class=\"accent\">Ask us.</span>",
           "lead": "Coaches, fees, tryouts or sponsoring. Email us."},
  "band": {"img": "tw-12-sports-hall-wide.jpg", "h2": "See you at <span class=\"accent\">tryouts.</span>", "cta": ("Tryout details", "../tryouts/index.html"), "cta2": ("Email the club", f"mailto:{EMAIL}")}}, contact_body))

for p, b in pages:
    render(p, b)
print("built", len(pages) + 1, "pages")
