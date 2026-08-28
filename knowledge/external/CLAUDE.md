> 🟡 DEMO — `/onboard` replaces this file with yours.

# knowledge/external — ingestion manual

Intelligence about the outside world: clients, prospects, competitors, and market conditions.
Nothing about how Meridian itself does the work — that's `knowledge/playbook/`.

## What belongs here

- Durable facts about a specific client or prospect account — buying pattern, who the
  decision-maker is, what they've said no to before.
- Durable facts about a competitor — how they price, what they're good at, where they lose.
- Market or category conditions that will still be true in three months, not this week's news.

If a fact will be stale by next quarter, it's not a node — it belongs in a project file or a
conversation, not the wiki.

## Node format

One claim per file, not one topic per file. A node named after a company
(`northwind-labs.md`) that tries to hold everything ever learned about that company turns into
a dumping ground nobody reads in full. Prefer several small nodes over one big one once an
account has more than two or three distinct claims worth keeping.

```markdown
# <the claim, stated plainly>

<Two to five sentences: what this means and why it matters.>

**Source:** <call, document, person>
**Date:** <YYYY-MM-DD>

Related: [[hold-the-fee-negotiate-scope]]
```

## Links and the index

- Use `[[northwind-labs-pushes-for-rush-timelines]]`-style double-bracket syntax to link to
  another node's filename (without `.md`). Every link must resolve to a real file — a link to
  a node that doesn't exist yet is worse than no link, because it reads as knowledge that was
  never actually captured.
- `index.md` lists every node in this folder. Add the entry in the same pass you write the
  node — an index that lags the files it lists is `confusion`, not just untidy.
