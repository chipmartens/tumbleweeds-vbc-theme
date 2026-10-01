---
name: tumbleweeds-theme
description: >-
  Tumbleweeds Volleyball Club WordPress theme: ACF flex_content layouts, BEM section
  classes, CSS design tokens, PHP helpers, Club settings options page. Use when editing
  template-parts/content-flexcontent.php, inc/lib/flex.php or extras.php, src/scss/app.scss,
  acf-json, or the seed.
---

# Tumbleweeds theme: agent guidance

**Canonical reference:** the Cursor project rule `tumbleweeds-theme` (`.cursor/rules/tumbleweeds-theme.mdc`) has the token list, the BEM naming, the layout list and the new-layout recipe. The research behind it is `CHEZ-KOOP-CONVENTIONS.md`.

**Quick anchors**

- Flex loop: ACF field `flex_content`; each row's `get_row_layout()` is a `section_*` name; the markup is in `template-parts/content-flexcontent.php`.
- Fields are generated: edit `tools/build_acf_json.py`, run it, commit `acf-json/`.
- Copy lives in `tools/build_seed.py` (writes `seed/content.json`); `seed/import.php` loads it into a fresh WordPress.
- Build: `npm run build` then commit `assets/css/app.min.css`, its `.map` and `dist/js/app.bundle.js`.
- Check: run Playground (README), `node tools/shots.js <base> <dir>` at 1440 and 390, compare with `v2/` using `python3 tools/compare.py`.
