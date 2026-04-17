# Agent Instructions — Leightner Electronics Internal Tools

You are working on an internal web application for **Leightner Electronics Inc.**, a custom transformer manufacturer in McKinney, TX. The human operator of this project is **not a developer**. Treat them as the decision-maker and product owner, not as a coding partner. They will specify *what* to build; you produce the code and explain what you did.

**At the start of EVERY session, before doing any work, read these four files in this order:**
1. `PROJECT_CONTEXT.md` — business context, decisions, principles, what we're building
2. `CHANGELOG.md` — running log of changes made by all prior agent sessions. This is your memory across sessions. If you skip this, you will repeat work or undo things another agent did.
3. `AGENTS.md` — this file, how you work
4. `ARCHITECTURE.md` — how the codebase is structured. Every new feature follows the pattern documented there.

This `AGENTS.md` file is rules for *how you work*. `PROJECT_CONTEXT.md` is rules for *what we build*. `ARCHITECTURE.md` is rules for *how the code is organized*. `CHANGELOG.md` is the record of what has already been done.

---

## Ground rules — violating these causes real problems

### 1. Do not take actions outside the scope of what was asked
If the user asks you to change file A, do not also change files B, C, and D because you think they should also change. If you believe other changes are needed, propose them and wait for confirmation. Scope creep destroys trust and breaks working code.

### 2. Do not add dependencies without explicit approval
Every `pip install`, every `npm install`, every library added to `requirements.txt` must be approved first. Dependencies are a long-term maintenance tax. Prefer the standard library. Prefer one more line of code over one more dependency.

### 3. Do not rewrite working code to "improve" it
If something is working, it stays. Do not refactor, restructure, rename, or "clean up" code that wasn't part of the current task. Do not silently change formatting. Every change should be traceable to a specific request.

### 4. Ask before deleting
Never delete files, functions, database tables, or significant blocks of code without explicit permission. If something seems unused, say so and wait.

### 5. Commit small, commit often
After every working change, remind the user to commit to git. Every commit is a rollback point. Do not stack multiple unrelated changes into one commit.

### 6. Confirm before destructive operations
Database migrations that drop columns or tables. Operations that modify or delete existing data. Deployment commands. Changes to authentication. Always pause and confirm.

### 7. When stuck, stop and explain — don't guess
If you are 80%+ confident, proceed. If you are less confident, describe what you are unsure about and wait for input. Do not try three things in rapid succession hoping one works. That creates a mess the user has to clean up.

### 8. Match the existing style
Look at neighboring code before adding new code. Match the patterns, naming, and structure already present. Consistency across the codebase matters more than your stylistic preferences.

### 9. Verify before declaring "done"
Never say a task is complete without confirming the code actually works. For backend changes: the server must start cleanly with no errors. For endpoints: hit them and confirm the expected response. For frontend changes: load the page and confirm it renders. If you cannot verify (because tests don't exist yet, or you don't have a way to run something), say so explicitly: "I have not verified this runs. Please confirm before committing."

