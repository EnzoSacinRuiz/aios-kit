---
name: onboard
description: Use this on day one, right after someone clones this kit, or whenever they say "set me up," "onboard me," "let's get started," "fill in my info," or "get this ready for my business." Also fires on complaints like "this still thinks I'm the demo company," "why does the agent keep talking about a business that isn't mine," or "I never actually told it who I am." Runs a one-question-at-a-time interview, archives the demo content, and writes the operator's real context files and first rule. Safe to re-run any time — it updates in place and will not archive the demo twice.
---

# Onboard

A kit that ships with a demo company works perfectly in the demo and lies in every session
after that, because nobody replaced the example data with the truth. Every file the agent
reads at the start of a conversation — who you are, what you sell, who's on the team, what
the quarter's goal is — still describes a business that does not exist. That is `poisoning`,
and it is silent: nothing errors, the agent just confidently gets the operator wrong forever.
This skill replaces the demo with the operator's real context, on record, once.

## Procedure

1. **Check whether this is a first run or a re-run.**
   Read `context/me.md`. If it is missing, empty, or opens with
   `> 🟡 DEMO — `/onboard` replaces this file with yours.`, this is a first run — the demo is
   still installed. If the demo banner is gone and the file already describes a real operator,
   this is a re-run: skip step 3 (the demo is already archived) and go straight to the
   interview to refresh the files in place.

2. **Ask the working language before anything else.**
   Ask: "What language do you want this workspace to work in?" Everything you write from this
   point forward — every interview question, every file in `context/`, the new rule, the
   decision log entry — goes in that language. Do not translate `CLAUDE.md`, this skill, or
   anything else under `.claude/`; those stay in English so the kit behaves the same for every
   install regardless of who's running it.

3. **Archive the demo before writing anything new — first run only.**
   Don't archive by path list — the demo grows over time and a list goes stale the moment it
   does. Instead, find every file **by its first line**: the demo banner is exactly
   `> 🟡 DEMO — `/onboard` replaces this file with yours.`, and every demo file in this kit
   carries it as a global constraint. Run, in order:
   - `mkdir -p archives/demo`
   - Walk every tracked and untracked file in the repo, excluding `.git/` and anything already
     under `archives/demo/` (so a second run can't re-archive its own output), and test whether
     line 1 matches the banner **exactly**. For each match, preserve its relative path
     underneath `archives/demo/` — `knowledge/playbook/index.md` becomes
     `archives/demo/knowledge/playbook/index.md`, not a flat dump — creating parent directories
     as needed. Use `git mv <path> <dest> || mv <path> <dest>` for each: `git mv` fails
     whenever the path isn't tracked by git — a fresh clone with nothing committed yet, or a
     path a previous partial run already moved with plain `mv` — and the `mv` fallback still
     lands it in `archives/demo/` either way. Skip a path that's already gone; a previous run
     (or this loop, on a second pass) may already have moved it.
   - `mkdir -p context knowledge/external knowledge/playbook decisions` — recreate every
     directory the routing map in `CLAUDE.md` promises exists, even the ones now emptied by the
     move above, so the map never points at nothing.
   - `touch decisions/log.md`
   Tell the operator plainly, in your own words: nothing was deleted, the original demo
   content now lives in `archives/demo/` under the same paths it came from, and they can open
   it any time. Doing this before you write the new files matters — write first and archive
   after, and the operator's own answers get swept into `archives/demo/` along with the
   fictional company. Because the check is "does line 1 match," not "is this on a list," a
   second run finds no banners left to match and does nothing — archiving is idempotent by
   construction, not by a flag you have to remember to check.

4. **Run the interview. One question per message — never a form, never batched.**
   Ask each of these seven in its own message and wait for the answer before asking the next:
   1. Who are you, and what do you do?
   2. What do you sell, and to whom?
   3. What's your goal for this quarter?
   4. Who's on your team, and when should the agent pull each of them in?
   5. What tool holds the actual truth about your tasks, and about your money?
   6. What eats your time over and over, that you wish ran on its own?
   7. What should the agent never do, no matter what?
   On a re-run, show the current content of each file first and ask only what changed —
   don't re-run the full interview against someone who already answered it.

5. **Write the context files.**
   - `context/me.md` — answer 1, in plain first-person-about-the-operator terms.
   - `context/work.md` — answer 2 (what's sold, to whom), plus answer 5 written as a pointer,
     not a copy: name the tool that holds task and money status, and say explicitly that its
     numbers are never duplicated here. Add answer 6 under a short "recurring friction" note —
     this is what `/leverage` reads when it looks for something worth automating.
   - `context/team.md` — answer 4: names, roles, and the trigger for looping each person in.
   - `context/priorities.md` — answer 3. State it as the one place quarter goals get edited,
     and warn against copying it anywhere else — a copied goal is correct today and wrong the
     day it changes, because nobody remembers to update the copy.
   - `decisions/log.md` — append one entry: `[YYYY-MM-DD] DECISION: workspace initialized via
     /onboard | REASONING: replaced demo content with the operator's real context | CONTEXT:
     operator said the agent must never <answer 7, verbatim>.`

6. **Turn answer 7 into a standing rule.**
   Read `.claude/rules/README.md` first — it is the format contract every rule in that folder
   follows, and this step must match it exactly: the rule stated plainly, then the reasoning
   behind it. If the operator's answer to question 7 didn't include a reason, ask one follow-up
   — "why does that matter?" — before writing the file. Name the file after the topic, not
   after the word "rule" (`client-email-review.md`, not `rule-1.md` or `never-do.md`). Write it
   into `.claude/rules/`.

7. **Close with proof, not a summary.**
   Don't recap what you wrote. Tell the operator to ask this exact question next: "based on
   what you now know about me, what should I focus on this week?" That question only lands if
   the files you just wrote were actually read — it's the test, not a courtesy.

**Idempotent by construction.** Step 1 is the only gate that matters: the demo banner's
presence in `context/me.md` is the single source of truth for "has this already run." A
re-run always updates files in place through steps 2, 4, 5, and 6; it only skips step 3, and
only when the banner is already gone. Never check `archives/demo/` for this — a manually
copied backup there would produce a false positive and leave the demo installed forever.

## When NOT to run this

- **`context/` already describes the operator, and one fact in it is now wrong.** Don't run
  the interview again for a single correction — edit the file directly, or run `/route-fix` if
  the agent acted on the wrong fact and you need to trace why.
- **Raw material — a transcript, a document, a pile of notes — needs to become knowledge.**
  That's `/distill`, not this. `/onboard` sets up who the operator is; `/distill` is the
  ongoing feed of what they learn afterward.
