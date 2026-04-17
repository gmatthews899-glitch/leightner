# Architecture — Leightner Internal Tools

This document describes how the codebase is structured. Agents MUST read this before creating new files or adding new modules. Every new feature follows the same pattern documented here. Do not invent new patterns without discussion.

---

## Philosophy

This is a small internal tool maintained by a non-developer. The architecture prioritizes:

1. **Readability over cleverness.** Any reasonably technical person should be able to open a file and understand what it does in under a minute.
2. **Consistency over flexibility.** Every module looks the same. New modules do not get to invent new patterns.
3. **No magic.** Explicit imports, explicit route registration, explicit database session handling. If a framework feature would make code shorter but harder to follow, we don't use it.
4. **Few files, not many small ones.** Don't split code into tiny files just because. A 200-line file is fine; a 20-file feature is not.

---

## The layered structure

Every feature in this app is built in four predictable layers. Understanding these four layers is enough to understand the whole codebase.

```
┌─────────────────────────────────────────────────┐
│ 1. HTML TEMPLATES (what the user sees)         │
│    frontend/templates/*.html                    │
└─────────────────────────────────────────────────┘
                      ▲
                      │ rendered by
                      │
┌─────────────────────────────────────────────────┐
│ 2. ROUTES (handle HTTP requests)               │
│    backend/routes/*.py                          │
│    - Parse request                              │
│    - Call service function                      │
│    - Return response (HTML or JSON)             │
└─────────────────────────────────────────────────┘
                      ▲
                      │ calls
                      │
┌─────────────────────────────────────────────────┐
│ 3. SERVICES (business logic)                   │
│    backend/services/*.py                        │
│    - All the "thinking" lives here              │
│    - Receives data, talks to database,          │
│      returns data                               │
└─────────────────────────────────────────────────┘
                      ▲
                      │ uses
                      │
┌─────────────────────────────────────────────────┐
│ 4. MODELS (database tables)                    │
│    backend/models/*.py                          │
│    - Defines what the data looks like           │
│    - One class per database table               │
└─────────────────────────────────────────────────┘
```

**Rules about the layers:**

- Routes NEVER talk directly to the database. They call services.
- Services DO talk to the database via models. They contain all business logic.
- Models NEVER call services or routes. They just define data shape.
- Templates NEVER contain business logic. They just render data the route passes in.

If you catch yourself writing a database query in a route handler, stop and move it to a service.

---

## Full project structure (target)

```
leightner/
├── AGENTS.md                    # Agent instructions (how to work)
├── ARCHITECTURE.md              # This file
├── CLAUDE.md                    # Claude-specific pointer
├── PROJECT_CONTEXT.md           # Business context
├── CHANGELOG.md                 # History of changes
├── README.md                    # How to run
├── requirements.txt             # Pinned dependencies
├── .gitignore
├── .env                         # Secrets, never committed
├── .env.example                 # Placeholder template, committed
├── leightner-hub.html           # Reference prototype, do not modify
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app assembly, middleware, route registration
│   ├── database.py              # SQLAlchemy engine + session factory
│   ├── config.py                # Load env vars, centralize config
│   ├── dependencies.py          # Shared FastAPI dependencies (get_db, get_current_user)
│   ├── auth.py                  # Login, session, password hashing helpers
│   │
│   ├── models/
│   │   ├── __init__.py          # Base = declarative_base(); re-export models
│   │   ├── user.py              # User model
│   │   ├── order.py             # Order model
│   │   └── issue.py             # Issue model (when we port it)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── hub.py               # GET / → hub landing page
│   │   ├── auth.py              # GET/POST /login, POST /logout
│   │   ├── orders.py            # Orders CRUD (pages + API)
│   │   └── issues.py            # Issues CRUD (when we port it)
│   │
│   └── services/
│       ├── __init__.py
│       ├── order_service.py     # list_orders, create_order, update_order, etc.
│       └── issue_service.py     # (when we port it)
│
├── frontend/
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Common layout (header, nav, footer)
│   │   ├── hub.html             # Landing page
│   │   ├── login.html
│   │   ├── orders/
│   │   │   ├── list.html        # List view
│   │   │   ├── new.html         # Create form
│   │   │   └── edit.html        # Edit form
│   │   └── issues/...
│   │
│   └── static/
│       ├── css/
│       │   └── styles.css       # One global stylesheet
│       └── js/
│           └── app.js           # One global JS file (if needed)
│
└── data/
    └── leightner.db             # SQLite database file (gitignored)
```

