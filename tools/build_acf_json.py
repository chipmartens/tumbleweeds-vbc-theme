#!/usr/bin/env python3
"""Generates acf-json/*.json (ACF local JSON, loads in ACF Pro and Secure Custom Fields).
Edit the field set HERE and rerun (python3 tools/build_acf_json.py); do not hand-edit the generated files.

Editor-proof rules (Chip, 2026-09-23): choice first (Kind / Style), then conditional boxes that only show
what that choice uses, plain labels, one line of instruction on every field, no mini-syntax in text boxes.
Names follow the Chez Koop vocabulary: flex_content, section_<noun>, section_eyebrow, section_heading,
section_text, section_cta, section_image, section_bg_color."""
import json, pathlib, time

OUT = pathlib.Path(__file__).resolve().parent.parent / "acf-json"
OUT.mkdir(exist_ok=True)
for old in OUT.glob("*.json"):
    old.unlink()
MOD = 1790000000  # fixed, so reruns do not churn the files

WRAP = {"width": "", "class": "", "id": ""}


def F(prefix, type_, name, label, instr="", show_if=None, width="", **kw):
    """One field. show_if = (sibling_name, operator, value) or a list of such tuples (all must match)."""
    f = {"key": f"field_tvbc_{prefix}_{name}", "label": label, "name": name, "aria-label": "", "type": type_,
         "instructions": instr, "required": 0, "conditional_logic": 0, "wrapper": {**WRAP, "width": width}}
    if show_if:
        conds = show_if if isinstance(show_if, list) else [show_if]
        f["conditional_logic"] = [[{"field": f"field_tvbc_{prefix}_{c[0]}", "operator": c[1], "value": c[2]} for c in conds]]
    f.update(kw)
    return f


def maker(prefix):
    return lambda type_, name, label, instr="", **kw: F(prefix, type_, name, label, instr, **kw)


def text(f, name, label, instr="", **kw):
    return f("text", name, label, instr, default_value=kw.pop("default_value", ""), maxlength="", placeholder=kw.pop("placeholder", ""), prepend="", append="", **kw)


def area(f, name, label, instr="", rows=3, **kw):
    return f("textarea", name, label, instr, default_value="", maxlength="", rows=rows, placeholder="", new_lines="", **kw)


def toggle(f, name, label, instr="", default=0, on="Yes", off="No", **kw):
    return f("true_false", name, label, instr, message="", default_value=default, ui=1, ui_on_text=on, ui_off_text=off, **kw)


def select(f, name, label, instr, choices, default="", **kw):
    return f("select", name, label, instr, choices=choices, default_value=default, return_format="value", multiple=0, allow_null=0, ui=0, ajax=0, placeholder="", **kw)


def image(f, name, label, instr="", **kw):
    return f("image", name, label, instr, return_format="array", library="all", min_width="", min_height="", min_size="", max_width="", max_height="", max_size="", mime_types="", preview_size="medium", **kw)


def link(f, name, label, instr="", **kw):
    return f("link", name, label, instr, return_format="array", **kw)


def wysiwyg(f, name, label, instr="", **kw):
    return f("wysiwyg", name, label, instr, default_value="", tabs="visual", toolbar="minimal", media_upload=0, delay=0, **kw)


def rng(f, name, label, instr, **kw):
    return f("range", name, label, instr, default_value=50, min=0, max=100, step=1, prepend="", append="%", **kw)


def repeater(f, name, label, instr, subs, button="Add row", layout="block", mn=0, mx=0, collapsed=None, **kw):
    # collapsed = name of the sub field whose value labels a closed row (rows then start closed, so long lists stay short)
    key = ""
    if collapsed:
        key = next(x["key"] for x in subs if x["name"] == collapsed)
    return f("repeater", name, label, instr, sub_fields=subs, layout=layout, pagination=0, min=mn, max=mx, collapsed=key, button_label=button, rows_per_page=20, **kw)


