# Technology Stack

## Programming Languages

### Python (3.x)
- **Version**: 3.10+ (recommended)
- **Usage**: Backend application logic, database operations, HTTP routing
- **Files**: app.py, database.py, tests/
- **Justification**: 
  - Simple, readable syntax
  - Excellent web framework support (Flask)
  - Built-in SQLite support
  - Rapid development

### HTML5
- **Version**: HTML5 (latest standard)
- **Usage**: Page structure, semantic markup
- **Files**: templates/*.html
- **Features Used**:
  - Semantic elements (nav, footer, section)
  - Form validation attributes (required, type="email", type="url")
  - Data attributes (data-testid)

### CSS3
- **Version**: CSS3 (latest standard)
- **Usage**: Visual styling, responsive design, animations
- **Files**: static/css/*.css
- **Features Used**:
  - CSS Custom Properties (variables)
  - Flexbox and Grid layouts
  - Media queries (responsive design)
  - Animations and transitions
  - Pseudo-classes and pseudo-elements

### JavaScript (ES6+)
- **Version**: ECMAScript 2015+ (ES6+)
- **Usage**: Client-side form validation
- **Files**: static/js/form.js
- **Features Used**:
  - Arrow functions
  - Template literals
  - const/let declarations
  - DOM manipulation
  - Event listeners

## Frameworks

### Flask (3.0.3)
- **Version**: 3.0.3
- **Purpose**: Web application framework
- **Usage**:
  - HTTP routing (@app.route decorators)
  - Request/response handling
  - Template rendering (Jinja2)
  - Development server
- **Key Features Used**:
  - Route decorators
  - Request object (form data)
  - Redirect and url_for
  - render_template
- **License**: BSD-3-Clause

### Jinja2 (Bundled with Flask)
- **Version**: Bundled with Flask 3.0.3
- **Purpose**: Template engine
- **Usage**:
  - Dynamic HTML generation
  - Template inheritance
  - Variable interpolation
  - Conditional rendering
- **Key Features Used**:
  - {{ variable }} syntax
  - {% if %} conditionals
  - {% for %} loops
  - url_for() function
  - Filters (e.g., |default)

## Infrastructure

### SQLite (3.x)
- **Version**: 3.x (bundled with Python)
- **Purpose**: Embedded relational database
- **Usage**: User profile data persistence
- **Database File**: resume_portfolio.db
- **Features Used**:
  - Single table (profile)
  - INTEGER PRIMARY KEY
  - TEXT columns
  - NOT NULL constraints
  - Parameterized queries (SQL injection prevention)
- **Justification**:
  - Zero configuration
  - File-based (no server needed)
  - Perfect for single-user applications
  - ACID compliant

### Flask Development Server (Werkzeug)
- **Version**: Bundled with Flask
- **Purpose**: Local development HTTP server
- **Usage**: Serve application during development
- **Features**:
  - Auto-reload on code changes
  - Debug mode
  - Port 5000 (default)
- **Note**: Not for production use

## Build Tools

### pip (Python Package Manager)
- **Version**: Latest (bundled with Python)
- **Purpose**: Dependency management
- **Usage**: Install Flask from requirements.txt
- **Commands**:
  - `pip install -r requirements.txt` - Install dependencies
  - `pip freeze` - List installed packages

### No Build Step Required
- **Reason**: Pure Python application
- **No Compilation**: Interpreted language
- **No Bundling**: Direct file serving
- **No Transpilation**: Modern browser support

## Testing Tools

### Pytest
- **Version**: Latest (not in requirements.txt, dev dependency)
- **Purpose**: Unit and integration testing
- **Usage**: Test Flask routes and database operations
- **Files**: tests/test_*.py
- **Features Used**:
  - Test fixtures (conftest.py)
  - Test discovery
  - Assertions
  - Test client (Flask)

## Development Tools (Not in Production)

### Python Standard Library
- **sqlite3**: Database operations
- **os**: File path operations
- **typing**: Type hints (documentation)

### Browser DevTools
- **Purpose**: Frontend debugging
- **Usage**: Inspect HTML, debug CSS, test JavaScript

## Technology Stack Summary Table

| Category | Technology | Version | Purpose | Required |
|----------|-----------|---------|---------|----------|
| **Backend** |
| Language | Python | 3.10+ | Application logic | ✅ Yes |
| Framework | Flask | 3.0.3 | Web framework | ✅ Yes |
| Template Engine | Jinja2 | (bundled) | HTML generation | ✅ Yes |
| Database | SQLite | 3.x | Data persistence | ✅ Yes |
| **Frontend** |
| Markup | HTML5 | Latest | Page structure | ✅ Yes |
| Styling | CSS3 | Latest | Visual design | ✅ Yes |
| Scripting | JavaScript | ES6+ | Client validation | ✅ Yes |
| **Development** |
| Package Manager | pip | Latest | Dependencies | ✅ Yes |
| Testing | Pytest | Latest | Automated tests | ⚠️ Dev only |
| Server | Werkzeug | (bundled) | Dev server | ⚠️ Dev only |

## Dependency Graph

```
Application Runtime
    |
    +-- Python 3.x (interpreter)
        |
        +-- Flask 3.0.3
            |
            +-- Jinja2 (template engine)
            +-- Werkzeug (WSGI server)
            +-- Click (CLI)
            +-- MarkupSafe (template safety)
        |
        +-- sqlite3 (standard library)
        +-- os (standard library)

Development/Testing
    |
    +-- Pytest (test runner)
    +-- Browser (Chrome/Firefox/Safari)
```

## Version Compatibility

### Python Version Requirements
- **Minimum**: Python 3.7 (Flask 3.0 requirement)
- **Recommended**: Python 3.10+
- **Tested**: Python 3.10

### Browser Compatibility
- **Modern Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Features Required**:
  - CSS Grid and Flexbox
  - CSS Custom Properties
  - ES6 JavaScript
  - HTML5 form validation

### Operating System Compatibility
- **Windows**: ✅ Supported
- **macOS**: ✅ Supported
- **Linux**: ✅ Supported
- **Note**: Python and SQLite are cross-platform

## Security Considerations

### Current Security Measures
- ✅ Parameterized SQL queries (SQL injection prevention)
- ✅ Client-side input validation
- ✅ HTTPS URL validation
- ✅ Email format validation

### Security Limitations (Development Only)
- ❌ No authentication/authorization
- ❌ No HTTPS (HTTP only)
- ❌ No CSRF protection
- ❌ No rate limiting
- ❌ Debug mode enabled
- ❌ Single-user design (no multi-tenancy)

### Production Readiness
- **Status**: ⚠️ Not production-ready
- **Reason**: Development server, no security hardening
- **Recommendation**: For learning/personal use only

## Technology Choices Rationale

### Why Flask?
- ✅ Lightweight and simple
- ✅ Perfect for small applications
- ✅ Excellent documentation
- ✅ Built-in template engine
- ✅ Easy to learn

### Why SQLite?
- ✅ Zero configuration
- ✅ File-based (portable)
- ✅ Perfect for single-user apps
- ✅ No separate database server
- ✅ Included with Python

### Why Vanilla JavaScript?
- ✅ No build step required
- ✅ Fast page loads
- ✅ Simple validation logic
- ✅ No framework overhead
- ✅ Easy to understand

### Why No Frontend Framework?
- ✅ Simple requirements
- ✅ Server-side rendering sufficient
- ✅ Faster initial development
- ✅ No build complexity
- ✅ Beginner-friendly

## Future Technology Considerations (Redesign)

### Potential Additions
- ⚠️ **PDF Generation**: Library like WeasyPrint or ReportLab
- ⚠️ **AI Integration**: OpenAI API for content suggestions
- ⚠️ **Enhanced Styling**: CSS framework (optional)

### Technologies to Avoid (Keep Simple)
- ❌ React/Vue/Angular (overkill for this use case)
- ❌ TypeScript (adds build complexity)
- ❌ Webpack/Vite (no bundling needed)
- ❌ PostgreSQL/MySQL (SQLite sufficient)
- ❌ Docker (local development only)

## Installation Instructions

### Prerequisites
```bash
# Check Python version (3.10+ recommended)
python --version

# Check pip is installed
pip --version
```

### Setup
```bash
# Navigate to project directory
cd resume-portfolio-builder

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Open browser
# Navigate to: http://localhost:5000
```

### No Additional Setup Required
- ✅ No database server installation
- ✅ No environment variables
- ✅ No configuration files
- ✅ No build step
- ✅ Database created automatically on first run
