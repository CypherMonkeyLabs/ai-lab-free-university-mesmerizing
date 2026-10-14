# Contributing

Thank you for improving a free campus. The bar is the same for a typo and a new school: a stranger can open the result offline, the section count is true, and nothing personal or secret landed in the diff.

Read [docs/REMIX.md](./docs/REMIX.md) for file layout, lesson ids, themes, zips, and how to use a coding agent. This file is the review checklist.

## Before you open a pull request

1. Edit the lesson source in `campus/` (`lessons_core.py`, `lessons_apply.py`, `lessons_ref.py`, or `diagrams.py`). The golden slice is edited directly when the change belongs there.
2. Rebuild the campus with `python3 -m campus.build_campus`.
3. If the HTML changed, run `python3 scripts/rebuild_zips.py`.
4. Run `python3 scripts/verify_campus.py` from the repository root.
5. Explain why in the pull request. Point at the lesson id (`07-01`, not “the MCP bit”).

## What we merge

- A correction a learner would be misled without
- A new lesson that teaches a mechanism, a falsifier, and where the artifact goes
- A theme that stays readable in light and dark surroundings
- Clearer docs, as long as every README link still resolves

## What we do not merge

- API keys, tokens, customer data, private chats, internal hostnames, or phone numbers
- Real names beyond the **CYPHER0X9** handle, employer or client names, or personal link-in-bio URLs
- A CDN `<script>` or stylesheet. The campus must open from disk
- A lesson count in the README that the HTML does not contain
- A generated zip that does not match the HTML beside it
- A renumbered lesson that already shipped. Add the next free id in that track instead

## Issues

Use the templates. A curriculum issue names the lesson id and the sentence that is wrong. A bug names the browser and whether you opened the HTML from disk or from the zip.

## AI-assisted edits

Coding agents are welcome. You still read the diff. Point the agent at `docs/REMIX.md`, ask for one lesson or one theme, and do not let it add secrets, personal links, or network dependencies. The human who opens the pull request is the author of the change.
