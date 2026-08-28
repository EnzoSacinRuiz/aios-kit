# Anatomy

Every folder and file in this kit, what it is for, which of the four mechanisms it serves, and
which skill writes to it.

Open this when you are setting up your own workspace and need to know where something goes.
For why the structure is shaped this way, read [`how-it-works.md`](how-it-works.md).

---

## The tree

Verified against the repository. Files marked **demo** carry the `🟡 DEMO` banner and are moved
into `archives/demo/` the first time `/onboard` runs.

```
.
├── CLAUDE.md                      # the operating manual: precedence, routing, failure protocol, automations
├── README.md                      # what this kit is, in English
├── README.es.md                   # what this kit is, in Spanish
├── LICENSE                        # MIT
├── .gitignore                     # the repo carries the brain, never deliverables, binaries or secrets
├── .env.example                   # copy to .env; the kit itself needs no keys
├── .mcp.json                      # MCP servers; nothing wired by default, example only
│
├── .claude/                       # the machinery, not the content
│   ├── settings.json              # wires the SessionStart hook to scripts/aios-freshness-check.sh
│   ├── rules/
│   │   ├── README.md              # the format contract every rule file follows
│   │   └── communication-style.md # internal register vs. client-facing register
│   └── skills/                    # one folder per skill, each with a SKILL.md
│       ├── onboard/SKILL.md       # install: interview, archive the demo, write real context
│       ├── distill/SKILL.md       # feed: raw material becomes routed, linked knowledge
│       ├── route-fix/SKILL.md     # repair: diagnose a confirmed miss, fix the cause
│       ├── os-audit/SKILL.md      # is it still true: six read-only drift checks
│       ├── blueprint/SKILL.md     # is it built right: score out of 100, top three fixes
│       ├── leverage/SKILL.md      # extend weekly: friction → cut → machine
│       └── skill-builder/SKILL.md # extend on demand: nine-block interview → a new skill
│
├── context/                       # the always-loaded layer — @imported into every session
│   ├── me.md                      # demo — who the operator is
│   ├── work.md                    # demo — what the business sells and to whom
│   ├── team.md                    # demo — who is on the team and when to loop them in
│   └── priorities.md              # demo — the quarter's goals; the owner of that fact
│
├── knowledge/
│   ├── external/                  # intelligence about the outside world
│   │   ├── CLAUDE.md              # demo — what belongs here, node format, link rules
│   │   ├── index.md               # demo — lists every node in this folder
│   │   ├── northwind-labs-pushes-for-rush-timelines.md   # demo — account node
│   │   └── pulse-category-research-undercuts-on-price.md # demo — competitor node
│   └── playbook/                  # the operator's own reusable method
│       ├── CLAUDE.md              # demo — what belongs here, node format, link rules
│       ├── index.md               # demo — lists every node in this folder
│       ├── hold-the-fee-negotiate-scope.md   # demo — sales principle node
│       ├── record-before-synthesize.md       # demo — delivery principle node
│       └── respondents-are-never-named-to-the-client.md # demo — delivery principle node
│
├── decisions/
│   └── log.md                     # demo — append-only. What was decided, why, in what context
│
├── projects/                      # work per account or initiative; deliverables, not context
│   ├── README.md
│   └── northwind-labs-landscape-study/
│       ├── brief.md                  # demo — scope, objective, constraints
│       ├── deliverable-outline.md    # demo — the shape of what gets handed over
│       └── interview-progress-2026-08-20.md  # demo — the status snapshot the other two point at
│
├── reports/                       # output written by skills; generated, not authored
│   └── README.md                  # ships empty; /os-audit and /blueprint write the first files
│
├── references/                    # stable material you point at rather than restate
│   ├── README.md
│   ├── voice.md                   # demo — how the operator's writing sounds
│   └── sops/
│       └── win-loss-retainer-setup.md   # demo — one file per repeatable process
│
├── templates/
│   └── README.md                  # starting points for recurring deliverables; copy, don't edit in place
│
├── archives/
│   └── README.md                  # nothing is deleted here; /onboard puts the demo in archives/demo/
│
├── scripts/
│   └── aios-freshness-check.sh    # the SessionStart drift check; POSIX sh, always exits 0, silent when clean
│
└── docs/                          # documentation about the kit itself, for humans
    ├── how-it-works.md            # the four mechanisms and what each costs to maintain
    ├── how-it-works.es.md         # the same, in Spanish
    ├── anatomy.md                 # this file
    └── credits.md                 # ideas that shaped this kit but did not originate here
```

