# Application Design: AI CV Builder

## Executive Summary

This document consolidates the complete application design for the AI CV Builder redesign, including component definitions, method signatures, service layer decisions, and dependency relationships.

**Design Approach**: Beginner-friendly Flask application with minimal service layer, using helper functions instead of service classes.

**Architecture Pattern**: Model-View-Controller (MVC) with template inheritance and client-side interactivity.

**Key Design Decisions**:
- ✅ Template inheritance for consistent layout (base.html)
- ✅ Multi-step form with client-side state management (JavaScript)
- ✅ Three separate resume template files with dynamic inclusion
- ✅ Minimal service layer (helper functions instead of classes)
- ✅ Client-side validation with optional server-side backup
- ✅ Flat routing structure in app.py (beginner-friendly)
- ✅ Existing database pattern maintained (database.py functions)

---

## 1. Component Overview

### 1.1 Component Summary

| Category | Count | Components |
|----------|-------|------------|
| **Frontend Templates** | 10 | base.html, landing.html, form.html, template-selection.html, resume-template{1,2,3}.html, view.html, navigation (in base), footer (in base) |
| **Backend** | 2 | app.py (route handlers), database.py (data access) |
| **JavaScript** | 3 | form-wizard.js, form.js, template-preview.js |
| **CSS** | 2 | style.css, print.css |
| **Total** | 17 | All components |

### 1.2 Component Responsibilities

**Frontend Templates**:
- **base.html**: Common layout structure, navigation, footer
- **landing.html**: Welcome page with hero section, features, testimonials
- **form.html**: Multi-step form wizard (5 steps) for profile input
- **template-selection.html**: Display 3 template options with preview
- **resume-template{1,2,3}.html**: Three distinct resume styles
- **view.html**: Final resume + portfolio display with action buttons

**Backend**:
- **app.py**: HTTP routing, request handling, template rendering
- **database.py**: SQLite database operations (CRUD)

**JavaScript**:
- **form-wizard.js**: Multi-step form navigation and state management
- **form.js**: Client-side form validation
- **template-preview.js**: Template preview modal handling

**CSS**:
- **style.css**: Global styles, premium theme (white + navy + teal)
- **print.css**: Print-optimized styles for PDF download

---

## 2. Component Methods

### 2.1 Backend Methods (app.py)

**Route Handlers** (7 methods):
1. `index()` - GET / - Display landing page
2. `form()` - GET /form - Display multi-step form
3. `save()` - POST /save - Save/update profile data
4. `select_template()` - GET /select-template - Display template selection
5. `save_template_choice()` - POST /save-template - Save template choice
6. `view()` - GET /view - Display final resume + portfolio
7. `get_template_name()` - Helper to map template choice to filename

**Helper Functions** (4 functions):
- `get_template_filename(template_choice)` - Map choice to filename
- `get_default_template_choice()` - Return default template
- `extract_form_data(request_form)` - Extract and clean form data
- `validate_required_fields(data)` - Optional server-side validation

### 2.2 Database Methods (database.py)

**Existing Methods** (5 methods):
1. `init_db()` - Initialize database and create table
2. `save_data(data)` - Insert new profile
3. `get_data()` - Retrieve profile (returns dict or None)
4. `update_data(data)` - Update existing profile
5. `_fill_defaults(data)` - Ensure all keys present

**New Optional Method** (1 method):
6. `update_template_choice(template_choice)` - Update only template field

### 2.3 JavaScript Methods

**Form Wizard** (8 methods):
- `initFormWizard()` - Initialize on page load
- `showStep(stepNumber)` - Display specific step
- `nextStep()` - Validate and move to next step
- `prevStep()` - Move to previous step
- `validateStep(stepNumber)` - Validate step fields
- `saveFormState()` - Save form data to memory
- `restoreFormState()` - Restore form data from memory
- `updateProgress(stepNumber)` - Update progress indicator

**Form Validation** (7 methods):
- `validateForm(event)` - Main validation handler
- `validateRequired(fieldId, errorId, message)` - Check required fields
- `validateEmail(value)` - Validate email format
- `validateUrl(value)` - Validate URL format
- `validateOptionalUrl(fieldId, errorId, message)` - Validate optional URLs
- `showError(fieldId, errorId, message)` - Display error
- `clearErrors()` - Clear all errors

**Template Preview** (5 methods):
- `initTemplatePreview()` - Initialize on page load
- `showPreview(templateId)` - Show modal with preview
- `closePreview()` - Close modal
- `selectTemplate(templateId)` - Save selection and navigate
- `renderPreview(templateId, profileData)` - Generate preview HTML

### 2.4 Template Methods (Jinja2 Macros)

