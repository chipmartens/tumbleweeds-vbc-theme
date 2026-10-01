#!/usr/bin/env python3
"""Generates acf-json/*.json (local JSON for ACF Pro or Secure Custom Fields).
Edit the field set HERE and rerun; do not hand-edit the generated files.
Labels are written for a club volunteer: plain words, one line of instruction, choice first, conditional boxes."""
import json, pathlib, time
OUT = pathlib.Path(__file__).resolve().parent.parent / "acf-json"
OUT.mkdir(exist_ok=True)
MOD = int(time.time())


def field(prefix, type_, name, label, instr="", show_if=None, siblings=None, **kw):
    key = f"field_tvbc_{prefix}_{name}"
    f = {"key": key, "label": label, "name": name, "aria-label": "", "type": type_,
         "instructions": instr, "required": 0, "conditional_logic": 0, "wrapper": {"width": "", "class": "", "id": ""}}
    if show_if:
        sib, val = show_if
        f["conditional_logic"] = [[{"field": f"field_tvbc_{prefix}_{sib}", "operator": "==", "value": val}]]
    f.update(kw)
    return f


def mk(prefix):
    def _f(type_, name, label, instr="", **kw):
        return field(prefix, type_, name, label, instr, **kw)
    return _f


def group(key, title, fields, location, menu_order=0, hide=None, position="normal"):
    return {"key": key, "title": title, "fields": fields, "location": location, "menu_order": menu_order,
            "position": position, "style": "default", "label_placement": "top", "instruction_placement": "label",
            "hide_on_screen": hide or [], "active": True, "description": "", "show_in_rest": 0, "modified": MOD}


def write(g):
    (OUT / f"{g['key']}.json").write_text(json.dumps(g, indent=4, ensure_ascii=False) + "\n")


BG = lambda f: f("select", "bg", "Background", "Pick a colour band for this section.",
                 choices={"light": "Light", "sand": "Sand panel", "dark": "Dark green"}, default_value="light", return_format="value")
EYEBROW = lambda f: f("text", "eyebrow", "Small label above the heading", "Optional. A few words, like \"Fees\".")
HEADING = lambda f: f("text", "heading", "Heading", "One plain sentence that says what the reader gets.")
INTRO = lambda f: f("textarea", "intro", "Text under the heading", "Optional. One or two short sentences.", rows=3, new_lines="")
LINK = lambda f, name="link", label="Link": f("link", name, label, "Pick a page or paste a web address.", return_format="array")


