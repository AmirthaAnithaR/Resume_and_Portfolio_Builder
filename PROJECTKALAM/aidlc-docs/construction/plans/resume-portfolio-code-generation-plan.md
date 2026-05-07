# Code Generation Plan
# Unit: resume-portfolio

---

## Unit Context

- **Project Type**: Greenfield, single unit
- **Application Code Location**: Workspace root (`resume-portfolio-builder/`)
- **Documentation Location**: `aidlc-docs/construction/resume-portfolio/code/`
- **Tech Stack**: Python 3.8+ / Flask, HTML5/CSS3/Vanilla JS, SQLite (stdlib)
- **Dependencies**: Flask (only external dependency)

## Stories Covered

All functional requirements from `aidlc-docs/inception/requirements/requirements.md`:
- FR-01: User Input Form (name, email, phone, github, linkedin, education, skills, 3 projects, 3 certs)
- FR-02: Data Persistence (SQLite, single-user, re-submit overwrites)
- FR-03: Resume View (all sections, clean layout)
- FR-04: PDF Download (browser print-to-PDF, print.css)
- FR-05: Portfolio Webpage (same page, About Me / Education / Skills / Projects / Contact)
- FR-06: Navigation (navbar, home ↔ view)

---

## Generation Steps

### Step 1: Project Structure Setup
- [ ] Create `resume-portfolio-builder/` root folder (workspace root)
- [ ] Create `resume-portfolio-builder/templates/` directory
- [ ] Create `resume-portfolio-builder/static/css/` directory
- [ ] Create `resume-portfolio-builder/static/js/` directory
- [ ] Verify `database.py` already exists (generated earlier) — copy/confirm in place

### Step 2: Backend — `app.py`
- [x] Create `resume-portfolio-builder/app.py`
- [x] Implement Flask app initialization and `init_db()` call on startup
- [x] Implement `GET /` route — `index()`: fetch profile, render `index.html`
- [x] Implement `POST /save` route — `save()`: extract form fields, save or update, redirect
- [x] Implement `GET /view` route — `view()`: fetch profile, render `view.html` or redirect
- [x] Add inline comments on every function and route
- [x] Mark FR-02, FR-06 implemented

### Step 3: Backend — `requirements.txt`
- [x] Create `resume-portfolio-builder/requirements.txt`
- [x] Pin Flask version (Flask==3.0.3)

### Step 4: Form Template — `templates/index.html`
- [x] Create `resume-portfolio-builder/templates/index.html`
- [x] Add navbar with Home and View Resume links
- [x] Add Personal Information section (name*, email*, phone*, github, linkedin)
- [x] Add Education section (textarea)
- [x] Add Skills section (textarea)
- [x] Add Projects section (3 fixed groups: title, description, url)
- [x] Add Certifications section (3 fixed groups: name, org, year)
- [x] Add submit button with `data-testid="form-submit-button"`
- [x] Implement Jinja2 pre-population for all fields
- [x] Link `style.css` and `form.js`
- [x] Add `data-testid` attributes to all inputs and the form
- [x] Mark FR-01, FR-06 implemented

### Step 5: View Template — `templates/view.html`
- [x] Create `resume-portfolio-builder/templates/view.html`
- [x] Add navbar
- [x] Add Resume section with all subsections (personal info, education, skills, projects, certs)
- [x] Implement conditional rendering for `github_url`, `linkedin_url`, project URLs
- [x] Add "Download as PDF" button (`onclick="window.print()"`, `data-testid="download-pdf-button"`)
- [x] Add "Edit Details" link (`data-testid="edit-details-link"`)
- [x] Add Portfolio section (About Me, Education, Skills as badges, Projects, Contact)
- [x] Implement skills badge rendering via Jinja2 split loop
- [x] Link `style.css` and `print.css`
- [x] Mark FR-03, FR-04, FR-05, FR-06 implemented

### Step 6: Main Stylesheet — `static/css/style.css`
- [x] Create `resume-portfolio-builder/static/css/style.css`
- [x] Define CSS variables: white background, navy (#1a3c5e) primary, teal (#2a9d8f) accent, light grey (#f5f5f5) secondary
- [x] Style navbar
- [x] Style form layout (sections, labels, inputs, textareas, button)
- [x] Style resume section (clean, professional, print-ready structure)
- [x] Style portfolio section (visually distinct — teal accent headings, card-style projects)
- [x] Style skill badges
- [x] Style action buttons
- [x] Style error messages (red, small, inline)

### Step 7: Print Stylesheet — `static/css/print.css`
- [x] Create `resume-portfolio-builder/static/css/print.css`
- [x] Hide navbar, `.btn-download`, `.btn-edit`, `.portfolio-section` on print
- [x] Set resume section to full width, no background colors, clean margins
- [x] Add `page-break-inside: avoid` on each resume section block
- [x] Set appropriate font size (11pt) and margins (1cm) for print
- [x] Mark FR-04 fully implemented

### Step 8: Form Validation — `static/js/form.js`
- [x] Create `resume-portfolio-builder/static/js/form.js`
- [x] Implement `validateForm(event)` — main handler, attached to form submit
- [x] Implement `validateRequired(fieldId, errorId)` — non-empty check
- [x] Implement `validateEmail(value)` — regex check
- [x] Implement `validateUrl(value)` — http/https regex check
- [x] Implement `clearErrors()` — remove all error messages before re-validation
- [x] Show inline error messages for all failing fields
- [x] Block form submission if any validation fails
- [x] Add comments on every function
- [x] Mark FR-01 validation implemented

### Step 9: Database file placement
- [x] Copy / confirm `database.py` is at `resume-portfolio-builder/database.py`
- [x] Verify schema matches all fields including `github_url`, `linkedin_url`

### Step 10: README — `README.md`
- [x] Create `resume-portfolio-builder/README.md`
- [x] Add project description
- [x] Add prerequisites (Python 3.8+)
- [x] Add setup instructions (clone, venv, pip install)
- [x] Add run instructions (`python app.py`, open browser)
- [x] Add sample test data section
- [x] Add folder structure overview
- [x] Add feature list

### Step 11: Code Summary Documentation
- [x] Create `aidlc-docs/construction/resume-portfolio/code/code-summary.md`
- [x] List all generated files with paths and purpose
- [x] Note any implementation decisions made during generation

---

## Total Steps: 11
## Estimated Files Generated: 10 application files + 1 documentation file
