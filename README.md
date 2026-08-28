> 🇪🇸 [Léelo en español](README.es.md)

# aios-kit

An operating system for your AI agent's context — four mechanisms and seven skills that stop it missing what it already knows.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## The problem

You ask the agent about something you settled six weeks ago. It searches, finds nothing, and tells you the thing does not exist — while the file sits three folders away, written by you.

More context is not the fix. A bigger pile takes longer to search and hides more contradictions.

It cannot find what it already knows. That is a filing problem, and filing is what this kit fixes.

---

## The four mechanisms

| Mechanism | What it fixes |
|---|---|
| **Precedence** | One fact lives in one place; everything else points at it. |
| **Routing** | A table of what each folder holds and when to go there. |
| **Failure protocol** | When the agent misses something that exists, name the failure mode and fix the cause, not the symptom. |
| **Maintenance loop** | The system audits and repairs itself, or it rots. |

All four live in `CLAUDE.md`, the manual the agent reads before it reads anything else.

**Precedence** exists because a copied number is correct the day you paste it and wrong forever after. Nobody updates the copy, because nobody remembers it exists. Six weeks later a session opens, reads the stale copy out of the always-loaded layer, and confidently tells you something false.

**Routing** is a table covering every first-level folder — what it holds, and when to go there. A folder the map does not mention is a folder the agent will not find. Add a folder, add its row, same commit.

The **failure protocol** runs the moment a miss is confirmed. Every miss is one of exactly four failure modes, and the kit uses the same four words everywhere: `poisoning` (a preloaded file asserted something false), `bloat` (the answer was there, buried in too much), `confusion` (the map is silent or points somewhere irrelevant), `clash` (two files disagree and the agent believed the wrong one). Naming the mode is what turns an apology into a repair — a file found by hand and not re-routed will be lost again next week.

The **maintenance loop** is the one people skip. Manuals, indexes and context files are claims about what exists, and nobody re-verifies a claim once it is written down. A workspace nobody maintains stops being true in about sixty days, and a system that is confidently wrong is worse than no system at all. So the kit checks itself: a read-only drift check runs on every session start and speaks only when something has moved, and two skills — one for accuracy, one for structure — put the workspace on the record monthly.

---

## Quickstart

```sh
git clone https://github.com/EnzoSacinRuiz/aios-kit.git my-workspace
cd my-workspace
claude
```

Then, in the session:

```
/onboard
```

It asks what language you want the workspace to work in, interviews you one question at a time, archives the demo company, and writes your real context files and your first standing rule. It is safe to re-run — a second run updates in place and will not archive the demo twice.

That is the whole install. No package to add, nothing to configure first.

---

## Anatomy

```
aios-kit/
├── CLAUDE.md                     The operating manual. Precedence table, routing
│                                 map, failure protocol, automation table.
├── context/                      Loaded into every session. Four small files.
│   ├── me.md                     Who the operator is.
│   ├── work.md                   What the business sells and to whom.
│   ├── team.md                   Who does what, and who signs.
│   └── priorities.md             This quarter's goals. The only place goals are edited.
├── knowledge/
│   ├── external/                 The outside world: clients, prospects, competitors.
│   │                             A [[wiki-link]] graph with its own index.md and
│   │                             an ingestion manual.
│   └── playbook/                 Your own method: principles and plays. Same shape.
├── decisions/log.md              Append-only. What was decided, why, in what context.
├── projects/                     Work per account. Deliverables, not context —
│                                 go to the one project, never load the folder.
├── reports/                      What the skills write. Generated, not authored.
├── references/                   voice.md and sops/ — one file per
│                                 repeatable process.
├── templates/                    Starting points you copy rather than edit in place.
├── archives/                     Nothing is deleted here, it is archived.
├── scripts/
│   └── aios-freshness-check.sh   Read-only drift check. Runs on every session start,
│                                 prints nothing when nothing has drifted.
├── docs/                         Documentation about the kit itself, for humans.
└── .claude/
    ├── rules/                    Permanent standing rules — the rule, then why.
    ├── skills/                   Seven skills, one folder each.
    └── settings.json             Wires the session hook.
```

### It ships full, not empty

Most template repositories are hollow: folders with a `.gitkeep` and a README describing a system that has never held anything. This one arrives pre-filled with a worked example — **Meridian Research**, a fictional four-person market-research consultancy — so you can read a live workspace instead of guessing at one.

Click into `knowledge/playbook/` and you will find a sales principle written as one claim per file, linked to the client account in `knowledge/external/` that keeps triggering it and to the entry in `decisions/log.md` it came from. Click into `context/priorities.md` and you will see quarter goals sitting next to an explicit warning that the cash balance must never be written there. That is the whole thesis, working, in files you can open right now.

Every demo file opens with the same line — `> 🟡 DEMO — /onboard replaces this file with yours.` — and `/onboard` finds them by that line, not by a list that would go stale, moves them to `archives/demo/` with their paths intact, and writes yours in their place. Nothing is deleted, so you can go back and read the example after your own workspace is running.

---

## The lifecycle

| Skill | Role |
|---|---|
| `/onboard` | **Install.** Interviews you and replaces the demo with your real context. |
| `/distill` | **Feed.** Turns a transcript, a document or a pile of notes into routed, linked knowledge — decisions to the log, outside facts to one wiki, your own method to the other, action items to your task tool. Never one dumped file. |
| `/route-fix` | **Repair.** You missed something that existed. Trace what you read, name the failure mode, fix the cause. |
| `/os-audit` | **Is it still true?** Six read-only checks of every claim the manual makes against what is on disk. Writes a report; changes nothing. |
| `/blueprint` | **Is it built right?** Scores the workspace out of 100 on routing, precedence, freshness and the loop, and names the three highest-leverage fixes with the exact command for each. |
| `/leverage` | **Extend, weekly.** Find the friction, cut the part of it that should not exist, then build the smallest machine for what survives. |
| `/skill-builder` | **Extend, on demand.** Turns a process you keep re-explaining into a skill, through a nine-block interview that asks before it writes. |

`/os-audit` and `/blueprint` measure different things and both matter. A workspace can score 95 for structure and be full of stale facts; it can be perfectly current and score 40 because nothing holds it together. Run both, monthly.

---

## What this is not

- **Not a prompt pack.** There are no clever prompts to paste. The unit of work is where a fact lives and who owns it.
- **Not an agent framework.** Nothing here orchestrates models, manages state or wraps an API. It is markdown your agent reads.
- **No subscription, no account, no telemetry.** MIT licensed. Fork it, rename it, sell what you build with it.
- **No dependencies and no build step.** Markdown files plus one POSIX shell script that runs on macOS and Linux without modification. Under a megabyte, so it clones instantly and stays readable from a phone.
- **Not a knowledge base you fill and forget.** The loop is the product. Without it the other three mechanisms are correct on day one and quietly false by day sixty.

Built for Claude Code, and portable in principle to any agent that reads a project manual from the repository root.

---

## More

- [How it works](docs/how-it-works.md) — the essay: what breaks without each mechanism, and what each one costs to maintain.
- [Credits](docs/credits.md) — ideas that shaped this kit but did not originate here.
- [Léelo en español](README.es.md)
- Author: **Enzo Sacin Ruiz** — [LinkedIn](https://www.linkedin.com/in/enzosacin/)

MIT. Issues and pull requests welcome.
