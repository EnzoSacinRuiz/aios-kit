---
name: blueprint
description: Scores this workspace out of 100 on how well it is built — routing, precedence, freshness, and the maintenance loop — and names the three highest-leverage fixes with the exact command for each. Fires on "run blueprint", "score my setup", "is my AIOS built right", "grade my workspace", "how solid is my context setup", "give me a score out of 100", "rate how this thing is organized", and on complaints like "everything is up to date and my agent still gets things wrong", "this is just a pile of markdown files and I don't know if it's any good", or "I set this up months ago and I have no idea if it's still put together right". Also fires when the operator asks what to fix first, or wants to see whether last month's fixes moved the number.
---

# Blueprint

The failure this prevents: a workspace that is full and current and still structurally wrong —
no map, the same number living in four files, and no loop keeping any of it honest. It reads
as healthy right up to the session where the agent answers confidently out of a stale copy,
and nothing in the system was ever going to catch that.

`/os-audit` asks whether the workspace is still **true**. This asks whether it is **built
right**. A workspace can score 95 here and be full of stale facts; it can be perfectly current
and score 40 because nothing holds it together. Run both.

## Procedure

1. **Take the inventory before scoring anything.** Read `CLAUDE.md` in full — its routing map,
   its precedence table, its automation table. Then collect the ground truth you will score it
   against. Run every command; do not score from memory of the manual.

   ```sh
   ls -d */ | grep -v '^\.'            # every first-level folder on disk
   ls .claude/skills/                  # skills that actually exist
   wc -l context/*.md                  # size of the always-loaded layer
   cat .claude/settings.json           # is the hook wired
   ls -lt reports/ | head -20          # what the loop has produced
   tail -20 decisions/log.md           # is the log alive
   find . -path ./archives -prune -o -name '*.md' -mtime -30 -print  # what moved this month
   ```

   Never run a `git` command in this skill. Use file modification times. A workspace cloned
   yesterday has one commit and thirty files older than the clone — git history scores it
   wrong every time.

2. **Score Routing (25).** Is there a map, and does it point at things that exist?
   - Every first-level folder on disk has a row in the routing map. Count the ones that don't.
   - Every path the map names exists on disk. `test -e` each one. Count the dead paths.
   - No row points somewhere that exists but holds something else — a row that sends you to
     the wrong real place is worse than a missing row, because you stop looking.
   - Each wiki-shaped folder (`knowledge/external/`, `knowledge/playbook/`) has an `index.md`.
   - **15 vs 10:** one folder on disk the map never mentions, everything else resolving, is a
     15 — one real gap. Half the folders unmentioned, or a whole named layer whose rows point
     at directories nobody ever created, is a 10 — the map is describing a workspace that only
     partly exists.

3. **Score Precedence (25).** Does each fact live in exactly one place?
   - `CLAUDE.md` has a precedence table naming an owner for each contested class of fact.
   - Pick the distinctive strings out of the owned files — the quarter's target numbers, dated
     goals, headcount — and grep for them everywhere else:
     `grep -rn "<the number>" --include='*.md' . | grep -v '^./archives'`. Every hit outside
     the owner is a copy.
   - No status that a task tool owns is written into a file. Grep for status words
     (`in progress`, `won`, `closed`, `blocked`) attached to named projects outside `reports/`.
   - No money or runway figure anywhere in `context/`.
   - Nothing enumerates what the disk owns — a written list of "the skills we have" or "our
     projects" is a copy that goes stale the next time someone adds one.
   - **15 vs 10:** one number copied into one second file — the quarter target repeated in a
     project README — is a 15. No precedence table at all, or a whole class of fact routinely
     duplicated (every project file restating status the task tool owns), is a 10: the
     discipline isn't implemented, it just hasn't bitten yet.

4. **Score Freshness (25).** Is what gets preloaded every session still true?
   - The four `@import`ed files exist and none carries a demo banner:
     `grep -rl "DEMO" context/`. A demo string in the always-loaded layer is `poisoning` by
     construction — it is false in every session forever.
   - No `context/` file untouched for more than 60 days: `find context -type f -mtime +60`.
   - The always-loaded layer stays small. Over ~200 lines total across the four files is
     `bloat` — flag it; over ~400 it is a real finding.
   - Each `index.md` is at least as new as the newest node beside it:
     `ls -lt knowledge/external/ | head -5`. A frozen index means nodes exist that nothing
     points at.
   - **15 vs 10:** one always-loaded file untouched past 60 days while the other three are
     current is a 15. The demo still installed in one or two of the four, or an index frozen
     since scaffolding while nodes kept arriving, is a 10 — the layer is partly somebody
     else's workspace.

