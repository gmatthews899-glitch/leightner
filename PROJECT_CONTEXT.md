# Leightner Electronics Inc. — Internal Tools Project

**Last updated:** April 17, 2026
**Maintainer:** [Your name]
**Status:** Phase 0 — prototype built, Rusty has seen an informal preview, formal demo pending

---

## What this document is

The long-term context for this project. Every decision, principle, and reason we've agreed on so far. When a future conversation starts with "what did we decide about X," the answer lives here. Update it when we make new decisions; don't rewrite history when we change our minds — add the new decision and note what changed.

Rusty conversations are being recorded and transcribed. Those transcripts are the primary source material for understanding what to build. Don't design from assumptions — go back to the transcripts.

---

## The company

Leightner Electronics Inc. is a custom transformer and magnetics manufacturer in McKinney, TX, founded in 1968. Low-volume, high-mix, engineered-to-order. Customers include aerospace, defense, space (ISS, NASA programs), maritime (submarines), and oilfield. Long-lifecycle jobs spanning quote → design → prototype → test → production → ship.

Current state of operations: largely paper-based, shared OneDrive for files, no documented SOPs. They use an ERP called **DBA** for sales orders, work orders, and shipping schedules — but it has significant limitations (see DBA notes below). A previous attempt at ISO certification was started but not completed.

### DBA — their current ERP
- Used for sales orders, work orders, and generating shipping schedule reports
- Rusty runs a shipping schedule report regularly to know what's due and when
- Key limitation: when a sales order due date changes, the work order does not automatically update. Rusty tracks the real due date in the sales order only. Work packets printed at job creation show the original date, which quickly becomes stale.
- Not user-friendly. Rusty describes it as having "8 million spices" — it can do a lot but doesn't tell you how.
- **Integration plan: none for now.** Active Jobs data will be entered manually. DBA-to-hub automation is a future consideration, not current scope. We are not blocking on this.

---

## The people

- **Rusty** — General Manager. Wants the tool built, engaged positively in the 04/17 conversation. Skeptical of technology generally but sold himself on the value during the winder machine story. Final decision-maker.
- **Dan** — Owner. Does not always read context or backstory before forming opinions. Rusty sees the issue tracker partly as a way to get Dan up to speed without having to brief him verbally, where Dan filters everything through his own interpretation. The activity log specifically addresses this.
- **Charlie** — Does detailed longhand notes in Access. Knowledgeable but information is siloed and inaccessible to others.
- **Shop floor techs** — future users. Need access from the floor, potentially on tablets. UI must be simple enough that a tech can log an issue without training.
- **Me** — New hire leading this initiative. Not a developer. Working with Claude as planning/design partner and Antigravity (IDE agent) for execution.

---

## The vision

A central hub that acts as the front door to multiple internal tools. Modular — add one tool at a time. Each tool solves a specific pain point.

**Modules and status:**

| # | Module | Status | Notes |
|---|--------|--------|-------|
| 1 | Issue & Corrective Action Tracker | Prototype built | Rusty informal preview done. Formal demo pending. |
| 2 | Active Jobs | Planned — next after module 1 ships | See spec below |
| 3 | Customers & Contacts | Planned | Order not locked |
| 4 | Documents & SOPs | Planned | Order not locked |
| 5 | Reports & Metrics | Planned | Order not locked |

Order of modules 3–5 is not locked. Decided only after current module ships and is in use.

---

## Module specs

### Module 1: Issue & Corrective Action Tracker

**The core problem it solves:** When something goes wrong, the investigation is scattered — verbal updates, personal notes, no shared record. People come back to a problem and don't know what was already tried. New people come in without context and re-litigate settled ground. The tracker gives every issue a single home with a running log of what was tried, what was found, and what was decided.

**Key design insight from Rusty (04/17):** The winder machine story. Rusty diagnosed a shaft balance problem and said to replace the machine. Dan "fixed" it by addressing a different problem entirely — because Dan never read the actual diagnosis. Rusty's words: "if what you had done to fix it was in the activity log, you would have known." The activity log is the most important feature of this module.

**ISO alignment (silent):** The six-stage structure (describe → contain → root cause → corrective action → verify → close) matches ISO 9001 clause 10.2. Not labeled that way in the UI.

