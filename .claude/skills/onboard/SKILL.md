---
name: onboard
description: Use this on day one, right after someone clones this kit, or whenever they say "set me up," "onboard me," "let's get started," "fill in my info," or "get this ready for my business." Also fires on complaints like "this still thinks I'm the demo company," "why does the agent keep talking about a business that isn't mine," or "I never actually told it who I am." Runs a one-question-at-a-time interview, archives the demo content, and writes the operator's real context files, wiki indexes, voice profile, and first rule. Safe to re-run any time — it updates in place, will not archive the demo twice, and will not overwrite a wiki index that already holds real nodes.
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
   - `find projects -mindepth 1 -type d -empty -delete` — a project folder that existed only to
     hold the demo's files is now an empty shell, and an empty `projects/<name>/` reads as a
     live engagement that isn't one. Run this **only** under `projects/`: the routing map names
     no individual project, so nothing there is promised to exist.
   - `mkdir -p context knowledge/external knowledge/playbook decisions references/sops` —
     recreate every directory the routing map in `CLAUDE.md` promises exists, even the ones now
     emptied by the move above, so the map never points at nothing. These five are the opposite
     case from the line above: the map declares them, so they come back empty rather than being
     swept away.
   - `touch decisions/log.md`
   Directories are not enough. The banner predicate is right for demo *content*, but it also
   catches files that are **machinery** — an `index.md` is the entry point the routing map
   promises, and `references/voice.md` is a routing row of its own. Step 5 writes both back;
   an empty `knowledge/` folder or a missing voice profile is the kit failing its own Routing
   check, produced by its own installer. (The two `knowledge/*/CLAUDE.md` ingestion manuals
   carry no banner on purpose — they are format contracts, not demo data, and survive this
   step untouched.)
   Tell the operator plainly, in your own words: nothing was deleted, the original demo
   content now lives in `archives/demo/` under the same paths it came from, and they can open
   it any time. Doing this before you write the new files matters — write first and archive
   after, and the operator's own answers get swept into `archives/demo/` along with the
   fictional company. Because the check is "does line 1 match," not "is this on a list," a
   second run finds no banners left to match and does nothing — archiving is idempotent by
   construction, not by a flag you have to remember to check.

4. **Run the interview. One question per message — never a form, never batched.**
   Ask each of these eight in its own message and wait for the answer before asking the next:
   1. Who are you, and what do you do?
   2. What do you sell, and to whom?
   3. What's your goal for this quarter?
   4. Who's on your team, and when should the agent pull each of them in?
   5. What tool holds the actual truth about your tasks, and about your money?
   6. What eats your time over and over, that you wish ran on its own?
   7. What should the agent never do, no matter what?
   8. When the agent writes as you, how should it sound — and what should it never sound
      like? Ask for the register too: does anything change between an internal note and
      something a client reads?
   **If the answer to question 4 is "nobody, I work alone," don't accept it and move on.**
   Taken literally it produces a two-line `context/team.md` in the always-loaded layer — a file
   that costs budget in every session and answers no question anyone will ask. Ask the
   follow-up instead: who do you rely on who isn't on your payroll? A subcontractor you call
   when the work overflows, a bookkeeper or accountant, a designer or editor you always use,
   a lawyer, a peer you check hard decisions with. Record each one exactly as you would an
   employee — name, what they cover, and the trigger that pulls them in — and say plainly in
   the file that these are outside the company. Someone always has a team; it is just not
   payroll. If they genuinely rely on no one at all, write that as the one line it is and move
   on — a short true file beats an invented roster.

   On a re-run, show the current content of each file first and ask only what changed —
   don't re-run the full interview against someone who already answered it.

5. **Write the operator's files — `context/`, both wiki indexes, and the voice profile.**
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
   - `knowledge/external/index.md` and `knowledge/playbook/index.md` — the demo's indexes were
     archived in step 3, and the routing map promises each of these folders is a
     `[[wiki-link]]` graph **with its own `index.md`**. Write both back as empty stubs, not as
     content: a `# knowledge/<folder> — index` title, one line naming what this wiki holds and
     pointing at the `CLAUDE.md` beside it for the node format, then a `## Nodes` heading with
     nothing under it. Invent no nodes — the list stays empty until `/distill` writes the
     first one, and `/distill` needs the file to exist so it has something to append to.
     **On a re-run, only create these if they are missing.** An index that already lists real
     nodes is months of accumulated knowledge — overwriting it with a stub would be the worst
     damage this skill could do.
   - `references/voice.md` — answer 8, as a short profile with four parts: tone, what the
     operator sounds like, what they avoid, and how internal writing differs from
     client-facing. The routing map promises a voice profile in `references/`, and the demo's
     was archived — leaving this unwritten points that row at nothing. Write only what the
     operator actually said; if answer 8 was thin, say so in the file and leave the sections
     short rather than filling them in. A guessed voice is `poisoning` in the one file whose
     entire job is to sound like them.

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
