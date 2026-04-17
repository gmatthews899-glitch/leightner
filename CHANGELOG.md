# Change Log

Running record of all changes to the Leightner internal tools project. Newest entries at the top.

All agents must read this file at the start of every session and append an entry at the end of every task. See `AGENTS.md` section "CHANGELOG.md — your memory across sessions" for the required format.

---

## 2026-04-17 — Added Orders JSON API routes and registered router
**Agent:** Codex
**Session summary:** The operator asked for Steps 3 and 4 of the Orders feature only: add JSON API routes in `backend/routes/orders.py` and register that router in `backend/main.py`.

**Files created:**
- `backend/routes/orders.py`

**Files modified:**
- `backend/main.py` — imported and registered the Orders router while keeping the lifespan and `/health` endpoint unchanged
- `CHANGELOG.md` — appended this session entry at the top in the required format

**Files deleted:**
- none

**Dependencies added:**
- none

**Verified by:**
- Activated the project venv and confirmed Python version:
  - `source .venv/bin/activate`
  - `python --version`
  - Output: `Python 3.12.13`
- Started the server without reload:
  - `uvicorn backend.main:app --port 8000`
  - Output included:
    - `INFO:     Started server process [57117]`
    - `INFO:     Waiting for application startup.`
    - `INFO:     Application startup complete.`
    - `INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`
- Ran the API checks sequentially, one command at a time:
  - `curl -s http://127.0.0.1:8000/api/orders`
  - Output: `[]`
  - `curl -s -X POST http://127.0.0.1:8000/api/orders -H "Content-Type: application/json" -d '{"customer_code":"LMCO","customer_name":"Lockheed Martin","credit_hold":false,"sales_order_number":"SO-TEST-001","item_number":"P-100","description":"Test widget","ship_qty":5,"backorder_qty":10}'`
  - Output: `{"id":1,"customer_code":"LMCO","customer_name":"Lockheed Martin","credit_hold":false,"sales_order_number":"SO-TEST-001","item_number":"P-100","description":"Test widget","ship_qty":5,"backorder_qty":10,"total_qty":15,"estimated_ship_date":null,"notes":null,"created_at":"2026-04-17T17:51:09","updated_at":"2026-04-17T17:51:09","updated_by":null}`
  - `curl -s http://127.0.0.1:8000/api/orders/1`
  - Output: `{"id":1,"customer_code":"LMCO","customer_name":"Lockheed Martin","credit_hold":false,"sales_order_number":"SO-TEST-001","item_number":"P-100","description":"Test widget","ship_qty":5,"backorder_qty":10,"total_qty":15,"estimated_ship_date":null,"notes":null,"created_at":"2026-04-17T17:51:09","updated_at":"2026-04-17T17:51:09","updated_by":null}`
  - `curl -s -X PUT http://127.0.0.1:8000/api/orders/1 -H "Content-Type: application/json" -d '{"ship_qty":20,"notes":"Updated via API test"}'`
  - Output: `{"id":1,"customer_code":"LMCO","customer_name":"Lockheed Martin","credit_hold":false,"sales_order_number":"SO-TEST-001","item_number":"P-100","description":"Test widget","ship_qty":20,"backorder_qty":10,"total_qty":30,"estimated_ship_date":null,"notes":"Updated via API test","created_at":"2026-04-17T17:51:09","updated_at":"2026-04-17T17:53:54","updated_by":null}`
  - `curl -s -w "\nHTTP %{http_code}\n" -X POST http://127.0.0.1:8000/api/orders -H "Content-Type: application/json" -d '{"customer_code":"LMCO","customer_name":"Lockheed Martin","credit_hold":false,"sales_order_number":"SO-TEST-001","item_number":"P-200","description":"Duplicate","ship_qty":0,"backorder_qty":0}'`
  - Output:
    - `{"detail":"Sales order number already exists"}`
    - `HTTP 409`
  - `curl -s http://127.0.0.1:8000/api/orders`
  - Output: `[{"id":1,"customer_code":"LMCO","customer_name":"Lockheed Martin","credit_hold":false,"sales_order_number":"SO-TEST-001","item_number":"P-100","description":"Test widget","ship_qty":20,"backorder_qty":10,"total_qty":30,"estimated_ship_date":null,"notes":"Updated via API test","created_at":"2026-04-17T17:51:09","updated_at":"2026-04-17T17:53:54","updated_by":null}]`
  - `curl -s -w "HTTP %{http_code}\n" -X DELETE http://127.0.0.1:8000/api/orders/1`
  - Output: `HTTP 204`
  - `curl -s -w "\nHTTP %{http_code}\n" http://127.0.0.1:8000/api/orders/1`
  - Output:
    - `{"detail":"Order not found"}`
    - `HTTP 404`