def build_page_group():
    p = "page"
    f = mk(p)
    hero_btns = mk("page_btn")
    hero = [
        f("tab", "tab_hero", "Top of page", placement="top"),
        f("radio", "hero_style", "Top of page style", "Pick the look first. Home is the dark green one with a photo.",
          choices={"page": "Page (light, text only)", "home": "Home (dark green with a photo)"}, default_value="page", layout="vertical", return_format="value"),
        f("text", "hero_eyebrow", "Small label above the heading", "A few words, like \"Kamloops youth volleyball\"."),
        f("text", "hero_heading", "Heading", "Keep it to the plain thing the page is about. Under 8 words is best."),
        f("textarea", "hero_text", "Intro text", "One or two short sentences.", rows=3, new_lines=""),
        f("repeater", "hero_buttons", "Buttons", "Up to two. The first one is the main button.", min=0, max=2, layout="table", button_label="Add button",
          sub_fields=[
              hero_btns("text", "label", "Button text", "Two to four words."),
              hero_btns("link", "link", "Where it goes", "", return_format="array"),
          ]),
        f("text", "hero_note", "Small note under the buttons", "Optional. For example a date and place."),
        f("image", "hero_photo", "Photo", "A cut-out (clear background) head and shoulders photo works best. Add a description in the Media Library.",
          show_if=("hero_style", "home"), return_format="id", preview_size="medium", library="all"),
        f("tab", "tab_sections", "Page sections", placement="top"),
    ]

    layouts = {}

    def lay(name, label, subs):
        subs = [x for x in subs if x["name"] != "anchor"]
        subs.insert(0, field(f"l_{name}", "text", "anchor", "Link name", "Optional. Lowercase, no spaces, so a link can jump to this section (example: fees)."))
        layouts[f"layout_tvbc_{name}"] = {"key": f"layout_tvbc_{name}", "name": name, "label": label, "display": "block", "sub_fields": subs, "min": "", "max": ""}

    g = mk("l_intro")
    lay("intro", "Heading and text", [BG(g), EYEBROW(g), HEADING(g), g("textarea", "text", "Text", "Short paragraphs. Press Enter for a new paragraph.", rows=6, new_lines=""),
                                       g("text", "button_label", "Button text", "Optional."), LINK(g, "button_link", "Button goes to")])
    g = mk("l_feature")
    lay("feature", "Text and photo", [BG(g), EYEBROW(g), HEADING(g), g("textarea", "text", "Text", "", rows=5, new_lines=""),
                                       g("repeater", "bullets", "List", "Optional. One line each.", layout="table", button_label="Add line",
                                         sub_fields=[mk("l_feature_b")("text", "line", "Line")]),
                                       g("image", "photo", "Photo", "", return_format="id", preview_size="medium"),
                                       g("radio", "photo_side", "Photo goes on the", "", choices={"right": "Right", "left": "Left"}, default_value="right", layout="horizontal", return_format="value"),
                                       g("text", "button_label", "Button text", "Optional."), LINK(g, "button_link", "Button goes to")])
    g = mk("l_numbered")
    lay("numbered_list", "Numbered list", [BG(g), EYEBROW(g), HEADING(g), INTRO(g),
                                           g("repeater", "items", "Items", "The numbers appear on their own.", layout="block", button_label="Add item",
                                             sub_fields=[mk("l_numbered_i")("text", "title", "Title"), mk("l_numbered_i")("textarea", "text", "Text", "", rows=3, new_lines=""),
                                                         mk("l_numbered_i")("text", "link_label", "Link text", "Optional."), LINK(mk("l_numbered_i"), "link", "Link goes to")])])
    g = mk("l_cards")
    lay("cards", "Cards", [BG(g), EYEBROW(g), HEADING(g), INTRO(g),
                           g("select", "columns", "Cards per row", "On phones they stack.", choices={"2": "2", "3": "3", "4": "4"}, default_value="3", return_format="value"),
                           g("repeater", "items", "Cards", "", layout="block", button_label="Add card",
                             sub_fields=[mk("l_cards_i")("text", "label", "Small label", "Optional. For example \"12U\"."),
                                         mk("l_cards_i")("text", "title", "Title"),
                                         mk("l_cards_i")("textarea", "text", "Text", "", rows=3, new_lines=""),
                                         mk("l_cards_i")("text", "flag", "Warning tag", "Optional. Use \"Not confirmed yet\" when the details are still open."),
                                         mk("l_cards_i")("text", "link_label", "Link text", "Optional."), LINK(mk("l_cards_i"), "link", "Link goes to")])])
    g = mk("l_people")
    lay("people", "Coaches and staff", [BG(g), EYEBROW(g), HEADING(g), INTRO(g),
                                        g("radio", "source", "Who to show", "Choose first.", choices={"all": "Everyone, in the order set under Coaches", "pick": "Pick people"}, default_value="all", layout="vertical", return_format="value"),
                                        g("relationship", "pick", "People", "Add them in the order you want them shown.", show_if=("source", "pick"), post_type=["coach"], filters=["search"], return_format="id", min="", max="")])
    g = mk("l_facts")
    lay("fact_table", "Facts table", [BG(g), EYEBROW(g), HEADING(g), INTRO(g),
                                     g("repeater", "rows", "Rows", "Type [Fee: $TBC] style placeholders in square brackets where a detail is not confirmed. They show up highlighted.", layout="block", button_label="Add row",
                                       sub_fields=[mk("l_facts_r")("text", "label", "Question or label"), mk("l_facts_r")("textarea", "value", "Answer", "", rows=3, new_lines=""),
                                                   mk("l_facts_r")("text", "note", "Small note", "Optional.")])])
    g = mk("l_dates")
    lay("key_dates", "Dates", [BG(g), EYEBROW(g), HEADING(g), INTRO(g),
                               g("repeater", "rows", "Dates", "", layout="block", button_label="Add date",
                                 sub_fields=[mk("l_dates_r")("text", "date", "Date", "For example \"Sun, Oct 4\" or [Date TBC]."), mk("l_dates_r")("text", "title", "What happens"),
                                             mk("l_dates_r")("textarea", "text", "Details", "", rows=2, new_lines="")])])
    g = mk("l_faq")
    lay("faq", "Questions and answers", [BG(g), EYEBROW(g), HEADING(g), INTRO(g),
                                         g("true_false", "collapse", "Hide the answers until a question is clicked", "Leave off so parents can scan every answer.", ui=1, default_value=0),
                                         g("repeater", "items", "Questions", "", layout="block", button_label="Add question",
                                           sub_fields=[mk("l_faq_i")("text", "question", "Question"), mk("l_faq_i")("textarea", "answer", "Answer", "", rows=4, new_lines="")])])
    g = mk("l_news")
    lay("news_list", "Latest news", [BG(g), EYEBROW(g), HEADING(g), g("number", "count", "How many posts", "", default_value=6, min=1, max=20)])
    g = mk("l_callout")
    lay("callout", "Call to action", [g("select", "style", "Style", "", choices={"dark": "Dark green band", "sand": "Sand band", "helpline": "Helpline box"}, default_value="dark", return_format="value"),
                                     EYEBROW(g), HEADING(g), g("textarea", "text", "Text", "", rows=3, new_lines=""),
                                     g("text", "button_label", "Button text", "Optional."), LINK(g, "button_link", "Button goes to"),
                                     g("text", "detail", "Big line", "Optional. For example a phone number.", show_if=("style", "helpline"))])

    flex = f("flexible_content", "flex_content", "Page sections", "Add sections, drag to reorder. Each one is a ready-made block.", layouts=layouts, button_label="Add section", min="", max="")
    return group("group_tvbc_page", "Page", hero + [flex], [[{"param": "post_type", "operator": "==", "value": "page"}]], hide=["the_content"])


