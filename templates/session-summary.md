# Session summary — YYYY-MM-DD — <topic>

Copy this file, don't edit it in place. Fill it in at the end of a working session, while the
session is still in front of you. Delete any section that genuinely has nothing in it — an
empty heading kept for symmetry is noise the next reader has to step over.

Anything in here that is durable does not stay in here. This file is a holding pen, not a
destination: it exists so nothing gets lost between the end of the session and the moment it
gets routed. The last section is what routes it.

---

## What this session was about

One or two sentences. What was on the table, and why it came up now.

## What was decided

One line per decision, each with the reason. A decision with no reason gets re-litigated the
next time someone disagrees with it.

- **Decided:** … — **because:** …

## What changed

Files, systems, or agreements that are different now than they were this morning. Name the
path or the person, not the general area.

- `path/or/thing` — what changed.

## What is still open

The questions this session did not settle. For each one, say what it is blocked on and who
has to move — an open question with no owner is a question nobody will answer.

- **Open:** … — **blocked on:** … — **owner:** …

## Next

The next concrete action, not an intention. If it has a date, put the date.

- [ ] …

## Where each of these goes

Walk the list above and route it. Nothing durable is allowed to end its life in this file.

- A decision → append it to `decisions/log.md`, in that file's format.
- A durable fact about the outside world → a node in `knowledge/external/`, listed in its `index.md`.
- Something you now know about how to do the work → a node in `knowledge/playbook/`, same.
- An action with an owner and a date → your task tool, not here.
- A fact that changes who you are, what you sell, the team, or the quarter → edit `context/`.
- Anything that is only true for one engagement → `projects/<name>/`, with the rest of it.

If a line above fits none of these, the routing map in `CLAUDE.md` is missing a row. That is a
finding, not a shrug — run `/route-fix`.
