# Remix this campus

Anyone can improve, re-teach, or retheme this campus. The MIT license lets you copy it. The engineering bar is: one stranger, one browser, no network, and a section count that matches the file.

## File structure

```text
campus/ai-lab-university.html   the full campus (source of truth)
campus/golden-slice.html        the short Phase-1 page
downloads/*.zip                 built from campus/; do not edit by hand
docs/                           guides, FAQ, preview image
labs/                           zero-key Python; standard library only
scripts/rebuild_zips.py         rewrites the zips
scripts/verify_campus.py        count, offline rule, privacy, labs, zips
```

There is no separate generator and no `curriculum/` package. The HTML is the curriculum. That is intentional: the file you open is the file you edit.

## How a lesson is built

Each lesson is an `<article class="sec">` in `campus/ai-lab-university.html`.

```html
<article class="sec" id="11-04" data-school="11" data-level="intermediate" data-search="mcp tools protocol">
  <div class="meta">
    <span class="id">11-04</span>
    <span class="school">11 · 2026 skills</span>
    <span class="lvl">intermediate</span>
  </div>
  <h2>MCP: tools as a protocol</h2>
  <div class="body">
    <p>Teaching prose.</p>
    <div class="green"><strong>Falsifier.</strong> What would prove this wrong.</div>
  </div>
  <div class="sec-actions">
    <button type="button" class="btn mark" data-mark="11-04">Mark studied</button>
    <button type="button" class="btn copy" data-copy="11-04">Copy id</button>
  </div>
</article>
```

When you add a lesson, update all of these or the checker fails:

1. The `<article>` itself.
2. A sidebar link: `<a class="nav" data-id="11-04" href="#11-04">`.
3. The school’s `<span>` count in that sidebar group.
4. A filter pill if you added a school: `data-filter-school`.
5. `window.AILAB_META`: `stats.sections`, `stats.by_school`, `section_ids`, and `schools` if the school is new.
6. The visible hero numbers (sections, and schools if that changed).
7. The README, `CITATION.cff`, and the docs that state the count.
8. The zips, via `python3 scripts/rebuild_zips.py`.

`data-search` is extra hay for the search box. The script also searches the visible text, so write the lesson in the body first.

`data-level` is `beginner`, `intermediate`, or `advanced`.

## Naming

| Kind | Pattern | Example |
|---|---|---|
| Numbered school | `00`–`11` | `06` agents |
| Handbook schools | short letters | `RT`, `GL`, `PX`, `IV`, `FQ` |
| Lesson id | `{school}-{two digits}` | `06-04`, `RT-01`, `11-12` |
| Files | kebab-case, say what they are | `ai-lab-university.html` |
| Labs | `labs/NN-short-name.py` | `labs/03-golden-eval.py` |
| Theme token | one word, matches CSS | `paper` |

Do not renumber a lesson that already shipped. School 03 jumps from `03-15` to `03-17`. That gap is history. New work gets the next free id in that school.

## Add a theme

Themes are CSS variables on `html[data-theme=…]`, plus a `<option>` in the theme menu. **Paper** is the worked example. Copy that block.

In `campus/ai-lab-university.html`:

```css
html[data-theme=paper]{
  --bg:#F6F3EC; --card:#FFFCF7; --ink:#1C1917; --muted:#57534E;
  --line:#E7E5E4; --border:#D6D3D1;
  --a1:#4F46E5; --a2:#6366F1; --a3:#15803D;
  --shadow:0 8px 24px rgba(28,25,23,.06)
}
```

Then add `<option value="paper">Paper</option>` and, if code blocks would become unreadable, a `pre` background next to the Warm and Forest rule.

Check both a light theme (Paper, Warm, Forest) and a dark theme (Night, Cobalt). Text, cards, and code must stay readable. Do not load a font from the network. The campus uses system fonts on purpose.

**Focus** is not a color theme. It is the button that hides the sidebar (`body.focus`). Leave that behavior alone when you add a color.

Mirror a new theme into `campus/golden-slice.html` if the slice should offer it too.

## Regenerate the zips

From the repository root, after the HTML is saved:

```bash
python3 scripts/rebuild_zips.py
python3 scripts/verify_campus.py
```

`rebuild_zips.py` writes:

- `downloads/ai-lab-university.html.zip` containing only `ai-lab-university.html`
- `downloads/golden-slice.html.zip` containing only `golden-slice.html`

The zip has no Unix user id and no extra fields. Hand-edited zips drift. The checker rejects a zip whose bytes do not match the HTML.

`bash scripts/verify_slice.sh` is the older name for the same checker. Lessons still say it. Keep the script.

## Use a coding agent

Cursor, Claude Code, Codex-style CLIs, and similar tools are fine. They are loops with a filesystem. Treat them like school 06.

A prompt that works:

```text
Read docs/REMIX.md. Add one lesson to school 11 in campus/ai-lab-university.html.
Follow the article.sec pattern. Update the nav, the meta JSON, and the hero count.
Do not add a CDN, a personal link, a key, or an employer name.
Then run python3 scripts/rebuild_zips.py and python3 scripts/verify_campus.py.
```

If you use MCP tools (docs, issues, browser), give the agent the tool it needs for the task and no secret-bearing tool “just in case.” Skills files are instructions: have the agent read the relevant skill, then do the one edit.

You still:

- read the diff
- refuse a change you cannot explain
- keep the pull request to one idea
- run the checker yourself if the agent claims it passed

Do not ask an agent to invent a new section count, scrape private data into a lesson, or “clean up” by deleting schools.

## A small remix checklist

- [ ] Lesson teaches a mechanism and a falsifier
- [ ] Id is unique and the nav href matches
- [ ] Meta `sections` equals the number of `<article class="sec">` tags
- [ ] README and citation say that same number
- [ ] No banned personal data (the checker looks)
- [ ] HTML still has no external script or stylesheet
- [ ] Zips rebuilt
- [ ] `python3 scripts/verify_campus.py` prints `PASS`