**Current prototype fields:**
- id / displayId (e.g. LEI-2026-0001)
- title, description
- reportedBy, dateReported
- category (Production/Process, Quality/Test Failure, Material/Supplier, Design/Engineering, Equipment/Tooling, Shipping/Packaging, Other)
- severity (High / Medium / Low)
- relatedJob, partNumber (both optional)
- containment — immediate action to prevent bad product shipping
- rootCause — underlying cause, not symptom
- correctiveAction — permanent fix
- verification — evidence the fix worked
- status (Open / Contained / Investigating / Action In Progress / Verifying Fix / Closed - Verified / Won't Fix)
- log — dated activity entries with author
- createdAt, updatedAt

Fields are an educated guess pending Rusty's formal review.

---

### Module 2: Active Jobs

**The core problem it solves:** Job due dates change constantly. The shop floor works off paper work packets printed at job creation — those dates go stale immediately. Operators are working jobs based on wrong due dates. Rusty is the only person who knows what's really due when. The result: wrong prioritization, last-minute scrambles, operators feeling like they let the company down when the real problem was bad information.

**Rusty's words (04/17):** "If I had a system where I update the sales order due date and it's readily available — an operator could look it up and go, okay, when's that one really due?" And: "That's probably one of the easiest things we could build, honestly."

**What this module is:**
A simple list of open jobs with a single due date per job that Rusty can update any time. Live, accurate, accessible to everyone on the floor. That's it.

**What it is NOT:**
- Not a replacement for DBA
- Not a work order system
- Not a scheduling tool
- Not automated (manually maintained for now — DBA sync is a someday item)

**Key behavior:**
- When a date changes, the row highlights for 24 hours so operators know something changed
- Operators look up a job by work order number and see the real current due date
- Rusty or a designee updates dates manually when they change in DBA

**Proposed fields (to confirm with Rusty):**
- Job / work order number (from DBA)
- Customer name
- Part description
- Quantity ordered / quantity building (may differ — Rusty sometimes builds extra for yield)
- Due date (the real one, manually maintained)
- Stage (needs Rusty input — Winding? Potting? Test? Ship?)
- Notes (free text)
- Last updated timestamp + who updated
- Recently-changed flag (drives 24-hour highlight behavior)

---

## Real problems we're designing for

### Stycast 2850 FT Blue potting bubbles
30–50% of coil castings show small bubbles after potting. Wasn't a problem before — something changed. Prior engineer Nicholas did a thorough investigation and made process improvements, but knowledge partially left when he did. Dan later re-discovered the same findings without realizing it. A running issue log would have shown Dan what Nicholas already figured out. Classic case of institutional knowledge loss that the tracker prevents.

### Wet-wound bobbin turn count shortage
On certain bobbins, technician completes 80 turns/row on some units but by rows 3–4 can only fit 79 or fewer. Same wire, operator, machine. Suggests bobbin dimensional variation, wire diameter drift, or tension/lubrication inconsistency. Currently measuring bobbins pre-wind.

### The winder machine / shaft balance problem
Machine had worn shaft bearing causing vibration. Rusty diagnosed it, said replace the machine. Dan heard secondhand, "fixed" a different symptom, machine still broken. Root cause of miscommunication: no shared written diagnosis. This story is the clearest argument for the activity log.

---

## Guiding principles

### 1. One thing at a time, all the way through
Don't start the next module until the current one is genuinely done — in use, with real data, backed up. Every new idea goes on the someday list.

### 2. Rusty's approval is a gate, not a suggestion
If he isn't on board, we don't proceed. His skepticism keeps us honest.

### 3. The source of truth is what users say, not what we imagine
Transcripts first. Design from real language and real pain.

### 4. Boring > clever
Proven tools. Every dependency is a future maintenance tax.

### 5. No per-user monthly fees where avoidable
Self-hosted over SaaS. Zero recurring cost is the easiest conversation with Rusty.

### 6. ISO 9001 / AS9100 is a silent design constraint
Structure data so certification records exist if ever pursued. Don't announce it. Don't use ISO jargon in the UI.

### 7. Functional over fancy
Plain sans-serif, sentence case, practical labels. No decorative elements. No clever copy.

### 8. Manual before automated
When there's a choice between "works now, manually" and "works later, automatically," ship manual first. Applies directly to DBA integration — Active Jobs starts as manual entry.

---

## Technical decisions

### Phase 0 (current): Local HTML prototype
- Single HTML file, runs in browser, data in localStorage
- Purpose: show Rusty the vision before investing in real infrastructure
- Not scalable, not multi-user — intentional
- File: leightner-hub.html
- JSON export for backup and future migration

### Phase 1+ (once Rusty approves): Real web app

- **Backend:** Python + FastAPI
- **Database:** SQLite (single file, no server process)
- **Frontend:** HTML/CSS/JavaScript — no React, no build step, no npm
- **Hosting:** Linux mini-PC on the Leightner LAN. Accessible via browser on any office machine.
- **Auth:** Simple username/password to start
- **Backups:** Automated nightly SQLite copy to separate location + OneDrive
- **Deployment:** Local IT consultant for one-day install. We build the app; they handle the Linux box, networking, backups. One-time cost ~$1,000–2,500. Ongoing: $0/month.
- **Hardware:** ~$300–600 mini-PC, one-time.

### Why this stack
- Zero recurring cost
- On-premise — sidesteps ITAR/CMMC concerns from the aerospace/defense customer list
- Simple enough to hand off later
- SQLite = the entire database is one file, trivially backed up
- No build step = a fresh developer can understand the project in 10 minutes

### Tools for building
- **Claude (this project)** — all thinking work: planning, design, data model, writing prompts for the IDE agent
- **Antigravity** — all execution work: file creation, database setup, running the app, iterating
- **Git** — commit after every working change; every commit is a rollback point

### How Claude and Antigravity work together
1. Come to Claude with a goal
2. Claude thinks it through — data model, UX, edge cases, tradeoffs
3. Claude writes a specific, scoped prompt for Antigravity
4. Paste that prompt into Antigravity
5. Agent executes
6. Test the result
7. If it works: git commit
8. If something breaks: bring the error back to Claude

Antigravity should never get open-ended goals. Every prompt specifies: which files to touch, what to change, what NOT to touch, how to verify it worked.

---

## Honest assessment of where we are

- **Prototype:** built and functional. Rusty saw an informal preview 04/17, responded positively.
- **Next gate:** formal demo with Rusty, get explicit green light to move to real build
- **ISO coverage:** ~5–8% of ISO 9001 / AS9100 requirements (Corrective Action clause 10.2, partial Monitoring clause 9.1). Full certification is 12–18 months with a consultant. Not the current goal.
- **Biggest risk:** initiative fizzles because Rusty loses patience or nobody uses what we build. Mitigation: ship fast, get feedback early, never build infrastructure before user validation.

---

## Someday list

Deliberately deferred. Don't touch until current module is done and in use.

- DBA → Active Jobs automated sync
- AI-assisted root cause suggestions on issues (watch API costs carefully)
- Mobile-optimized views for shop floor tablets
- Notifications when issue status changes
- Attachment support on issues (photos, data sheets, PDFs)

---

## Decision log

| Date | Decision | Reason |
|------|----------|--------|
| 2026-04-16 | Start with Issue Tracker as first module | Rusty identified recurring problems as biggest pain; ISO-valuable |
| 2026-04-16 | Build local HTML prototype first | De-risk: get buy-in before infrastructure investment |
| 2026-04-16 | System sans-serif fonts only, no uppercase styling | Rusty preference: functional, no fluff |
| 2026-04-16 | Remove logo from header | User preference |
| 2026-04-16 | Drop explicit ISO references from UI | ISO is quiet design input, not a sales pitch |
| 2026-04-16 | Target Python + FastAPI + SQLite + plain HTML for Phase 1+ | Boring, proven, zero recurring cost, on-prem-friendly |
| 2026-04-16 | Use Claude for planning + IDE agent for execution | Matches strengths of each tool |
| 2026-04-17 | Active Jobs confirmed as module 2 | Rusty described the due-date problem explicitly in 04/17 transcript |
| 2026-04-17 | Active Jobs will use manual entry, not DBA integration | Ship something useful now; automate later |
| 2026-04-17 | ERP confirmed: DBA | Rusty showed DBA in 04/17 conversation |
| 2026-04-17 | Deployment via local IT consultant | Non-developer shouldn't also be sysadmin; one-time cost, zero recurring |

---

## Open questions / still needs Rusty input

- Exact field set for issues — current set is an educated guess
- What job stages exist at Leightner? (For Active Jobs "stage" field)
- Who can log issues — proposed: everyone including floor techs on a shared machine
- What does "High severity" mean at Leightner specifically?
- Who updates Active Jobs dates when DBA changes? (Rusty? An admin?)
- Any fields or concepts missing that he'd expect to see?
