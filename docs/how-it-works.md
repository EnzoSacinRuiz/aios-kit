# How it works

An agent with a good memory and a bad filing system behaves exactly like an agent with no
memory at all. It searches, finds nothing, and tells you the thing does not exist — while the
file sits three folders away, written by you, six weeks ago.

This kit is four mechanisms that make that failure rare, and one loop that catches it when it
happens anyway.

| Mechanism | What it is |
|---|---|
| **Precedence** | One fact lives in one place; everything else points at it. |
| **Routing** | A table of what each folder holds and when to go there. |
| **Failure protocol** | When the agent misses something that exists, name the failure mode and fix the cause, not the symptom. |
| **Maintenance loop** | The system audits and repairs itself, or it rots. |

Each section below answers three questions in the same order: what breaks without the
mechanism, what the mechanism actually is, and what it costs you to keep running. The third
question is the one most context kits skip. Every mechanism here has a maintenance bill, and
you should see it before you decide to adopt any of this.

---

## 1. Precedence

### What breaks without it

You write your quarterly target into `context/priorities.md`. Two weeks later you are drafting
a project brief and you type the number again, because typing it is faster than opening the
file. Now it exists twice.

The copy is correct on the day you paste it and wrong forever after. Nobody updates it,
because nobody remembers it is there. Two months later a session opens, reads the copy, and
tells you something false in a confident voice. Nothing errors. Nothing looks broken.

Multiply that by every number, status, date, and headcount you have ever mentioned twice, and
the workspace stops being a source of truth and becomes a pile of claims of unknown age.

### What the mechanism is

`CLAUDE.md` opens with a precedence table. Each row names a class of fact and the one place
that owns it:

| About… | The owner |
|---|---|
| Quarter goals | `context/priorities.md` |
| Task and project status | your task tool |
| Which skills exist | the disk — `ls .claude/skills/` |
| Money and runway | your bank and your accounting |
| What was decided and why | `decisions/log.md` |

Everything outside the owner points at it and never restates it. `context/work.md` does not
list the quarter's proposal target; it says the target lives in `context/priorities.md`. No
file enumerates the skills, because `ls .claude/skills/` cannot go stale.

The rule generalizes past the table: if you catch yourself copying a number or a status into a
second file, write down where it lives instead.

### What it costs you

- **It is slower in the moment.** Pasting the number takes two seconds. Opening the owner file,
  confirming it is still the owner, and writing a pointer instead takes thirty. You will feel
  that tax every time, and the payoff arrives months later as an error that never happened.
- **You have to decide an owner before you can write.** For a new class of fact — who owns
  pricing, who owns headcount — that is a real decision, and skipping it means the fact lands
  in two files by default.
- **The table needs a row per contested class.** A precedence table with three rows in a
  workspace with ten contested facts is worse than none, because it implies coverage it does
  not have.
- **Pointers read worse to humans.** "See `context/priorities.md`" is less useful to a person
  skimming than the number itself. You are trading human convenience for machine truth. That
  trade is right, and it is still a trade.

---

## 2. Routing

### What breaks without it

The agent needs the note you wrote about a client's negotiating pattern. It looks in
`projects/`. It looks in `reports/`. It does not look in `knowledge/external/`, because nothing
told it that folder holds account intelligence. It reports that no such note exists.

You paste the path. Work continues. Next week it happens again with a different file.

A workspace with no map is not searchable, it is guessable — and the agent guesses using the
folder names you happened to pick, which mean something to you and nothing to it.

### What the mechanism is

A single table in `CLAUDE.md` with one row per first-level folder and three columns: the
folder, what it holds, and **when to go there**.

The third column is the one that does the work. "Deliverables, not context" describes
`projects/`. "A specific piece of client or project work — go to the one project, never load
the folder" tells the agent when to open it and when to stay out. The map is indexed by the
question being asked, not by the contents of the folder.

Three properties keep it honest:

- **It covers every first-level folder.** Including `.claude/`. The only deliberate exception
  is `.git/`, and the map says so explicitly, so an audit does not flag it every month.
- **The wikis carry their own indexes.** `knowledge/external/` and `knowledge/playbook/` each
  hold an `index.md` listing every node, and a folder-level `CLAUDE.md` describing the node
  format. A node not listed in its index is invisible to anyone following the graph, even
  though the file is right there.
- **It carries a `Last verified` date.** Which means something only if you move it when you
  verify, and never otherwise.

### What it costs you

- **The table must be updated in the same commit as the folder.** Not the same day, not the
  same week — the same commit. A folder created on Tuesday and mapped on Friday is unfindable
  for three days, and the habit of deferring is how maps die.
