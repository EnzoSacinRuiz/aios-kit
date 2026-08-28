# Rules

A rule goes in this folder when it is **permanent**, applies **across every session**, and is
**too specific to belong in `CLAUDE.md`**. `CLAUDE.md` is the map of the whole workspace — it
stays short on purpose. A rule is one narrow, standing instruction that would otherwise get
re-decided (and re-argued) every time it comes up.

## Format

One file per topic. Each file states:

1. **The rule** — plain, unambiguous, no hedging.
2. **Why** — the reasoning behind it.

A rule without its reason gets overridden the first time it's inconvenient. If you can't state
why a rule exists, it probably shouldn't be a rule — it should be a default, or nothing.

Name the file after the topic, not after the word "rule": `communication-style.md`, not
`rule-1.md`. Keep each file short — a rule is a sentence or two plus its reasoning, not a
policy document.

## Precedence

**Rules beat defaults. The user's direct instruction beats rules.**

If the user tells you to do something that conflicts with a rule in this folder, follow the
user — then, if the conflict looks like it will come up again, ask whether the rule itself
should change. A rule that gets silently overridden every session isn't a rule anymore; it's
noise. Update it or remove it.

## Adding a rule

Most rules start as a one-off correction — the operator tells you something once, and it needs
to hold from then on. When that happens:

1. Write the file: the rule, then why.
2. Give it a clear, topic-based filename.
3. If the rule reverses or narrows something written elsewhere (a default in `CLAUDE.md`, a
   habit you'd fall back to), say so in the file, so the next reader isn't left reconciling two
   sources by hand.

`/onboard` and other skills write new rule files into this folder following this same format —
this README is the contract they follow, not just a description of what's already here.
