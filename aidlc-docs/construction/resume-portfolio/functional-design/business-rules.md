# Business Rules

## Overview
This document defines all business rules, validation logic, and constraints for the AI CV Builder application.

---

## 1. Form Validation Rules

### BR-01: Required Field Validation
**Rule**: Name, email, and phone fields are required and must not be empty

**Scope**: Form Step 1 (Personal Information)

**Validation Logic**:
```
FOR EACH field IN [name, email, phone]:
    value = TRIM(field.value)
    IF value is empty OR value is NULL:
        SHOW ERROR: "[Field name] is required"
        MARK field as invalid
        PREVENT form submission
```

**Error Messages**:
- Name: "Name is required"
- Email: "Email is required"
- Phone: "Phone number is required"

**Enforcement**:
- Client-side: JavaScript validation on blur and submit
- Server-side: Optional backup validation in Flask route

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-02: Email Format Validation
**Rule**: Email must match valid email format

**Scope**: Form Step 1 (Personal Information)

**Validation Logic**:
```
email_regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
value = TRIM(email.value)

IF value is not empty:
    IF NOT email_regex.test(value):
        SHOW ERROR: "Please enter a valid email address"
        MARK field as invalid
        PREVENT form submission
```

**Email Format Requirements**:
- Must contain exactly one @ symbol
- Must have characters before @
- Must have characters after @
- Must have a dot (.) after @
- Must have characters after the dot
- No whitespace allowed

**Examples**:
- ✅ Valid: "john.doe@example.com", "user+tag@domain.co.uk"
- ❌ Invalid: "john@", "@example.com", "john doe@example.com", "john@example"

**Enforcement**:
- Client-side: JavaScript validation on blur and submit
- Server-side: Optional backup validation

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-03: URL Format Validation
**Rule**: URLs must start with http:// or https://

**Scope**: Form Step 1 (GitHub, LinkedIn) and Step 4 (Project URLs)

**Validation Logic**:
```
url_regex = /^https?:\/\/.+/
value = TRIM(url.value)

IF value is not empty:
    IF NOT url_regex.test(value):
        SHOW ERROR: "URL must start with http:// or https://"
        MARK field as invalid
        PREVENT form submission
```

**URL Format Requirements**:
- Must start with "http://" or "https://"
- Must have at least one character after the protocol
- No whitespace allowed

**Examples**:
- ✅ Valid: "https://github.com/user", "http://example.com"
- ❌ Invalid: "github.com/user", "www.example.com", "ftp://example.com"

**Enforcement**:
- Client-side: JavaScript validation on blur and submit
- Server-side: Optional backup validation

**Related Requirements**: FR-02 (Multi-Step Form Flow), FR-04 (Resume Template 1)

---

### BR-04: Optional Field Validation
**Rule**: Optional fields can be empty, but if provided, must meet format requirements

**Scope**: All optional fields (GitHub, LinkedIn, project URLs, education, skills, projects, certifications)

**Validation Logic**:
```
FOR EACH optional_field:
    value = TRIM(field.value)
    
    IF value is empty:
        ALLOW (no validation needed)
    ELSE:
        IF field is URL type:
            APPLY BR-03 (URL format validation)
        ELSE:
            ALLOW (no format validation)
```

**Optional Fields**:
- github_url (URL validation if provided)
- linkedin_url (URL validation if provided)
- education (no validation)
- skills (no validation)
- project1_url, project2_url, project3_url (URL validation if provided)
- All project and certification fields (no validation)

**Enforcement**:
- Client-side: JavaScript validation on blur and submit
- Server-side: Optional backup validation

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

## 2. Form Step Progression Rules

### BR-05: Step Validation Before Next
**Rule**: User cannot proceed to next step without validating current step

**Scope**: Multi-step form wizard (Steps 1-5)

