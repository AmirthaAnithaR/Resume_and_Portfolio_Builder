# Code Structure

## Build System
- **Type**: pip (Python package manager)
- **Configuration**: requirements.txt
- **Dependencies**: Flask==3.0.3 (only external dependency)
- **Installation**: `pip install -r requirements.txt`
- **Execution**: `python app.py`

## Project Structure

```
resume-portfolio-builder/
|-- app.py                    # Flask application entry point
|-- database.py               # Database operations module
|-- requirements.txt          # Python dependencies
|-- resume_portfolio.db       # SQLite database (generated at runtime)
|-- README.md                 # Project documentation
|-- templates/                # Jinja2 HTML templates
|   |-- index.html            # Form input page
|   |-- view.html             # Resume/portfolio view (placeholder)
|-- static/                   # Static assets
|   |-- css/
|   |   |-- style.css         # Screen styles (24KB)
|   |   |-- print.css         # Print-specific styles
|   |-- js/
|       |-- form.js           # Client-side form validation
|-- tests/                    # Test suite
    |-- __init__.py
    |-- conftest.py           # Pytest configuration
    |-- test_app.py           # Application tests
    |-- test_database.py      # Database tests
```

## Existing Files Inventory

### Backend Files (Python)

#### `app.py` - Flask Application Entry Point
- **Purpose**: HTTP routing and request handling
- **Key Functions**:
  - `index()` - GET / - Render form page
  - `save()` - POST /save - Process form submission
  - `view()` - GET /view - Render resume/portfolio page
- **Business Rules Enforced**:
  - BR-01: Required field validation (name, email, phone)
  - BR-04: INSERT vs UPDATE decision
  - BR-09: POST-Redirect-GET pattern
  - BR-10: Redirect to form if no profile exists
- **Lines of Code**: ~140
- **Dependencies**: Flask, database module

#### `database.py` - Data Access Layer
- **Purpose**: SQLite database operations
- **Key Functions**:
  - `init_db()` - Create profile table if not exists
  - `save_data(data)` - Insert new profile (id=1)
  - `get_data()` - Retrieve profile or None
  - `update_data(data)` - Update existing profile
  - `_fill_defaults(data)` - Ensure all keys present
- **Database Schema**: 27 columns (personal info, education, skills, 3 projects, 3 certifications)
- **Lines of Code**: ~200
- **Dependencies**: sqlite3 (standard library)

### Frontend Files (HTML/CSS/JS)

#### `templates/index.html` - Form Input Page
- **Purpose**: User input form for profile data
- **Sections**:
  - Personal Information (name, email, phone, GitHub, LinkedIn)
  - Education (free-text textarea)
  - Skills (comma-separated textarea)
  - Projects (3 fixed entries: title, description, URL)
  - Certifications (3 fixed entries: name, org, year)
- **Features**:
  - Pre-population on edit (Jinja2 conditionals)
  - Required field indicators (red asterisks)
  - Responsive form layout
  - Client-side validation hooks
- **Lines of Code**: ~400
- **Dependencies**: style.css, form.js

#### `templates/view.html` - Resume/Portfolio View
- **Purpose**: Display formatted resume and portfolio
- **Current State**: Placeholder (empty file)
- **Expected Sections** (based on requirements):
  - Hero section with name and contact
  - About Me
  - Education
  - Skills (badge display)
  - Projects (card grid)
  - Certifications (timeline)
  - Contact section
- **Dependencies**: style.css, print.css

#### `static/css/style.css` - Screen Styles
- **Purpose**: Visual styling for all pages
- **Features**:
  - CSS custom properties (color palette)
  - Responsive design (mobile-first)
  - Sticky navigation
  - Hamburger menu (pure CSS)
  - Card-based layouts
  - Animations (fade-in effects)
  - Premium color scheme (navy + teal + white)
- **Lines of Code**: ~800
- **Color Palette**:
  - Primary: #1a3c5e (navy blue)
  - Accent: #2a9d8f (teal)
  - Background: #ffffff (white)
  - Text: #1e293b (dark slate)

#### `static/css/print.css` - Print Styles
- **Purpose**: Optimize layout for PDF/print output
- **Features**:
  - Hide navigation and interactive elements
  - Adjust spacing for paper
  - Ensure black text on white background
  - Page break control