**Do not create files that aren't needed by the current task.** The structure above is a target, not an instruction to build everything at once.

---

## How a new feature is added (the repeatable pattern)

When adding a new module (e.g. Orders, Issues, Contacts), follow these steps IN ORDER. Do not skip steps or reorder them.

### Step 1: Model
Create `backend/models/<name>.py` with a SQLAlchemy class. One class per table.

### Step 2: Service
Create `backend/services/<name>_service.py` with functions like `list_X`, `get_X`, `create_X`, `update_X`, `delete_X`. All database queries live here.

### Step 3: Routes
Create `backend/routes/<name>.py` with route handlers. Each handler calls a service function and returns a response.

### Step 4: Register the router in `main.py`
Add one line to import the router and one line to `app.include_router()`.

### Step 5: Templates
Create templates under `frontend/templates/<name>/`. Extend `base.html`.

### Step 6: Update navigation
Add the new page to `base.html`'s navigation if appropriate.

### Step 7: Add CHANGELOG entry
As always.

Every feature gets these same 7 steps. No shortcuts, no creative reinterpretations.

---

## Conventions that apply everywhere

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Database tables: `snake_case`, plural (`orders`, `issues`, `users`)
- URL paths: kebab-case or lowercase (`/orders`, `/login`, `/api/orders/recent-updates`)

### Database
- Every model has `id: int` primary key, `created_at: datetime` (UTC), `updated_at: datetime` (UTC)
- `updated_at` auto-updates on any row change (SQLAlchemy `onupdate=func.now()`)
- Timestamps are timezone-aware, stored as UTC
- Date-only fields (due dates) use `Date`, not `DateTime`
- Foreign keys are explicit and named `<table>_id` (e.g. `user_id`)
- No cascading deletes without discussion — prefer soft deletes via a `deleted_at` column if needed

### Routes
- GET routes return rendered HTML (for pages) or JSON (for API endpoints under `/api/`)
- POST/PUT/DELETE that come from forms redirect to a GET after success (post-redirect-get pattern)
- All routes that require authentication use the `get_current_user` dependency
- Admin-only routes use `get_current_admin` dependency
- Errors return user-friendly messages; server logs get the details

### Services
- Every service function receives a `db: Session` as its first argument
- Services return plain data (model instances, dicts, lists), not HTTP responses
- No `print()` calls — use the Python `logging` module when needed
- Validation errors raise exceptions; the route catches them and returns a friendly response

### Templates
- Every template extends `base.html` via `{% extends "base.html" %}`
- Every template has one job — the list view, the edit form, etc. — no branching inside templates
- Inline `{% if user.is_admin %}` is fine; complex logic moves to the service layer
- No JavaScript frameworks. Plain `<script>` tags or Alpine.js/HTMX only (see AGENTS.md)

### Styles
- One stylesheet: `frontend/static/css/styles.css`
- Uses CSS variables for colors (copy the palette from `leightner-hub.html`)
- System sans-serif fonts only
- No separate stylesheet per page unless there's a specific reason

---

## What to NOT do

- **Do not introduce new layers** (e.g. "repositories," "managers," "facades"). The four layers are enough.
- **Do not add service "base classes"** or abstract parent classes for models. Each model is its own class, repeated patterns are OK.
- **Do not add dependency injection frameworks**, decorators for cross-cutting concerns, or metaclass magic. FastAPI's built-in `Depends()` is enough.
- **Do not split routes into multiple files per module.** One file per module (`routes/orders.py`, `routes/issues.py`). No `orders_list.py` + `orders_create.py`.
- **Do not add configuration that isn't used.** Don't add a "plugins" folder because we might want plugins someday. Add things when they're needed, not before.
- **Do not reorganize the structure when adding a new feature.** If a feature doesn't fit the pattern, stop and discuss — don't reinvent.

---

## Summary checklist for agents

Before starting any new feature, confirm:

- [ ] I have read `PROJECT_CONTEXT.md`, `CHANGELOG.md`, `AGENTS.md`, and this file
- [ ] I know which module I'm adding and what it's called
- [ ] I will follow the 7-step pattern in order: model → service → routes → register → templates → nav → changelog
- [ ] I will not invent new architectural layers or patterns
- [ ] I will match existing naming conventions
- [ ] I will update the CHANGELOG when done

If any of those are unclear, ask the operator before writing code.