**Validation Logic**:
```
FUNCTION nextStep():
    current_step = getCurrentStep()
    
    IF validateStep(current_step) == false:
        SHOW errors for invalid fields
        SCROLL to first error
        PREVENT navigation to next step
        RETURN
    
    MARK current_step as completed
    INCREMENT current_step
    SHOW next step
```

**Step-Specific Validation**:
- **Step 1**: Validate name, email, phone (required), GitHub/LinkedIn (optional URL format)
- **Step 2**: No validation (education is optional)
- **Step 3**: No validation (skills are optional)
- **Step 4**: Validate project URLs (optional URL format)
- **Step 5**: No validation (certifications are optional)

**Enforcement**:
- Client-side: JavaScript form wizard
- User Experience: Show errors, prevent navigation, scroll to error

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-06: Back Navigation Without Validation
**Rule**: User can navigate back to previous steps without validation

**Scope**: Multi-step form wizard (Steps 1-5)

**Navigation Logic**:
```
FUNCTION prevStep():
    current_step = getCurrentStep()
    
    IF current_step > 1:
        DECREMENT current_step
        SHOW previous step
        NO validation required
```

**Rationale**: Allow users to review and edit previous steps without forcing validation

**Enforcement**:
- Client-side: JavaScript form wizard
- User Experience: Immediate navigation, no validation

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-07: Form State Persistence
**Rule**: Form data persists across steps during the same session

**Scope**: Multi-step form wizard (Steps 1-5)

**Persistence Logic**:
```
FUNCTION saveFormState():
    FOR EACH field in form:
        formState[field.name] = field.value
    
    sessionStorage.setItem('formState', JSON.stringify(formState))

FUNCTION restoreFormState():
    formState = JSON.parse(sessionStorage.getItem('formState'))
    
    IF formState exists:
        FOR EACH field in formState:
            form[field].value = formState[field]
```

**Persistence Strategy**:
- Use sessionStorage (persists during browser session)
- Clear on successful form submission
- Restore on page load (for browser back button)

**Enforcement**:
- Client-side: JavaScript form wizard
- Storage: sessionStorage API

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

## 3. Data Persistence Rules

### BR-08: Profile Creation vs Update
**Rule**: If profile exists, update it; otherwise, create new profile

**Scope**: Form submission (POST /save)

**Persistence Logic**:
```
FUNCTION save():
    form_data = extract_form_data(request.form)
    existing_profile = get_data()
    
    IF existing_profile is None:
        save_data(form_data)  # INSERT
    ELSE:
        update_data(form_data)  # UPDATE
    
    REDIRECT to /select-template
```

**Database Operations**:
- **INSERT**: Create new profile with id=1
- **UPDATE**: Update existing profile with id=1

**Enforcement**:
- Server-side: Flask route handler
- Database: SQLite (database.py functions)

**Related Requirements**: FR-02 (Multi-Step Form Flow), FR-11 (Database Schema Updates)

---

### BR-09: Empty String to NULL Conversion
**Rule**: Empty strings are converted to NULL before database storage

**Scope**: All form fields

**Conversion Logic**:
```
FUNCTION _fill_defaults(data):
    FOR EACH field in expected_fields:
        IF field not in data:
            data[field] = None
        ELSE IF data[field] == '':
            data[field] = None
        ELSE:
            data[field] = TRIM(data[field])
    
    RETURN data
```

**Rationale**: Distinguish between "not provided" (NULL) and "provided but empty" (empty string)

**Enforcement**:
- Server-side: database.py (_fill_defaults function)
- Database: SQLite (NULL values)

**Related Requirements**: FR-11 (Database Schema Updates)

---

### BR-10: Single Profile Constraint
**Rule**: Only one profile exists in the database (id=1)

**Scope**: Database operations

**Constraint Logic**:
```
FUNCTION save_data(data):
    # Always insert with id=1
    INSERT INTO profile (id, ...) VALUES (1, ...)

FUNCTION update_data(data):
    # Always update row with id=1
    UPDATE profile SET ... WHERE id = 1

FUNCTION get_data():
    # Always query row with id=1
    SELECT * FROM profile WHERE id = 1
```

