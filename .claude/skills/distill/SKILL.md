---
name: distill
description: Turns raw material — a meeting transcript, a PDF, a pasted pile of notes, a call recording summary, a document someone sent over — into routed, linked knowledge instead of one giant dumped file. Fires on requests like "distill this transcript", "process these meeting notes", "I just got off a call, here's the dump", "turn this into knowledge", "file this away properly", "my knowledge base is just a pile of unprocessed transcripts", "I keep pasting raw notes and nothing happens to them", "where does this go", or "ingest this document". Also fires when the user pastes a large block of raw text (a transcript, an email thread, a call recap) with no further instruction — that paste is the raw material, not a request to summarize it back to them.
---

# Distill

The failure this prevents: raw material gets pasted whole into a knowledge file. Nothing gets
decided, nothing gets routed, nothing gets linked — a transcript just becomes a longer file.
Six months later the agent reads four thousand words to find one fact, most sessions never
read it at all, and the one decision buried on page three of the transcript never made it to
`decisions/log.md`. That's `bloat` plus a decision that, for every practical purpose, was
never made.

## Procedure

1. **Read the raw input in full.** Don't skim for a summary — you're about to split it into
   pieces, and you can't split what you haven't read. Never copy it verbatim into a knowledge
   file. If you cannot tell what kind of material this is (transcript, document, notes),
   ask before routing.

2. **Route into four destinations, not one.** Most of the value in raw material is destroyed
   by filing it in a single place — a transcript is never one kind of thing. Go through the
   material looking for each of these separately, because a single paragraph can contain more
   than one:
   - **Decisions** — something was decided, chosen, ruled out, or committed to. Append to
     `decisions/log.md` in the format `[YYYY-MM-DD] DECISION: … | REASONING: … | CONTEXT: …`.
     Use today's date, not the date of the source material, unless the operator says otherwise.
   - **Durable facts about the outside world** — a client, a prospect, a competitor, a market
     condition, something true about someone or something outside the operator's own company.
     Goes to `knowledge/external/` as one or more knowledge nodes (see step 4).
   - **The operator's own reusable method** — a principle, a play, a way of doing the work that
     will apply again next time, not just this once. Goes to `knowledge/playbook/` as one or
     more knowledge nodes (see step 4).
   - **Action items** — something someone needs to go do. These do not go in a knowledge file
     at all. Check the precedence table in `CLAUDE.md` for "Task and project status" — that
     names the task tool this operator actually uses (ClickUp, Linear, Notion, or similar).
     Send action items there. If no task tool is configured, say so and ask where they should
     go rather than inventing a file for them.

   If a piece of material doesn't fit any of the four, it's probably not worth keeping —
   raw material is not automatically knowledge. Say what you're leaving out and why.

3. **Check for contradictions before you write.** Before adding or editing a node, search
   `knowledge/external/` and `knowledge/playbook/` for existing claims on the same subject. If
   the new material contradicts one:
   - Do **not** silently overwrite it. That's `clash`, and it destroys whichever version was
     right without leaving a trace that there was ever a question.
   - Surface both versions to the operator and ask which one wins.
   - Record the resolution in `decisions/log.md` in the same format as step 2, regardless of
     which side won — the fact that a contradiction was found and resolved is itself worth
     keeping.

4. **Write each knowledge node as one claim, not one topic.** A node is a single fact or
   principle, with its source and its date, linked to its neighbors. Don't write a node titled
   after the meeting ("2026-08-27 call notes") — write one node per claim that survives the
   meeting. Shape:

   ```markdown
   # <the claim, stated plainly>

   <Two to five sentences. What this means and why it matters. Nothing the reader
   has to dig for.>

   **Source:** <where this came from — call, document, person>
   **Date:** <YYYY-MM-DD>

   Related: [[other-node-slug]], [[another-node-slug]]
   ```

   A forty-minute call might produce zero nodes, one node, or five — it depends on how many
   distinct claims survive. It almost never produces one node per transcript.

5. **Update the wiki's `index.md` in the same pass — not as a follow-up.** Every new file in
   `knowledge/external/` or `knowledge/playbook/` gets an entry in that folder's `index.md`
   before you consider the work done. An index that lags the nodes it's supposed to list is
   `confusion`: the next session reads the index, doesn't see the node, and reports that the
   knowledge doesn't exist — even though the file is sitting right there unlinked.

6. **Say where the raw file should live, and leave it there.** This kit does not impose a
   folder for raw source material — that's a deliberate gap, not an oversight. Tell the
   operator where you'd put it (next to the project it belongs to, or wherever they keep source
   material) and let them place it. Don't invent a new top-level folder to hold it — an
   undocumented folder is exactly the kind of drift `/os-audit` exists to catch.

7. **Report what you did, not what you read.** Close with a short list: which decisions got
   logged, which nodes got written or updated (with their paths), which contradictions got
   surfaced, and where the action items went. If nothing in the material warranted any of the
   four routes, say that plainly instead of manufacturing a node to justify the pass.

## When NOT to run this

`/route-fix` is for when the agent already had knowledge somewhere and *failed to find it* —
a routing, index, or precedence problem. This skill is for when the knowledge doesn't exist
in routed form yet and needs to be added. If the operator says "the agent should have known
this" about something already on disk, that's `/route-fix`; if they're handing you something
new to process, that's this skill.
