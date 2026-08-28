# knowledge/playbook — ingestion manual

The operator's own method: sales principles, delivery principles, and plays that will apply
again next time — not facts about the outside world. Facts about a client, prospect, or
competitor go in `knowledge/external/` instead.

## What belongs here

- A sales principle: how we price, negotiate, or qualify a deal, distilled from a pattern
  across more than one deal.
- A delivery principle: how we run the work itself — interview discipline, review steps,
  quality gates — distilled from a pattern across more than one project.

A one-off preference isn't a principle. If it only happened once, it's not ready for this
folder yet — wait for the pattern to repeat, or note it in the project file it came from.

## Node format

One claim per file.

```markdown
# <the claim, stated plainly>

<Two to five sentences: what this means and why it matters.>

**Source:** <call, document, decision, person>
**Date:** <YYYY-MM-DD>

Related: [[<filename-of-a-related-node>]]
```

## Links and the index

- `[[filename-of-another-node]]`-style double-bracket links point to another node's
  filename (without `.md`), in this folder or in `knowledge/external/`. A principle earns more
  trust when it's tied to the account or competitor fact that produced it — link across the
  two wikis rather than restating the fact.
- Every link must resolve to a real file. `index.md` lists every node in this folder and is
  updated in the same pass as the node, not after.