`.git/` is the only folder deliberately left out of the routing map in `CLAUDE.md`. An audit
that flags it as unrouted is scoped wrong.

---

## Folder → mechanism → skill

| Folder | Mechanism it serves | Skills that write to it |
|---|---|---|
| `context/` | **Precedence.** It is the always-loaded layer, so anything wrong here is wrong in every session forever. `priorities.md` is the named owner of quarter goals. | `/onboard` writes all four files. Nothing else writes here — you edit them by hand when a fact changes. |
| `knowledge/external/` | **Routing.** A `[[wiki-link]]` graph with an `index.md` that must list every node, and a folder-level `CLAUDE.md` defining the node format. | `/distill` writes nodes and updates `index.md` in the same pass. `/route-fix` edits the index when a node was unreachable. |
| `knowledge/playbook/` | **Routing.** Same shape, for the operator's own method rather than the outside world. | `/distill` writes nodes and updates `index.md`. `/route-fix` edits the index. |
| `decisions/` | **Failure protocol.** A rule changed without a log entry is a rule the next session will not know about. | `/distill` appends decisions found in raw material. `/route-fix` appends when a fix changes a rule. `/leverage` appends what it built and what it cut. `/onboard` appends the initialization entry. |
| `projects/` | **Routing.** Deliverables, not context — the map tells the agent to open one project and never the folder. | Nothing in the kit writes here automatically; this is where your work lives. `/os-audit` reads it looking for raw material that never got distilled. |
| `reports/` | **Maintenance loop.** Generated output, so it is safe to delete and regenerate. | `/os-audit` writes `os-audit-YYYY-MM-DD.md`. `/blueprint` writes `blueprint-YYYY-MM-DD.md`. Both are read-only everywhere else. |
| `references/` | **Precedence.** Stable material you point at instead of restating — voice, frameworks, and one SOP file per repeatable process in `sops/`. | `/leverage` writes an SOP to `sops/` when the machine it ships is smaller than a skill. `/leverage` reads `sops/` before cutting a process. |
| `templates/` | **Precedence.** A template is copied, never edited in place, so the original stays the one authority on the shape. | Nothing writes here automatically. You add templates as recurring deliverables emerge. |
| `archives/` | **Failure protocol.** Keeping history intact is what lets a later repair reconstruct why a file moved. | `/onboard` moves the demo here on its first run, preserving the original paths under `archives/demo/`. Every audit ignores this folder by design. |
| `scripts/` | **Maintenance loop.** Automation that runs outside a session. | `/leverage` writes here when the machine it ships is a script. Every automation added here needs a row in the automation table in `CLAUDE.md`. |
| `docs/` | **Routing.** Documentation about the kit for humans, kept out of the always-loaded layer so it costs nothing per session. | Nothing writes here automatically. |
| `.claude/rules/` | **Precedence.** A standing rule that would otherwise be re-decided every session. Rules beat defaults; your direct instruction beats rules. | `/onboard` writes the operator's first rule file. `/skill-builder` and other skills follow the format contract in `README.md`. |
| `.claude/skills/` | **Maintenance loop.** The disk is the source of truth for which skills exist — no file enumerates them. | `/skill-builder` writes `.claude/skills/<name>/SKILL.md`. `/leverage` hands off to it rather than drafting skill files itself. |
| `.claude/settings.json` | **Maintenance loop.** Wires the `SessionStart` hook. A hook lives in the repo and runs forever; a session-scoped cron dies with the session. | Edited by hand. `/blueprint` reads it to score whether the loop is actually wired. |

