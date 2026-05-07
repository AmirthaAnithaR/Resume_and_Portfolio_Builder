# Components

## Overview
This document defines all components in the AI CV Builder application, their responsibilities, and interfaces.

---

## Frontend Components (Templates)

### 1. Base Template Component
**File**: `templates/base.html`

**Purpose**: Provide common layout structure for all pages

**Responsibilities**:
- Define HTML document structure (head, body)
- Include common CSS and JavaScript files
- Provide navigation bar block
- Provide content block for page-specific content
- Provide footer block
- Define responsive meta tags

**Interface**:
- Blocks: `{% block title %}`, `{% block content %}`, `{% block scripts %}`
- Variables: `current_page` (for active nav highlighting)

---

### 2. Landing Page Component
**File**: `templates/landing.html`

**Purpose**: Welcome users and introduce the AI CV Builder

**Responsibilities**:
- Display hero section with heading, subheading, description, CTA button
- Display features section explaining benefits
- Display testimonials or sample resume examples
- Provide "Get Started" button linking to form page
- Implement responsive design with premium theme

**Interface**:
- Extends: `base.html`
- No input variables required
- CTA button links to `/form` route

---

### 3. Multi-Step Form Component
**File**: `templates/form.html`

**Purpose**: Collect user information through a multi-step wizard

**Responsibilities**:
- Display form steps (5 steps: Personal Info, Education, Skills, Projects, Certifications)
- Show progress indicator (Step X of 5)
- Provide Next/Back/Submit buttons
- Validate current step before allowing Next
- Persist form data across steps (client-side)
- Pre-populate fields if profile exists (edit mode)

**Interface**:
- Extends: `base.html`
- Input variables: `profile` (dict or None)
- Form submits to `/save` route (POST)
- JavaScript manages step visibility and state

**Sub-Components** (Jinja2 macros):
- `form_step_1`: Personal Information fields
- `form_step_2`: Education fields
- `form_step_3`: Skills fields
- `form_step_4`: Projects fields (3 projects)
- `form_step_5`: Certifications fields (3 certifications)

---

### 4. Template Selection Component
**File**: `templates/template-selection.html`

**Purpose**: Allow users to choose from 3 resume templates

**Responsibilities**:
- Display 3 template cards side-by-side (responsive grid)
- Show thumbnail preview for each template
- Provide "Use Template" button for each
- Show modal with live preview when card is clicked
- Handle template selection and navigation to final resume

**Interface**:
- Extends: `base.html`
- Input variables: `profile` (dict with user data)
- Template cards link to `/select-template?template=X` route
- Modal preview renders template with user data

---

### 5. Resume Template 1 - Corporate Professional
**File**: `templates/resume-template1.html`

**Purpose**: Render resume in Corporate Professional style (ATS-friendly)

**Responsibilities**:
- Display user data in conservative professional layout
- Use navy/grey accents, subtle borders, professional fonts
- Single-column layout with clear sections
- Optimize for ATS compatibility (simple structure)
- Support print-friendly styling

**Interface**:
- Can be included in `view.html` or rendered standalone
- Input variables: `profile` (dict with all user data)
- Sections: Header, Education, Skills, Projects, Certifications

---

### 6. Resume Template 2 - Modern Developer
**File**: `templates/resume-template2.html`

**Purpose**: Render resume in Modern Developer style

**Responsibilities**:
- Display user data with skills badges and project cards
- Use modern layout with visual hierarchy
- Show skills as colored pills/badges
- Show projects as cards with tech stack tags
- Support responsive and print-friendly styling

**Interface**:
- Can be included in `view.html` or rendered standalone
- Input variables: `profile` (dict with all user data)
- Sections: Header, Skills (badges), Projects (cards), Education, Certifications

---

### 7. Resume Template 3 - Creative Portfolio
**File**: `templates/resume-template3.html`

**Purpose**: Render resume in Creative Portfolio style

