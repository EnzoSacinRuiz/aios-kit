---
name: skill-builder
description: Turns a process the operator keeps repeating by hand into a real skill instead of one more one-off prompt they'll have to re-explain next time. Fires on requests like "my agent doesn't know how to do this yet", "I keep typing the same instructions every time", "turn this into a skill", "can you make a skill for this", "I do this every week and it's always slightly different", "build me a command for X", "why do I have to explain this from scratch every time", "make this repeatable", or "I wrote this out again, can we automate it". Also fires when the operator describes a multi-step task they say they do "every time" or "constantly" without naming a skill that already covers it.
---

# Skill Builder

The failure this prevents has two shapes, not one. Either the skill you write never fires,
because its description doesn't say what the operator actually types when they hit this
problem — or it fires and produces the wrong thing, because the task was ambiguous and the
model filled the gaps with its own guess instead of the operator's intent. Both failures are
cheap to prevent and expensive to live with: a clarifying question costs the operator twenty
seconds, once. A skill that guesses wrong costs those twenty seconds back, plus a rewrite,
every single time it runs after that. This skill exists to ask before it writes.

## Procedure

1. **Confirm this is one process, not two.** Ask what the operator wants automated, in their
   own words. If the answer describes two jobs joined by "and" — draft the thing *and* send
   the thing, research *and* write — stop and say so: that's two skills, not one. Get
   agreement on the single job before block 1.

2. **Run the interview as nine separate messages, one block per message, in this exact order.**
   Do not collapse blocks into one wall of questions and do not skip a block because the answer
   seems obvious — an obvious-seeming answer is exactly the kind that turns out to be wrong.
   Wait for the operator's reply before sending the next block.

   - **Block 1 — Identity.** Ask for the skill's name (the directory name it will live at) and
     a one-line purpose. Reject a name that's a verb-less noun ("reports") — push for a name
     that names the action ("write-status-report").
   - **Block 2 — Persona.** Ask who the skill is being when it runs, and what it's expert in.
     A skill with no persona defaults to a generic assistant voice, which is how client-facing
     output ends up sounding like nobody in particular.
   - **Block 3 — Task.** Ask for the single job in one sentence. If a second sentence shows up
     with "and", that's the two-skills problem from step 1 again — resolve it before moving on.
   - **Block 4 — Inputs.** Ask what the operator will hand the skill each time, and — separately
     — what the skill should do when that input is missing or incomplete. "Ask the operator"
     is a valid answer here; "guess" is not, and if the operator says "just figure it out,"
     push back once before accepting it.
   - **Block 5 — Instructions.** Ask for the ordered steps the operator actually follows today,
     by hand. Write these down as the numbered procedure verbatim — don't paraphrase into
     something more generic. A step the operator didn't actually describe is a step you invented.
   - **Block 6 — Output.** Ask for the exact output format and the exact destination path. Not
     "a summary" — what kind of file, in what shape, saved where. If the answer names a folder
     this repo doesn't have yet, flag it now, not at step 5 below.
   - **Block 7 — Tools.** Ask what the skill needs to read, what it needs to write, and what
     external tool or service (if any) it needs to call. Write the shortest tool list that
     covers what was described — an unused tool listed "just in case" is a tool the model will
     try to justify using.
   - **Block 8 — Configuration.** Collect **at least five distinct trigger phrases, in the
     operator's own words** — not your paraphrase of their intent. This is the block where
     firing is won or lost: a description full of correct-sounding generic language is the
     single most common reason a skill never fires. Explicitly ask how the operator would
     *complain* about this problem when it's bugging them ("I keep having to…", "why do I
     always…"), not only how they'd request the solution — a complaint and a command read
     completely differently to a description match.
   - **Block 9 — Validation.** Ask how the operator will know a run was good, and ask for one
     concrete example of a bad output to avoid. A bad-output example is worth more than another
     paragraph of instructions, because it rules out a failure mode instead of describing a
     success.

3. **Check the target folder against the routing map before writing.** Read `CLAUDE.md`'s
   routing map. If the destination path from block 6 lands inside a folder the map already
   lists, use it as-is. If it doesn't — a new top-level folder, or a new subfolder the map is
   silent on — tell the operator you're adding a row for it, and do so in the same pass (see
   step 5). Writing to an unmapped folder without updating the map recreates the exact failure
   `/route-fix` exists to catch: a file nobody can find because nothing points at it.

4. **Write `.claude/skills/<name>/SKILL.md`** using the nine answers directly — every block
   maps to a part of the file:
   - Frontmatter `name` from block 1; `description` built from block 8's five-plus phrases plus
     one line of context from block 3, written the way a user types, not the way a spec reads.
   - Opening: one or two sentences naming the failure the skill prevents (drawn from what goes
     wrong today without it — usually visible in blocks 3 and 9's bad-output example), not a
     restatement of the task.
   - Numbered procedure from block 5, each step naming what to read, what to ask, what to
     write — no step that says "handle it appropriately" or "as needed."
   - Output section from block 6 with the literal path.
   - Tools noted inline wherever a step uses one, matching block 7 — don't list a tool the
     procedure never calls.
   - A `## When NOT to run this` section naming at least one skill from this kit's seven that
     the new skill could get confused with, and the one-line distinction — ask the operator if
     it isn't obvious from the interview.
   - Keep the whole file under 200 lines. If the interview produced more than that, the task
     was probably still two jobs — go back to step 1.

5. **Add the routing row, if step 3 found a new folder.** Edit `CLAUDE.md`'s routing map table
   in the same pass: new folder name, what it holds, when to go there. Do this before showing
   the finished skill, not after — a skill that writes to a place the map doesn't mention is
   invisible the moment this session ends.

6. **Show the finished file to the operator before treating this as done.** Print the full
   `SKILL.md`, not a summary of it. Ask them to try the exact trigger phrases from block 8
   against the description out loud — if any of the five don't obviously match, fix the
   description now, because this is the cheapest moment this skill will ever have to fix it.

## When NOT to run this

`/leverage` is for finding what's worth automating in the first place — it surfaces friction
across a week of work and decides what's worth building. This skill is for *after* that
decision is made: the operator already knows the process, already knows it repeats, and needs
it turned into a real skill. If the operator isn't sure yet what to automate, send them to
`/leverage` first. This skill also never runs an existing skill on the operator's behalf — if
a skill covering this already exists on disk, say so and stop instead of writing a duplicate.