**Rationale**: Single-user design, no multi-user support

**Enforcement**:
- Server-side: database.py functions
- Database: SQLite (id=1 constraint)

**Related Requirements**: FR-11 (Database Schema Updates)

---

## 4. Template Selection Rules

### BR-11: Template Choice Required
**Rule**: User must select one of three templates before viewing final resume

**Scope**: Template selection page

**Selection Logic**:
```
FUNCTION selectTemplate(templateId):
    IF templateId NOT IN ['template1', 'template2', 'template3']:
        SHOW ERROR: "Invalid template selection"
        RETURN
    
    profile = get_data()
    profile['template_choice'] = templateId
    update_data(profile)
    
    REDIRECT to /view
```

**Valid Template IDs**:
- "template1" (Corporate Professional Resume)
- "template2" (Modern Developer Resume)
- "template3" (Creative Portfolio Resume)

**Enforcement**:
- Server-side: Flask route handler
- Client-side: JavaScript template selection

**Related Requirements**: FR-03 (Template Selection Page)

---

### BR-12: Default Template Fallback
**Rule**: If no template is selected, default to template1

**Scope**: Resume rendering (GET /view)

**Fallback Logic**:
```
FUNCTION view():
    profile = get_data()
    
    IF profile is None:
        REDIRECT to / (landing page)
    
    template_choice = profile.get('template_choice')
    
    IF template_choice is None OR template_choice NOT IN ['template1', 'template2', 'template3']:
        template_choice = 'template1'  # Default
    
    template_file = get_template_filename(template_choice)
    RENDER view.html with profile and template_file
```

**Default Template**: template1 (Corporate Professional Resume)

**Enforcement**:
- Server-side: Flask route handler
- Fallback: Always provide valid template

**Related Requirements**: FR-03 (Template Selection Page), FR-07 (Final Resume + Portfolio Page)

---

### BR-13: Template Change Preserves Data
**Rule**: Changing template preserves all profile data

**Scope**: Template selection and change

**Preservation Logic**:
```
FUNCTION changeTemplate(newTemplateId):
    profile = get_data()  # Get existing profile
    profile['template_choice'] = newTemplateId  # Update only template field
    update_data(profile)  # Save with all existing data
    
    REDIRECT to /view
```

**Rationale**: Template is presentation only, not data

**Enforcement**:
- Server-side: Flask route handler
- Database: UPDATE only template_choice field

**Related Requirements**: FR-03 (Template Selection Page), FR-07 (Final Resume + Portfolio Page)

---

## 5. Resume Rendering Rules

### BR-14: Empty Project Hiding
**Rule**: Projects with empty title AND empty description are hidden in resume

**Scope**: Resume templates (all three)

**Filtering Logic**:
```
FUNCTION filterProjects(profile):
    projects = []
    
    FOR i = 1 to 3:
        title = profile['project' + i + '_title']
        desc = profile['project' + i + '_desc']
        url = profile['project' + i + '_url']
        
        IF title is not empty OR desc is not empty:
            projects.append({
                'title': title,
                'description': desc,
                'url': url
            })
    
    RETURN projects
```

**Display Logic**:
- Show project if title OR description is provided
- URL is optional (can be NULL)
- Hide project if both title AND description are empty

**Enforcement**:
- Server-side: Jinja2 template logic
- Client-side: Template rendering

**Related Requirements**: FR-04, FR-05, FR-06 (Resume Templates)

---

### BR-15: Empty Certification Hiding
**Rule**: Certifications with empty name are hidden in resume

**Scope**: Resume templates (all three)

