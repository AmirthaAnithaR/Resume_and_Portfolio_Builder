# Component Dependencies

## Overview
This document maps dependencies and communication patterns between all components in the AI CV Builder application.

---

## Dependency Matrix

| Component | Depends On | Used By | Communication Pattern |
|-----------|------------|---------|----------------------|
| **Frontend Templates** |
| base.html | style.css, print.css | All page templates | Template inheritance |
| landing.html | base.html, style.css | None (entry point) | Extends base |
| form.html | base.html, style.css, form.js, form-wizard.js | None (user navigates) | Extends base, includes JS |
| template-selection.html | base.html, style.css, template-preview.js | None (after form submit) | Extends base, includes JS |
| resume-template1.html | style.css, print.css | view.html | Included by view.html |
| resume-template2.html | style.css, print.css | view.html | Included by view.html |
| resume-template3.html | style.css, print.css | view.html | Included by view.html |
| view.html | base.html, style.css, print.css, resume templates | None (final page) | Extends base, includes template |
| **Backend Components** |
| app.py | database.py, Flask, Jinja2 | None (entry point) | Function calls |
| database.py | sqlite3, os | app.py | Function calls |
| **JavaScript Components** |
| form-wizard.js | form.html DOM | None | DOM manipulation |
| form.js | form.html DOM | form-wizard.js (indirectly) | DOM manipulation, event handling |
| template-preview.js | template-selection.html DOM | None | DOM manipulation, fetch API |
| **CSS Components** |
| style.css | None | All templates | CSS import/link |
| print.css | None | Resume templates, view.html | CSS media query |

---

## Dependency Graph

```
User Browser
    |
    +-- landing.html
    |   |-- extends base.html
    |   |-- uses style.css
    |   |-- links to /form
    |
    +-- form.html
    |   |-- extends base.html
    |   |-- uses style.css
    |   |-- includes form-wizard.js
    |   |-- includes form.js
    |   |-- submits to POST /save
    |
    +-- template-selection.html
    |   |-- extends base.html
    |   |-- uses style.css
    |   |-- includes template-preview.js
    |   |-- links to /view?template=X
    |
    +-- view.html
        |-- extends base.html
        |-- uses style.css, print.css
        |-- includes resume-template{1,2,3}.html
        |-- links to /form (edit), /select-template (change)

Flask Application (app.py)
    |
    +-- Route: GET /
    |   |-- renders landing.html
    |
    +-- Route: GET /form
    |   |-- calls database.get_data()
    |   |-- renders form.html with profile
    |
    +-- Route: POST /save
    |   |-- calls database.get_data()
    |   |-- calls database.save_data() or update_data()
    |   |-- redirects to /select-template
    |
    +-- Route: GET /select-template
    |   |-- calls database.get_data()
    |   |-- renders template-selection.html with profile
    |
    +-- Route: POST /save-template or GET with ?template=X
    |   |-- calls database.get_data()
    |   |-- calls database.update_data() with template_choice
    |   |-- redirects to /view
    |
    +-- Route: GET /view
        |-- calls database.get_data()
        |-- determines template filename
        |-- renders view.html with profile and template

Database (database.py)
    |
    +-- init_db()
    |   |-- connects to resume_portfolio.db
    |   |-- creates profile table
    |
    +-- save_data(data)
    |   |-- connects to resume_portfolio.db
    |   |-- inserts row with id=1
    |
    +-- get_data()
    |   |-- connects to resume_portfolio.db
    |   |-- selects row with id=1
    |   |-- returns dict or None
    |
    +-- update_data(data)
        |-- connects to resume_portfolio.db
        |-- updates row with id=1
```

---

## Communication Patterns

### Pattern 1: Template Inheritance (Jinja2)
**Components**: base.html → landing.html, form.html, template-selection.html, view.html

**Flow**:
```
base.html defines structure
    ↓
Child template extends base.html
    ↓
Child template overrides blocks (title, content, scripts)
    ↓
Jinja2 renders combined template
```

