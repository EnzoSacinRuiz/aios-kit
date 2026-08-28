---
name: route-fix
description: Repairs the workspace after you missed something that was there all along. Use when the operator says "it's right there", "that file exists", "you looked in the wrong place", "why didn't you find that", "you missed it again", "my agent keeps forgetting things it already knows", "you keep asking me for stuff I already wrote down", "route-fix", "fix the routing", or pastes a path you should have found on your own. Also use in reverse, when the manual promises a file or folder that is not on disk — "that path doesn't exist", "the routing map is lying". Diagnoses the miss as poisoning, bloat, confusion, or clash, fixes the cause, and shows the diff before writing anything.
---

# route-fix

The agent says "I couldn't find it." The operator says "it's right there," pastes the path, and
work continues — and the same miss happens again next week, because nothing about the system
changed. The apology is the problem: it feels like a resolution and fixes nothing.

Run this the moment a miss is confirmed, while you still remember what you read.

---

## 1. Trace

Not an apology. Not "you're right." A trace. Write out, in order:

- **Every path you read**, in the order you read them, including the ones that returned nothing.
- **Every search you ran** — the exact query, and what it matched.
- **Which row of the routing map in `CLAUDE.md` sent you there.** Quote the row.
- **Where the answer actually was**, and how the operator found it.

Then answer one question in writing: *why did the map point away from the file?*

If you never consulted the routing map at all, stop — **that is the finding.** No file is broken.
Say so plainly, name the step you skipped, and go to "When the system is not at fault." Editing
the map to cover for a lookup you never did makes the map worse.

## 2. Name the failure mode

Exactly one of four. Never two, never a new one.

| Mode | What happened |
|---|---|
| `poisoning` | A preloaded file asserted something false or stale, and you believed it. |
| `bloat` | The answer was there, in a file you opened, buried in too much. |
| `confusion` | The routing map is silent, or points somewhere irrelevant. You never opened the right file. |
| `clash` | Two files disagree, and you believed the wrong one. |

**Telling them apart.** Two questions, in this order:

1. **Can you quote a specific line that pointed you wrong?**
   - **No** → the defect is an absence. Go to question 2a.
   - **Yes** → the defect is an assertion. Go to question 2b.
2. **a. Did you open the file that held the answer?** Opened it and missed it inside → `bloat`.
   Never opened it, because nothing sent you there → `confusion`.
   **b. Is a correct version of that same fact also somewhere in the workspace?**
   Yes → `clash` (two owners, you picked the wrong one). No → `poisoning` (the only copy is wrong).

Second tie-breaker, when a case still reads both ways: delete the offending line and ask whether
the workspace can still answer the question. `clash` → yes, the other file answers it.
`poisoning` → no, and that is the correct state; a workspace that says nothing beats one that
lies. For `bloat` vs `confusion`: bloat is a file that is too fat to read; confusion is a map
that never named the file. If both are true, the mode is **the first wrong turn, not the last** —
a map that misrouted you is `confusion` even if the file it hid was also enormous.

Write one sentence of evidence for the mode you chose. If you cannot cite the line, the file, or
the missing row, you have not diagnosed it yet.

## 3. Fix the cause, matched to the mode

Only the fix that matches the mode. A `confusion` miss is never fixed by trimming a file.

**`poisoning`** — correct the fact, or delete it if you cannot verify it. Then hunt the copies:
grep the workspace for the stale value, the stale name, and the phrase around it. A false fact
that was pasted into three files is three bugs. Check `context/` first — anything wrong there is
wrong in every session you will ever open. Then apply precedence: if the fact has a real owner,
the other copies become pointers, not corrections.

**`bloat`** — split or index. Split when the file holds two subjects that were never one: move
the smaller subject to its own file and add its routing row. Index when the subject is one but
long: put a table of contents at the top, one line per section, with the answer's location
named in the operator's own words. Ceiling: if you would have to skim more than a screen to
answer the question again, it is still bloated.