**Responsibilities**:
- Display user data with balanced creativity
- Use modern design with unique elements but still professional
- Asymmetric or grid-based layout with visual interest
- Creative section dividers and icons
- Support responsive and print-friendly styling

**Interface**:
- Can be included in `view.html` or rendered standalone
- Input variables: `profile` (dict with all user data)
- Sections: Header, About, Skills (visual), Projects (portfolio cards), Education, Certifications

---

### 8. Final Resume + Portfolio Component
**File**: `templates/view.html`

**Purpose**: Display generated resume and portfolio with action buttons

**Responsibilities**:
- Render selected resume template at top
- Display portfolio section below (expanded projects view)
- Show action buttons (Download PDF, Edit Details, Change Template, Share Link)
- Handle template selection (include correct template file)
- Support responsive design

**Interface**:
- Extends: `base.html`
- Input variables: `profile` (dict with user data), `template_choice` (template1/template2/template3)
- Includes selected template: `{% include 'resume-template' + profile.template_choice + '.html' %}`
- Action buttons link to appropriate routes

---

### 9. Navigation Component
**File**: Included in `base.html`

**Purpose**: Provide consistent navigation across all pages

**Responsibilities**:
- Display sticky navigation bar with logo and links
- Show "My CV Creator" branding
- Provide links: Home, View Resume, Edit (contextual)
- Highlight active page
- Implement hamburger menu for mobile
- Use navy background with white text

**Interface**:
- Variables: `current_page` (for active link highlighting)
- Links: `/` (Home/Landing), `/form` (Edit), `/view` (View Resume)

---

### 10. Footer Component
**File**: Included in `base.html`

**Purpose**: Provide footer information

**Responsibilities**:
- Display copyright or branding text
- Provide links to additional pages (if any)
- Use consistent styling with theme

**Interface**:
- No input variables required
- Simple text or links

---

## Backend Components (Python)

### 11. Route Handler Component
**File**: `app.py`

**Purpose**: Handle HTTP requests and route to appropriate handlers

**Responsibilities**:
- Define routes for all pages (GET/POST)
- Render templates with appropriate data
- Handle form submissions
- Manage redirects and error handling
- Initialize database on startup

**Routes**:
- `GET /` - Landing page or form page (based on design decision)
- `GET /landing` - Landing page (if separate from /)
- `GET /form` - Multi-step form page
- `POST /save` - Save form data
- `GET /select-template` - Template selection page
- `POST /save-template` - Save template choice
- `GET /view` - Final resume + portfolio page

**Interface**:
- Uses Flask decorators: `@app.route()`
- Calls database functions: `get_data()`, `save_data()`, `update_data()`
- Renders templates: `render_template()`

---

### 12. Database Component
**File**: `database.py`

**Purpose**: Handle all database operations

**Responsibilities**:
- Initialize database and create tables
- Save new profile data (INSERT)
- Retrieve existing profile data (SELECT)
- Update existing profile data (UPDATE)
- Handle optional new fields (template_choice, summary)

**Functions**:
- `init_db()` - Create profile table
- `save_data(data)` - Insert new profile
- `get_data()` - Retrieve profile (returns dict or None)
- `update_data(data)` - Update existing profile
- `_fill_defaults(data)` - Ensure all keys present

**Interface**:
- Called by route handlers in app.py
- Returns dict with profile data or None
- Handles 27 existing fields + 2 new optional fields

---

## Frontend JavaScript Components

### 13. Form Wizard Component
**File**: `static/js/form-wizard.js`

**Purpose**: Manage multi-step form navigation and state

**Responsibilities**:
- Show/hide form steps based on current step
- Update progress indicator
- Handle Next/Back/Submit button clicks
- Validate current step before allowing Next
- Persist form data across steps (in-memory object)
- Scroll to top when changing steps

**Functions**:
- `showStep(stepNumber)` - Display specific step
- `nextStep()` - Validate and move to next step
- `prevStep()` - Move to previous step
- `validateStep(stepNumber)` - Validate current step fields
- `saveFormState()` - Save form data to memory
- `restoreFormState()` - Restore form data from memory

