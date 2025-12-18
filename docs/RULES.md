# PARKSY.KR — FINAL USER MANUAL + CODED ENFORCEMENT
(Status: VERIFIED & LOCKED)

## Purpose
This instruction:
1) Defines how parksy.kr is allowed to be used
2) Explicitly defines what must NEVER be done
3) Codifies these rules so that:
   - Humans are warned
   - AI agents are constrained
   - GitHub blocks violations automatically

parksy.kr is NOT a normal website.
It is a **Single-File Codex**.

---

## 0. Identity Lock (Non-Negotiable)

- Domain: https://parksy.kr/
- Repo role: **Single-File Codex**
- Build system: NONE (intentional)
- Frameworks: NONE (intentional)
- Publish rule: `git push == publish`
- Current state: **VERIFIED & LOCKED**

If this identity is questioned, STOP immediately.

---

## 1. DO NOT LIST (Human Rules)

### 1.1 Structural Prohibitions
You must NOT:
- Add files to repository root
- Create new HTML pages in root
- Introduce PWA artifacts (`sw.js`, `manifest*`)
- Change directory structure
- Reintroduce build systems or package managers

### 1.2 Technology Prohibitions
You must NOT:
- Add React / Vue / Astro / Next / Vite
- Add npm, yarn, pnpm, bun
- Add CI/CD beyond guardrails
- Add automation "just in case"

### 1.3 Git / Ops Prohibitions
You must NOT:
- Bypass guardrails
- Ignore failing GitHub Actions
- Commit red builds "temporarily"

---

## 2. ALLOWED ACTIONS (Human Rules)

You MAY:
- Edit content inside `index.html`
- Add images only to `/assets`
- Move obsolete pages to `/archive`
- Add documentation under `/docs`
- Publish immediately via push

If a change feels "architectural", it does NOT belong here.

---

## 3. AI OPERATION RULES (Mandatory)

Any AI agent (Claude, MCP, etc.) must:

1) Read this document BEFORE any operation
2) Assume the repo is **LOCKED**
3) Ask explicit permission before:
   - Adding files
   - Changing structure
   - Modifying workflows
4) Abort operation if a rule is violated

### Mandatory AI Command Prefix
```
Read PARKSY.KR User Manual and Guard Rules.
Confirm compliance before executing.
```

---

## 4. CODED ENFORCEMENT (Non-Human, Mandatory)

### 4.1 Guardrail Script
`scripts/parksy_guard.py` is the **law enforcement layer**.

It enforces:
- Root whitelist
- PWA artifact ban
- Python trash ban (`__pycache__`, `*.pyc`)
- Space-containing filenames ban

### 4.2 Guardrail Workflow
`.github/workflows/repo-guard.yml`

This workflow:
- Runs on every push and PR
- Blocks merges on violation
- Makes rule-breaking unmergeable

**Human intention is irrelevant.**
**Green Actions = only source of truth.**

---

## 5. Failure Protocol

If GitHub Actions turns RED:

1) STOP immediately
2) Read the guard output
3) Remove or move violating files
4) Re-push until GREEN

Never "fix later".

---

## 6. Intentional Failure Test

Once per major refactor:
- Intentionally add a forbidden file (e.g. `sw.js`)
- Confirm guardrail blocks it
- Remove file and restore GREEN

If this test fails → guardrail is broken → FIX FIRST.

---

## 7. Status Declaration

```
Status: VERIFIED & LOCKED
Allowed changes: content only
Structural changes: forbidden without explicit redesign decision
```

---

## 8. Decision Rule (Critical)

If you think:
- "This would be cleaner with X"
- "Maybe one more page"
- "What if we automate this"

→ You are in the WRONG REPO.

Create a new repository instead.

---

## FINAL STATEMENT

parksy.kr is not optimized.
parksy.kr is not scalable.
parksy.kr is not extensible.

parksy.kr is **deliberately constrained**.

Breaking these constraints is not innovation.
It is regression.