---

## The four always-loaded files

`CLAUDE.md` `@import`s exactly these four, and nothing else:

```
@context/me.md
@context/work.md
@context/team.md
@context/priorities.md
```

That is a privilege and a liability. Anything false in these four files is false in every
conversation you will ever have, and no session has any way to notice. Two rules follow:

- **Keep them small.** `/blueprint` flags the layer as bloat past roughly 200 lines across all
  four, and treats past 400 as a real finding.
- **Keep them durable.** A fact that is true today and irrelevant next month costs context
  budget in every session for something rarely needed. Situational facts belong in the project
  they came from; reusable method belongs in `knowledge/playbook/`.

Money and runway figures never go here at all. Any number about cash goes stale within weeks
and becomes a false claim preloaded into every session — the real balance is in the bank.

---

## The skills that ship with the kit

The disk is the source of truth for which skills exist: run `ls .claude/skills/`, and read each
one's `description` frontmatter — that is what actually fires it. The table below is a snapshot
of what is in the box today, not a claim about how many there are.

| Skill | Question it answers | Writes to |
|---|---|---|
| `/onboard` | Whose workspace is this? | `context/`, `.claude/rules/`, `decisions/log.md`, `archives/demo/` |
| `/distill` | Where does this raw material go? | `knowledge/external/`, `knowledge/playbook/`, `decisions/log.md`, your task tool |
| `/route-fix` | Why did you miss something that was there? | `CLAUDE.md`, an `index.md`, the file that misled you, `decisions/log.md` |
| `/os-audit` | Is it still true? | `reports/os-audit-YYYY-MM-DD.md` only |
| `/blueprint` | Is it built right? | `reports/blueprint-YYYY-MM-DD.md` only |
| `/leverage` | What should I automate next? | `references/sops/` or `scripts/`, plus `decisions/log.md` |
| `/skill-builder` | How do I stop re-explaining this? | `.claude/skills/<name>/SKILL.md`, plus a routing row if the destination is new |

Two pairs are easy to confuse:

- **`/os-audit` vs `/blueprint`.** One asks whether the claims are still true, the other
  whether the mechanisms that keep claims true were ever built. A workspace can pass one and
  fail the other badly, in either direction. Run the audit first, then the score.
- **`/route-fix` vs `/distill`.** `/route-fix` repairs a route to something real. If the fact
  was never written down, there is no route to repair — that is `/distill`.

---

## What the session hook checks

`scripts/aios-freshness-check.sh`, wired to `SessionStart` in `.claude/settings.json`.
Read-only, silent when nothing has drifted.

**The script owns the list of checks.** Open it — every check is numbered and commented in
place. This page does not restate them, on purpose: an enumerated copy here is correct the day
it is written and wrong the next time a check is added or removed, and a reader who diffs the
two would catch this kit failing its own precedence rule.

What the hook covers, as a category: drift the operator would not otherwise notice, tested
mechanically and cheaply enough to run on every single session. A check that needs context to
interpret does not belong in it — that is `/os-audit`'s job, monthly, where the judgement can
be made properly. The script's header comment states that constraint, and one check has already
been removed for failing it.

It always exits 0, including on every error path: a `SessionStart` hook that returns non-zero
breaks the session. It is POSIX `sh` with no bashisms, so it runs unmodified on macOS's default
`/bin/sh` and on Linux.

---

## Adding a folder

Create the folder and add its row to the routing map in `CLAUDE.md` **in the same commit**. A
folder the map does not mention is a folder you will not find — and a folder on disk with no
row is a finding the next audit will raise as `confusion`.

The same discipline applies in reverse: if `CLAUDE.md` names a path that is not on disk, that
is a dead path. Delete the row or create the thing. A path that is neither deleted nor created
gets followed again by every future session.