**`confusion`** — the map or the location is wrong, so change one of them. Add the missing
routing row, or correct the one that misled you. If the file sits somewhere the manual does not
describe, move it to where the manual says it belongs — that is cheaper than a new row and keeps
the map short. If the miss was vocabulary — the operator's word for the thing appears nowhere in
the file or the map — add their word to the relevant `index.md` and to the "When to go there"
column. The map is indexed by how the operator asks, not by how the file is titled.

**`clash`** — apply the precedence rule in `CLAUDE.md`. Pick one owner: the file the precedence
table already names, or the one closest to where the fact is produced. Delete the fact from the
other file and replace it with a pointer to the owner. Two files that both state a fact will
disagree eventually; you are not choosing today's winner, you are removing the second copy.
If the precedence table has no row for this kind of fact, add one — that is a rule change, and
step 4 makes you log it.

## 4. Show the diff and stop

**Never write without approval.** Present, in one block:

- The mode and the one-sentence evidence.
- Every file you would touch, with before/after for each changed line.
- Which line of the fix prevents the specific miss that just happened. If you cannot draw that
  line, the fix is decoration — go back to step 2.

Then stop and wait. When the operator approves, apply it, and finish the bookkeeping:

- **The fix changed a rule** — a precedence row, a naming convention, where a class of file
  lives — append it to `decisions/log.md`. One dated entry, matching the format already in that
  file: what changed, why, and the miss that triggered it. A rule changed without a log entry is
  a rule the next session will not know about.
- **The fix changed routing** — a row added, corrected, or removed in the routing map, or a file
  moved — update the `Last verified` date in `CLAUDE.md`. Only then; do not bump the date for a
  fix that left the map untouched, or the date stops meaning anything.

---

## Reverse mode — the manual promises a path that is not on disk

Same class of defect, running the other way: `CLAUDE.md` names a folder, or an `index.md` links a
file, and it is not there. The agent goes looking, finds nothing, and reports an absence that the
manual insists is presence. That is a **dead path**.

Run the same procedure. The trace is the promise you followed and the empty result. The mode is
`confusion` — the map points somewhere irrelevant, in this case at nothing — unless the manual
also asserts a fact about the missing thing's contents, which makes it `poisoning`. The fix is
binary and you must choose, not defer: **delete the row, or create the thing.** Create it when
the operator wants it and it will be filled this week. Delete it otherwise. A path that is
neither deleted nor created will be followed again by every future session.

## When the system is not at fault

Some misses are yours, and saying so is faster than a fake repair. It is not a system defect if:

- **The fact was never written down.** Nothing routes to what does not exist. That is `/distill`,
  not this skill.
- **The file was created after you searched.** Nothing to fix. Say when you looked.
- **You had the path and did not read it.** Own it. Do not edit a map that was already correct.
- **You never opened the routing map.** Your procedure failed, not the map's content.

In all four, produce the trace anyway — steps 1 and 2 cost a paragraph — and stop there. Do not
propose a file change. Edits made to look responsive add rows nobody needs, and a map padded with
rows that fixed nothing is how a map becomes unreadable.

One exception worth catching: if the operator's word for the thing is nowhere in the workspace,
that is not a miss you own. That is `confusion`, and step 3 has the fix.

## When NOT to run this

- **The information genuinely does not exist yet** — no file holds it, no one wrote it down.
  That is `/distill`: raw material becomes routed knowledge. `/route-fix` repairs a route to
  something real; it cannot route to nothing.
- **Nothing failed and you want a health check.** That is `/os-audit`, which sweeps every claim
  the manual makes against the disk on a schedule. The difference is the trigger: `/os-audit`
  runs on the calendar and finds defects nobody hit yet; `/route-fix` runs on a confirmed miss
  and starts from the trace of that specific miss. If you cannot name the miss, you want the
  audit.
- **The workspace scores badly overall** and you want to know what to build next — `/blueprint`.

---

**A file found by hand and not re-routed will be lost again.** The operator handing you the path
resolved this conversation. It changed nothing about the next one.