**Form Step Macros** (5 macros):
- `render_step_1(profile)` - Personal Information
- `render_step_2(profile)` - Education
- `render_step_3(profile)` - Skills
- `render_step_4(profile)` - Projects
- `render_step_5(profile)` - Certifications

**Resume Template Macros** (5 macros):
- `render_header(profile)` - Header with name and contact
- `render_education(profile)` - Education section
- `render_skills(profile, style)` - Skills section (list/badges/visual)
- `render_projects(profile, style)` - Projects section (list/cards/portfolio)
- `render_certifications(profile, style)` - Certifications section (list/timeline/badges)

**Total Methods**: 43 methods across all components

---

## 3. Service Layer Design

### 3.1 Service Architecture Decision

**Approach**: **Minimal Service Layer** - Use helper functions instead of service classes

**Rationale**:
- Beginner-friendly requirement favors simplicity
- Flask application is small and straightforward
- Avoid over-engineering for a learning project
- Business logic is not complex enough to warrant separate service classes

### 3.2 Helper Functions (Instead of Services)

**Template Selection Helpers**:
- `get_template_filename(template_choice)` - Map choice to filename
- `get_default_template_choice()` - Return default template

**Form Data Helpers**:
- `extract_form_data(request_form)` - Extract and clean form data

**Validation Helpers** (Optional):
- `validate_required_fields(data)` - Server-side validation backup

**Data Formatting Helpers**:
- `format_skills_list(skills_text)` - Parse skills into list
- `truncate_text(text, max_length)` - Truncate long text

### 3.3 Orchestration Patterns

**Pattern 1: Form Submission Flow**
```
User submits form → POST /save → extract_form_data() → 
get_data() → save_data() or update_data() → Redirect to /select-template
```

**Pattern 2: Template Selection Flow**
```
User selects template → GET /select-template?template=X → 
get_data() → update template_choice → update_data() → Redirect to /view
```

**Pattern 3: Resume Rendering Flow**
```
User visits /view → GET /view → get_data() → 
get_template_filename() → render_template() → Include resume template
```

---

## 4. Component Dependencies

### 4.1 Dependency Matrix

| Component | Depends On | Used By |
|-----------|------------|---------|
| base.html | style.css, print.css | All page templates |
| landing.html | base.html | None (entry point) |
| form.html | base.html, form-wizard.js, form.js | None |
| template-selection.html | base.html, template-preview.js | None |
| resume-template{1,2,3}.html | style.css, print.css | view.html |
| view.html | base.html, resume templates | None |
| app.py | database.py, Flask, Jinja2 | None (entry point) |
| database.py | sqlite3 | app.py |
| form-wizard.js | form.html DOM | None |
| form.js | form.html DOM | form-wizard.js (indirectly) |
| template-preview.js | template-selection.html DOM | None |
| style.css | None | All templates |
| print.css | None | Resume templates, view.html |

### 4.2 Communication Patterns

**Pattern 1: Template Inheritance** (Jinja2)
- base.html defines structure → Child templates extend and override blocks

**Pattern 2: Template Inclusion** (Jinja2)
- view.html includes selected resume template dynamically

**Pattern 3: HTTP Request/Response** (Flask)
- Browser → Flask route handler → Database → Flask → Browser

**Pattern 4: DOM Manipulation** (JavaScript)
- JavaScript attaches event listeners → User interacts → JavaScript updates DOM

**Pattern 5: Form Submission** (HTML → Flask)
- User fills form → Form submits → Flask processes → Database saves → Redirect

**Pattern 6: CSS Styling** (CSS → HTML)
- Templates link CSS → Browser loads and applies styles

### 4.3 Dependency Rules

1. **No Circular Dependencies**: Templates extend base.html but base.html doesn't depend on children
2. **One-Way Data Flow**: Backend → Frontend (Flask passes data to templates)
3. **JavaScript Independence**: JavaScript communicates via HTTP, not direct backend calls
4. **Template Independence**: Each template is self-contained (except inheritance)
5. **Database Access Control**: Only app.py calls database functions

### 4.4 Data Flow

**User Creates Resume**:
```
User → Landing Page → Form Page (5 steps) → POST /save → Database → 
Template Selection → GET /view → Final Resume Page
```

**User Edits Resume**:
```
User → Final Resume Page → Edit Details → Form Page (pre-populated) → 
POST /save → Database → Template Selection → Final Resume Page (updated)
```

**User Changes Template**:
```
User → Final Resume Page → Change Template → Template Selection → 
Select New Template → Database → Final Resume Page (new template)
```

---

## 5. Design Patterns

### 5.1 Architectural Patterns

