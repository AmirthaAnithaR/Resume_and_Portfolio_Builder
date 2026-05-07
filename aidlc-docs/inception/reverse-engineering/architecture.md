# System Architecture

## System Overview

The Resume + Portfolio Builder is a single-user web application built with Flask (Python) that allows users to create and manage their professional resume and portfolio. The system follows a traditional three-tier architecture with a presentation layer (HTML/CSS/JS), application layer (Flask), and data layer (SQLite).

## Architecture Diagram

```
+---------------------------------------------------------------+
|                         User Browser                          |
|  +----------------------------------------------------------+ |
|  |  HTML Templates (Jinja2)                                 | |
|  |  - index.html (Form)                                     | |
|  |  - view.html (Resume/Portfolio)                          | |
|  +----------------------------------------------------------+ |
|  +----------------------------------------------------------+ |
|  |  Static Assets                                           | |
|  |  - style.css (Screen styling)                            | |
|  |  - print.css (Print styling)                             | |
|  |  - form.js (Client-side validation)                      | |
|  +----------------------------------------------------------+ |
+---------------------------------------------------------------+
                              |
                              | HTTP (GET/POST)
                              v
+---------------------------------------------------------------+
|                      Flask Application                        |
|  +----------------------------------------------------------+ |
|  |  app.py (Routes & Controllers)                           | |
|  |  - GET  /       -> Show form                             | |
|  |  - POST /save   -> Save profile                          | |
|  |  - GET  /view   -> Show resume                           | |
|  +----------------------------------------------------------+ |
|                              |                                |
|                              | Function calls                 |
|                              v                                |
|  +----------------------------------------------------------+ |
|  |  database.py (Data Access Layer)                         | |
|  |  - init_db()    -> Create table                          | |
|  |  - save_data()  -> Insert profile                        | |
|  |  - get_data()   -> Retrieve profile                      | |
|  |  - update_data() -> Update profile                       | |
|  +----------------------------------------------------------+ |
+---------------------------------------------------------------+
                              |
                              | SQL queries
                              v
+---------------------------------------------------------------+
|                    SQLite Database                            |
|  +----------------------------------------------------------+ |
|  |  resume_portfolio.db                                     | |
|  |  - profile table (single row, id=1)                      | |
|  +----------------------------------------------------------+ |
+---------------------------------------------------------------+
```

## Component Descriptions

### User Browser (Presentation Layer)
- **Purpose**: Render user interface and handle client-side interactions
- **Responsibilities**: 
  - Display forms and content
  - Validate user input before submission
  - Apply responsive styling
  - Handle print formatting
- **Dependencies**: Flask application (HTTP)
- **Type**: Client-side web interface

### Flask Application (Application Layer)
- **Purpose**: Handle HTTP requests and business logic
- **Responsibilities**:
  - Route management (/, /save, /view)
  - Request processing
  - Template rendering
  - Business rule enforcement
  - Session management (POST-Redirect-GET pattern)
- **Dependencies**: Database layer, Jinja2 templates
- **Type**: Python web application

### Database Layer (Data Access Layer)
- **Purpose**: Abstract database operations
- **Responsibilities**:
  - Database initialization
  - CRUD operations for profile data
  - Data validation and defaults
  - Connection management
- **Dependencies**: SQLite database
- **Type**: Python module

### SQLite Database (Data Layer)
- **Purpose**: Persist user profile data
- **Responsibilities**:
  - Store single user profile
  - Maintain data integrity
  - Provide ACID transactions
- **Dependencies**: None (file-based)
- **Type**: Embedded database

## Data Flow

### User Story: Create/Update Profile

```
User fills form -> Client validation -> POST /save
                                            |
                                            v
                                    Extract form data
                                            |
                                            v
                                    Check if profile exists
                                            |
                        +-------------------+-------------------+
                        |                                       |
                        v                                       v
                  Profile exists                         No profile
                        |                                       |
                        v                                       v
                  update_data()                           save_data()
                        |                                       |
                        +-------------------+-------------------+
                                            |
                                            v
                                    UPDATE/INSERT SQL
                                            |
                                            v
                                    Redirect to /view
                                            |
                                            v
                                    GET /view -> Render resume
```

### User Story: View Resume

```
User clicks "View Resume" -> GET /view
                                |
                                v
                          get_data()
                                |
                                v
                          Profile exists?
                                |
                +---------------+---------------+
                |                               |
                v                               v
              Yes                              No
                |                               |
                v                               v
        Render view.html                Redirect to /
        with profile data               (form page)
```

## Integration Points

### External APIs
- None (standalone application)

### Databases
- **SQLite** (`resume_portfolio.db`): Single-user profile storage
  - Location: Same directory as app.py
  - Schema: Single `profile` table with 27 columns
  - Access: Python sqlite3 module

### Third-party Services
- None (no external dependencies beyond Flask)

## Infrastructure Components

### Deployment Model
- **Type**: Local development server
- **Runtime**: Python 3.x with Flask
- **Server**: Flask built-in development server (Werkzeug)
- **Port**: 5000 (default)
- **Environment**: Single-machine deployment

### Networking
- **Protocol**: HTTP
- **Host**: localhost (127.0.0.1)
- **Port**: 5000
- **Security**: None (development only, not production-ready)

### File Structure
```
resume-portfolio-builder/
|-- app.py                    (Flask application entry point)
|-- database.py               (Database operations)
|-- requirements.txt          (Python dependencies)
|-- resume_portfolio.db       (SQLite database file)
|-- templates/
|   |-- index.html            (Form page)
|   |-- view.html             (Resume/portfolio page)
|-- static/
|   |-- css/
|   |   |-- style.css         (Screen styles)
|   |   |-- print.css         (Print styles)
|   |-- js/
|       |-- form.js           (Client-side validation)
|-- tests/                    (Test files)
```

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Backend | Python | 3.x | Application runtime |
| Web Framework | Flask | 3.0.3 | HTTP routing and templating |
| Database | SQLite | 3.x | Data persistence |
| Template Engine | Jinja2 | (bundled with Flask) | HTML generation |
| Frontend | HTML5 | - | Structure |
| Styling | CSS3 | - | Presentation |
| Client Script | JavaScript | ES6+ | Form validation |

## Design Patterns

### Pattern: Model-View-Controller (MVC)
- **Model**: database.py (data access)
- **View**: templates/*.html (presentation)
- **Controller**: app.py (request handling)

### Pattern: POST-Redirect-GET (PRG)
- **Location**: /save route
- **Purpose**: Prevent duplicate form submissions on page refresh
- **Implementation**: POST /save -> 302 redirect -> GET /view

### Pattern: Repository Pattern
- **Location**: database.py
- **Purpose**: Abstract database operations
- **Implementation**: CRUD functions (save_data, get_data, update_data)

### Pattern: Single Responsibility Principle
- **app.py**: HTTP routing only
- **database.py**: Data access only
- **form.js**: Client validation only