def build_coach_group():
    f = mk("coach")
    fields = [
        f("text", "role", "Role at the club", "For example \"President\" or \"Head coach, 14U girls\"."),
        f("text", "teams", "Teams", "Optional. Age groups this person coaches."),
        f("image", "photo", "Photo", "A cut-out (clear background) head and shoulders photo works best.", return_format="id", preview_size="medium"),
        f("textarea", "summary", "Short summary", "Two sentences for the card on the Coaches page.", rows=3, new_lines=""),
        f("wysiwyg", "bio", "Full bio", "Shown on this coach's own page. Leave empty for a card with no link.", tabs="visual", toolbar="basic", media_upload=0),
        f("repeater", "credentials", "Facts about this coach", "One line each. Only things the club has confirmed.", layout="table", button_label="Add line",
          sub_fields=[mk("coach_c")("text", "line", "Line")]),
    ]
    return group("group_tvbc_coach", "Coach details", fields, [[{"param": "post_type", "operator": "==", "value": "coach"}]], hide=["the_content", "excerpt"])


def build_team_group():
    f = mk("team")
    fields = [
        f("select", "age_group", "Age group", "", choices={x: x for x in ["12U", "13U", "14U", "15U", "16U", "17U", "18U"]}, return_format="value"),
        f("select", "gender", "Girls or boys", "", choices={"girls": "Girls", "boys": "Boys", "tbc": "Not confirmed yet"}, default_value="tbc", return_format="value"),
        f("post_object", "head_coach", "Head coach", "", post_type=["coach"], return_format="id", allow_null=1),
        f("text", "practice", "Practice nights and place", "For example Tuesday and Thursday evenings, plus the gym."),
        f("repeater", "roster", "Roster", "Sample names only until families agree to be listed.", layout="table", button_label="Add athlete",
          sub_fields=[mk("team_r")("text", "name", "Name"), mk("team_r")("text", "number", "Jersey number")]),
    ]
    return group("group_tvbc_team", "Team details", fields, [[{"param": "post_type", "operator": "==", "value": "team"}]], hide=["the_content"])


def build_settings_group():
    f = mk("set")
    fields = [
        f("text", "contact_email", "Club email", "", default_value="info@tumbleweedsvolleyball.com"),
        f("text", "instagram_handle", "Instagram handle", "", default_value="@tumbleweedsvball"),
        f("url", "instagram_url", "Instagram link", "", default_value="https://www.instagram.com/tumbleweedsvball/"),
        f("text", "header_cta_label", "Header button text", "", default_value="Tryouts"),
        f("link", "header_cta_link", "Header button goes to", "", return_format="array"),
        f("textarea", "footer_blurb", "Footer line", "One or two sentences about the club.", rows=3, new_lines=""),
        f("text", "helpline_name", "Helpline name", "", default_value="Abuse-Free Sport Helpline"),
        f("text", "helpline_phone", "Helpline phone", "", default_value="1-888-83SPORT (77678)"),
        f("text", "complaints_contact", "Club complaints contact", "Someone outside the coaching staff. Keep the brackets until it is confirmed.", default_value="[Complaints contact TBC]"),
        f("text", "practice_location", "Practice location", "Keep the brackets until it is confirmed.", default_value="[Practice location TBC]"),
    ]
    loc = [[{"param": "options_page", "operator": "==", "value": "club-settings"}],
           [{"param": "page_type", "operator": "==", "value": "front_page"}]]
    return group("group_tvbc_settings", "Club settings", fields, loc)


for g in (build_page_group(), build_coach_group(), build_team_group(), build_settings_group()):
    write(g)
print("wrote", [p.name for p in sorted(OUT.glob("*.json"))])