**Filtering Logic**:
```
FUNCTION filterCertifications(profile):
    certifications = []
    
    FOR i = 1 to 3:
        name = profile['cert' + i + '_name']
        org = profile['cert' + i + '_org']
        year = profile['cert' + i + '_year']
        
        IF name is not empty:
            certifications.append({
                'name': name,
                'organization': org,
                'year': year
            })
    
    RETURN certifications
```

**Display Logic**:
- Show certification if name is provided
- Organization and year are optional (can be NULL)
- Hide certification if name is empty

**Enforcement**:
- Server-side: Jinja2 template logic
- Client-side: Template rendering

**Related Requirements**: FR-04, FR-05, FR-06 (Resume Templates)

---

### BR-16: Skills Parsing
**Rule**: Skills text is parsed into individual skills (comma or newline separated)

**Scope**: Resume templates (all three)

**Parsing Logic**:
```
FUNCTION parseSkills(skillsText):
    IF skillsText is None OR skillsText is empty:
        RETURN []
    
    skillsText = TRIM(skillsText)
    
    IF skillsText contains ',':
        skills = SPLIT(skillsText, ',')
    ELSE IF skillsText contains '\n':
        skills = SPLIT(skillsText, '\n')
    ELSE:
        skills = [skillsText]
    
    # Trim and filter
    skills = [TRIM(skill) FOR skill IN skills IF TRIM(skill) is not empty]
    
    RETURN skills
```

**Parsing Strategy**:
- Try comma-separated first
- Fall back to newline-separated
- Single skill if no delimiter found
- Trim whitespace from each skill
- Filter out empty skills

**Enforcement**:
- Server-side: Jinja2 filter or Python helper function
- Client-side: Template rendering

**Related Requirements**: FR-04, FR-05, FR-06 (Resume Templates)

---

### BR-17: Optional Field Display
**Rule**: Optional fields are hidden if empty, shown if provided

**Scope**: Resume templates (all three)

**Display Logic**:
```
FOR EACH optional_field IN [github_url, linkedin_url, education, skills, summary]:
    IF profile[optional_field] is not empty:
        SHOW field in resume
    ELSE:
        HIDE field in resume
```

**Optional Fields**:
- GitHub URL (show as link if provided)
- LinkedIn URL (show as link if provided)
- Education (show as text if provided)
- Skills (show as list/badges if provided)
- Summary (show as text if provided, future enhancement)

**Enforcement**:
- Server-side: Jinja2 conditional logic
- Client-side: Template rendering

**Related Requirements**: FR-04, FR-05, FR-06 (Resume Templates)

---

## 6. Navigation and Redirect Rules

### BR-18: Redirect to Landing if No Profile
**Rule**: If user visits /view without a profile, redirect to landing page

**Scope**: Final resume page (GET /view)

**Redirect Logic**:
```
FUNCTION view():
    profile = get_data()
    
    IF profile is None:
        REDIRECT to / (landing page)
        RETURN
    
    # Continue with resume rendering
```

**Rationale**: Prevent viewing empty resume page

**Enforcement**:
- Server-side: Flask route handler
- HTTP: 302 redirect

**Related Requirements**: FR-07 (Final Resume + Portfolio Page)

---

### BR-19: POST-Redirect-GET Pattern
**Rule**: After form submission, redirect to next page (no direct rendering)

**Scope**: Form submission and template selection

**Redirect Logic**:
```
# Form submission
POST /save → Process data → REDIRECT to /select-template

# Template selection
POST /save-template → Process data → REDIRECT to /view
```

**Rationale**: Prevent duplicate submissions on page refresh

**Enforcement**:
- Server-side: Flask route handlers
- HTTP: 302 redirect after POST

**Related Requirements**: FR-02 (Multi-Step Form Flow), FR-03 (Template Selection Page)

---

### BR-20: Form Pre-Population on Edit
**Rule**: When editing, form is pre-populated with existing profile data

**Scope**: Form page (GET /form)