### 10. Protect the database
The SQLite file at `data/leightner.db` may contain real issues and orders once this app is used. Never delete, truncate, or re-create the database to "fix" a schema issue or "start fresh" unless the operator explicitly asks for it. If a schema change is needed on a database with data, propose an additive migration (add columns, don't drop them) and wait for approval. Loss of real data is the worst possible outcome.

### 11. Do not modify files outside the current codebase
Specifically: `leightner-hub.html` is the original prototype and is kept as reference only. Do not modify it. Do not modify `AGENTS.md`, `CLAUDE.md`, `PROJECT_CONTEXT.md`, or `ARCHITECTURE.md` unless explicitly asked. `CHANGELOG.md` is append-only.

---

## The tech stack (do not change without discussion)

- **Python version:** 3.10 or newer. Before writing any Python code in a new session, check the actual version with `python --version` and note it in your response. Do not assume 3.12 features are available.
- **Backend:** FastAPI
- **Database:** SQLite via SQLAlchemy 2.x
- **Migrations:** For the MVP, schema changes can be handled by modifying the model and letting SQLAlchemy `create_all()` on a fresh database. Once the app has real data in production, we will switch to Alembic migrations. Do not add Alembic until explicitly asked.
- **Frontend:** Plain HTML/CSS/JavaScript. No React. No build step. No npm. No bundlers.
- **Light JS enhancement:** Alpine.js or HTMX are acceptable if justified and discussed. Load from a single CDN, not npm. Nothing else without discussion.
- **Auth:** Simple username/password with server-side sessions (signed cookies via `itsdangerous` or FastAPI's `SessionMiddleware`). No OAuth, no JWTs in the MVP.
- **Password hashing:** `bcrypt`. Confirmed, already in `requirements.txt`.
- **Deployment target:** Eventually a Linux mini-PC on the Leightner LAN. For MVP, runs on the operator's machine at `http://localhost:8000`.

### Why this stack matters
- Zero recurring cost
- On-premise compatible (ITAR/aerospace customer base may require this later)
- Boring and proven — the operator isn't a developer and needs something they can hand off to someone else later
- SQLite means the entire database is one file, trivially backed up

### Explicitly banned from this project without discussion
- React, Vue, Svelte, any SPA framework
- Node.js, npm, any build step
- Docker (until deployment phase — not now)
- Cloud services (Vercel, Supabase, AWS, etc.) — this is on-premise
- Any subscription/paid service
- TypeScript (we use plain JavaScript)
- CSS frameworks with build steps (Tailwind's JIT, etc.). Plain CSS only.
- Third-party CDNs other than what's already loaded. Every new `<script src>` or `<link rel=stylesheet href=...>` to an external URL needs approval.

---

## Secrets and credentials

- **Never hardcode passwords, API keys, or secret tokens in source code.** Ever.
- **Use a `.env` file** for any secret (session signing key, initial admin password, etc.). The `.env` file must be listed in `.gitignore` and never committed.
- **Provide `.env.example`** in the repo with the variable names and placeholder values (e.g. `SESSION_SECRET=replace-me`) so a new developer knows what env vars are needed.
- **Passwords in the database are hashed with bcrypt**, never stored plain.
- **Error messages to the user must not leak internals.** "Invalid username or password" — not "User 'rusty' not found in table users." Real error details go to server logs only.
- **Session cookies:** `httpOnly=True`, `secure=True` in production, `samesite="lax"`.

If an operator asks you to hardcode a password "just for testing," propose using an env var with a default value instead, and wait for confirmation before hardcoding.

---

## Dates, times, and timezones

Leightner is in McKinney, TX (Central Time). Due dates, timestamps, and "recently updated" logic all need to work in local time to make sense to the operator and Rusty.

- **Store all timestamps in UTC** in the database (ISO 8601 format, timezone-aware)
- **Convert to America/Chicago** when displaying to users
- **Date-only fields** (like an order due date) should be stored as `DATE` type, not `DATETIME`, to avoid timezone confusion. A due date of "April 30" should mean April 30 in Central Time regardless of when it's viewed.
- The "recently changed — highlight for 24 hours" logic: 24 hours from the last update timestamp, compared in UTC. Straightforward.
- Use `zoneinfo` from the standard library. Do not add `pytz` as a dependency.

---

## Project structure

Current state (files that actually exist are shown; planned files are notes, not instructions to create them preemptively):

```
leightner/
├── AGENTS.md              # This file
├── CLAUDE.md              # Claude-specific pointer to this file
├── PROJECT_CONTEXT.md     # Business context, decisions, principles
├── ARCHITECTURE.md        # How the code is structured; patterns new features follow
├── CHANGELOG.md           # Running record of changes (append-only)
├── README.md              # How to run the project
├── requirements.txt       # Python dependencies (pinned)
├── .gitignore
├── .env.example           # Placeholder env vars, committed
├── .env                   # Real env vars, NEVER committed
├── leightner-hub.html     # Original prototype (reference only, do not modify)
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   └── [other files added as needed, one feature at a time]
├── frontend/
│   └── static/
│       ├── css/
│       └── js/
└── data/
    └── leightner.db      # SQLite file (gitignored; may contain real data)
```

**Do not pre-create files that aren't needed yet.** If the current task is "scaffolding," don't also create `auth.py` just because auth is on the roadmap. Create files when they're first used.

---

## Coding conventions

### Python
- Use type hints on function signatures
- Use `from __future__ import annotations` at the top of files that use forward references
- Prefer explicit over clever — readability over brevity
- **Comment the "why," not the "what."** The operator is not a developer; comments should explain *why a piece of code exists*, not restate what the code is obviously doing. Example: `# Cache the token for 1 hour to avoid rate-limiting on the validation endpoint` (good) vs `# Set the token` (bad).
- Database session management: use FastAPI dependency injection, don't create sessions inside handlers
- Route handlers: keep them thin. Business logic goes in service functions, not in the route itself.

### JavaScript
- Plain ES modules or plain `<script>` tags. No bundlers.
- `const` unless reassignment is needed. Never `var`.
- `async/await` over raw promises
- Event delegation on parent elements over attaching handlers to every child
- Comment the "why" just like Python

### HTML/CSS
- Semantic HTML (`<main>`, `<nav>`, `<section>`, not `<div>` for everything)
- System sans-serif fonts only — no Google Fonts, no Inter, no Roboto, no display serifs
- Sentence case for all UI copy — never Title Case, never ALL CAPS
- No decorative elements, no marketing-style hero text, no emoji in UI
- The operator has explicitly stated preferences for "functional, not fancy" — respect this

---

## Running and testing the app

### Local development
- Use a virtual environment at `.venv/` (already in `.gitignore`)
- Start the dev server with: `uvicorn backend.main:app --reload --port 8000`
- If port 8000 is already in use, try 8001, 8002, etc. — never kill whatever is on 8000 without asking. Tell the operator which port the server started on.

### Do not leave orphan servers running
If you start a server during a session, remember to stop it before the session ends, OR tell the operator clearly "the server is still running on port X, stop it with Ctrl+C when done." Never start a second server if one is already running — use the existing one or stop it first.

### Testing
For the MVP, automated tests are not required. Manual verification is sufficient: start the server, hit the endpoint or load the page, confirm the behavior matches the expectation.

When manual verification is done, be explicit in the CHANGELOG entry: "Verified manually: hit GET /orders and confirmed the response includes all three seeded records."

If tests are added later (pytest is the planned framework), all future changes must run the tests before being declared done.

---

## Authentication model (MVP)

Two roles:
- **Admin** (Rusty): can create, read, update, delete orders and issues. Manages the system.
- **Tech** (shop floor / everyone else): read-only access to orders. Can log new issues and add updates to existing issues, but cannot delete or modify others' entries.

This is the MVP model. Do not add role-based permissions beyond these two without discussion.

Login method: username + password. Server-side session cookies. Password hashing with `bcrypt`.

Initial admin account: created via a one-time script or environment variables, never hardcoded in source. The operator must be able to set/change the admin password without editing code.

---

## Workflow for any change

When the operator asks you to do something:

1. **Read `PROJECT_CONTEXT.md`, `CHANGELOG.md`, and `ARCHITECTURE.md` first** if you haven't this session. The changelog tells you what previous sessions (you or other agents) already did — do not repeat or undo that work. Architecture tells you how to structure new code.
2. **Summarize what you understand** the task to be, in one or two sentences
3. **List the files you will create or modify** — explicitly, by path
4. **List what you will NOT touch** — explicitly, to show you understand the scope
5. **Wait for "go ahead"** on anything non-trivial before writing code
6. After making changes: **verify the code runs** (per rule #9) and **summarize what you did**, what to test, and remind the operator to commit
7. **Append an entry to `CHANGELOG.md`** (see rules below)

### What "non-trivial" means — always confirm first
- Any change touching more than 2 files
- Any new dependency
- Any database schema change (new table, new column, altering existing columns)
- Any change to auth, sessions, or security
- Any deletion of existing code
- Any change to the project structure or folder layout

Small edits (fix a typo, adjust a CSS value, rename one variable in a scoped function) can proceed without explicit confirmation.

### When the operator says "continue where we left off"
Check `CHANGELOG.md` top entry first to see what was most recently done and what the "Next suggested step" was. Summarize what you found and propose the next concrete action before acting.

---

## CHANGELOG.md — your memory across sessions

The `CHANGELOG.md` file at the project root is a running log of everything done to the project. This is how agents (you, or future Claude/Codex/other sessions) maintain context across time. It is NOT optional.

### When to update it
Append a new entry **every time you complete a task**, before telling the operator you're done. Update it in the same response as the work itself. If a task has sub-steps, one entry per completed step is fine.

### Entry format
Use this exact structure. Newest entries go at the TOP of the file (below the heading), so the most recent work is easy to find.

```
## YYYY-MM-DD — [Short task title]
**Agent:** [Codex / Claude Code / whichever you are]
**Session summary:** One sentence describing what the operator asked for.

**Files created:**
- `path/to/file1.py`
- `path/to/file2.html`

**Files modified:**
- `path/to/file3.py` — brief description of what changed

**Files deleted:**
- (none, or list them)

**Dependencies added:**
- (none, or list with versions)

**Verified by:**
- Describe how you confirmed the change works. "Started server, hit GET /health, got {status: ok}" — specific commands and outputs.
- If not verified: "NOT VERIFIED — operator needs to confirm."

**Decisions made during this session:**
- Any small decision you made that wasn't explicitly in the prompt (e.g. "named the route /api/orders because it's a JSON endpoint"). If you made no independent decisions, write "none."

**What was NOT done / deferred:**
- Anything the operator asked about but we decided to defer
- Anything you considered doing but held off on

**Next suggested step:**
- One sentence on what would logically come next, so the operator (or next agent) has a starting point.
```

### Rules for writing changelog entries
- **Be factual, not promotional.** "Added login route" not "Implemented a beautiful new login system."
- **Be specific about files.** Paths, not descriptions.
- **Include failures and rollbacks.** If you tried something and it didn't work, log it with "Rolled back: [what and why]" so future sessions know not to try the same approach.
- **If a session ended without completing a task**, still write an entry describing how far you got and what remains.
- **Do NOT overwrite or delete existing changelog entries.** Only append new ones. The history is the point.

### If you're about to start work without checking the changelog
Stop. Go check the changelog. Then continue. Skipping this step is how agents undo each other's work.

---

## When things break

If the user says something is broken:

1. **Don't immediately try to fix it.** First understand what broke.
2. **Ask for the error message or the specific symptom.** "It doesn't work" isn't enough to act on.
3. **Check git log and CHANGELOG.md** — was there a recent change that might be responsible?
4. **Propose a diagnosis** before proposing a fix
5. **Small targeted fix** — do not "take the opportunity" to also fix other things

---

## Talking to the operator

- Plain language. No jargon unless you define it.
- When you explain what you did, explain the "why" not just the "what."
- When the operator asks a question you don't know the answer to, say so. Do not guess.
- If the operator's plan seems wrong, say so — once. They may have context you don't. After one pushback, follow their direction.
- Never say "I've gone ahead and..." for things that weren't explicitly requested.
- When giving commands to run, give them one at a time in separate code blocks, clearly labeled. Do not combine multiple unrelated commands into one block.
- If a command's expected output would be informative, tell the operator what success looks like.

---

## The MVP scope (current phase)

Right now we are building an **MVP to demonstrate functionality to Leightner's owner**. This is a convincing tool, not a finished product. Priorities:

1. **Orders module** — Rusty (admin) can enter, edit, and update sales/work orders with current due dates. Techs (logged in as the tech role) can view the orders and see current dates. When a date is changed, the row is visually flagged (color highlight) for 24 hours so techs know to pay attention. Note: the existing prototype calls this "Active Jobs" — the MVP renames it to "Orders."
2. **Issue tracker** — port the existing HTML prototype into the real app with a proper database backend. Keep the fields and behavior that exist in the prototype.
3. **Login** — admin account for Rusty, tech account for shop floor. That is the entire auth model for MVP.
4. **Hub landing page** — 5 tiles total: 2 live (Orders, Issue Tracker) and 3 "Coming Soon" placeholders (Customers & Contacts, Documents & SOPs, Reports & Metrics). The placeholders are deliberate — they show the overall vision to stakeholders without requiring us to build them yet.

Anything outside this scope goes on the someday list in `PROJECT_CONTEXT.md`.

---

## Red flags — stop and ask if you see these

- You are about to start work without having read `CHANGELOG.md`, `PROJECT_CONTEXT.md`, and `ARCHITECTURE.md` this session
- You are about to install more than one new library
- You are about to modify a file that wasn't in the current task
- You are about to run a database migration that changes existing columns
- You are about to delete files or functions
- You are about to restructure the folder layout
- You are about to add a new page or endpoint that wasn't requested
- You are about to delete `data/leightner.db` or reset the database for any reason
- You are about to commit a `.env` file, a password, or any secret to git
- You are about to declare "done" without having verified the change runs
- You are about to hardcode a password, API key, or secret in source code
- The task as stated would take more than ~50 lines of code and you haven't confirmed the approach
- You completed work without updating `CHANGELOG.md`

Any of these: pause, describe what you're about to do, wait for approval.
