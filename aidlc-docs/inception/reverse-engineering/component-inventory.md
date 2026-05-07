# Component Inventory

## Application Packages
- **resume-portfolio-builder** - Main application package containing Flask web app, database layer, templates, and static assets

## Infrastructure Packages
- None (local development only, no cloud infrastructure)

## Shared Packages
- None (monolithic single-package application)

## Test Packages
- **tests/** - Pytest test suite for application and database layers

## Detailed Component Breakdown

### Application Components

#### Backend Components
| Component | Type | Language | LOC | Purpose |
|-----------|------|----------|-----|---------|
| app.py | Application | Python | ~140 | Flask routes and HTTP handling |
| database.py | Data Access | Python | ~200 | SQLite database operations |

#### Frontend Components
| Component | Type | Language | LOC | Purpose |
|-----------|------|----------|-----|---------|
| templates/index.html | View | HTML | ~400 | Profile input form |
| templates/view.html | View | HTML | ~10 | Resume/portfolio display (placeholder) |
| static/css/style.css | Stylesheet | CSS | ~800 | Screen styling |
| static/css/print.css | Stylesheet | CSS | ~100 | Print-specific styling |
| static/js/form.js | Client Script | JavaScript | ~180 | Form validation |

#### Configuration Components
| Component | Type | Format | Purpose |
|-----------|------|--------|---------|
| requirements.txt | Dependency | Text | Python package dependencies |
| README.md | Documentation | Markdown | Project documentation |

### Test Components

#### Test Files
| Component | Type | Language | Purpose |
|-----------|------|----------|---------|
| tests/__init__.py | Test Package | Python | Package marker |
| tests/conftest.py | Test Config | Python | Pytest fixtures |
| tests/test_app.py | Unit Tests | Python | Flask route tests |
| tests/test_database.py | Unit Tests | Python | Database operation tests |

### Data Components

#### Database
| Component | Type | Format | Purpose |
|-----------|------|--------|---------|
| resume_portfolio.db | Database | SQLite | User profile storage |

## Component Relationships

```
app.py
  |-- depends on --> database.py
  |-- renders --> templates/index.html
  |-- renders --> templates/view.html
  |-- serves --> static/css/style.css
  |-- serves --> static/css/print.css
  |-- serves --> static/js/form.js

database.py
  |-- connects to --> resume_portfolio.db

templates/index.html
  |-- references --> static/css/style.css
  |-- references --> static/js/form.js

templates/view.html
  |-- references --> static/css/style.css
  |-- references --> static/css/print.css

tests/test_app.py
  |-- tests --> app.py
  |-- uses --> tests/conftest.py

tests/test_database.py
  |-- tests --> database.py
  |-- uses --> tests/conftest.py
```

## Component Size Analysis

### By Type
| Type | Count | Total LOC |
|------|-------|-----------|
| Python Modules | 2 | ~340 |
| HTML Templates | 2 | ~410 |
| CSS Stylesheets | 2 | ~900 |
| JavaScript Files | 1 | ~180 |
| Test Files | 3 | ~300 (estimated) |
| **Total** | **10** | **~2,130** |

### By Layer
| Layer | Components | LOC |
|-------|------------|-----|
| Backend | 2 | ~340 |
| Frontend | 5 | ~1,490 |
| Tests | 3 | ~300 |
| **Total** | **10** | **~2,130** |

## Total Count
- **Total Packages**: 1 (resume-portfolio-builder)
- **Application**: 1
- **Infrastructure**: 0
- **Shared**: 0
- **Test**: 1 (tests/ subdirectory)

## Component Maturity

### Production-Ready Components
- ✅ database.py - Complete, well-documented
- ✅ app.py - Complete, follows best practices
- ✅ templates/index.html - Complete, responsive
- ✅ static/css/style.css - Complete, comprehensive
- ✅ static/js/form.js - Complete, robust validation

### Incomplete Components
- ⚠️ templates/view.html - **Placeholder only** (main redesign target)
- ⚠️ static/css/print.css - Exists but may need updates for new design

### Missing Components (Redesign Scope)
- ❌ templates/landing.html - Landing page (new requirement)
- ❌ templates/template-selection.html - Template chooser (new requirement)
- ❌ Multiple resume templates - Template 1, 2, 3 (new requirement)

## Deployment Artifacts

### Runtime Requirements
- Python 3.x interpreter
- Flask 3.0.3 package
- SQLite3 (bundled with Python)

### Generated Artifacts
- resume_portfolio.db (created at runtime)
- __pycache__/ (Python bytecode cache)
- .pytest_cache/ (test cache)

### No Build Step Required
- Pure Python application
- No compilation needed
- No bundling/minification
- Direct execution: `python app.py`

## External Dependencies

### Python Packages (from requirements.txt)
| Package | Version | Purpose | License |
|---------|---------|---------|---------|
| Flask | 3.0.3 | Web framework | BSD-3-Clause |

### Standard Library Dependencies
| Module | Purpose |
|--------|---------|
| sqlite3 | Database operations |
| os | File path operations |

### Frontend Dependencies
- None (vanilla HTML/CSS/JS, no frameworks)

## Component Ownership

### Backend
- **Owner**: Application layer
- **Responsibility**: Business logic, data access, HTTP routing
- **Files**: app.py, database.py

### Frontend
- **Owner**: Presentation layer
- **Responsibility**: User interface, client-side validation, styling
- **Files**: templates/, static/

### Tests
- **Owner**: Quality assurance
- **Responsibility**: Automated testing, regression prevention
- **Files**: tests/

## Redesign Impact Analysis

### High Impact (Major Changes Required)
- ✅ templates/view.html - Complete rewrite needed
- ✅ static/css/style.css - Significant updates for premium theme
- ✅ **NEW** templates/landing.html - New file
- ✅ **NEW** templates/template-selection.html - New file

### Medium Impact (Moderate Changes)
- ⚠️ templates/index.html - Update styling, keep structure
- ⚠️ static/js/form.js - May need enhancements

### Low Impact (Minor or No Changes)
- ✅ app.py - Add new routes only (landing, template selection)
- ✅ database.py - No changes (data structure compatible)
- ✅ requirements.txt - No new dependencies

### No Impact (Keep As-Is)
- ✅ tests/ - Update tests after implementation
- ✅ resume_portfolio.db - Schema unchanged