def message(f, name, label, text_, **kw):
    return f("message", name, label, "", message=text_, new_lines="wpautop", esc_html=0, **kw)


def tab(f, name, label, **kw):
    return f("tab", name, label, "", placement="top", endpoint=0, **kw)


def group(key, title, fields, location, menu_order=0, hide=None, position="normal", description=""):
    return {"key": key, "title": title, "fields": fields, "location": location, "menu_order": menu_order,
            "position": position, "style": "default", "label_placement": "top", "instruction_placement": "label",
            "hide_on_screen": hide or [], "active": True, "description": description, "show_in_rest": 0, "modified": MOD}


def write(g):
    (OUT / f"{g['key']}.json").write_text(json.dumps(g, indent=4, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- shared pieces
def fact_fields(f):
    return [
        text(f, "fact_label", "Label", "The short name on the left, for example Season."),
        area(f, "fact_value", "Answer", "The answer. Web and email addresses turn into links by themselves. Leave empty if it is not decided yet.", rows=3),
        link(f, "fact_link", "Answer as a link (optional)", "Use this instead of Answer when the answer is a link, for example an email address. Pick the page or paste an address, then write the words people click."),
        text(f, "fact_note", "Small line under the answer", "Optional."),
        text(f, "fact_tag", "Status tag", "Optional. For an answer that is not ready, write Coming soon. Leave empty when the answer is filled in."),
    ]


def focus_fields(f, show_if=None):
    return [
        rng(f, "focus_x", "Keep this part in view: left to right", "Slide to choose which part of the photo stays visible when it is cropped. 0 is the left edge, 100 the right.", width="50", show_if=show_if),
        rng(f, "focus_y", "Keep this part in view: top to bottom", "0 is the top edge, 100 the bottom.", width="50", show_if=show_if),
    ]


def head(f, side=True, lede=False, number=True, bg=True, anchor=True):
    out = []
    if anchor:
        out.append(text(f, "section_anchor", "Link name (optional)", "One lowercase word that links can point to. For example coming-up makes the link #coming-up. Leave empty if nothing links here."))
    out.append(text(f, "section_eyebrow", "Small label above the heading", "A few words, for example Fees. Optional."))
    if number:
        out.append(toggle(f, "show_number", "Number this section", "Puts the next number (01, 02, 03) in front of the small label.", default=1))
    out.append(text(f, "section_heading", "Heading", "The big line of the section."))
    out.append(text(f, "section_heading_accent", "Last words in italic (optional)", "Shown in the club's italic style at the end of the heading. Example: heading is Fundamentals, italic words are first. Leave empty for none."))
    if lede:
        out.append(area(f, "section_lede", "Short text under the heading", "One or two sentences. Optional.", rows=3))
    if side:
        out.append(select(f, "section_side", "Something to the right of the heading", "Pick what sits on the right on a wide screen.", {"none": "Nothing", "text": "A short line of text", "link": "A link"}, default="none"))
        out.append(text(f, "section_side_text", "Text on the right", "One short line.", show_if=("section_side", "==", "text")))
        out.append(link(f, "section_side_link", "Link on the right", "Pick the page or paste a web address, then write the words people click.", show_if=("section_side", "==", "link")))
    if bg:
        out.append(select(f, "section_bg_color", "Background colour", "White paper is the normal look. Pick a colour only when you want this section to stand out.", {"": "White paper", "sage": "Sage green", "sun": "Sun yellow", "sand": "Sand"}, default=""))
    return out


# ---------------------------------------------------------------- Page Content (flexible content)
def layouts():
    L = []

    def layout(name, label, fn, display="block"):
        f = maker(name)
        L.append((name, {"key": f"layout_tvbc_{name}", "name": name, "label": label, "display": display, "sub_fields": fn(f), "min": "", "max": ""}))

    layout("section_ticker", "Scrolling words strip", lambda f: [
        message(f, "ticker_note", "Where the words come from", "The words that scroll across come from <strong>Club settings</strong>, tab <em>Scrolling strip</em>. Change them there and every page updates.")])

    def cards(f):
        return head(f, side=True) + [
            toggle(f, "show_card_numbers", "Number the cards", "Puts 01, 02, 03 on each card.", default=1),
            toggle(f, "cards_dates", "Show a row of dates above the heading", "A short row of up to three dates, like the one on the home page."),
            repeater(f, "dates", "Dates", "Each box in the row.", [
                select(f, "date_kind", "Kind", "Pick what this date is.", {"info_session": "The info session (comes from Club settings)", "custom": "Something else"}, default="custom"),
                text(f, "date_label", "Date or time", "For example Late November.", show_if=("date_kind", "==", "custom")),
                text(f, "date_title", "Title", "For example Tryouts.", show_if=("date_kind", "==", "custom")),
                text(f, "date_line", "One line of detail", "For example In the Volleyball BC tryout window.", show_if=("date_kind", "==", "custom")),
                link(f, "date_link", "Where it links", "Optional. The page this box opens."),
            ], "Add a date", mn=0, mx=3, collapsed="date_title", show_if=("cards_dates", "==", "1")),
            repeater(f, "cards", "Cards", "Two, three or five cards look best. Drag the row handle to reorder.", [
                select(f, "card_colour", "Card colour", "The colour of the card.", {"sage": "Sage green", "sun": "Sun yellow", "sand": "Sand"}, default="sage"),
                image(f, "card_image", "Photo", "Optional. Leave empty for a card without a photo."),
                text(f, "card_title", "Title", "The card heading."),
                area(f, "card_text", "Text", "One or two sentences.", rows=3),
                select(f, "card_foot", "Bottom of the card", "What goes at the bottom.", {"none": "Nothing", "tag": "A status tag (for example Coming soon)", "link": "A link", "button": "A button"}, default="none"),
                text(f, "card_foot_tag", "Status tag", "For example Coming soon.", show_if=("card_foot", "==", "tag")),
                link(f, "card_foot_link", "Link", "Pick the page or paste a web address, then write the words people click.", show_if=("card_foot", "any", None)),
            ], "Add a card", mn=0, mx=5, collapsed="card_title"),
        ]
    layout("section_cards", "Cards", cards)

    layout("section_strip", "Photo strip (4 photos)", lambda f: [
        repeater(f, "strip_photos", "Photos", "Exactly four photos. They sit in a row on a wide screen and scroll sideways on a phone.", [
            image(f, "strip_image", "Photo", "Describe the photo in its Alt text box in the Media Library so everyone can follow it."),
        ] + focus_fields(f), "Add a photo", layout="row", mn=4, mx=4)])

    layout("section_people", "People (coaches)", lambda f: head(f, side=True) + [
        f("relationship", "people_coaches", "Who to show", "Leave empty to show every coach. Or pick coaches here to choose who shows and in what order. Add or edit coaches under Coaches in the left menu.",
          post_type=["coach"], taxonomy="", filters=["search"], return_format="id", min="", max="", elements="", bidirectional=0)])

    layout("section_statement", "Big statement", lambda f: [
        text(f, "section_heading", "Statement", "One short line, big on a dark panel. Example: Fundamentals"),
        text(f, "section_heading_accent", "Last words in italic", "Shown in the italic style in yellow. Example: first.")])

    def events(f):
        return head(f, side=True) + [
            repeater(f, "events", "Dates and events", "One row for each thing that is coming up.", [
                select(f, "event_kind", "Kind", "Pick what this row is.", {"info_session": "The info session (comes from Club settings)", "other": "Something else"}, default="other"),
                text(f, "event_date", "Date or time", "For example Late Nov.", show_if=("event_kind", "==", "other")),
                text(f, "event_title", "Title", "For example Tryouts.", show_if=("event_kind", "==", "other")),
                area(f, "event_text", "Details", "One or two sentences.", rows=3, show_if=("event_kind", "==", "other")),
                select(f, "event_side", "Right-hand side of the row", "What sits at the right end.", {"none": "Nothing", "tag": "A status tag (for example Coming soon)", "button": "A button"}, default="none"),
                text(f, "event_side_tag", "Status tag", "For example Coming soon.", show_if=("event_side", "==", "tag")),
                link(f, "event_side_link", "Button", "Pick the page or paste a web address, then write the words on the button.", show_if=("event_side", "==", "button")),
            ], "Add a row", collapsed="event_title")]
    layout("section_events", "Dates and events list", events)

    def faq(f):
        return head(f, side=False, lede=True) + [
            toggle(f, "faq_numbered", "Number the questions", "Puts 01, 02, 03 in front of each question."),
            toggle(f, "faq_open_first", "Open the first answer", "The first answer starts open.", default=1),
            repeater(f, "faq_items", "Questions", "One row for each question.", [
                text(f, "faq_question", "Question", "Write it the way a parent would ask it."),
                text(f, "faq_anchor", "Link name (optional)", "One lowercase word that links can point to, for example training. Then #training opens this answer."),
                select(f, "answer_kind", "Kind of answer", "Pick how the answer looks.", {"text": "Written answer", "facts": "A list of facts (label and answer rows)"}, default="text"),
                wysiwyg(f, "answer_text", "Answer", "Write the answer. Use the link button to link to a page.", show_if=("answer_kind", "==", "text")),
                repeater(f, "answer_facts", "Facts", "One row for each fact.", fact_fields(f), "Add a fact", collapsed="fact_label", show_if=("answer_kind", "==", "facts")),
            ], "Add a question", collapsed="faq_question")]
    layout("section_faq", "Questions and answers", faq)

    def cta(f):
        return [
            select(f, "cta_style", "Style", "Pick how it looks.", {"banner": "Yellow banner (one line and a button)", "highlight": "Tinted section (heading, text and a button)"}, default="banner"),
            text(f, "section_anchor", "Link name (optional)", "One lowercase word that links can point to. For example registration makes the link #registration."),
            text(f, "section_eyebrow", "Small label", "A few words, for example Talk to us."),
            toggle(f, "show_number", "Number this section", "Puts the next number (01, 02, 03) in front of the small label.", default=0, show_if=("cta_style", "==", "highlight")),
            text(f, "section_heading", "Heading", "One line."),
            area(f, "section_lede", "Text under the heading", "One or two sentences.", rows=3, show_if=("cta_style", "==", "highlight")),
            text(f, "cta_tag", "Status tag", "Optional. For example Coming soon.", show_if=("cta_style", "==", "highlight")),
            link(f, "section_cta", "Button", "Pick the page or paste a web address, then write the words on the button."),
        ]
    layout("section_cta", "Call to action", cta)

    def facts(f):
        lay = select(f, "facts_layout", "Layout", "Pick where the heading goes.", {"above": "Heading above the list", "left": "Heading on the left, list on the right"}, default="above")
        h_above = head(f, side=True, lede=False)
        h_left = head(f, side=False, lede=True)
        # fields that only exist in one layout get a condition; shared ones are shown for both
        shared = {"section_anchor", "section_eyebrow", "show_number", "section_heading", "section_heading_accent", "section_bg_color"}
        out = [lay]
        for fld in h_above:
            if fld["name"] not in shared:
                fld["conditional_logic"] = [[{"field": "field_tvbc_section_facts_facts_layout", "operator": "==", "value": "above"}]]
            out.append(fld)
        for fld in h_left:
            if fld["name"] not in shared:
                out.append(fld)
                fld["conditional_logic"] = [[{"field": "field_tvbc_section_facts_facts_layout", "operator": "==", "value": "left"}]]
        out += [
            toggle(f, "facts_box", "Add a highlight box above the list", "A yellow box with a heading, a sentence and a few small labels.", show_if=("facts_layout", "==", "above")),
            text(f, "box_eyebrow", "Box: small label", "For example Season total.", show_if=[("facts_layout", "==", "above"), ("facts_box", "==", "1")]),
            text(f, "box_heading", "Box: heading", "One line.", show_if=[("facts_layout", "==", "above"), ("facts_box", "==", "1")]),
            area(f, "box_text", "Box: text", "One or two sentences.", rows=3, show_if=[("facts_layout", "==", "above"), ("facts_box", "==", "1")]),
            text(f, "box_tag", "Box: status tag", "Optional. For example Posting before tryouts.", show_if=[("facts_layout", "==", "above"), ("facts_box", "==", "1")]),
            repeater(f, "box_chips", "Box: small labels", "Short labels that sit in the box.", [text(f, "chip_text", "Label", "A word or two.")], "Add a label", layout="table", show_if=[("facts_layout", "==", "above"), ("facts_box", "==", "1")]),
            repeater(f, "facts_rows", "Facts", "One row for each fact. Drag the row handle to reorder.", fact_fields(f), "Add a fact", collapsed="fact_label"),
        ]
        return out
    layout("section_facts", "Facts list", facts)

    layout("section_ages", "Age groups", lambda f: head(f, side=True) + [
        repeater(f, "ages", "Age groups", "One box for each age group.", [
            text(f, "age_label", "Age group", "For example 12U."),
            text(f, "age_caption", "Small caption", "For example Volleyball BC."),
        ], "Add an age group", layout="table"),
        text(f, "ages_note", "Line under the boxes", "Optional. One sentence."),
        text(f, "ages_note_tag", "Status tag", "Optional. For example Posting before tryouts.")])

    layout("section_helpline", "Helpline panel", lambda f: [
        text(f, "section_anchor", "Link name (optional)", "One lowercase word that links can point to."),
        text(f, "section_eyebrow", "Small label", "For example Safe Sport."),
        toggle(f, "show_number", "Number this section", "Puts the next number (01, 02, 03) in front of the small label.", default=1),
        text(f, "section_heading", "Heading", "One line."),
        area(f, "section_lede", "Text", "One or two sentences.", rows=3),
        message(f, "helpline_note", "Where the number comes from", "The big phone number comes from <strong>Club settings</strong>, tab <em>Helpline</em>. Change it there and it changes here and in the footer.")])

    def contact(f):
        return head(f, side=False, lede=True) + [
            repeater(f, "contact_rows", "Contact details", "One row for each detail. Email and web addresses turn into links by themselves.", fact_fields(f), "Add a detail", collapsed="fact_label"),
            text(f, "form_heading", "Form heading", "For example Send a message."),
            repeater(f, "form_topics", "What the message can be about", "The choices in the drop-down list.", [text(f, "topic_text", "Topic", "For example Coaches.")], "Add a topic", layout="table"),
            text(f, "form_note", "Small line under the button", "Optional. For example: This opens your email app with the message ready to send."),
        ]
    layout("section_contact", "Contact details and form", contact)

    layout("section_news", "Latest news", lambda f: head(f, side=True) + [
        f("number", "news_count", "How many posts to show", "Newest first. Posts are written under Posts in the left menu.", default_value=12, min=1, max=50, step=1, placeholder="", prepend="", append="")])

    layout("section_band", "Closing photo banner", lambda f: [
        select(f, "band_size", "Size", "Standard suits every page. Tall is the roomier banner used on the home page.", {"standard": "Standard", "tall": "Tall"}, default="standard"),
        image(f, "band_image", "Photo", "A wide photo. A dark tint is added so the words can be read."),
        text(f, "band_heading", "Heading", "One short line. Example: See you at"),
        text(f, "band_heading_accent", "Last words in italic", "Shown in the italic style. Example: tryouts."),
        link(f, "band_button_1", "Main button (yellow)", "Pick the page or paste a web address, then write the words on the button."),
        link(f, "band_button_2", "Second button (outline)", "Optional.")])

    return L


def flex_group():
    ls = layouts()
    # the "any" operator above is a stand-in: show the card link box for both link and button
    for _, lay in ls:
        for fld in lay["sub_fields"]:
            if fld["name"] == "cards":
                for sub in fld["sub_fields"]:
                    if sub["name"] == "card_foot_link":
                        sub["conditional_logic"] = [
                            [{"field": "field_tvbc_section_cards_card_foot", "operator": "==", "value": "link"}],
                            [{"field": "field_tvbc_section_cards_card_foot", "operator": "==", "value": "button"}]]
    flex = {"key": "field_tvbc_page_flex_content", "label": "Page sections", "name": "flex_content", "aria-label": "", "type": "flexible_content",
            "instructions": "The page is built from sections, top to bottom. Add a section, fill in its boxes, and drag the handle to change the order.",
            "required": 0, "conditional_logic": 0, "wrapper": dict(WRAP),
            "layouts": {f"layout_tvbc_{n}": lay for n, lay in ls}, "min": "", "max": "", "button_label": "Add a section"}
    return group("group_tvbc_page", "Page Content", [flex], [[{"param": "post_type", "operator": "==", "value": "page"}]], menu_order=10)


# ---------------------------------------------------------------- Hero Content (page)
def hero_group():
    f = maker("hero")
    cond = ("hero_layout", "!=", "none")
    fields = [
        select(f, "hero_layout", "Top of the page", "Pick the look of the big photo at the top.", {"page": "Page hero (photo with the page title)", "home": "Home hero (larger, with the round badge)", "none": "No hero"}, default="page"),
        image(f, "hero_image", "Hero photo", "A wide photo. A dark tint is added so the words can be read.", show_if=cond),
        rng(f, "hero_focus_x", "Keep this part in view: left to right", "Slide to choose which part of the photo stays visible when it is cropped. 0 is the left edge, 100 the right.", width="50", show_if=cond),
        rng(f, "hero_focus_y", "Keep this part in view: top to bottom", "0 is the top edge, 100 the bottom.", width="50", show_if=cond),
        toggle(f, "hero_phone_focus", "Frame the photo differently on a phone", "A phone shows a tall slice of the photo. Switch this on to choose which part stays in view there.", show_if=cond),
        rng(f, "hero_phone_x", "On a phone: left to right", "0 is the left edge, 100 the right.", width="50", show_if=[("hero_layout", "!=", "none"), ("hero_phone_focus", "==", "1")]),
        rng(f, "hero_phone_y", "On a phone: top to bottom", "0 is the top edge, 100 the bottom.", width="50", show_if=[("hero_layout", "!=", "none"), ("hero_phone_focus", "==", "1")]),
        text(f, "hero_tag", "Small label in the pill", "A few words above the heading, for example Tryouts, late November.", show_if=cond),
        text(f, "hero_heading", "Heading", "The big line. Leave empty to use the page title.", show_if=cond),
        text(f, "hero_heading_accent", "Last words in italic (optional)", "Shown in the club's italic style at the end of the heading. Example: heading is Programs by, italic words are age group.", show_if=cond),
        area(f, "hero_subhead", "Short text under the heading", "One or two sentences. Optional.", rows=3, show_if=cond),
        link(f, "hero_button_1", "Main button (white)", "Optional. Pick the page or paste a web address, then write the words on the button.", show_if=cond),
        link(f, "hero_button_2", "Second button (outline)", "Optional.", show_if=cond),
    ]
    # Pages are built from the fields, so the empty text editor and other unused boxes are hidden from volunteers
    hide = ["the_content", "excerpt", "discussion", "comments", "revisions", "author", "featured_image", "send-trackbacks", "custom_fields"]
    return group("group_tvbc_hero", "Hero Content", fields, [[{"param": "post_type", "operator": "==", "value": "page"}]], menu_order=0, hide=hide)


# ---------------------------------------------------------------- Coach Details (CPT coach)
def coach_group():
    f = maker("coach")
    fields = [
        text(f, "coach_role", "Role", "Shown under the name, for example President."),
        area(f, "coach_summary", "One line for the cards", "One sentence that shows on the People section and in search results.", rows=2),
        image(f, "coach_photo", "Photo (head and shoulders)", "A cut-out photo on a transparent background works best."),
        wysiwyg(f, "coach_bio", "Bio", "Write the bio. A few short paragraphs is plenty."),
        repeater(f, "coach_facts", "Facts", "Short facts that sit under the bio, like Experience or Award.", [
            text(f, "fact_label", "Label", "For example Experience."),
            text(f, "fact_value", "Answer", "One line. Leave empty if it is not decided yet."),
            text(f, "fact_tag", "Status tag", "Optional. For something not ready yet, write Coming soon."),
        ], "Add a fact", layout="table"),
        image(f, "coach_hero_image", "Photo for the top of the page", "A wide photo behind the coach's name."),
        rng(f, "hero_focus_x", "Keep this part in view: left to right", "Slide to choose which part of the top photo stays visible. 0 is the left edge, 100 the right.", width="50"),
        rng(f, "hero_focus_y", "Keep this part in view: top to bottom", "0 is the top edge, 100 the bottom.", width="50"),
    ]
    return group("group_tvbc_coach", "Coach Details", fields, [[{"param": "post_type", "operator": "==", "value": "coach"}]], menu_order=0)


def band_group():
    f = maker("band")
    fields = [
        image(f, "band_image", "Photo", "A wide photo at the bottom of the page. A dark tint is added so the words can be read."),
        text(f, "band_heading", "Heading", "One short line. Example: Come meet us"),
        text(f, "band_heading_accent", "Last words in italic", "Shown in the italic style. Example: before tryouts."),
        link(f, "band_button_1", "Main button (yellow)", "Pick the page or paste a web address, then write the words on the button."),
        link(f, "band_button_2", "Second button (outline)", "Optional."),
    ]
    return group("group_tvbc_band", "Closing Banner", fields,
                 [[{"param": "post_type", "operator": "==", "value": "coach"}], [{"param": "post_type", "operator": "==", "value": "post"}]], menu_order=20)


def news_group():
    f = maker("news")
    fields = [
        rng(f, "hero_focus_x", "Keep this part of the photo in view: left to right", "The photo at the top is the Featured image. Slide to choose which part stays visible. 0 is the left edge, 100 the right.", width="50"),
        rng(f, "hero_focus_y", "Keep this part of the photo in view: top to bottom", "0 is the top edge, 100 the bottom.", width="50"),
    ]
    return group("group_tvbc_news", "News Photo", fields, [[{"param": "post_type", "operator": "==", "value": "post"}]], menu_order=10)


# ---------------------------------------------------------------- Club settings (options page)
def settings_group():
    f = maker("set")
    on = ("announcement_show", "==", "1")
    fields = [
        tab(f, "tab_top", "Top of every page"),
        toggle(f, "announcement_show", "Show the bar at the very top", "The thin bar above the menu. Switch it off when there is nothing to announce."),
        text(f, "announcement_text", "What the bar says", "One sentence.", show_if=on),
        link(f, "announcement_link", "Link in the bar", "Optional. Pick the page, then write the words people click, for example Details.", show_if=on),
        f("date_picker", "announcement_from", "Start showing on", "Optional. The bar stays hidden until this day.", display_format="F j, Y", return_format="Ymd", first_day=0, show_if=on, width="50"),
        f("date_picker", "announcement_until", "Stop showing after", "Optional. The bar disappears by itself after this day.", display_format="F j, Y", return_format="Ymd", first_day=0, show_if=on, width="50"),
        text(f, "logo_text", "Name next to the logo", "The word beside the round logo in the menu.", default_value="Tumbleweeds"),
        image(f, "logo_mark", "Logo (optional)", "Leave empty to use the club's tumbleweed mark. To change it, upload a one-colour logo with a transparent background (SVG or PNG)."),
        image(f, "favicon", "Tab icon (optional)", "The tiny icon in the browser tab. Leave empty to use the tumbleweed mark. A square PNG, at least 64 by 64."),
        link(f, "header_cta", "Yellow button in the menu", "Pick the page, then write the words on the button, for example Tryouts."),
        link(f, "phone_menu_link", "Extra link on the phone menu only", "Optional. A page that shows in the full-screen menu on phones but not in the bar on a computer, for example News."),
        f("post_object", "coaches_page", "Page that lists the coaches", "So Coaches stays lit in the menu on a coach's page.", post_type=["page"], return_format="object", multiple=0, allow_null=1, ui=1),
        message(f, "menu_note", "The menu links", "The links in the menu and in the footer are set under <strong>Appearance, Menus</strong> (Header Menu and Footer Menu)."),

        tab(f, "tab_info", "Info session"),
        text(f, "info_title", "Name of the event", "For example Parent info session.", default_value="Parent info session"),
        f("date_picker", "info_date", "Date", "When it happens. After this day, every place that shows the info session hides it by itself. Clear the date to hide it now.", display_format="F j, Y", return_format="Ymd", first_day=0),
        text(f, "info_time", "Time", "For example 7:00 to 8:30 pm."),
        text(f, "info_place", "Place", "For example TRU Science Building S337."),
        area(f, "info_details", "Extra details", "Optional. For example parking and how to join online.", rows=3),

        tab(f, "tab_ticker", "Scrolling strip"),
        repeater(f, "ticker_phrases", "Words that scroll across the strip", "Short phrases. They repeat along the strip on the home page.", [text(f, "ticker_phrase", "Phrase", "A few words.")], "Add a phrase", layout="table"),

        tab(f, "tab_badge", "Round badge"),
        text(f, "badge_text", "Words around the round badge", "The slowly turning badge on the home page photo. Keep it to about 60 characters.", ),

        tab(f, "tab_contact", "Contact and social"),
        text(f, "contact_email", "Club email", "Where messages from the contact form go."),
        text(f, "club_location", "Town", "For example Kamloops, BC."),
        link(f, "footer_contact_link", "Link to the contact page", "Pick the contact page, then write the words, for example Contact page."),
        repeater(f, "socials", "Social media", "One row for each account.", [
            select(f, "social_network", "Network", "Which site.", {"instagram": "Instagram", "facebook": "Facebook", "tiktok": "TikTok", "youtube": "YouTube"}, default="instagram"),
            text(f, "social_label", "What shows", "For example @tumbleweedsvball."),
            f("url", "social_url", "Web address", "The full address of the account.", default_value="", placeholder="https://"),
        ], "Add an account", layout="table"),

        tab(f, "tab_helpline", "Helpline"),
        text(f, "helpline_name", "Helpline name", "For example Abuse-Free Sport Helpline."),
        text(f, "helpline_phone", "Helpline number", "Exactly as it should show, for example 1-888-83SPORT (77678)."),
        text(f, "complaints_contact", "Club complaints contact", "A named person outside the club. Until it is decided, leave the words coming soon.", default_value="coming soon"),

        tab(f, "tab_footer", "Footer"),
        area(f, "footer_blurb", "Short line about the club", "Shown under the logo in the footer.", rows=2),
        text(f, "footer_signup_title", "Sign-up heading", "For example Stay in the loop."),
        area(f, "footer_signup_code", "Sign-up form code (optional)", "If you have a sign-up form from your email service, paste its embed code here. Leave empty to use the simple form that opens the visitor's email app.", rows=4),
        text(f, "footer_status_line", "Line after the copyright", "For example A Volleyball BC member club (new club), Zone 2 Thompson-Okanagan."),
        text(f, "footer_small_print", "Small print", "Optional. For example the photo credit."),
    ]
    return group("group_tvbc_settings", "Club Settings", fields, [[{"param": "options_page", "operator": "==", "value": "club-settings"}]], menu_order=0)


if __name__ == "__main__":
    for g in (hero_group(), flex_group(), coach_group(), band_group(), news_group(), settings_group()):
        write(g)
    print("acf-json written:", sorted(p.name for p in OUT.glob("*.json")))