**Pre-Population Logic**:
```
FUNCTION form():
    profile = get_data()
    
    IF profile is None:
        RENDER form.html with empty fields
    ELSE:
        RENDER form.html with profile data
```

**Pre-Population Behavior**:
- All fields filled with existing values
- User can edit any field
- Submit updates existing profile (BR-08)

**Enforcement**:
- Server-side: Flask route handler
- Client-side: Jinja2 template (value="{{ profile.field }}")

**Related Requirements**: FR-02 (Multi-Step Form Flow), FR-07 (Final Resume + Portfolio Page)

---

## 7. PDF Download Rules

### BR-21: PDF Download via Print Dialog
**Rule**: PDF download uses browser's print functionality (window.print())

**Scope**: Final resume page (Download PDF button)

**Download Logic**:
```
FUNCTION downloadPDF():
    window.print()  # Opens browser print dialog
```

**Print Styling**:
- Use print.css for print-optimized layout
- Hide navigation, footer, action buttons
- Adjust spacing for paper (A4/Letter)
- Ensure black text on white background

**Enforcement**:
- Client-side: JavaScript (window.print())
- Styling: print.css (@media print)

**Related Requirements**: FR-07 (Final Resume + Portfolio Page)

---

## 8. Error Handling Rules

### BR-22: Validation Error Display
**Rule**: Validation errors are displayed below the invalid field with red border

**Scope**: Form validation (client-side)

**Error Display Logic**:
```
FUNCTION showError(fieldId, errorId, message):
    field = document.getElementById(fieldId)
    errorSpan = document.getElementById(errorId)
    
    field.classList.add('input-error')  # Red border
    errorSpan.textContent = message
    errorSpan.style.display = 'block'
```

**Error Styling**:
- Red border on invalid field (input-error class)
- Error message below field (red text)
- Scroll to first error on validation failure

**Enforcement**:
- Client-side: JavaScript validation
- Styling: CSS (input-error class)

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-23: Error Clearing on Correction
**Rule**: Errors are cleared when user corrects the field

**Scope**: Form validation (client-side)

**Error Clearing Logic**:
```
FUNCTION clearErrors():
    FOR EACH field WITH 'input-error' class:
        field.classList.remove('input-error')
    
    FOR EACH errorSpan:
        errorSpan.textContent = ''
        errorSpan.style.display = 'none'
```

**Clearing Triggers**:
- User corrects field (on blur)
- User clicks Next/Submit (before validation)

**Enforcement**:
- Client-side: JavaScript validation
- Event: blur, submit

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-24: Database Error Handling
**Rule**: Database errors are logged and handled gracefully

**Scope**: Database operations (database.py)

**Error Handling Logic**:
```
FUNCTION save_data(data):
    TRY:
        # Execute INSERT query
    EXCEPT SQLite Error:
        LOG error to console
        RETURN None or raise exception
```