**Interface**:
- Attached to form#profile-form
- Listens for button clicks (Next, Back, Submit)
- Updates DOM (show/hide steps, update progress)

---

### 14. Form Validation Component
**File**: `static/js/form.js` (existing, enhanced)

**Purpose**: Validate form fields (client-side)

**Responsibilities**:
- Validate required fields (name, email, phone)
- Validate email format
- Validate URL format (GitHub, LinkedIn, project URLs)
- Show error messages
- Prevent submission if invalid

**Functions**:
- `validateForm(event)` - Main validation handler
- `validateRequired(fieldId, errorId, message)` - Check required fields
- `validateEmail(value)` - Validate email format
- `validateUrl(value)` - Validate URL format
- `showError(fieldId, errorId, message)` - Display error
- `clearErrors()` - Clear all errors

**Interface**:
- Attached to form submit event
- Updates DOM (error messages, input styling)

---

### 15. Template Preview Component
**File**: `static/js/template-preview.js`

**Purpose**: Handle template preview modal and interactions

**Responsibilities**:
- Show modal with live preview when template card clicked
- Fetch preview HTML from server or render client-side
- Handle modal open/close
- Handle "Use Template" button click
- Navigate to final resume page with selected template

**Functions**:
- `showPreview(templateId)` - Open modal with preview
- `closePreview()` - Close modal
- `selectTemplate(templateId)` - Save selection and navigate
- `renderPreview(templateId, profileData)` - Generate preview HTML

**Interface**:
- Attached to template card click events
- Updates DOM (modal visibility, preview content)
- Navigates to `/view?template=X` or calls `/save-template` API

---

## CSS Components

### 16. Global Styles Component
**File**: `static/css/style.css`

**Purpose**: Provide global styles and theme

**Responsibilities**:
- Define CSS custom properties (color palette: white, navy, teal)
- Provide base styles (typography, layout, spacing)
- Define component styles (navigation, footer, buttons, cards)
- Implement responsive design (media queries)
- Provide animations and transitions
- Define utility classes

**Sections**:
- CSS Variables (`:root`)
- Reset and base styles
- Navigation styles
- Form styles
- Button styles
- Card styles
- Responsive styles (`@media`)
- Animation keyframes

---

### 17. Print Styles Component
**File**: `static/css/print.css`

**Purpose**: Optimize layout for printing/PDF

**Responsibilities**:
- Hide navigation and action buttons
- Adjust spacing for paper
- Ensure black text on white background
- Control page breaks
- Optimize for A4/Letter paper size

**Sections**:
- Hide elements (`@media print`)
- Adjust spacing and margins
- Page break control
- Color adjustments

---

## Component Summary

| Component | Type | File | Purpose |
|-----------|------|------|---------|
| Base Template | Template | base.html | Common layout structure |
| Landing Page | Template | landing.html | Welcome and introduction |
| Multi-Step Form | Template | form.html | Collect user information |
| Template Selection | Template | template-selection.html | Choose resume template |
| Resume Template 1 | Template | resume-template1.html | Corporate Professional style |
| Resume Template 2 | Template | resume-template2.html | Modern Developer style |
| Resume Template 3 | Template | resume-template3.html | Creative Portfolio style |
| Final Resume | Template | view.html | Display resume + portfolio |
| Navigation | Template | base.html (included) | Sticky navigation bar |
| Footer | Template | base.html (included) | Footer information |
| Route Handler | Backend | app.py | HTTP request handling |
| Database | Backend | database.py | Database operations |
| Form Wizard | JavaScript | form-wizard.js | Multi-step navigation |
| Form Validation | JavaScript | form.js | Client-side validation |
| Template Preview | JavaScript | template-preview.js | Preview modal handling |
| Global Styles | CSS | style.css | Theme and component styles |
| Print Styles | CSS | print.css | Print optimization |

**Total Components**: 17 (8 templates, 2 backend, 3 JavaScript, 2 CSS, 2 shared template sections)
