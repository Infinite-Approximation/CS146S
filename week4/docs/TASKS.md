# Tasks for Repo

> **Final status:** All 7 tasks completed. 31 tests pass, format clean.
> Subagents used: **test-agent** (TDD tests), **code-agent** (implementation), **docs-agent** (API.md)

---

## 1) Enable pre-commit and fix the repo
- [x] Install hooks: `pre-commit install`
- [x] Run: `pre-commit run --all-files`
- [x] Fix any formatting/lint issues (black/ruff)

**Completed by:** Claude (main agent, no subagent needed)
**Changes:**
- Copied `pre-commit-config.yaml` → `.pre-commit-config.yaml`
- black reformatted 34 files, ruff auto-fixed 61 issues, end-of-file-fixer fixed 30 files, trailing-whitespace fixed 19 files
- Manually fixed 6 B904 ruff errors (`raise ... from err/None`) across `week1/`, `week2/`, `week6/`

---

## 2) Add search endpoint for notes
- [x] Add/extend `GET /notes/search?q=...` (case-insensitive) using SQLAlchemy filters
- [x] Update `frontend/app.js` to use the search query
- [x] Add tests in `backend/tests/test_notes.py`

**Completed by:** test-agent + code-agent (parallel)
**Changes:**
- Backend search endpoint already existed — verified case-insensitive (SQLite LIKE)
- **test-agent**: wrote 7 search tests (case-insensitive, partial match, no results, title/content match, empty q, no q)
- **code-agent**: added search input `#note-search` in `index.html`, wired `loadNotes()` to call `/notes/search/?q=...` with 300ms debounce

---

## 3) Complete action item flow
- [x] Implement `PUT /action-items/{id}/complete` (already scaffolded)
- [x] Update UI to reflect completion (already wired) and extend test coverage

**Completed by:** test-agent + Claude (main agent)
**Changes:**
- Backend endpoint and frontend UI were already fully implemented
- **test-agent**: wrote 4 tests (404 on nonexistent, idempotent completion, partial completion, initial uncompleted state)
- Added 4 tests to `backend/tests/test_action_items.py`

---

## 4) Improve extraction logic
- [x] Extend `backend/app/services/extract.py` to parse tags like `#tag` and return them
- [x] Add tests for the new parsing behavior
- [x] (Optional) Expose `POST /notes/{id}/extract` that turns notes into action items
- [x] Update API.md

**Completed by:** code-agent (implementation + tests) + docs-agent (API.md)
**Changes:**
- **code-agent**: added `extract_tags(text)` using `re.findall(r"(?:^|\s)#(\w+)", text)`, added `ExtractResult` schema, added `POST /{note_id}/extract` endpoint, wrote 7 tag extraction tests
- **docs-agent**: created `API.md` documenting all 8 endpoints

---

## 5) Notes CRUD enhancements
- [x] Add `PUT /notes/{id}` to edit a note (title/content)
- [x] Add `DELETE /notes/{id}` to delete a note
- [x] Update `frontend/app.js` to support edit/delete; add tests
- [x] Update API.md

**Completed by:** code-agent (implementation + frontend) + Claude (main agent, tests + API.md)
**Changes:**
- **code-agent**: added `NoteUpdate` schema, `PUT /{note_id}` and `DELETE /{note_id}` endpoints, added Edit/Delete buttons in `loadActions()`
- **Claude**: wrote 4 CRUD tests (update, update 404, delete, delete 404), updated API.md with PUT/DELETE docs

---

## 6) Request validation and error handling
- [x] Add simple validation rules (e.g., min lengths) to `schemas.py`
- [x] Return informative 400/404 errors where appropriate; add tests for validation failures
- [x] Update API.md

**Completed by:** test-agent + code-agent (parallel)
**Changes:**
- **test-agent**: wrote 6 validation failure tests (empty title, empty content, missing fields, update empty title, empty description, missing description)
- **code-agent**: added `Field` constraints to `NoteCreate` (title: 1-200, content: min 1), `NoteUpdate` (same), `ActionItemCreate` (description: min 1)

---

## 7) Docs drift check (manual for now)
- [x] Create/maintain a simple `API.md` describing endpoints and payloads
- [x] After each change, verify docs match actual OpenAPI (`/openapi.json`)

**Completed by:** Claude (main agent)
**Changes:**
- Drift found: schema docs missing `Field` validation constraints from Task 6
- Updated `NoteCreate`, `NoteUpdate`, `ActionItemCreate` tables with Constraints column
- All 8 endpoints verified correct — no endpoint drift
