# Dependencies

## Internal Dependencies

The application has a simple internal dependency structure with clear separation of concerns:

```
app.py (Flask Application)
    |
    |-- imports --> database.py (Data Access Layer)
    |
    |-- renders --> templates/index.html (Form View)
    |-- renders --> templates/view.html (Resume View)
    |
    |-- serves --> static/css/style.css (Screen Styles)
    |-- serves --> static/css/print.css (Print Styles)
    |-- serves --> static/js/form.js (Client Validation)

database.py (Data Access Layer)
    |
    |-- connects to --> resume_portfolio.db (SQLite Database)
    |
    |-- uses --> sqlite3 (Python Standard Library)
    |-- uses --> os (Python Standard Library)

templates/index.html (Form View)
    |
    |-- references --> static/css/style.css (via url_for)
    |-- references --> static/js/form.js (via url_for)
    |
    |-- submits to --> POST /save (app.py route)

templates/view.html (Resume View)
    |
    |-- references --> static/css/style.css (via url_for)
    |-- references --> static/css/print.css (via url_for)
    |
    |-- links to --> GET / (app.py route)

static/js/form.js (Client Validation)
    |
    |-- validates --> form#profile-form (in index.html)
    |-- manipulates --> DOM elements (inputs, error spans)

tests/test_app.py (Application Tests)
    |
    |-- imports --> app (from app.py)
    |-- imports --> database (from database.py)
    |-- uses --> tests/conftest.py (fixtures)

tests/test_database.py (Database Tests)
    |
    |-- imports --> database (from database.py)
    |-- uses --> tests/conftest.py (fixtures)
```

## Dependency Details

### app.py depends on database.py
- **Type**: Compile-time (import)
- **Reason**: Needs database functions for CRUD operations
- **Functions Used**:
  - `init_db()` - Initialize database on startup
  - `get_data()` - Retrieve profile for display
  - `save_data()` - Insert new profile
  - `update_data()` - Update existing profile
- **Coupling**: Loose (interface-based, no direct SQL in app.py)

### app.py depends on Flask
- **Type**: Runtime
- **Reason**: Web framework for HTTP handling
- **Features Used**:
  - Route decorators (@app.route)
  - Request object (form data)
  - Response functions (render_template, redirect, url_for)
- **Coupling**: Tight (Flask-specific code)

### database.py depends on sqlite3
- **Type**: Runtime
- **Reason**: Database operations
- **Features Used**:
  - Connection management
  - SQL execution
  - Row factory (dict-like access)
- **Coupling**: Medium (could be abstracted with ORM)

### templates/*.html depend on static assets
- **Type**: Runtime (browser)
- **Reason**: Styling and client-side functionality
- **Mechanism**: url_for() generates URLs
- **Coupling**: Loose (standard HTML/CSS/JS references)

### static/js/form.js depends on index.html
- **Type**: Runtime (browser)
- **Reason**: DOM manipulation for validation
- **Mechanism**: getElementById, querySelector
- **Coupling**: Medium (expects specific element IDs)

## External Dependencies

### Flask (3.0.3)
- **Version**: 3.0.3 (pinned)
- **Purpose**: Web application framework
- **License**: BSD-3-Clause
- **Installation**: `pip install Flask==3.0.3`
- **Transitive Dependencies**:
  - Jinja2 (template engine)
  - Werkzeug (WSGI server)
  - Click (CLI)
  - MarkupSafe (template safety)
  - Blinker (signals)
  - itsdangerous (session security)

### Python Standard Library Dependencies
These are included with Python and require no installation:

#### sqlite3
- **Purpose**: SQLite database operations
- **Usage**: Database connection, SQL execution
- **Version**: Bundled with Python 3.x

#### os
- **Purpose**: File path operations
- **Usage**: Construct database file path
- **Version**: Bundled with Python 3.x

## Dependency Versions

### requirements.txt
```
Flask==3.0.3
```

### Transitive Dependencies (Installed Automatically)
```
Flask==3.0.3
├── Jinja2>=3.1.2
├── Werkzeug>=3.0.0
├── Click>=8.1.3
├── MarkupSafe>=2.1.1
├── Blinker>=1.6.2
└── itsdangerous>=2.1.2
```

## Dependency Graph Visualization

```
Application
    |
    +-- Direct Dependencies
    |   |
    |   +-- Flask 3.0.3 (external, PyPI)
    |   +-- database.py (internal, local)
    |   +-- templates/*.html (internal, local)
    |   +-- static/**/* (internal, local)
    |
    +-- Transitive Dependencies (via Flask)
    |   |
    |   +-- Jinja2 (template engine)
    |   +-- Werkzeug (WSGI server)
    |   +-- Click (CLI)
    |   +-- MarkupSafe (XSS protection)
    |   +-- Blinker (signals)
    |   +-- itsdangerous (session security)
    |
    +-- Standard Library Dependencies
        |
        +-- sqlite3 (database)
        +-- os (file paths)
```

## Dependency Analysis

### Critical Dependencies (Application Won't Run Without)
- ✅ Flask 3.0.3 - Core web framework
- ✅ Python 3.7+ - Runtime environment
- ✅ sqlite3 - Database operations (bundled)