5. **Score Loop (25).** Can the system repair and grow itself — and is it actually running?
   Both halves count. Machinery that exists and never fires scores the same as machinery that
   was never built.
   - `.claude/settings.json` wires the `SessionStart` hook, and the script it names exists and
     exits 0: `sh scripts/aios-freshness-check.sh; echo "exit=$?"`.
   - An audit report inside 60 days: `find reports -name 'os-audit-*' -mtime -60`.
   - A skill added or edited inside 30 days: `find .claude/skills -name SKILL.md -mtime -30`.
   - `decisions/log.md` has an entry inside 30 days.
   - Every automation that writes files has a row in the manual's automation table. An
     undocumented one scores as a finding here — output arrives, nobody knows from where, and
     nobody notices when it stops.
   - **15 vs 10:** hook wired, script clean, skills present, but no audit in 60 days is a 15 —
     one habit lapsed. The hook pointing at a script that is missing or exits non-zero, or
     reports arriving while no skill and no decision moved in a month, is a 10: the loop runs
     on one cylinder.

6. **Convert findings to a band. Use only these six values.** No half points, no 22.

   | Score | Means |
   |---|---|
   | 25 | No findings. The mechanism exists, is complete, and is being used. |
   | 20 | Cosmetic only — wording, ordering, a stale "last verified" date. Nothing an agent would act on wrongly. |
   | 15 | One real gap. The mechanism is built and working; one thing slipped through it. |
   | 10 | Partly unimplemented. The mechanism exists in outline but does not cover what it claims to. |
   | 5 | The mechanism is absent. No map, no precedence table, no dates, no loop. |
   | 0 | Actively wrong. It points somewhere false and an agent following it lands on the wrong answer. |

   **Two deterministic rules, so a second run lands on the same number:**
   - The band is set by the **most severe single finding**, never by the count. One dead path
     is a 15 whether or not the rest of the map is perfect.
   - If **two or more distinct findings** land in that same band, drop exactly one step
     (25→20→15→10→5→0). Floor at 0. Do not drop twice for four findings.

   Write down the finding that set each band. That sentence is what makes the next run
   comparable — a score with no named cause cannot be re-derived.

7. **Rank the top three fixes by leverage, not by severity.** Leverage is points recovered
   divided by effort. A 15 you can close in two minutes outranks a 5 that needs an afternoon.
   Break ties by: the lowest axis first, then whichever fix unblocks another axis — repairing
   the routing map usually raises Precedence too, because you cannot tell what is duplicated
   until you know where things live.

   Every fix ships with the exact command or the exact edit. Not "improve the routing map" —
   `add a row for assets/ to the routing map in CLAUDE.md`. Not "run an audit" — `/os-audit`.
   A fix the operator has to design themselves will not get done.

8. **Write the report** to `reports/blueprint-YYYY-MM-DD.md`, using today's date. Print the
   score line in the session too — the operator should not have to open a file to see it.

   ```markdown
   # Blueprint — YYYY-MM-DD

   **Score: NN/100** — Routing NN · Precedence NN · Freshness NN · Loop NN
   _(Previous run: NN/100 on YYYY-MM-DD)_

   ## What is built right
   <Two to four lines. Name the mechanisms that scored 25 or 20 and why.
   Strengths are not filler — they are what the operator must not break while fixing.>

   ## Score detail
   | Axis | Score | The finding that set the band |
   |---|---|---|
   | Routing | NN | … |
   | Precedence | NN | … |
   | Freshness | NN | … |
   | Loop | NN | … |

   ## Top three fixes, by leverage
   1. **<fix>** — recovers ~N points on <axis>. Run: `<exact command or edit>`
   2. **<fix>** — recovers ~N points on <axis>. Run: `<exact command or edit>`
   3. **<fix>** — recovers ~N points on <axis>. Run: `<exact command or edit>`

   ## Everything else found
   <The findings that did not make the top three, one line each, so the next run
   is not surprised by them.>
   ```

9. **Close by telling them to re-run.** Before writing the report, check for a previous one
   (`ls reports/blueprint-*.md`) and fill the previous-score line. Then say it plainly: do the
   three fixes and run `/blueprint` again — the number moves, and the movement is the only
   proof the fixes were real. A score you take once is a verdict. A score you take monthly is
   a control loop, and this workspace stops being true in about sixty days without one.

## Rules

- **Read-only except the report.** You score; you do not repair. If a fix is obvious and small,
  it still goes in the report as a command, not into the working tree. An audit that quietly
  edits what it measures can never be re-run honestly.
- **Never run a `git` command.** Not to check history, not to check status.
- **Never score an axis you did not run the commands for.** If a command fails, say the axis is
  unscored and why. A guessed 20 poisons the comparison with every future run.
- **Ignore `archives/`** in every grep and every count. Retired material is meant to be stale.

## When NOT to run this

- **The workspace has stale facts, not structural problems** — the map is fine, the numbers in
  it are old. That is `/os-audit`. It checks whether every claim the manual makes is still
  true; this checks whether the mechanisms that keep claims true exist at all. A workspace can
  pass one and fail the other badly in either direction.
- **You just missed one specific thing that was there** — that is `/route-fix`. It repairs the
  single cause behind a single miss. Do not run a full scoring pass to fix one bad routing row;
  the score will tell you nothing you did not already learn from the miss.
- **The demo is still installed and the operator has never set this up** — run `/onboard`
  first. Scoring a demo workspace measures the template, not their workspace, and the number
  is meaningless.
- **The operator wants something built, not measured** — `/leverage` finds the week's friction
  and ships one machine for it; `/skill-builder` turns a repeated process into a skill. This
  skill produces a diagnosis and stops.