**Error Scenarios**:
- Connection failure: Database file not accessible
- Constraint violation: Invalid data (shouldn't happen with validation)
- Unknown error: Log and show generic message

**Enforcement**:
- Server-side: database.py (try-except blocks)
- Logging: Console or log file

**Related Requirements**: NFR-04 (Maintainability)

---

## 9. Business Constraint Rules

### BR-25: Maximum Projects Constraint
**Rule**: User can enter maximum 3 projects

**Scope**: Form Step 4 (Projects)

**Constraint Logic**:
- Form provides exactly 3 project input sections
- No ability to add more projects
- Empty projects are hidden in resume (BR-14)

**Rationale**: Simplicity, beginner-friendly design

**Enforcement**:
- Client-side: Fixed form structure (3 project sections)
- Server-side: Database schema (9 project fields)

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-26: Maximum Certifications Constraint
**Rule**: User can enter maximum 3 certifications

**Scope**: Form Step 5 (Certifications)

**Constraint Logic**:
- Form provides exactly 3 certification input sections
- No ability to add more certifications
- Empty certifications are hidden in resume (BR-15)

**Rationale**: Simplicity, beginner-friendly design

**Enforcement**:
- Client-side: Fixed form structure (3 certification sections)
- Server-side: Database schema (9 certification fields)

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-27: Single User Constraint
**Rule**: Application supports only one user (no multi-user support)

**Scope**: Entire application

**Constraint Logic**:
- Database stores single profile (id=1)
- No authentication or user management
- No user sessions or login

**Rationale**: Beginner-friendly design, local development

**Enforcement**:
- Server-side: Database design (single row)
- Application: No authentication logic

**Related Requirements**: TC-01 (Technology Stack)

---

## 10. UI/UX Business Rules

### BR-28: Progress Indicator Update
**Rule**: Progress indicator updates to show current step and completion

**Scope**: Multi-step form wizard

**Progress Logic**:
```
FUNCTION updateProgress(stepNumber):
    progressText = "Step " + stepNumber + " of 5"
    progressBar.width = (stepNumber / 5 * 100) + "%"
    
    FOR i = 1 to stepNumber - 1:
        MARK step i as completed (checkmark)
```

**Progress Display**:
- Text: "Step X of 5"
- Progress bar: X/5 * 100%
- Completed steps: Checkmark icon

**Enforcement**:
- Client-side: JavaScript form wizard
- Styling: CSS (progress bar, checkmarks)

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-29: Button Visibility Rules
**Rule**: Next/Back/Submit buttons visibility changes based on current step

**Scope**: Multi-step form wizard

**Visibility Logic**:
```
FUNCTION updateButtonVisibility(stepNumber):
    IF stepNumber == 1:
        HIDE Back button
    ELSE:
        SHOW Back button
    
    IF stepNumber == 5:
        HIDE Next button
        SHOW Submit button
    ELSE:
        SHOW Next button
        HIDE Submit button
```

**Button States**:
- Step 1: Next only
- Steps 2-4: Back + Next
- Step 5: Back + Submit

**Enforcement**:
- Client-side: JavaScript form wizard
- Styling: CSS (display: none/block)

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

### BR-30: Scroll to Top on Step Change
**Rule**: Page scrolls to top when changing steps

**Scope**: Multi-step form wizard

**Scroll Logic**:
```
FUNCTION showStep(stepNumber):
    # ... show/hide step logic ...
    
    window.scrollTo(0, 0)  # Scroll to top
```

**Rationale**: Ensure user sees step heading and progress indicator

**Enforcement**:
- Client-side: JavaScript form wizard
- Browser API: window.scrollTo()

**Related Requirements**: FR-02 (Multi-Step Form Flow)

---

## Business Rules Summary

| Category | Rule Count | Key Rules |
|----------|------------|-----------|
| Form Validation | 4 | BR-01 to BR-04 (required, email, URL, optional) |
| Form Step Progression | 3 | BR-05 to BR-07 (validation, back nav, state persistence) |
| Data Persistence | 3 | BR-08 to BR-10 (create/update, NULL conversion, single profile) |
| Template Selection | 3 | BR-11 to BR-13 (required, default, preserve data) |
| Resume Rendering | 4 | BR-14 to BR-17 (hide empty, parse skills, optional fields) |
| Navigation and Redirect | 3 | BR-18 to BR-20 (redirect, POST-Redirect-GET, pre-population) |
| PDF Download | 1 | BR-21 (print dialog) |
| Error Handling | 3 | BR-22 to BR-24 (display, clearing, database errors) |
| Business Constraints | 3 | BR-25 to BR-27 (max projects/certs, single user) |
| UI/UX | 3 | BR-28 to BR-30 (progress, buttons, scroll) |

**Total Business Rules**: 30 rules across 10 categories

---

## Rule Enforcement Matrix

| Rule | Client-Side | Server-Side | Database | Notes |
|------|-------------|-------------|----------|-------|
| BR-01 | ✅ Primary | ⚠️ Optional | - | JavaScript validation |
| BR-02 | ✅ Primary | ⚠️ Optional | - | Regex validation |
| BR-03 | ✅ Primary | ⚠️ Optional | - | Regex validation |
| BR-04 | ✅ Primary | ⚠️ Optional | - | Conditional validation |
| BR-05 | ✅ | - | - | Form wizard logic |
| BR-06 | ✅ | - | - | Form wizard logic |
| BR-07 | ✅ | - | - | sessionStorage |
| BR-08 | - | ✅ | ✅ | INSERT vs UPDATE |
| BR-09 | - | ✅ | ✅ | NULL conversion |
| BR-10 | - | ✅ | ✅ | Single row constraint |
| BR-11 | ✅ | ✅ | - | Template validation |
| BR-12 | - | ✅ | - | Default fallback |
| BR-13 | - | ✅ | ✅ | UPDATE logic |
| BR-14 | - | ✅ | - | Jinja2 filtering |
| BR-15 | - | ✅ | - | Jinja2 filtering |
| BR-16 | - | ✅ | - | Parsing logic |
| BR-17 | - | ✅ | - | Conditional display |
| BR-18 | - | ✅ | - | Redirect logic |
| BR-19 | - | ✅ | - | POST-Redirect-GET |
| BR-20 | - | ✅ | - | Pre-population |
| BR-21 | ✅ | - | - | window.print() |
| BR-22 | ✅ | - | - | Error display |
| BR-23 | ✅ | - | - | Error clearing |
| BR-24 | - | ✅ | - | Exception handling |
| BR-25 | ✅ | ✅ | ✅ | Fixed structure |
| BR-26 | ✅ | ✅ | ✅ | Fixed structure |
| BR-27 | - | ✅ | ✅ | Single row design |
| BR-28 | ✅ | - | - | Progress update |
| BR-29 | ✅ | - | - | Button visibility |
| BR-30 | ✅ | - | - | Scroll behavior |

**Legend**:
- ✅ Primary enforcement point
- ⚠️ Optional/backup enforcement
- - Not applicable

---

## Rule Dependencies

### Rule Dependency Graph

```
BR-01 (Required) ──┐
BR-02 (Email)     ├──> BR-05 (Step Validation) ──> BR-19 (POST-Redirect-GET)
BR-03 (URL)       ├──> BR-22 (Error Display)
BR-04 (Optional)  ┘

BR-05 (Step Validation) ──> BR-07 (State Persistence)
BR-06 (Back Nav)        ──> BR-07 (State Persistence)

BR-08 (Create/Update) ──> BR-09 (NULL Conversion) ──> BR-10 (Single Profile)

BR-11 (Template Required) ──> BR-12 (Default Fallback)
BR-13 (Preserve Data)     ──> BR-08 (Create/Update)

BR-14 (Hide Projects) ──┐
BR-15 (Hide Certs)    ├──> BR-17 (Optional Fields)
BR-16 (Parse Skills)  ┘

BR-18 (Redirect if No Profile) ──> BR-10 (Single Profile)
BR-20 (Pre-Population)         ──> BR-08 (Create/Update)

BR-28 (Progress) ──┐
BR-29 (Buttons)  ├──> BR-05 (Step Validation)
BR-30 (Scroll)   ┘
```

---

## Conclusion

This comprehensive set of 30 business rules ensures the AI CV Builder operates correctly, consistently, and user-friendly. The rules cover all aspects of the application from form validation to resume rendering, with clear enforcement points and dependencies.

**Key Principles**:
- **Validation First**: Client-side validation for UX, optional server-side backup
- **Data Integrity**: NULL conversion, single profile constraint, required fields
- **User Experience**: Progressive disclosure, error feedback, state persistence
- **Simplicity**: Fixed structure (3 projects, 3 certs), single user, beginner-friendly