- **Renames are now two-file operations.** Moving `reports/` to `output/` means editing the
  map, and probably a skill or two that writes there.
- **You have to resist padding it.** Every miss creates an urge to add a row. A map with forty
  rows is not more precise than one with twelve; it is unread. When a file sits somewhere the
  manual does not describe, moving the file is usually cheaper than adding a row for it.
- **The `Last verified` date is a promise you have to keep.** Bumping it during a pass that
  verified nothing turns the whole map into a claim with no evidence behind it.

---

## 3. Failure protocol

### What breaks without it

This is the exchange that quietly destroys context systems:

> **Agent:** I couldn't find anything about that.
> **You:** It's right there — `knowledge/playbook/hold-the-fee-negotiate-scope.md`.
> **Agent:** You're right, my apologies. Reading it now.

Work continues. Nothing about the system changed, so the same miss recurs next week, and the
week after. The apology is the problem: it feels like a resolution and repairs nothing.

Over a few months you learn to stop trusting the agent to find things, and start pasting paths
by hand. At that point you are the index, and the workspace is decoration.

### What the mechanism is

A confirmed miss triggers a fixed four-step procedure, which `/route-fix` walks:

1. **Trace, don't apologize.** Every path read, in order, including the ones that returned
   nothing. Every search run and what it matched. Which row of the routing map sent the agent
   the wrong way, quoted. Then one question answered in writing: why did the map point away
   from the file?
2. **Name the failure mode.** Exactly one of four. Never two, never a new one.
3. **Fix the cause, matched to the mode.** A `confusion` miss is never fixed by trimming a
   file.
4. **Show the diff and stop.** Nothing is written without approval, and the fix has to name the
   line that prevents this specific miss from recurring. If you cannot draw that line, the fix
   is decoration.

### The four failure modes

Always these four, always lowercase, always in this order.

**`poisoning`** — a preloaded or indexed file asserts something false or stale, and the agent
believed it. *Example:* `context/team.md` still lists someone who left in June. Every session
this quarter has planned work around a person who is not there, and no session had any way to
know.

**`bloat`** — the answer was in a file the agent opened, buried in too much. *Example:* a
four-thousand-word transcript was pasted whole into a knowledge file. The one decision that
mattered is on page three. The agent read the file, missed the line, and most sessions skip
the file entirely because it is too expensive to open.

**`confusion`** — the routing map is silent, or points somewhere irrelevant, so the right file
was never opened at all. *Example:* you added an `assets/` folder and never added its row. The
agent has no reason to believe it exists, and never looks.

**`clash`** — two files disagree and the agent believed the wrong one. *Example:* the quarter
target is `6 proposals a month` in `context/priorities.md` and `10 a month` in a project
README written before the goal was revised. Both are preloaded. The agent picks one.

The distinction that matters most in practice is `bloat` versus `confusion`: bloat is a file
too fat to read, confusion is a map that never named the file. When both are true, the mode is
the **first** wrong turn, not the last.

### What it costs you

- **It interrupts the work you were actually doing.** The miss happens mid-task. The protocol
  says stop, trace, diagnose, and propose — which is exactly when you least want to. Running it
  later does not work: the trace depends on what the agent still remembers reading.
- **It requires an approval pass every time.** The protocol deliberately refuses to write
  unattended, because a repair that edits the map wrongly is worse than the original miss.
- **Some misses are the agent's fault, and the honest outcome is no edit at all.** If the agent
  never consulted the routing map, the map is not broken — the procedure was skipped. Editing
  the map to look responsive adds rows nobody needs, and a padded map is how a map becomes
  unreadable.
- **Some misses are yours.** Nothing routes to a fact that was never written down. That is not
  a routing defect; it is missing material, and it belongs to `/distill`.

---

## 4. Maintenance loop

### What breaks without it

Everything above decays, silently, and none of it announces the decay.

Precedence decays the first time someone pastes a number rather than a pointer. Routing decays
the first time a folder is created after hours. The always-loaded layer decays continuously,
because businesses change and files do not. Wiki indexes decay every time a node is written in
a hurry.

None of that throws an error. A workspace in decay looks exactly like a healthy one from the
outside — same folders, same files, same confident answers. The only observable symptom is
that the answers get subtly wrong, which is the symptom you are least equipped to notice,
because you asked the question in the first place.

### What the mechanism is

Four layers, running on different clocks.

**Every session — the hook.** `.claude/settings.json` wires `SessionStart` to
`scripts/aios-freshness-check.sh`. It is POSIX `sh`, always exits 0, and prints nothing when
nothing has drifted. It checks five things: `context/` untouched for 60 days, no audit report
in 30 days, material in `projects/` newer than the last entry in `decisions/log.md`, the
`🟡 DEMO` banner still sitting in `context/me.md`, and tracked files that look like secrets.
It fixes nothing. Silence is the success state, which is what keeps it from becoming noise you
learn to scroll past.