### Optional Dependencies (Development Only)
- ⚠️ Pytest - Testing framework (not in requirements.txt)
- ⚠️ Browser - Frontend testing and usage

### No Dependencies
- ✅ No CSS frameworks (vanilla CSS)
- ✅ No JavaScript frameworks (vanilla JS)
- ✅ No build tools (no compilation)
- ✅ No database server (SQLite is file-based)

## Dependency Security

### Known Vulnerabilities
- ✅ Flask 3.0.3 - No known critical vulnerabilities (as of 2024)
- ✅ All transitive dependencies - Regularly updated

### Security Best Practices
- ✅ Pinned version (Flask==3.0.3) prevents unexpected updates
- ✅ Minimal dependency tree (only 1 direct dependency)
- ✅ No deprecated packages
- ✅ No unmaintained packages

### Dependency Update Strategy
- **Check for updates**: `pip list --outdated`
- **Update Flask**: `pip install --upgrade Flask`
- **Test after updates**: Run test suite
- **Update requirements.txt**: `pip freeze > requirements.txt`

## Dependency Licenses

### Direct Dependencies
| Package | Version | License | Commercial Use |
|---------|---------|---------|----------------|
| Flask | 3.0.3 | BSD-3-Clause | ✅ Yes |

### Transitive Dependencies
| Package | License | Commercial Use |
|---------|---------|----------------|
| Jinja2 | BSD-3-Clause | ✅ Yes |
| Werkzeug | BSD-3-Clause | ✅ Yes |
| Click | BSD-3-Clause | ✅ Yes |
| MarkupSafe | BSD-3-Clause | ✅ Yes |
| Blinker | MIT | ✅ Yes |
| itsdangerous | BSD-3-Clause | ✅ Yes |

**License Summary**: All dependencies use permissive open-source licenses (BSD-3-Clause or MIT) that allow commercial use, modification, and distribution.

## Dependency Installation

### Fresh Installation
```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Expected Output
```
Package        Version
-------------- -------
Flask          3.0.3
Jinja2         3.1.x
Werkzeug       3.0.x
Click          8.1.x
MarkupSafe     2.1.x
Blinker        1.6.x
itsdangerous   2.1.x
pip            xx.x.x
setuptools     xx.x.x
```

## Dependency Conflicts

### No Known Conflicts
- ✅ Flask 3.0.3 is compatible with Python 3.7+
- ✅ All transitive dependencies are compatible
- ✅ No version conflicts in dependency tree

### Potential Issues
- ⚠️ Python 3.6 or earlier: Not supported (Flask 3.0 requires Python 3.7+)
- ⚠️ Conflicting Flask versions: Ensure only one Flask version installed

## Dependency Footprint

### Disk Space
- **Flask + dependencies**: ~5 MB
- **Python standard library**: ~50 MB (already installed)
- **Application code**: ~100 KB
- **Total**: ~5.1 MB (excluding Python runtime)

### Memory Usage
- **Flask application**: ~30-50 MB RAM
- **SQLite database**: ~1-5 MB RAM (depending on data)
- **Total**: ~35-55 MB RAM

### Network Usage
- **Installation**: ~5 MB download (Flask + dependencies)
- **Runtime**: 0 MB (no external API calls)

## Redesign Impact on Dependencies

### No New Dependencies Required
- ✅ Frontend redesign: Pure HTML/CSS/JS (no frameworks)
- ✅ Landing page: Jinja2 templates (already available)
- ✅ Template selection: Flask routing (already available)
- ✅ Premium UI: CSS only (no libraries)

### Optional Dependencies (Future Enhancements)
- ⚠️ **PDF Generation**: WeasyPrint or ReportLab (if PDF download needed)
- ⚠️ **AI Integration**: OpenAI Python SDK (if AI features added)
- ⚠️ **Image Optimization**: Pillow (if image uploads added)

### Dependencies to Avoid (Keep Simple)
- ❌ React/Vue/Angular - Adds build complexity
- ❌ Bootstrap/Tailwind - Vanilla CSS sufficient
- ❌ jQuery - Vanilla JS sufficient
- ❌ PostgreSQL/MySQL - SQLite sufficient

## Dependency Management Best Practices

### Version Pinning
- ✅ **Current**: Flask==3.0.3 (exact version)
- ✅ **Benefit**: Reproducible builds, no surprises
- ⚠️ **Trade-off**: Manual updates required

### Virtual Environments
- ✅ **Recommended**: Use venv or virtualenv
- ✅ **Benefit**: Isolated dependencies per project
- ✅ **Command**: `python -m venv venv`

### Dependency Auditing
```bash
# Check for security vulnerabilities
pip install safety
safety check

# Check for outdated packages
pip list --outdated

# Generate dependency tree
pip install pipdeptree
pipdeptree
```

## Conclusion

The application has a **minimal and clean dependency structure**:
- **1 external dependency** (Flask)
- **6 transitive dependencies** (all from Flask)
- **2 standard library dependencies** (sqlite3, os)
- **No frontend dependencies** (vanilla HTML/CSS/JS)

This simplicity makes the application:
- ✅ Easy to install
- ✅ Easy to maintain
- ✅ Fast to start
- ✅ Secure (small attack surface)
- ✅ Portable (few dependencies)