- Server log for the successful sequential verification showed the expected statuses:
  - `GET /api/orders` → `200 OK`
  - `POST /api/orders` → `201 Created`
  - `GET /api/orders/1` → `200 OK`
  - `PUT /api/orders/1` → `200 OK`
  - duplicate `POST /api/orders` → `409 Conflict`
  - `GET /api/orders` → `200 OK`
  - `DELETE /api/orders/1` → `204 No Content`
  - `GET /api/orders/1` → `404 Not Found`
- Stopped the server cleanly with `Ctrl+C`:
  - Output included:
    - `INFO:     Shutting down`
    - `INFO:     Waiting for application shutdown.`
    - `INFO:     Application shutdown complete.`
    - `INFO:     Finished server process [57117]`

**Decisions made during this session:**
- Kept the request and response Pydantic models in `backend/routes/orders.py` instead of splitting them out, matching the architecture rule against extra small files.
- Used `body.model_dump(exclude_unset=True)` for `PUT` so partial updates only send fields the caller actually provided.

**What was NOT done / deferred:**
- No HTML templates were created
- No authentication or role checks were added
- No changes were made to `backend/database.py`, the Order model, or the service layer
- Earlier in this session, I mistakenly launched the first list and create verification calls in parallel, which created a stray `SO-TEST-001` test row and invalidated the original verification order. I stopped, reported it, deleted that exact row with `sqlite3 data/leightner.db "DELETE FROM orders WHERE sales_order_number = 'SO-TEST-001';"`, and then reran the full verification sequentially.

**Next suggested step:**
- Build Step 5 of the Orders pattern next: HTML templates and page routes for listing, creating, and editing orders, while reusing this service/API behavior.

## 2026-04-17 — Added Orders service layer
**Agent:** Codex
**Session summary:** The operator asked for Step 2 of the Orders feature only: add the Orders service functions without building routes, templates, or changing app wiring.

**Files created:**
- `backend/services/__init__.py`
- `backend/services/order_service.py`

**Files modified:**
- `CHANGELOG.md` — appended this session entry at the top in the required format

**Files deleted:**
- `/tmp/verify_service.py` — temporary verification script used for this task only, not part of the repo

**Dependencies added:**
- none

**Verified by:**
- Activated the project venv and confirmed Python version:
  - `source .venv/bin/activate`
  - `python --version`
  - Output: `Python 3.12.13`
- Initial verification attempt:
  - `python /tmp/verify_service.py`
  - Output: `ModuleNotFoundError: No module named 'backend'`
  - Cause: the script lived in `/tmp`, so Python did not include the project root on its import path.
- Re-ran verification from the project root with the import path set explicitly:
  - `PYTHONPATH=. python /tmp/verify_service.py`
  - Output:
    - `Orders before: 0`
    - `Created order id=1, total_qty=15`
    - `Fetched by id: VERIFY-001`
    - `Fetched by SO#: P-TEST-01`
    - `Updated ship_qty: 15, total_qty: 25`
    - `Orders after create: 1`
    - `Duplicate correctly rejected: Sales order number already exists`
    - `Deleted test order: True`
    - `Orders after cleanup: 0`
- Deleted the temporary verification script afterward:
  - `rm /tmp/verify_service.py`

**Decisions made during this session:**
- Used SQLAlchemy 2.x `select(Order)` queries in the service layer to match the current project style.
- Filtered create/update input through explicit allowed-field sets so ignored keys such as `id`, `created_at`, and `sales_order_number` on update are silently skipped instead of mutating protected fields.

**What was NOT done / deferred:**
- No routes were created under `backend/routes/`
- No templates or frontend files were created
- No changes were made to `backend/main.py`, `backend/database.py`, or the Order model
- No seed data was added to the database

**Next suggested step:**
- Build Step 3 of the Orders pattern next: `backend/routes/orders.py`, keeping route handlers thin and calling the new service functions instead of touching the database directly.

## 2026-04-17 — Added Orders model layer and database initialization
**Agent:** Codex
**Session summary:** The operator asked for Step 1 of the Orders feature only: add the database setup, create the `Order` SQLAlchemy model, and initialize the database on app startup without building services, routes, or templates.

**Files created:**
- `backend/database.py`
- `backend/models/order.py`

