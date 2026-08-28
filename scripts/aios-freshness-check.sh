#!/bin/sh
# aios-freshness-check.sh
#
# Read-only drift check. Runs on SessionStart (see .claude/settings.json) and
# is documented in CLAUDE.md -> "What runs on its own". Fixes nothing — it
# only speaks up when something has drifted.
#
# POSIX sh only: no bashisms, no GNU-only flags. Must run unmodified on
# macOS's default /bin/sh and on Linux.
#
# Contract:
#   - Always exits 0, including on every error path. A SessionStart hook
#     that returns non-zero breaks the session.
#   - Prints nothing when nothing has drifted. Silence is the success state.
#   - Files this script reads may not exist yet on a freshly scaffolded
#     workspace (decisions/log.md, context/me.md) — that is not a warning,
#     it is just guarded and skipped.

WARNED=0

warn() {
  printf '⚠️  %s\n' "$1"
  WARNED=1
}

# 1. context/ — no file modified in the last 60 days.
if [ -d context ]; then
  ctx_files=$(find context -type f 2>/dev/null)
  if [ -n "$ctx_files" ]; then
    ctx_fresh=$(find context -type f -mtime -60 2>/dev/null)
    if [ -z "$ctx_fresh" ]; then
      warn "context/ has no file modified in the last 60 days — check it's still true."
    fi
  fi
fi

# 2. Last /os-audit — newest reports/os-audit-* file is older than 30 days,
#    or none exists at all.
if [ -d reports ]; then
  audit_fresh=$(find reports -name 'os-audit-*' -type f -mtime -30 2>/dev/null)
  if [ -z "$audit_fresh" ]; then
    audit_any=$(find reports -name 'os-audit-*' -type f 2>/dev/null)
    if [ -z "$audit_any" ]; then
      warn "No /os-audit report found in reports/ — run /os-audit."
    else
      warn "Last /os-audit report is more than 30 days old — run /os-audit."
    fi
  fi
fi

# 3. Undistilled raw material — a file in projects/ newer than the newest
#    entry in decisions/log.md. Skipped until that file exists (created in
#    Task 11 of the aios-kit build, or by the operator).
#
#    projects/ only — NOT reports/. reports/ is skill-generated output by
#    definition (see CLAUDE.md routing map: "Generated, not authored"), so
#    it is never raw input to distill. /os-audit itself writes into
#    reports/, so scanning reports/ here would make this hook warn on the
#    very next session after every single audit — a hook that fires every
#    session gets ignored. If raw material ever ends up in reports/ by
#    mistake, that is a routing error and belongs to /os-audit check 6, not
#    this hook. Do not add reports/ back to this scan.
if [ -f decisions/log.md ]; then
  raw=""
  if [ -d projects ]; then
    raw="$raw$(find projects -type f -newer decisions/log.md 2>/dev/null)"
  fi
  if [ -n "$raw" ]; then
    warn "There's material in projects/ newer than the last decisions/log.md entry — distill it."
  fi
fi

# 4. Demo still installed — context/me.md contains the demo banner.
#    Skipped until that file exists (created by /onboard).
if [ -f context/me.md ]; then
  if grep -qF '🟡 DEMO' context/me.md 2>/dev/null; then
    warn "Still running the demo company. Run /onboard."
  fi
fi

# 5. Apparent secrets — a tracked file matching *.env, *token*, *secret*.
if command -v git >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  secrets=$(git ls-files 2>/dev/null | grep -iE '(\.env$|token|secret)' 2>/dev/null)
  if [ -n "$secrets" ]; then
    secrets_line=$(printf '%s' "$secrets" | tr '\n' ' ')
    warn "Tracked file(s) look like secrets: $secrets_line"
  fi
fi

if [ "$WARNED" = "1" ]; then
  printf '\n'
fi

exit 0