**Benefits**:
- DRY (Don't Repeat Yourself) - navigation and footer defined once
- Consistent layout across pages
- Easy to update common elements

---

### Pattern 2: Template Inclusion (Jinja2)
**Components**: view.html → resume-template{1,2,3}.html

**Flow**:
```
view.html determines template choice
    ↓
view.html includes selected template: {% include template_file %}
    ↓
Resume template renders with profile data
    ↓
Jinja2 renders combined output
```

**Benefits**:
- Dynamic template selection
- Reusable resume templates
- Separation of concerns (view logic vs template rendering)

---

### Pattern 3: HTTP Request/Response (Flask)
**Components**: Browser → Flask app.py → Database database.py

**Flow**:
```
User action (click, form submit)
    ↓
Browser sends HTTP request (GET/POST)
    ↓
Flask route handler receives request
    ↓
Route handler calls database functions
    ↓
Database returns data or None
    ↓
Route handler renders template or redirects
    ↓
Flask sends HTTP response
    ↓
Browser displays page
```

**Benefits**:
- Standard web architecture
- Stateless (except database)
- RESTful-ish design

---

### Pattern 4: DOM Manipulation (JavaScript)
**Components**: form-wizard.js, form.js, template-preview.js → HTML DOM

**Flow**:
```
Page loads
    ↓
JavaScript initializes (DOMContentLoaded)
    ↓
JavaScript attaches event listeners
    ↓
User interacts (click, input)
    ↓
Event handler executes
    ↓
JavaScript manipulates DOM (show/hide, update text, add classes)
    ↓
Browser re-renders affected elements
```

**Benefits**:
- Interactive UI without page reloads
- Smooth transitions
- Immediate feedback

---

### Pattern 5: Form Submission (HTML → Flask)
**Components**: form.html → POST /save → database.py

**Flow**:
```
User fills form
    ↓
User clicks Submit (or Next on last step)
    ↓
JavaScript validates (optional)
    ↓
Form submits to POST /save
    ↓
Flask extracts form data (request.form)
    ↓
Flask calls database.save_data() or update_data()
    ↓
Database saves to SQLite
    ↓
Flask redirects to /select-template
    ↓
Browser navigates to template selection page
```

**Benefits**:
- Standard HTML form submission
- Server-side data persistence
- POST-Redirect-GET pattern prevents duplicate submissions

---

### Pattern 6: CSS Styling (CSS → HTML)
**Components**: style.css, print.css → All templates

**Flow**:
```
Template includes CSS: <link rel="stylesheet" href="...">
    ↓
Browser loads CSS file
    ↓
Browser applies styles to HTML elements
    ↓
Browser renders styled page
```

**Benefits**:
- Separation of content and presentation
- Reusable styles across pages
- Responsive design with media queries

---

## Dependency Rules

### Rule 1: No Circular Dependencies
**Enforcement**: Templates extend base.html but base.html doesn't depend on child templates

**Example**:
- ✅ GOOD: form.html extends base.html
- ❌ BAD: base.html extends form.html (circular)

---

### Rule 2: One-Way Data Flow (Backend → Frontend)
**Enforcement**: Flask passes data to templates, templates don't modify backend state directly

**Example**:
- ✅ GOOD: Flask calls database.get_data(), passes to template
- ❌ BAD: Template directly queries database (not possible in Jinja2, but conceptually wrong)

---

### Rule 3: JavaScript Doesn't Depend on Backend Code
**Enforcement**: JavaScript is client-side only, communicates via HTTP

**Example**:
- ✅ GOOD: JavaScript sends fetch() request to /api/preview
- ❌ BAD: JavaScript imports Python functions (not possible, but conceptually wrong)

---

### Rule 4: Templates Don't Depend on Each Other (Except Inheritance)
**Enforcement**: Each template is self-contained, only depends on base.html

**Example**:
- ✅ GOOD: form.html extends base.html
- ❌ BAD: form.html includes landing.html (unnecessary coupling)

---

### Rule 5: Database is Only Accessed by app.py
**Enforcement**: Only route handlers call database functions

**Example**:
- ✅ GOOD: app.py calls database.get_data()
- ❌ BAD: Template calls database.get_data() (not possible in Jinja2, but conceptually wrong)

---

## Data Flow Diagrams

### Data Flow 1: User Creates Resume

```
User
  |
  | 1. Visits /
  v
Landing Page (landing.html)
  |
  | 2. Clicks "Get Started"
  v
Form Page (form.html)
  |
  | 3. Fills form (5 steps)
  | 4. Clicks Submit
  v
POST /save (app.py)
  |
  | 5. Extracts form data
  | 6. Calls database.save_data()
  v
Database (database.py)
  |
  | 7. Inserts row into SQLite
  v
Redirect to /select-template
  |
  v
Template Selection Page (template-selection.html)
  |
  | 8. User clicks template
  | 9. Clicks "Use Template"
  v
GET /view?template=X (app.py)
  |
  | 10. Calls database.get_data()
  | 11. Updates template_choice
  | 12. Calls database.update_data()
  v
Redirect to /view
  |
  v
Final Resume Page (view.html)
  |
  | 13. Includes selected resume template
  | 14. Renders with profile data
  v
User sees resume + portfolio
```

---

### Data Flow 2: User Edits Resume

```
User
  |
  | 1. Visits /view (has existing profile)
  v
Final Resume Page (view.html)
  |
  | 2. Clicks "Edit Details"
  v
GET /form (app.py)
  |
  | 3. Calls database.get_data()
  | 4. Passes profile to template
  v
Form Page (form.html)
  |
  | 5. Pre-populates fields with profile data
  | 6. User edits fields
  | 7. Clicks Submit
  v
POST /save (app.py)
  |
  | 8. Extracts form data
  | 9. Calls database.update_data()
  v
Database (database.py)
  |
  | 10. Updates row in SQLite
  v
Redirect to /select-template
  |
  | (User can change template or keep existing)
  v
Final Resume Page (view.html)
  |
  | 11. Shows updated resume
  v
User sees updated resume
```

---

### Data Flow 3: User Changes Template

```
User
  |
  | 1. Visits /view (has existing profile)
  v
Final Resume Page (view.html)
  |
  | 2. Clicks "Change Template"
  v
GET /select-template (app.py)
  |
  | 3. Calls database.get_data()
  | 4. Passes profile to template
  v
Template Selection Page (template-selection.html)
  |
  | 5. Shows 3 templates with user's data
  | 6. User clicks different template
  | 7. Clicks "Use Template"
  v
GET /view?template=Y (app.py)
  |
  | 8. Calls database.get_data()
  | 9. Updates template_choice to Y
  | 10. Calls database.update_data()
  v
Redirect to /view
  |
  v
Final Resume Page (view.html)
  |
  | 11. Includes new template (Y)
  | 12. Renders with profile data
  v
User sees resume with new template
```

---

## Coupling Analysis

### Tight Coupling (Acceptable)
- **form.html ↔ form-wizard.js**: Form structure and wizard logic are tightly coupled (expected)
- **view.html ↔ resume templates**: View page must include resume templates (expected)
- **app.py ↔ database.py**: Route handlers must call database functions (expected)

### Loose Coupling (Good)
- **Templates ↔ CSS**: Templates reference CSS classes, but CSS can change independently
- **JavaScript ↔ Backend**: JavaScript communicates via HTTP, not direct function calls
- **Resume templates ↔ profile data**: Templates expect dict with specific keys, but handle missing data gracefully

### No Coupling (Ideal)
- **Landing page ↔ Form page**: Independent pages, only linked by navigation
- **Template 1 ↔ Template 2 ↔ Template 3**: Independent templates, no shared code (except base styles)

---

## Summary

**Total Dependencies**: 17 components with clear dependency relationships

**Dependency Patterns**:
- Template inheritance (Jinja2)
- Template inclusion (Jinja2)
- HTTP request/response (Flask)
- DOM manipulation (JavaScript)
- Form submission (HTML → Flask)
- CSS styling (CSS → HTML)

**Dependency Rules**:
- No circular dependencies
- One-way data flow (backend → frontend)
- JavaScript doesn't depend on backend code
- Templates don't depend on each other (except inheritance)
- Database only accessed by app.py

**Coupling Level**: Mostly loose coupling with some acceptable tight coupling where necessary

**Data Flow**: Clear unidirectional flow from user actions → backend → database → backend → frontend → user