**MVC (Model-View-Controller)**:
- **Model**: database.py (data access)
- **View**: templates/*.html (presentation)
- **Controller**: app.py (request handling)

**Template Inheritance** (Jinja2):
- base.html provides common structure
- Child templates extend and customize

**Repository Pattern**:
- database.py abstracts database operations
- CRUD functions (save, get, update)

**POST-Redirect-GET**:
- POST /save → Redirect to /select-template
- Prevents duplicate form submissions

### 5.2 Design Principles

**Single Responsibility**:
- app.py: HTTP routing only
- database.py: Data access only
- form.js: Client validation only

**DRY (Don't Repeat Yourself)**:
- base.html defines navigation and footer once
- CSS variables for color palette
- Helper functions for common operations

**Separation of Concerns**:
- Frontend (templates, CSS, JS) separate from backend (app.py, database.py)
- Presentation logic in templates, business logic in backend

**Progressive Enhancement**:
- Form works without JavaScript (server-side fallback)
- Client-side validation enhances UX

---

## 6. Database Schema

### 6.1 Existing Fields (27 fields)

**Personal Information** (5 fields):
- name, email, phone, github_url, linkedin_url

**Education and Skills** (2 fields):
- education, skills

**Projects** (9 fields):
- project1_title, project1_desc, project1_url
- project2_title, project2_desc, project2_url
- project3_title, project3_desc, project3_url

**Certifications** (9 fields):
- cert1_name, cert1_org, cert1_year
- cert2_name, cert2_org, cert2_year
- cert3_name, cert3_org, cert3_year

**Primary Key** (1 field):
- id (always 1 for single-user)

### 6.2 New Optional Fields (2 fields)

**Template Selection** (1 field):
- template_choice (TEXT, nullable) - Stores "template1", "template2", or "template3"

**Professional Summary** (1 field):
- summary (TEXT, nullable) - Optional professional summary/objective

### 6.3 Schema Migration

**Approach**: ALTER TABLE to add new columns with NULL defaults

**SQL**:
```sql
ALTER TABLE profile ADD COLUMN template_choice TEXT;
ALTER TABLE profile ADD COLUMN summary TEXT;
```

**Backward Compatibility**: Existing data remains intact, new fields are optional

---

## 7. Routing Structure

### 7.1 Route Map

| Route | Method | Purpose | Template | Redirect |
|-------|--------|---------|----------|----------|
| / | GET | Landing page | landing.html | - |
| /form | GET | Multi-step form | form.html | - |
| /save | POST | Save profile | - | /select-template |
| /select-template | GET | Template selection | template-selection.html | - |
| /save-template | POST | Save template choice | - | /view |
| /view | GET | Final resume | view.html | / (if no profile) |

### 7.2 Route Flow

```
GET / (Landing)
    ↓
GET /form (Form)
    ↓
POST /save (Save Data)
    ↓
GET /select-template (Choose Template)
    ↓
POST /save-template (Save Choice)
    ↓
GET /view (Final Resume)
```

### 7.3 Navigation Links

**Landing Page**:
- "Get Started" → /form

**Form Page**:
- "Back to Home" (nav) → /
- "Submit" (form) → POST /save

**Template Selection Page**:
- "Use Template" → POST /save-template → /view

**Final Resume Page**:
- "Home" (nav) → /
- "Edit Details" → /form
- "Change Template" → /select-template
- "Download PDF" → window.print()
- "Share Link" → Copy URL to clipboard

---

## 8. State Management

### 8.1 Server-Side State

**Database** (SQLite):
- Single profile row (id=1)
- Persistent across sessions
- Updated via save_data() and update_data()

**Flask Session** (Not Used):
- No session storage needed
- All state in database

### 8.2 Client-Side State

**Form Wizard State** (JavaScript):
- Current step number (1-5)
- Form data object (in-memory)
- Optional: sessionStorage for persistence

**Template Preview State** (JavaScript):
- Modal visibility (open/closed)
- Selected template for preview

**Navigation State** (CSS):
- Active page highlighting (via current_page variable)

---

## 9. Error Handling

### 9.1 Client-Side Errors

**Form Validation Errors**:
- Display error messages below fields
- Add error class to invalid inputs
- Prevent form submission
- Scroll to first error

**JavaScript Errors**:
- Console logging for debugging
- Graceful degradation (form still works without JS)

### 9.2 Server-Side Errors

**Route Handler Errors**:
- Try-except blocks (optional)
- Flask default error handling
- Redirect to appropriate page on error

**Database Errors**:
- SQLite errors logged to console
- Graceful failure (return None)

**404 Errors**:
- Flask default 404 page
- Or custom 404 template (future enhancement)

---

## 10. Security Considerations

### 10.1 Current Security Measures

**SQL Injection Prevention**:
- Parameterized queries in database.py
- No string concatenation for SQL

**XSS Prevention**:
- Jinja2 auto-escaping enabled
- User input escaped in templates

**Input Validation**:
- Client-side validation (form.js)
- Optional server-side validation

**URL Validation**:
- URLs must start with http:// or https://

### 10.2 Security Limitations (Development Only)

**No Authentication**: Single-user design, no login required

**No CSRF Protection**: No forms from external sites

**No Rate Limiting**: Local development only

**Debug Mode**: Enabled for development

**HTTP Only**: No HTTPS (local development)

---

## 11. Performance Considerations

### 11.1 Frontend Performance

**Page Load**:
- Minimal CSS/JS files
- No external dependencies (CDN)
- Fast local file serving

**Animations**:
- CSS transitions (60fps)
- JavaScript animations optimized
- No blocking operations

**Responsive Design**:
- Mobile-first approach
- Optimized images (if any)
- Efficient media queries

### 11.2 Backend Performance

**Database Queries**:
- Single-row operations (fast)
- No N+1 queries
- Indexed primary key (id)

**Template Rendering**:
- Jinja2 template caching
- Simple templates (fast rendering)

**Static Files**:
- Flask serves static files efficiently
- No build step required

---

## 12. Testing Strategy

### 12.1 Backend Testing

**Unit Tests** (Pytest):
- Test route handlers
- Test database functions
- Test helper functions

**Integration Tests**:
- Test full request/response cycle
- Test database operations
- Test redirects

### 12.2 Frontend Testing

**Manual Testing**:
- Multi-step form flow
- Template selection
- Resume rendering
- Responsive design
- Cross-browser compatibility

**Automated Testing** (Optional):
- Selenium for UI testing
- JavaScript unit tests (Jest)

---

## 13. Deployment Considerations

### 13.1 Current Deployment

**Environment**: Local development only

**Server**: Flask development server (Werkzeug)

**Database**: SQLite file (resume_portfolio.db)

**Port**: 5000 (default)

### 13.2 Future Production Deployment

**Server**: Gunicorn or uWSGI

**Database**: Keep SQLite or migrate to PostgreSQL

**Web Server**: Nginx reverse proxy

**HTTPS**: SSL certificate

**Environment Variables**: Configuration management

---

## 14. Design Summary

### 14.1 Key Design Decisions

1. ✅ **Template Inheritance**: base.html for consistent layout
2. ✅ **Multi-Step Form**: Client-side wizard with JavaScript
3. ✅ **Three Resume Templates**: Separate files with dynamic inclusion
4. ✅ **Minimal Service Layer**: Helper functions instead of classes
5. ✅ **Client-Side Validation**: Primary validation with optional server-side backup
6. ✅ **Flat Routing**: All routes in app.py (beginner-friendly)
7. ✅ **Existing Database Pattern**: Keep database.py functions
8. ✅ **Premium Theme**: White + navy + teal color scheme
9. ✅ **Responsive Design**: Mobile-first approach
10. ✅ **Print-Friendly**: Optimized for PDF download

### 14.2 Design Metrics

- **Total Components**: 17
- **Total Methods**: 43
- **Total Routes**: 6
- **Database Fields**: 29 (27 existing + 2 new)
- **Form Steps**: 5
- **Resume Templates**: 3

### 14.3 Design Quality

**Simplicity**: ✅ Beginner-friendly, minimal complexity

**Maintainability**: ✅ Clear separation of concerns, documented code

**Scalability**: ⚠️ Single-user design, not scalable (by design)

**Performance**: ✅ Fast page loads, smooth animations

**Security**: ⚠️ Development-level security (not production-ready)

**Testability**: ✅ Testable components, clear interfaces

---

## 15. Next Steps

After Application Design approval:

1. **Proceed to Functional Design** (CONSTRUCTION phase)
   - Define detailed business logic for each component
   - Specify validation rules and error handling
   - Design state management algorithms
   - Define data transformation logic

2. **Then Proceed to Code Generation**
   - Create detailed implementation plan (Part 1)
   - Generate all code (Part 2)

3. **Finally Build and Test**
   - Comprehensive testing
   - Validation and verification

---

## Appendix: Design Artifacts

This consolidated document references the following detailed design artifacts:

1. **components.md** - Component definitions and responsibilities (17 components)
2. **component-methods.md** - Method signatures and purposes (43 methods)
3. **services.md** - Service layer decisions and helper functions
4. **component-dependency.md** - Dependency relationships and communication patterns
5. **application-design.md** - This consolidated document

All artifacts are located in: `aidlc-docs/inception/application-design/`
