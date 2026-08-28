# CLAUDE.md — the operating manual for this AIOS

You are the operator's second brain. This file tells you how this workspace is organized, and
what to do when it fails you.

> **If `context/me.md` still opens with a 🟡 DEMO banner, this workspace has never been set up. Run `/onboard` before anything else.**

---

## Context

@context/me.md
@context/work.md
@context/team.md
@context/priorities.md

These four files load into every session. That is a privilege and a liability: anything wrong
in them is wrong in every conversation you will ever have. Keep them small, keep them true.

---

## Precedence — who wins when two files disagree

_Read this before the routing map. Without it, every duplicated fact is a conflict waiting to
go off._

| About… | The owner | Everything else |
|---|---|---|
| Quarter goals | `context/priorities.md` | points at it, never copies it |
| Task and project status | your task tool (ClickUp, Linear, Notion — whatever you use) | points at it, never copies it |
| Which skills exist | the disk — `ls .claude/skills/` | orients, never enumerates |
| Which projects exist | the disk — `ls projects/` | orients, never enumerates |
| Money and runway | your bank and your accounting | **never** written into the always-loaded layer |
| What was decided and why | `decisions/log.md` | points at it, never copies it |

**The rule underneath: one fact lives in one place; everything else points at it.**
If you catch yourself copying a number or a status into a second file, don't — write down
where it lives instead.

Why this matters more than it looks: a copied number is correct on the day you paste it and
wrong forever after. Nobody updates the copy, because nobody remembers it exists. Six weeks
later a session opens, reads the stale copy out of the always-loaded layer, and confidently
tells the operator something false. That failure has a name — `poisoning` — and precedence is
the only thing that prevents it.

---

## Routing map — where everything lives

_Last verified: 2026-08-27. This table covers every first-level folder. If you look for
something and it is not here, the table is stale — fix it (see the next section)._

| Folder | What it holds | When to go there |
|---|---|---|
| `context/` | The always-loaded layer: who the operator is, what they sell, who's on the team, what the quarter's goals are. | Never search it — it is already in your context. Edit it when a fact changes. |
| `knowledge/external/` | Intelligence about the outside world: clients, prospects, competitors, market. A `[[wiki-link]]` graph with its own `index.md`. | Preparing for a conversation with someone outside the company. |
| `knowledge/playbook/` | The operator's own method: principles, plays, how they do the work. Same graph shape. | Deciding how to do something you've done before. |
| `decisions/` | `log.md`, append-only. What was decided, why, and in what context. | Before re-opening a settled question. Always, when something is decided. |
| `projects/` | Work per account or initiative. Deliverables, not context. | A specific piece of client or project work. Go to the one project — never load the folder. |
| `reports/` | Output written by skills: audits, briefs, notes. Generated, not authored. | Finding a report a skill already produced. |
| `references/` | Voice profile, frameworks, and `sops/` — one file per repeatable process. | Matching the operator's voice, or following a process that already exists. |
| `templates/` | Starting points for recurring deliverables. | Beginning something you make repeatedly. Copy it; don't edit in place. |
| `archives/` | Retired material. Nothing is deleted here — it is archived. `/onboard` puts the demo company in `archives/demo/`. | Recovering something that was removed. |
| `scripts/` | Automation that runs outside a session. | Changing what runs on its own. |
| `docs/` | Documentation about this kit itself, for humans. | Explaining the system to a person, not using it. |
| `.claude/` | The machinery, not the content. `rules/` holds permanent standing rules, `skills/` holds one folder per skill, `settings.json` wires the session hook. | Adding a rule, adding a skill, or changing what runs automatically. |

**Adding a folder:** create the folder and add its row here in the same commit. A folder the
map doesn't mention is a folder you will not find.

**Scope of this map:** every folder above is in it, including `.claude/`. The only folder
deliberately left out is `.git/`, which belongs to git and not to you. An audit that flags
`.git/` as unrouted is scoped wrong.

---

## When you fail to find something

This is the most important section in this file.

If you searched, didn't find something, and it **turns out it was there all along** — or the
operator says "it's right there":

1. **Don't apologize and move on.** Trace it: say exactly which paths you read, in what order,
   and which row of the routing map sent you the wrong way.
2. **Name the failure mode.** It is one of exactly four:
   - `poisoning` — a preloaded file asserted something false or stale.
   - `bloat` — the answer was there, buried in too much.
   - `confusion` — the routing map is silent, or points somewhere irrelevant.
   - `clash` — two files disagree and you believed the wrong one.
3. **Fix the cause, not the symptom.** Update the routing map, or the wiki's `index.md`, or
   move the file to where this manual says it belongs. **A file found by hand and not
   re-routed will be lost again.**
4. **If the fix changes a rule, log it** in `decisions/log.md`.

Run **`/route-fix`** and it will walk you through all four.

The same rule runs in reverse: if this manual promises something that isn't on disk, that's a
dead path. Delete it or create it — don't leave it sitting there.

---

## What runs on its own

| What | When | What it does |
|---|---|---|
| `scripts/aios-freshness-check.sh` | `SessionStart` hook, every session | Checks five things and speaks only when something has drifted: stale `context/`, no audit in 30 days, raw material never distilled, the demo still installed, apparent secrets tracked by git. **Read-only. Fixes nothing.** |

**Why a hook and not a cron:** a hook lives in `.claude/settings.json` and runs on this
machine, every session, forever. A session-scoped cron dies when the session closes. If you
ever need work that runs with no session at all, that's a scheduled cloud agent — not a local
cron.

If you add an automation, add a row to this table. **An undocumented automation is a phantom
data source** — output appears, nobody knows where from, and nobody notices when it stops.

---

## Skills

_The disk is the source of truth: `ls .claude/skills/`. This table only orients._

| Skill | Role |
|---|---|
| `/onboard` | **Install.** Interviews the operator and replaces the demo with their real context. |
| `/distill` | **Feed.** Turns raw material — a transcript, a document, a pile of notes — into routed knowledge. |
| `/route-fix` | **Repair.** You missed something that existed. Name the failure mode, fix the cause. |
| `/os-audit` | **Is it still true?** Checks every claim this manual makes against what's on disk. |
| `/blueprint` | **Is it built right?** Scores the workspace out of 100 and names the three highest-leverage fixes. |
| `/leverage` | **Extend, weekly.** Find the friction, cut what shouldn't exist, build the smallest machine for what's left. |
| `/skill-builder` | **Extend, on demand.** Turn a process the operator repeats into a skill. |

---

## Keeping this current

- Priorities changed → edit `context/priorities.md`. It is the only place goals are edited.
- Something was decided → append to `decisions/log.md`.
- A workflow keeps repeating → `/skill-builder`.
- You missed something that was there → `/route-fix`.
- Monthly → `/os-audit`, then `/blueprint`.

A workspace nobody maintains stops being true in about sixty days, and a system that is
confidently wrong is worse than no system at all. The loop is what keeps it honest.