#### `static/js/form.js` - Client-Side Validation
- **Purpose**: Validate form before submission
- **Validation Rules**:
  - Required: name, email, phone (non-empty)
  - Email format: regex validation
  - URL format: must start with http:// or https:// (if non-empty)
- **Features**:
  - Real-time error display
  - Scroll to first error
  - Prevent submission if invalid
- **Lines of Code**: ~180
- **Dependencies**: None (vanilla JavaScript)

### Configuration Files

#### `requirements.txt` - Python Dependencies
- **Purpose**: Declare Python package dependencies
- **Contents**: Flask==3.0.3
- **Usage**: `pip install -r requirements.txt`

### Test Files

#### `tests/test_app.py` - Application Tests
- **Purpose**: Test Flask routes and business logic
- **Test Coverage**:
  - Route accessibility
  - Form submission
  - Redirect behavior
  - Template rendering

#### `tests/test_database.py` - Database Tests
- **Purpose**: Test database operations
- **Test Coverage**:
  - Table creation
  - Insert operations
  - Retrieve operations
  - Update operations

#### `tests/conftest.py` - Pytest Configuration
- **Purpose**: Shared test fixtures
- **Fixtures**:
  - Test database setup
  - Flask test client

## Design Patterns

### Pattern: Separation of Concerns
- **app.py**: HTTP layer only (no SQL)
- **database.py**: Data layer only (no HTTP)
- **templates/**: Presentation only (no logic)
- **static/js/**: Client validation only (no server logic)

### Pattern: Template Method
- **Location**: database.py
- **Implementation**: `_fill_defaults()` ensures consistent data structure before save/update

### Pattern: Guard Clause
- **Location**: app.py `view()` route
- **Implementation**: Early return (redirect) if no profile exists

### Pattern: DRY (Don't Repeat Yourself)
- **CSS Variables**: Centralized color palette in :root
- **Database Helper**: `_fill_defaults()` used by both save and update
- **Validation**: Single `validateForm()` function for all fields

## Code Quality Indicators

### Strengths
- Clear separation of concerns
- Comprehensive inline documentation
- Consistent naming conventions
- Defensive programming (null checks, defaults)
- Responsive design
- Accessibility considerations (semantic HTML, labels)

### Areas for Improvement (Redesign Scope)
- `view.html` is currently a placeholder
- No template selection mechanism
- No landing page
- No multi-step flow
- Basic styling (not premium/modern)
- No smooth transitions
- No AI assistance integration

## Critical Dependencies

### Flask (3.0.3)
- **Purpose**: Web framework for routing and templating
- **Usage**: All HTTP handling, Jinja2 rendering
- **Installation**: `pip install Flask==3.0.3`

### SQLite3 (Standard Library)
- **Purpose**: Embedded database
- **Usage**: Profile data persistence
- **Installation**: Included with Python

### Jinja2 (Bundled with Flask)
- **Purpose**: Template engine
- **Usage**: Dynamic HTML generation
- **Installation**: Automatic with Flask

## File Modification Scope (Redesign)

### Files to Update (Frontend Only)
- ✅ `templates/index.html` - Redesign form page
- ✅ `templates/view.html` - Implement resume/portfolio view
- ✅ `static/css/style.css` - Update to premium theme
- ✅ `static/js/form.js` - Enhance validation if needed
- ✅ **NEW**: `templates/landing.html` - Create landing page
- ✅ **NEW**: `templates/template-selection.html` - Create template chooser

### Files to Keep Compatible (Backend)
- ❌ `app.py` - Keep routes compatible (may add new routes)
- ❌ `database.py` - No changes (data structure stays same)
- ❌ `requirements.txt` - No new dependencies

## Lines of Code Summary

| File | Language | LOC | Purpose |
|------|----------|-----|---------|
| app.py | Python | ~140 | Flask routes |
| database.py | Python | ~200 | Data access |
| index.html | HTML | ~400 | Form page |
| view.html | HTML | ~10 | Resume view (placeholder) |
| style.css | CSS | ~800 | Screen styles |
| print.css | CSS | ~100 | Print styles |
| form.js | JavaScript | ~180 | Validation |
| **Total** | - | **~1,830** | - |
