# Business Overview

## Business Context

The Resume + Portfolio Builder is a web-based application that helps users create professional resumes and portfolio websites. The system provides a simple, single-user interface for entering personal information, education, skills, projects, and certifications, then generates a formatted resume and portfolio webpage.

## Business Description

**Core Business Value**: Enable users to quickly create professional-looking resumes and portfolio websites without design or coding skills.

**Target Users**: Job seekers, students, developers, and professionals who need to showcase their qualifications and work.

**Key Differentiator**: Simple, single-user application with no authentication complexity - perfect for personal use or learning purposes.

## Business Transactions

### BT-01: Create/Update Profile
- **Description**: User enters or updates their personal information, education, skills, projects, and certifications
- **Input**: Form data (name, email, phone, URLs, education, skills, 3 projects, 3 certifications)
- **Output**: Profile saved to database, user redirected to view page
- **Business Rules**:
  - Required fields: name, email, phone
  - Optional fields: GitHub URL, LinkedIn URL, project URLs
  - Single-user system: only one profile exists (id=1)
  - Update overwrites all fields

### BT-02: View Resume & Portfolio
- **Description**: User views their generated resume and portfolio webpage
- **Input**: None (retrieves stored profile)
- **Output**: Formatted HTML page with resume and portfolio sections
- **Business Rules**:
  - If no profile exists, redirect to form
  - Display all entered information in professional layout
  - Show only non-empty optional fields

### BT-03: Edit Profile
- **Description**: User returns to form to modify their information
- **Input**: None (retrieves stored profile)
- **Output**: Form pre-populated with existing data
- **Business Rules**:
  - Form shows current values for editing
  - Submission updates existing record

## Business Dictionary

| Term | Definition |
|------|------------|
| **Profile** | Complete set of user information including personal details, education, skills, projects, and certifications |
| **Resume** | Formatted document showing user's qualifications and experience |
| **Portfolio** | Web page showcasing user's projects and skills |
| **Project** | Work sample with title, description, and optional URL |
| **Certification** | Professional credential with name, issuing organization, and year |
| **Single-User** | Application designed for one user only (no multi-user support or authentication) |

## Component Level Business Descriptions

### Flask Application (app.py)
- **Purpose**: Serve web pages and handle user interactions
- **Responsibilities**: 
  - Display input form
  - Process form submissions
  - Render resume/portfolio view
  - Route management

### Database Layer (database.py)
- **Purpose**: Persist user profile data
- **Responsibilities**:
  - Initialize SQLite database
  - Save new profiles
  - Retrieve existing profile
  - Update profile data

### Frontend Templates (templates/)
- **Purpose**: Present user interface
- **Responsibilities**:
  - Input form (index.html)
  - Resume/portfolio view (view.html - currently placeholder)
  - Responsive layout
  - Form validation feedback

### Static Assets (static/)
- **Purpose**: Provide styling and client-side functionality
- **Responsibilities**:
  - CSS styling (style.css, print.css)
  - Form validation (form.js)
  - Responsive design
  - Print-friendly formatting