A hook was chosen over a cron deliberately: a hook lives in the repo and runs on this machine
every session, forever. A session-scoped cron dies when the session closes.

**Monthly — the two audits.** They ask different questions and you need both.

- `/os-audit` asks *is it still true?* Six read-only checks: path integrity, index truth,
  freshness, duplication and bloat, silent failures (tracked secrets, skills whose descriptions
  will never fire, automations listed but not wired), and context placement. Every finding is
  tagged with one of the four failure modes. The only file it writes is its own report, which
  ends in a numbered fix list — batched, ordered cheapest-first, and applied by nobody until
  you approve it.
- `/blueprint` asks *is it built right?* It scores four axes out of 25 — Routing, Precedence,
  Freshness, Loop — from banded values only, with the band set by the most severe single
  finding rather than the count. It names the finding that set each band, so two runs a month
  apart are comparable, and it ranks the top three fixes by leverage: points recovered divided
  by effort, each shipped with the exact command.

A workspace can score 95 on `/blueprint` and be full of stale facts. It can be perfectly
current and score 40 because nothing holds it together. The two failures are independent.

**On input — `/distill`.** Raw material gets split rather than filed: decisions to
`decisions/log.md`, durable facts about the outside world to `knowledge/external/`, reusable
method to `knowledge/playbook/`, action items to your task tool, and everything else discarded
out loud. Each knowledge node is one claim, not one topic, and the folder's `index.md` is
updated in the same pass. Contradictions with existing nodes get surfaced rather than
overwritten, because a silent overwrite destroys whichever version was right without leaving a
trace that there was ever a question.

**Weekly — `/leverage`, and `/skill-builder` on demand.** `/leverage` finds one recurring
friction, cuts the part of it that should not exist, and ships the smallest machine for what
survives — a checklist before a script, a script before a skill, a skill before a scheduled
agent. The run is not done until a file exists on disk that did not exist before.
`/skill-builder` runs the nine-block interview that turns a repeated process into a real skill,
and if that skill writes somewhere the routing map has never heard of, it adds the routing row
in the same pass — so the new folder is findable the moment the session that created it ends.

### What it costs you

This is the expensive mechanism, and the one people quietly drop.

- **The audits only pay off if someone runs them.** The hook will tell you an audit is overdue.
  It cannot run one. A month of overdue warnings that nobody acts on trains you to ignore the
  hook, which is worse than never installing it.
- **An audit produces a fix list, not fixes.** Both audits are read-only on purpose — an audit
  that quietly edits what it measures can never be re-run honestly. That means a second sitting
  to approve and apply, and a fix list nobody applies is a document about problems you now know
  you have.
- **`/distill` is slower than pasting.** Pasting a transcript into a file takes a keystroke.
  Splitting it into four destinations — decisions, durable outside facts, your own method,
  action items — checking for contradictions, and updating an index takes fifteen minutes. The tenth time you do it under deadline, you will want to paste.
- **A weekly ritual will lapse.** `/leverage` is designed to survive that — if nothing recurred
  this week, it tells you to log the skip rather than manufacture a candidate. But a skill run
  four times a year is not a loop.
- **Everything above is discipline, not automation.** The kit automates the *detection*. It
  does not automate the *repair*, and it never will, because a system that repairs its own
  context unattended can be confidently wrong in a new way every session.

---

## Why the loop matters most

Precedence, routing, and the failure protocol are all real mechanisms, and all three decay.

Precedence decays into duplicated numbers. Routing decays into rows pointing at folders that
were renamed. The failure protocol decays into apologies, because it only runs when someone
remembers to run it. Each of the three degrades in a way that produces no error, no warning,
and no visible difference in how the workspace looks.

The loop is the only mechanism that notices. The hook notices that nobody has audited in a
month. `/os-audit` notices that a row points at nothing and that two files disagree.
`/blueprint` notices that the mechanisms themselves were never fully built. Without them, the
other three mechanisms are a good idea you had once.

A workspace nobody maintains stops being true in about sixty days. That is not a hard
threshold, it is the rough half-life of a set of facts about a business that is still moving —
and the specific danger is not that the workspace goes empty. It is that it stays full. It
keeps answering. It sounds exactly as certain on the stale facts as on the current ones,
because nothing in a markdown file carries its own expiry date.

A system that is confidently wrong is worse than no system at all. With no system, you check.
With a wrong one, you don't.

The loop is what keeps it honest.

---

**Next:** [`anatomy.md`](anatomy.md) — the full folder tree, what each folder serves, and which
skill writes to it.
