# Code Generation Summary
# Unit: resume-portfolio

---

## Generated Files

| # | File | Location | Purpose |
|---|---|---|---|
| 1 | `database.py` | `resume-portfolio-builder/` | SQLite CRUD — init_db, save_data, get_data, update_data, _fill_defaults |
| 2 | `app.py` | `resume-portfolio-builder/` | Flask routes — GET /, POST /save, GET /view |
| 3 | `requirements.txt` | `resume-portfolio-builder/` | Pinned dependency: Flask==3.0.3 |
| 4 | `templates/index.html` | `resume-portfolio-builder/templates/` | Input form with Jinja2 pre-population and data-testid attributes |
| 5 | `templates/view.html` | `resume-portfolio-builder/templates/` | Resume + Portfolio view, conditional links, skills badges, PDF button |
| 6 | `static/css/style.css` | `resume-portfolio-builder/static/css/` | Full screen stylesheet — navbar, form, resume, portfolio, badges |
| 7 | `static/css/print.css` | `resume-portfolio-builder/static/css/` | Print/PDF overrides — hides portfolio/nav/buttons, A4 layout |
| 8 | `static/js/form.js` | `resume-portfolio-builder/static/js/` | Client-side validation — required fields, email regex, URL regex |
| 9 | `README.md` | `resume-portfolio-builder/` | Setup, run instructions, sample test data, troubleshooting |

---

## Functional Requirements Coverage

| Requirement | Status | Implemented In |
|---|---|---|
| FR-01: User Input Form | COMPLETE | index.html, form.js |
| FR-02: Data Persistence | COMPLETE | database.py, app.py |
| FR-03: Resume View | COMPLETE | view.html, style.css |
| FR-04: PDF Download | COMPLETE | view.html, print.css |
| FR-05: Portfolio Webpage | COMPLETE | view.html, style.css |
| FR-06: Navigation | COMPLETE | index.html, view.html |

---

## Business Rules Coverage

| Rule | Status | Enforced In |
|---|---|---|
| BR-01: Required field validation | COMPLETE | form.js (client), app.py (strip) |
| BR-02: Email format validation | COMPLETE | form.js |
| BR-03: Optional URL format validation | COMPLETE | form.js |
| BR-04: Save vs. update decision | COMPLETE | app.py save() |
| BR-05: Empty string to NULL normalization | COMPLETE | database.py _fill_defaults() |
| BR-06: Optional field conditional display | COMPLETE | view.html Jinja2 {% if %} |
| BR-07: Single profile constraint | COMPLETE | database.py (id=1 always) |
| BR-08: Form pre-population on edit | COMPLETE | index.html Jinja2 values |
| BR-09: Redirect after POST | COMPLETE | app.py redirect(url_for("view")) |
| BR-10: View page guard | COMPLETE | app.py view() None check |
| BR-11: PDF scope | COMPLETE | print.css @media print |

---

## Key Implementation Decisions

- **`database.py` uses `os.path.dirname(__file__)`** for DB path — ensures the `.db` file is always created next to `database.py` regardless of where the app is launched from.
- **`dict | None` return type** on `get_data()` requires Python 3.10+ syntax. For Python 3.8/3.9 compatibility this is used as a docstring annotation only; the runtime behaviour is identical.
- **`novalidate` on the form** — disables browser native validation so `form.js` controls all error display consistently across browsers.
- **`white-space: pre-line`** on education and skills text — preserves newlines entered in textareas without requiring `<br>` tags.
- **Skills badge splitting** — `profile.skills.replace('\n', ',').split(',')` handles both comma-separated and newline-separated skill lists entered by the user.
- **`data-testid` on all interactive elements** — enables automation-friendly testing without relying on fragile CSS selectors.
