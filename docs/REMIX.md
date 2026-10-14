# Remix this campus

Anyone can improve, re-teach, or retheme this campus. The MIT license lets you copy it. The engineering bar is: one stranger, one browser, no network, and a lesson count that matches the file.

## File structure

```text
campus/                         lesson source and the generator
campus/ai-lab-university.html   the built course (what you open)
campus/golden-slice.html        the short starter page
campus/art.py                   SVG heroes, plates, and step-through flows
campus/flowbook.py              joins the visual scripts
campus/v_front.py               scripts for tracks 00–06
campus/v_back.py                scripts for tracks 07–13
campus/v_ref.py                 glossary, interview, and question scripts
campus/v_meta.py                home, studio, track hubs, and narration
campus/visuals.py               lesson chrome, hubs, and the asset check
campus/studio.py                zero-key demos and audio markup
campus/media.py                 generated tone clips stored in the HTML
campus/player.js                playback, demos, search count, high contrast
campus/visual.css               layout for the visual layer
downloads/*.zip                 built from campus/; do not edit by hand
docs/                           guides, FAQ, screenshots, hero
labs/                           zero-key Python; standard library only
scripts/rebuild_zips.py         rewrites the zips
scripts/verify_campus.py        count, offline rule, privacy, labs, zips
tests/check_campus.py           headless navigation and network check
```

Lesson text lives in `campus/lessons_core.py`, `campus/lessons_apply.py`, and `campus/lessons_ref.py`. The six architecture figures live in `campus/diagrams.py`. Per-lesson heroes, flows, and plates are drawn from the scripts in `campus/v_front.py`, `campus/v_back.py`, `campus/v_ref.py`, and `campus/v_meta.py`. Tracks and routes live in `campus/schema.py`. Edit those sources. A hand edit to the HTML is overwritten on the next build.

Rebuild after an edit:

```bash
python3 -m campus.build_campus
python3 scripts/rebuild_zips.py
python3 scripts/verify_campus.py
```

`build_campus` rewrites `campus/ai-lab-university.html` and `docs/assets/hero.svg`. It refuses to write a page with fewer than 500 SVG elements, 100 flows, or a hero and a plate on every lesson. Audio clips must stay between 10 and 20.

## How a lesson is built

Each lesson is a `lesson(...)` call. The generator emits an `<article class="lesson">`.

```python
add(lesson(
    "07-01", "07", "core", 12,
    "MCP connects a model to tools you did not hard-code",
    "The Model Context Protocol is a standard way for an app to talk to a tool server.",
    [
        P("Teaching prose."),
        PR("The practice: a run, a trace, a metric, and an artifact."),
        CK("The check question?", "The answer."),
    ],
))
```

When you add a lesson:

1. Put it in the module for that half of the course, with a new id.
2. If it is a new track, add the track to `SCHOOLS` in `campus/schema.py`. Track lessons should stay at five or more; the generator refuses a thinner track.
3. If a diagram is new, add the SVG to `campus/diagrams.py` and refer to it with `FIG`.
4. State the new lesson count in `scripts/verify_campus.py` (`EXPECTED_LESSONS`), the README, `CITATION.cff`, and the docs that state the count.
5. Rebuild the HTML and the zips.

Search uses the title, the summary, and the lesson text. Write the lesson in the body first.

`level` in the source is `core` or `practice`. The page shows that as the lesson kind.

## Naming

| Kind | Pattern | Example |
|---|---|---|
| Numbered track | `00`–`13` | `07` MCP |
| Reference tracks | short letters | `GL`, `IV`, `FQ` |
| Lesson id | `{track}-{two digits}` | `07-01`, `IV-03`, `13-05` |
| Files | kebab-case, say what they are | `ai-lab-university.html` |
| Labs | `labs/NN-short-name.py` | `labs/03-golden-eval.py` |

Do not renumber a lesson that already shipped. New work gets the next free id in that track.

## Themes

Dark and light live on `html[data-theme]`. The sun and moon button toggles only those two. High contrast is a separate control, `html[data-contrast="high"]`, so it does not replace the theme. Colors are CSS variables so the same SVG figures work in each. Do not add a remote font. The page uses the system font stack.

The golden slice is a separate page. Theme it only when the change belongs on that short page.

## Regenerate the zips

From the repository root, after the HTML is rebuilt:

```bash
python3 scripts/rebuild_zips.py
python3 scripts/verify_campus.py
```

`rebuild_zips.py` writes:

- `downloads/ai-lab-university.html.zip` containing only `ai-lab-university.html`
- `downloads/golden-slice.html.zip` containing only `golden-slice.html`

The zip has no Unix user id and no extra fields. Hand-edited zips drift. The checker rejects a zip whose bytes do not match the HTML.

`bash scripts/verify_slice.sh` runs the same campus checker. Keep the script so older notes still work.

## Use a coding agent

Cursor and similar tools are fine. They are loops with a filesystem. Treat them like track 06 and track 08: a plan, a diff, tests, and a person who reads the result.

A prompt that works:

```text
Read docs/REMIX.md. Add one lesson to track 07 in campus/lessons_apply.py.
Follow the lesson() pattern. Update EXPECTED_LESSONS and the README count.
Do not add a CDN, a personal link, a key, or an employer name.
Then run python3 -m campus.build_campus, python3 scripts/rebuild_zips.py,
and python3 scripts/verify_campus.py.
```

You still:

- read the diff
- refuse a change you cannot explain
- keep the pull request to one idea
- run the checker yourself if the agent claims it passed

Do not ask an agent to invent a new lesson count, scrape private data into a lesson, or delete a track to “clean up.”

## A small remix checklist

- [ ] Lesson teaches a mechanism and a check
- [ ] Id is unique and the track exists
- [ ] `EXPECTED_LESSONS` equals the number of `<article class="lesson">` tags
- [ ] README and citation say that same number
- [ ] No banned personal data (the checker looks)
- [ ] HTML still has no external script or stylesheet
- [ ] Zips rebuilt with `scripts/rebuild_zips.py`
- [ ] `python3 scripts/verify_campus.py` prints `PASS`
