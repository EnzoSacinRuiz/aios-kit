---
name: os-audit
description: Use when the operator asks to run an OS audit, wants to know if their setup is still accurate, says things like "is my context still true", "is my setup stale", "check whether my context is still accurate", "it's been a while since I cleaned this up", "audit my workspace", "check my setup for drift", "is anything stale", "audit my AIOS", "run a freshness check", or when it has been roughly a month since the last audit report. This is a read-only check of whether the routing map, indexes, and always-loaded context still match what's actually on disk — not a score of how well the system is designed.
---

# Is it still true?

The manual, the indexes, and the wikis are claims about what exists and what is current. Nobody re-verifies a claim once it is written down, so it drifts silently — a folder gets renamed and the routing map doesn't, a transcript gets read once and never routed, a fact gets copied into two files that quietly disagree. Structure problems are loud: a missing folder throws an error. Freshness problems are silent: the agent reads a stale file, believes it, and answers confidently wrong. When the operator says "my agent keeps forgetting things," the agent isn't forgetting — it's faithfully reading an index that stopped being true weeks ago. This skill finds every place a claim and reality have separated.

**This is read-only.** You never move, rename, delete, or edit a source file during this audit. The only write is the report. Every fix gets listed for the operator to approve and run later.

## Before you start

Tell the operator to run `scripts/aios-freshness-check.sh` first, or run it yourself and read the output. **The script owns the list of what it checks — open `scripts/aios-freshness-check.sh` and read it there.** Don't restate that list here or in your report: a copy of it in this file is correct the day it's written and wrong the next time the script changes. What the hook covers is the cheap, mechanical end of what follows — drift the operator would not otherwise notice, tested on every session start with no judgement required. This audit re-verifies the same ground in full and extends it, so use the hook's output as a starting pointer and then go deeper.

## The four failure modes

Tag every finding with exactly one of these four, lowercase, no others:

- `poisoning` — a preloaded or indexed file asserts something false or stale.
- `bloat` — the fact is true but buried under too much to find or too long to trust.
- `confusion` — the routing map or index is silent, wrong, or points somewhere irrelevant.
- `clash` — two files assert different things about the same fact.

## The six checks

Run all six. Read `CLAUDE.md` once at the start and keep its routing map open — every check below refers back to it.

**1. Path integrity.** Read the routing map table in `CLAUDE.md` (the "Routing map — where everything lives" section) and the `@context/*.md` imports at the top. For every path named or implied, confirm it exists on disk (`ls`, `find`). A row pointing at a folder that isn't there is `confusion`. A folder on disk with no row in the routing map is also `confusion` — the manual said this table covers every first-level folder. Compare against the map as written: `CLAUDE.md`'s "Scope of this map" paragraph names `.git/` as the one folder deliberately left out of the map — never flag it as unrouted. Every other first-level folder, including `.claude/` (which has its own row), is in scope for this check.

**2. Index truth.** For each `index.md` under `knowledge/external/` and `knowledge/playbook/` (and any other wiki-style index you find), check both directions: (a) every `[[wiki-link]]` or listed entry resolves to a real file, and (b) every file in that folder is reachable from the index — not an orphan. A link to a file that's gone is `confusion` — the index points somewhere nothing answers. A real file the index never mentions is also `confusion` — it exists but can't be found by anyone following the graph. Either way the defect is a missing target, not a false assertion, so it is never `poisoning`.

