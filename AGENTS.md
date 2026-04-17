# Agent Instructions — Leightner Electronics Internal Tools

You are working on an internal web application for **Leightner Electronics Inc.**, a custom transformer manufacturer in McKinney, TX. The human operator of this project is **not a developer**. Treat them as the decision-maker and product owner, not as a coding partner. They will specify *what* to build; you produce the code and explain what you did.

**Read `PROJECT_CONTEXT.md` at the start of every session before doing any work.** That document contains the company context, design principles, decision log, and guiding rules. This `AGENTS.md` file is rules for *how you work*; `PROJECT_CONTEXT.md` is rules for *what we build*.

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

---

## The tech stack (do not change without discussion)

- **Backend:** Python 3.11+ with FastAPI
- **Database:** SQLite (single file, no separate server process)
- **ORM:** SQLAlchemy 2.x
- **Frontend:** Plain HTML/CSS/JavaScript. No React. No build step. No npm. No bundlers.
- **Light JS enhancement:** Alpine.js or HTMX are acceptable if justified. Nothing else without discussion.
- **Auth:** Simple username/password with server-side sessions. No OAuth, no JWTs in the MVP.
- **Deployment target:** Eventually a Linux mini-PC on the Leightner LAN. For MVP, runs on the operator's machine.

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
- CSS frameworks with build steps (Tailwind's JIT, etc.). Plain CSS or a single CDN-loaded CSS file only.

---

## Project structure

```
leightner/
├── AGENTS.md              # This file
├── CLAUDE.md              # Claude-specific pointer to this file
├── PROJECT_CONTEXT.md     # Business context, decisions, principles
├── README.md              # How to run the project
├── requirements.txt       # Python dependencies
├── .gitignore
├── backend/
│   ├── main.py           # FastAPI app entry point
│   ├── database.py       # SQLite connection setup
│   ├── auth.py           # Login/session logic
│   ├── models/           # SQLAlchemy models
│   └── routes/           # API endpoints
├── frontend/
│   ├── index.html        # Hub landing page
│   ├── login.html
│   ├── orders.html       # Orders/jobs view
│   ├── issues.html       # Issue tracker
│   ├── static/
│   │   ├── css/
│   │   └── js/
└── data/
    └── leightner.db      # SQLite file (gitignored)
```

Keep this structure. Do not reorganize without discussion.

---

## Coding conventions

### Python
- Use type hints on function signatures
- Use `from __future__ import annotations` at the top of files that need forward references
- Prefer explicit over clever — readability over brevity
- One route handler per file in routes/ when they get long; small related ones can share a file
- Database session management: use FastAPI dependency injection, don't create sessions inside handlers

### JavaScript
- Plain ES modules or plain `<script>` tags. No bundlers.
- No `let` when `const` works
- `async/await` over raw promises
- Event delegation on parent elements over attaching handlers to every child

### HTML/CSS
- Semantic HTML (`<main>`, `<nav>`, `<section>`, not `<div>` for everything)
- System sans-serif fonts only — no Google Fonts, no Inter, no Roboto, no display serifs
- Sentence case for all UI copy — never Title Case, never ALL CAPS
- No decorative elements, no marketing-style hero text
- The operator has explicitly stated preferences for "functional, not fancy" — respect this

---

## Authentication model (MVP)

Two roles:
- **Admin** (Rusty): can create, read, update, delete orders and issues. Manages the system.
- **Tech** (shop floor / everyone else): read-only access to orders. Can log new issues and add updates to existing issues, but cannot delete or modify others' entries.

This is the MVP model. Do not add role-based permissions beyond these two without discussion.

Login method: username + password. Server-side session cookies. Password hashing with `bcrypt` or `argon2` (both in the Python stdlib-adjacent ecosystem — confirm which before adding).

---

## Workflow for any change

When the operator asks you to do something:

1. **Read `PROJECT_CONTEXT.md` first** if you haven't this session
2. **Summarize what you understand** the task to be, in one or two sentences
3. **List the files you will create or modify** — explicitly, by path
4. **List what you will NOT touch** — explicitly, to show you understand the scope
5. **Wait for "go ahead"** on anything non-trivial before writing code
6. After making changes: **summarize what you did**, what to test, and remind the operator to commit

### What "non-trivial" means
- Any change touching more than 2 files → confirm first
- Any new dependency → confirm first
- Any database schema change → confirm first
- Any change to auth, sessions, or security → confirm first
- Any deletion of existing code → confirm first

Small edits (fix a typo, adjust a CSS value, rename one variable) can proceed without explicit confirmation.

---

## When things break

If the user says something is broken:

1. **Don't immediately try to fix it.** First understand what broke.
2. **Ask for the error message or the specific symptom.** "It doesn't work" isn't enough to act on.
3. **Check git log** — was there a recent change that might be responsible?
4. **Propose a diagnosis** before proposing a fix
5. **Small targeted fix** — do not "take the opportunity" to also fix other things

---

## Talking to the operator

- Plain language. No jargon unless you define it.
- When you explain what you did, explain the "why" not just the "what."
- When the user asks a question you don't know the answer to, say so. Do not guess.
- If the user's plan seems wrong, say so — once. They may have context you don't. After one pushback, follow their direction.
- Never say "I've gone ahead and..." for things that weren't explicitly requested.

---

## The MVP scope (current phase)

Right now we are building an **MVP to demonstrate functionality to Leightner's owner**. This is a convincing tool, not a finished product. Priorities:

1. **Orders module** — Rusty (admin) can enter, edit, and update sales/work orders with current due dates. Techs (logged in as the tech role) can view the orders and see current dates. When a date is changed, the row is visually flagged (color highlight) for 24 hours so techs know to pay attention.
2. **Issue tracker** — port the existing HTML prototype into the real app with a proper database backend. Keep the fields and behavior that exist in the prototype.
3. **Login** — admin account for Rusty, tech account for shop floor. That is the entire auth model for MVP.
4. **Hub** — simple landing page with tiles for Orders and Issues. Other modules from the prototype stay as "Coming Soon" placeholders.

Anything outside this scope goes on the someday list in `PROJECT_CONTEXT.md`.

---

## Red flags — stop and ask if you see these

- You are about to install more than one new library
- You are about to modify a file that wasn't in the current task
- You are about to run a database migration that changes existing columns
- You are about to delete files or functions
- You are about to restructure the folder layout
- You are about to add a new page or endpoint that wasn't requested
- The task as stated would take more than ~50 lines of code and you haven't confirmed the approach

Any of these: pause, describe what you're about to do, wait for approval.
