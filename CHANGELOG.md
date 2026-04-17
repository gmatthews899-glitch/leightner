# Change Log

Running record of all changes to the Leightner internal tools project. Newest entries at the top.

All agents must read this file at the start of every session and append an entry at the end of every task. See `AGENTS.md` section "CHANGELOG.md — your memory across sessions" for the required format.

---

## 2026-04-17 — Initial project scaffold
**Agent:** Codex
**Session summary:** The operator asked for the initial scaffold only: pinned dependencies, basic repo files, and a minimal FastAPI app with a single `/health` endpoint.

**Files created:**
- `.gitignore`
- `requirements.txt`
- `README.md`
- `backend/__init__.py`
- `backend/main.py`
- `backend/models/__init__.py`
- `backend/routes/__init__.py`
- `frontend/static/css/.gitkeep`
- `frontend/static/js/.gitkeep`
- `data/.gitkeep`

**Files modified:**
- `CHANGELOG.md` — appended this session entry at the top in the required format

**Files deleted:**
- none

**Dependencies added:**
- none

**Verified by:**
- Operator started `uvicorn backend.main:app --reload --port 8000` and confirmed the server started cleanly with no errors.
- Operator opened `http://127.0.0.1:8000/health` in the browser on 2026-04-17 at approximately 10:30:23 CDT and confirmed the response was `{"status":"ok"}`.
- Operator also confirmed a `200 OK` entry in the access log. A `404` on `/favicon.ico` was observed and is expected/harmless.

**Decisions made during this session:**
- Added `.env` to `.gitignore` to comply with the project rule that secrets must never be committed.
- Noted in `README.md` that Python 3.10 or newer is required, because the local machine currently reports Python 3.9.6.

**What was NOT done / deferred:**
- No database setup or SQLite file creation
- No models beyond empty package markers
- No auth code
- No HTML files
- No routes other than `GET /health`
- No verification run, per operator instruction

**Next suggested step:**
- Create a Python 3.10+ virtual environment, install dependencies, run `uvicorn`, and confirm that `GET /health` returns `{"status": "ok"}` before committing.

## 2026-04-17 — Expanded AGENTS.md with operational, security, and timezone rules
**Agent:** Claude (planning conversation)
**Session summary:** The operator identified that the initial AGENTS.md was missing important rules. This session audited the file against real-world failure modes and added comprehensive coverage.

**Files created:** none

**Files modified:**
- `AGENTS.md` — added rules 9 (verify before done), 10 (protect the database), 11 (don't modify docs/prototype); new section on secrets and credentials; new section on timezone handling (Leightner is Central Time); Python version check requirement; migration strategy (create_all for MVP, Alembic later); server port etiquette; no orphan servers rule; "comment the why" style rule; "continue where we left off" procedure; updated red flags list; updated CHANGELOG entry format to include "Verified by" field.

**Files deleted:** none

**Dependencies added:** none

**Verified by:**
- Visual review of full AGENTS.md content. No code to run — this was a documentation change only.

**Decisions made during this session:**
- Migrations: use SQLAlchemy `create_all()` for MVP, defer Alembic until real production data exists.
- Timezone: store UTC in database, display America/Chicago. Use `zoneinfo` from stdlib, not pytz.
- Password hashing: bcrypt (already in requirements.txt).
- Date-only fields (like order due dates): use `DATE` type, not `DATETIME`, to avoid timezone confusion.

**What was NOT done / deferred:**
- No code changes yet — still at scaffolding step
- CLAUDE.md was not updated; it's a pointer to AGENTS.md so the expansion carries through automatically

**Next suggested step:**
- Codex needs to re-read the updated AGENTS.md and confirm understanding of the new rules, then proceed with the scaffolding task (create empty directory structure, requirements.txt, README.md, minimal FastAPI app with /health endpoint).

---

## 2026-04-17 — Workspace setup and agent config
**Agent:** Claude (planning conversation, not an IDE agent session)
**Session summary:** The operator set up the initial workspace in Antigravity and established the rules and context for all future agent sessions.

**Files created:**
- `AGENTS.md` — general agent instructions, tool-agnostic
- `CLAUDE.md` — Claude-specific pointer to AGENTS.md
- `PROJECT_CONTEXT.md` — business context, decisions, principles, module specs
- `CHANGELOG.md` — this file
- `leightner-hub.html` — existing single-file HTML prototype (reference only, will be ported to the real app later)

**Files modified:** none (initial setup)

**Files deleted:** none

**Dependencies added:** none

**Verified by:**
- Not applicable — initial setup, no code to run.

**Decisions made during this session:**
- Stack locked: Python + FastAPI + SQLite + plain HTML/CSS/JS. No React, no Node, no build step. See AGENTS.md for the full banned list.
- MVP scope: hub with 5 tiles (2 live: Orders, Issue Tracker; 3 placeholder: Customers & Contacts, Documents & SOPs, Reports & Metrics), plus two-role login (admin/tech).
- Orders module renamed from "Active Jobs" (prototype terminology) to "Orders" per stakeholder feedback.
- Data will be entered manually in the Orders module for the MVP. DBA (the existing ERP) integration is deferred to the someday list.

**What was NOT done / deferred:**
- No application code written yet
- DBA integration deferred
- Real deployment (mini-PC, backups, IT consultant) deferred until after MVP is built and Rusty confirms continued buy-in

**Next suggested step:**
- Scaffold the project: create empty directory structure, requirements.txt, README.md, and a minimal FastAPI app with a single /health endpoint. No business logic, no database, no auth yet. Verify the server starts and /health returns `{"status": "ok"}`, then commit.