**3. Freshness.** Three things:
   - Raw material with no distilled trace: a file in `projects/` newer than the latest entry in `decisions/log.md`, or a document that looks like source material (a transcript, a dump of notes) with nothing downstream referencing it. Tag `confusion` — the knowledge exists but never got routed anywhere findable. Scan `projects/` only, never `reports/` — `reports/` is skill-generated output by definition, and this audit writes into it too, so scanning it would flag the very report this run is about to produce.
   - `context/` untouched for a long stretch relative to how fast the business or work actually moves — don't just repeat the 60-day mechanical check, read the content and ask whether it's plausible that nothing changed. If it's stale, tag `poisoning`.
   - Demo content still installed. Scan `context/`, `knowledge/`, `projects/`, `references/` and `decisions/` — those five trees and nothing else — for any file whose **first line** is the demo banner. First line only, and only those trees: that is the same predicate `/onboard` uses to decide what counts as demo content, and it is bounded here for the same reason. A file that quotes the banner further down the page is documentation *about* the demo — this skill, `/onboard`, both READMEs, `docs/anatomy.md` — and flagging it would make this check fire on every correctly onboarded workspace, forever. A real hit means `/onboard` was never finished. Tag `poisoning`; this is the worst case because every session loads it.

**4. Duplication and bloat.** Grep for the same fact — a number, a status, a date, a name — asserted in two or more files outside the owner named in `CLAUDE.md`'s precedence table. That's `clash` even if the values currently agree, because nothing keeps them in sync. Separately, list any file over roughly 500 lines (`wc -l` across the repo, excluding `archives/`) and any clutter sitting in the repo root that isn't one of the top-level folders the routing map names — both are `bloat`.

**5. Silent failures.** Three things:
   - Secrets: `git ls-files | grep -iE '(\.env$|token|secret|key)'` — anything tracked that looks like a credential. Tag `poisoning` (a leaked credential is a false "this is safe" claim).
   - Dead-on-arrival skills: read the `description` frontmatter of every `.claude/skills/*/SKILL.md`. If you can't construct a realistic sentence the operator would actually type that contains a trigger phrase from it, the skill will never fire. Tag `confusion`.
   - Dead automations: read the "What runs on its own" table in `CLAUDE.md` against `.claude/settings.json` hooks and anything in `scripts/`. An automation listed but not wired up, or wired up but not listed, is `confusion`.

**6. Context placement.** Two directions, both defects:
   - A fact in the always-loaded layer (`context/*.md`) that's actually situational — true today, not load-bearing every session, or scoped to one project/relationship rather than the whole operation. This is `bloat`: it costs context budget in every conversation for something rarely needed.
   - Durable, reusable expertise — a method, a principle, a play the operator uses repeatedly — sitting inside a single `projects/<name>/` folder where nobody doing unrelated work will ever find it. This is `confusion`: it should be one level up in `knowledge/playbook/`, reachable from its index.

## Writing the report

Write to `reports/os-audit-YYYY-MM-DD.md` (today's date). Use this structure every time, so two runs are comparable:

```markdown
# OS Audit — YYYY-MM-DD

## Summary
One paragraph: how many findings, which failure mode dominates, whether anything is urgent
(active poisoning in the always-loaded layer or a tracked secret always counts as urgent).

## Findings by failure mode

### poisoning
- [path] — what's false or stale, and what it would make the agent wrongly believe.

### bloat
- [path] — what's buried or oversized, and what it costs to search around it.

### confusion
- [path] — what's missing, silent, or unreachable, and what question it would fail to answer.

### clash
- [path A] vs [path B] — the two conflicting claims, and which one the precedence table says should win.

(Omit a subsection entirely if that mode had zero findings — don't write "none found.")

## Fix list (batched, for approval)
Numbered, ordered cheapest/highest-leverage first. Each line: what to change, in which file,
and which finding above it resolves. Nothing on this list has been applied yet.

1. ...
2. ...
```

Do not apply any fix from that list in this run. Stop once the report is written and tell the operator it's ready for their approval.

## When NOT to run this

Run `/blueprint` instead when the question is whether the system is *built right* — structure, coverage, whether the required pieces are in place — rather than whether what's already built is still *true*. `/blueprint` scores design quality out of 100 and doesn't check dates, staleness, or drift. This skill assumes the design is sound and checks whether reality has moved out from under it. If the operator wants both a build-quality score and a truth check, run this one first, then `/blueprint` — the audit surfaces the facts and `/blueprint`'s Freshness axis then scores against a report that actually exists.
