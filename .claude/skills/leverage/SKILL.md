---
name: leverage
description: Run this weekly, or when the operator says "let's level up", "what should I automate next", "find me leverage this week", "run my Friday automation review", "what's eating my time this week", or the complaint "I keep doing this by hand every week". Finds one recurring friction, cuts the part of it that shouldn't exist, and ships the smallest machine for what survives — never a planning conversation, always a file written by the end of the run.
---

# Leverage

The failure this prevents: automating a task that should not exist in the first place. That
makes a bad process faster, not better — and now it scales, because a machine repeats a
mistake exactly, every time, without getting tired of it.

## Procedure

### 1. Friction

- **Ask the operator:** "What stole your time this week?" Get a list of candidates, each with
  a rough hour estimate. Don't accept a vague answer like "meetings" — push for the specific,
  repeated action inside it ("re-typing meeting notes into three places").
- **Read `decisions/log.md`** for entries from the last few weeks and note anything that reads
  like the same friction showing up more than once. A friction that appears twice in the log
  is a pattern; a friction that appears once is an anecdote.
- **Pick one candidate.** Bias toward what recurs, not toward what was worst. The worst week of
  the year is not a pattern — it is an outlier, and building a machine for an outlier wastes
  the build on a case that won't come back.
- Write nothing yet. This step only narrows the field to one.

### 2. Cut

- **Ask:** "What part of this should not exist at all?" Before any automation, find the step
  that is pure waste — a report nobody reads, an approval nobody needs, a format conversion
  that exists only because two tools disagree.
- **Check `references/sops/`** for a file already describing this process. If one exists, read
  it end to end and mark which steps survive the cut and which don't.
- Effectiveness comes before efficiency: a faster version of the wrong process is worse than
  the slow right one, because the slow one at least stays contained to one person's slow week.
  A fast wrong process contaminates every run after this one.
- Decide, out loud, what gets deleted. If the honest answer is "nothing, the whole process
  earns its keep," say so and move on to step 3 with the process intact.

### 3. Machine

- **Build the smallest thing that handles what survived the cut.** Prefer the least machinery
  that works: a checklist beats a script, a script beats a skill, a skill beats a scheduled
  agent. Only reach for more machinery than the friction justifies if the friction is going to
  keep costing hours every week.
- **Name who maintains it** and **how you will know when it breaks** — a stale output, a
  missing file, a step someone skips. Write both into the artifact itself, not into a separate
  note that nobody will read again.
- **Ship exactly one file.** If the machine is a new repeatable workflow, hand off to
  `/skill-builder` now and let it write `.claude/skills/<name>/SKILL.md` — don't draft the
  skill file yourself here. If the machine is smaller than a skill (a checklist, a short
  script), write it directly to `references/sops/` or `scripts/`, whichever the routing map
  says owns that kind of file.
- **Append one entry to `decisions/log.md`**, in the standing format
  `[YYYY-MM-DD] DECISION: … | REASONING: … | CONTEXT: …`: DECISION is what you built,
  REASONING is what you cut and why, CONTEXT is which friction you picked and where the
  artifact lives.

## One run = one shipped artifact

If this run ends and no file exists on disk that didn't exist before, the run did not happen —
it was a conversation about automating something, which is exactly the kind of thing this
skill exists to cut. Don't report the run as done until you can point at the artifact's path.

## When NOT to run this

- **`/skill-builder`** — if the operator already knows exactly what they want built ("turn my
  weekly report process into a skill"), skip straight to `/skill-builder`. This skill exists
  to find *what* to build when that isn't clear yet; running it on a known target just adds two
  steps of friction-finding for a friction that's already found.
- If nothing recurred this week and last week's build is still unproven, don't force a new
  candidate. Log that in `decisions/log.md` — same format, e.g.
  `[YYYY-MM-DD] DECISION: skipped this week's leverage run | REASONING: nothing recurred and
  last week's build is still unproven | CONTEXT: … ` — and skip the run rather than shipping a
  machine for a friction that might not come back.