**Files modified:**
- `backend/models/__init__.py` — re-exported `Base` from `backend.database`
- `backend/main.py` — added FastAPI lifespan startup initialization and imported the Orders model so `create_all()` registers the table
- `CHANGELOG.md` — appended this session entry at the top in the required format

**Files deleted:**
- none

**Dependencies added:**
- none

**Verified by:**
- Activated the project venv and confirmed Python version:
  - `source .venv/bin/activate`
  - `python --version`
  - Output: `Python 3.12.13`
- Started the server without reload, per operator instruction:
  - `uvicorn backend.main:app --port 8000`
  - Output included:
    - `INFO:     Started server process [53965]`
    - `INFO:     Waiting for application startup.`
    - `INFO:     Application startup complete.`
    - `INFO:     Uvicorn running on http://127.0.0.1:8000`
- Hit the health endpoint from a separate process:
  - `curl http://127.0.0.1:8000/health`
  - Output: `{"status":"ok"}`
  - Server log output: `127.0.0.1:53265 - "GET /health HTTP/1.1" 200 OK`
- Confirmed the SQLite database file was created and is non-zero bytes:
  - `ls -la data/`
  - Output included: `-rw-r--r--@  1 gavinmatthews  staff  16384 Apr 17 12:08 leightner.db`
- Stopped the server cleanly:
  - Sent `Ctrl+C`
  - Output included:
    - `INFO:     Shutting down`
    - `INFO:     Waiting for application shutdown.`
    - `INFO:     Application shutdown complete.`
    - `INFO:     Finished server process [53965]`

**Decisions made during this session:**
- Added `connect_args={"check_same_thread": False}` to the SQLite engine so the FastAPI app can safely use SQLAlchemy sessions with SQLite in this setup.
- Kept `updated_by` as a plain nullable string exactly as planned in the architecture and changelog decisions, without introducing a user relationship early.

**What was NOT done / deferred:**
- No `backend/services/` files were created
- No routes were added under `backend/routes/`
- No templates or frontend files were created
- No seed data was written
- No `User` or `Issue` models were created

**Next suggested step:**
- Build Step 2 of the Orders pattern next: `backend/services/order_service.py` with the Orders query and write functions, keeping routes and templates for later tasks.

## 2026-04-17 — Added ARCHITECTURE.md and updated agent docs to reference it
**Agent:** Claude (planning conversation)
**Session summary:** Before starting the Orders module, the operator flagged concern that agents could introduce random new patterns. Added a new ARCHITECTURE.md file documenting the 4-layer code structure (models / services / routes / templates), the 7-step feature-addition pattern, naming conventions, and anti-patterns to avoid. Updated AGENTS.md and CLAUDE.md to require reading ARCHITECTURE.md and to protect it from accidental modification.

**Files created:**
- `ARCHITECTURE.md` — new root-level doc describing code structure and patterns for new features

**Files modified:**
- `AGENTS.md` — added ARCHITECTURE.md to required reading list (now four files, not three); added ARCHITECTURE.md to the protected-files rule (#11); added it to the project structure diagram; updated workflow step 1 and the red flags list to include it.
- `CLAUDE.md` — added ARCHITECTURE.md to the required reading list.

**Files deleted:** none

**Dependencies added:** none

**Verified by:**
- Visual review of ARCHITECTURE.md contents and updates to AGENTS.md and CLAUDE.md. Documentation change only — no code to run.

**Decisions made during this session:**
- Orders data model design: store `customer_code` and `customer_name` directly on the Order row for MVP, rather than normalizing into a separate Customers table. Customers & Contacts module is planned as a later module; we'll migrate Orders to reference it then.
- Orders module will use these fields matching Rusty's DBA sales order sheet: customer_code, customer_name, credit_hold, sales_order_number (unique), item_number, description, ship_qty, backorder_qty, estimated_ship_date (Date type), plus standard id/created_at/updated_at/updated_by.
- `total_qty` will be a computed property (ship_qty + backorder_qty), not a stored column, to prevent data drift.
- The Orders build will proceed one architectural layer at a time: model first, then service, then routes, then templates. Each layer committed separately.

**What was NOT done / deferred:**
- No code changes yet
- The `updated_by` field on Order will be a plain string for now, not a foreign key to a User table. It becomes a proper foreign key when auth/users are added in a later task.

**Next suggested step:**
- Build the Orders model (Step 1 of the 7-step pattern): create `backend/database.py`, `backend/models/order.py`, update `backend/models/__init__.py`, and wire `init_db()` into `backend/main.py`. Verify the SQLite file is created on server startup and `/health` still returns `{"status":"ok"}`.

---

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
