# Business Logic Model

## Overview
This document defines the detailed business logic and algorithms for the AI CV Builder application.

---

## 1. Multi-Step Form Wizard Logic

### 1.1 Step Navigation Algorithm

**Purpose**: Manage navigation between form steps

**Algorithm**:
```
FUNCTION showStep(stepNumber):
    1. Hide all step containers (set display: none)
    2. Show step container matching stepNumber (set display: block)
    3. Update progress indicator:
        - Set progress text to "Step {stepNumber} of 5"
        - Set progress bar width to (stepNumber / 5 * 100)%
        - Mark completed steps with checkmark
    4. Update button visibility:
        - IF stepNumber == 1: Hide "Back" button
        - ELSE: Show "Back" button
        - IF stepNumber == 5: Show "Submit" button, Hide "Next" button
        - ELSE: Show "Next" button, Hide "Submit" button
    5. Scroll to top of page
END FUNCTION
```

**State Variables**:
- `currentStep` (integer): Current step number (1-5)
- `formState` (object): Form data for all steps
- `completedSteps` (array): List of completed step numbers

---

### 1.2 Step Validation Algorithm

**Purpose**: Validate current step before allowing navigation

**Algorithm**:
```
FUNCTION validateStep(stepNumber):
    1. Get all input fields in step
    2. Initialize isValid = true
    3. Clear previous errors
    
    4. FOR EACH field in step:
        IF field is required AND field is empty:
            - Show error message
            - Add error class to field
            - Set isValid = false
        
        IF field is email AND field is not empty:
            - Validate email format (regex)
            - IF invalid: show error, set isValid = false
        
        IF field is URL AND field is not empty:
            - Validate URL format (must start with http:// or https://)
            - IF invalid: show error, set isValid = false
    
    5. IF isValid == false:
        - Scroll to first error
        - Return false
    
    6. Return true
END FUNCTION
```

**Validation Rules by Step**:
- **Step 1** (Personal Info): name, email, phone required; email format; URL format for GitHub/LinkedIn
- **Step 2** (Education): No required fields
- **Step 3** (Skills): No required fields
- **Step 4** (Projects): URL format for project URLs (if provided)
- **Step 5** (Certifications): No required fields

---

### 1.3 Form State Management Algorithm

**Purpose**: Persist form data across steps

**Algorithm**:
```
FUNCTION saveFormState():
    1. Initialize formState object
    2. FOR EACH input field in form:
        - Get field name and value
        - Store in formState[name] = value
    3. Save formState to sessionStorage
    4. Return formState
END FUNCTION

FUNCTION restoreFormState():
    1. Load formState from sessionStorage
    2. IF formState exists:
        FOR EACH field in formState:
            - Find input element by name
            - Set input value to formState[field]
    3. Return formState or null
END FUNCTION

FUNCTION clearFormState():
    1. Clear sessionStorage
    2. Reset formState object
    3. Clear all form fields
END FUNCTION
```

**Storage Strategy**:
- Use `sessionStorage` for persistence during session
- Clear on successful submission
- Restore on page load (for browser back button)

---

### 1.4 Form Submission Logic

**Purpose**: Handle form submission and redirect

**Algorithm**:
```
FUNCTION handleFormSubmit(event):
    1. Prevent default form submission
    2. Validate all steps (1-5)
    3. IF any step is invalid:
        - Show error message
        - Navigate to first invalid step
        - Return false
    4. Save form state to sessionStorage (backup)
    5. Allow form submission (POST /save)
    6. Server redirects to /select-template
END FUNCTION
```

**Server-Side Logic** (app.py):
```
FUNCTION save():
    1. Extract form data from request.form
    2. Strip whitespace from all fields
    3. Check if profile exists (get_data())
    4. IF profile exists:
        - Call update_data(data)
    5. ELSE:
        - Call save_data(data)
    6. Redirect to /select-template
END FUNCTION
```

---

## 2. Template Selection Logic

### 2.1 Template Preview Algorithm

**Purpose**: Show live preview of template with user data

**Algorithm**:
```
FUNCTION showPreview(templateId):
    1. Get profile data from page context or API
    2. Generate preview HTML:
        - Load template structure for templateId
        - Populate with profile data
        - Handle empty fields (show placeholder or hide)
    3. Insert preview HTML into modal
    4. Show modal (add 'visible' class)
    5. Attach close button listener
END FUNCTION

FUNCTION closePreview():
    1. Hide modal (remove 'visible' class)
    2. Clear modal content
END FUNCTION
```

**Preview Data Strategy**:
- Use actual user data where available
- Show placeholder text for empty fields
- Maintain template styling in preview

---

### 2.2 Template Selection Algorithm

**Purpose**: Save template choice and navigate to final resume

**Algorithm**:
```
FUNCTION selectTemplate(templateId):
    1. Validate templateId (must be template1, template2, or template3)
    2. Send request to save template choice:
        - Option A: POST /save-template with templateId
        - Option B: GET /view?template=templateId
    3. Server updates profile.template_choice
    4. Server redirects to /view
    5. Final resume page loads with selected template
END FUNCTION
```

**Server-Side Logic** (app.py):
```
FUNCTION save_template_choice():
    1. Get templateId from request (query param or form data)
    2. Validate templateId (must be template1/2/3)
    3. Get profile data (get_data())
    4. Update profile['template_choice'] = templateId
    5. Call update_data(profile)
    6. Redirect to /view
END FUNCTION
```

---

## 3. Resume Rendering Logic

### 3.1 Template Inclusion Algorithm

**Purpose**: Dynamically include selected resume template

**Algorithm** (Jinja2):
```
FUNCTION render_resume(profile):
    1. Get template_choice from profile
    2. IF template_choice is None:
        - Set template_choice = 'template1' (default)
    3. Map template_choice to filename:
        - template1 → resume-template1.html
        - template2 → resume-template2.html
        - template3 → resume-template3.html
    4. Include template file: {% include template_file %}
    5. Pass profile data to template
END FUNCTION
```

**Server-Side Logic** (app.py):
```
FUNCTION view():
    1. Get profile data (get_data())
    2. IF profile is None:
        - Redirect to / (landing page)
    3. Get template_choice from profile
    4. Get template filename (get_template_filename())
    5. Render view.html with profile and template_file
END FUNCTION
```

---

### 3.2 Data Binding Algorithm

**Purpose**: Bind profile data to template fields

**Algorithm** (Jinja2):
```
FUNCTION bind_profile_data(profile):
    1. FOR EACH field in template:
        - Get value from profile[field]
        - IF value is None or empty:
            - Hide field or show placeholder
        - ELSE:
            - Display value with proper formatting
    
    2. Special handling:
        - Skills: Parse comma/newline separated → list
        - Projects: Filter out empty projects (all 3 fields empty)
        - Certifications: Filter out empty certifications
        - URLs: Make clickable links
        - Education: Preserve newlines
END FUNCTION
```

**Empty Field Handling**:
- **Hide**: Projects, certifications (if all fields empty)
- **Show placeholder**: Optional fields in form
- **Required fields**: Always shown (validated on submission)

---

### 3.3 Skills Parsing Algorithm

**Purpose**: Parse skills text into individual skills

**Algorithm**:
```
FUNCTION parseSkills(skillsText):
    1. IF skillsText is None or empty:
        - Return empty array
    
    2. Trim whitespace from skillsText
    
    3. IF skillsText contains comma:
        - Split by comma
        - Trim each skill
        - Filter out empty strings
        - Return array of skills
    
    4. ELSE IF skillsText contains newline:
        - Split by newline
        - Trim each skill
        - Filter out empty strings
        - Return array of skills
    
    5. ELSE:
        - Return array with single skill
END FUNCTION
```

**Example**:
- Input: "Python, JavaScript, SQL"
- Output: ["Python", "JavaScript", "SQL"]

---

### 3.4 Project Filtering Algorithm

**Purpose**: Filter out empty projects

**Algorithm**:
```
FUNCTION filterProjects(profile):
    1. Initialize projects array
    2. FOR i = 1 to 3:
        - Get project_title = profile['project' + i + '_title']
        - Get project_desc = profile['project' + i + '_desc']
        - Get project_url = profile['project' + i + '_url']
        
        - IF title is not empty OR desc is not empty:
            - Add project to projects array:
                {
                    title: project_title,
                    description: project_desc,
                    url: project_url
                }
    
    3. Return projects array
END FUNCTION
```

**Logic**: Show project if title OR description is provided (URL is optional)

---

### 3.5 Certification Filtering Algorithm

**Purpose**: Filter out empty certifications

**Algorithm**:
```
FUNCTION filterCertifications(profile):
    1. Initialize certifications array
    2. FOR i = 1 to 3:
        - Get cert_name = profile['cert' + i + '_name']
        - Get cert_org = profile['cert' + i + '_org']
        - Get cert_year = profile['cert' + i + '_year']
        
        - IF name is not empty:
            - Add certification to certifications array:
                {
                    name: cert_name,
                    organization: cert_org,
                    year: cert_year
                }
    
    3. Return certifications array
END FUNCTION
```

**Logic**: Show certification if name is provided (org and year are optional)

---

## 4. Form Validation Logic

### 4.1 Required Field Validation

**Purpose**: Ensure required fields are not empty

**Algorithm**:
```
FUNCTION validateRequired(fieldId, errorId, message):
    1. Get field element by fieldId
    2. Get field value and trim whitespace
    3. IF value is empty:
        - Show error message in errorId element
        - Add 'input-error' class to field
        - Return false
    4. Return true
END FUNCTION
```

**Required Fields**:
- name (Step 1)
- email (Step 1)
- phone (Step 1)

---

### 4.2 Email Format Validation

**Purpose**: Validate email format

**Algorithm**:
```
FUNCTION validateEmail(value):
    1. Define email regex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    2. Test value against regex
    3. Return true if matches, false otherwise
END FUNCTION
```

**Regex Explanation**:
- `^[^\s@]+`: One or more non-whitespace, non-@ characters at start
- `@`: Literal @ symbol
- `[^\s@]+`: One or more non-whitespace, non-@ characters
- `\.`: Literal dot
- `[^\s@]+$`: One or more non-whitespace, non-@ characters at end

---

### 4.3 URL Format Validation

**Purpose**: Validate URL format

**Algorithm**:
```
FUNCTION validateUrl(value):
    1. Define URL regex: /^https?:\/\/.+/
    2. Test value against regex
    3. Return true if matches, false otherwise
END FUNCTION
```

**Regex Explanation**:
- `^https?`: Starts with http or https
- `:\/\/`: Literal ://
- `.+$`: One or more characters

---

### 4.4 Optional URL Validation

**Purpose**: Validate URL only if field is not empty

**Algorithm**:
```
FUNCTION validateOptionalUrl(fieldId, errorId, message):
    1. Get field element by fieldId
    2. Get field value and trim whitespace
    3. IF value is empty:
        - Return true (optional field)
    4. IF validateUrl(value) is false:
        - Show error message in errorId element
        - Add 'input-error' class to field
        - Return false
    5. Return true
END FUNCTION
```

**Optional URL Fields**:
- github_url (Step 1)
- linkedin_url (Step 1)
- project1_url, project2_url, project3_url (Step 4)

---

## 5. Navigation Logic

### 5.1 Page Navigation Algorithm

**Purpose**: Handle navigation between pages

**Algorithm**:
```
FUNCTION navigateTo(url):
    1. IF current page has unsaved changes:
        - (Optional) Show confirmation dialog
        - IF user cancels: return
    2. Navigate to url (window.location.href = url)
END FUNCTION
```

**Navigation Rules**:
- Landing page → Form page: Direct navigation
- Form page → Template selection: After form submission
- Template selection → Final resume: After template selection
- Final resume → Form page: Edit button
- Final resume → Template selection: Change template button
- Any page → Landing page: Home link in navigation

---

### 5.2 Redirect Logic

**Purpose**: Handle server-side redirects

**Algorithm** (Flask):
```
FUNCTION redirect_after_save():
    1. After successful save/update
    2. Redirect to /select-template (302 Found)
    3. Browser navigates to template selection page
END FUNCTION

FUNCTION redirect_after_template_selection():
    1. After saving template choice
    2. Redirect to /view (302 Found)
    3. Browser navigates to final resume page
END FUNCTION

FUNCTION redirect_if_no_profile():
    1. IF user visits /view without profile
    2. Redirect to / (landing page)
    3. User sees landing page with "Get Started" button
END FUNCTION
```

**POST-Redirect-GET Pattern**:
- POST /save → Redirect → GET /select-template
- POST /save-template → Redirect → GET /view
- Prevents duplicate submissions on page refresh

---

## 6. Error Handling Logic

### 6.1 Validation Error Handling

**Purpose**: Display validation errors to user

**Algorithm**:
```
FUNCTION showError(fieldId, errorId, message):
    1. Get field element by fieldId
    2. Get error element by errorId
    3. Add 'input-error' class to field (red border)
    4. Set error element text to message
    5. Make error element visible
END FUNCTION

FUNCTION clearErrors():
    1. Get all elements with 'input-error' class
    2. Remove 'input-error' class from each
    3. Get all error message elements
    4. Clear text and hide each
END FUNCTION
```

**Error Display**:
- Red border on invalid field
- Error message below field
- Scroll to first error on submit

---

### 6.2 Database Error Handling

**Purpose**: Handle database operation failures

**Algorithm** (Python):
```
FUNCTION handle_database_error(error):
    1. Log error to console
    2. IF error is connection error:
        - Show "Database connection failed" message
    3. ELSE IF error is constraint violation:
        - Show "Data validation failed" message
    4. ELSE:
        - Show generic "An error occurred" message
    5. Return error response or redirect to error page
END FUNCTION
```

**Error Scenarios**:
- Connection failure: Database file not accessible
- Constraint violation: Invalid data (shouldn't happen with validation)
- Unknown error: Log and show generic message

---

### 6.3 JavaScript Error Handling

**Purpose**: Handle JavaScript errors gracefully

**Algorithm**:
```
FUNCTION handleJavaScriptError(error):
    1. Log error to console
    2. IF error is in form wizard:
        - Fall back to standard form submission
    3. IF error is in template preview:
        - Show error message, allow template selection without preview
    4. IF error is in validation:
        - Fall back to server-side validation
END FUNCTION
```

**Graceful Degradation**:
- Form works without JavaScript (standard HTML form)
- Template selection works without preview
- Server-side validation as backup

---

## 7. Data Transformation Logic

### 7.1 Form Data Extraction

**Purpose**: Extract and clean form data

**Algorithm** (Python):
```
FUNCTION extract_form_data(request_form):
    1. Define field list (29 fields)
    2. Initialize data dictionary
    3. FOR EACH field in field list:
        - Get value from request_form.get(field, '')
        - Trim whitespace
        - IF value is empty string: set to None
        - ELSE: set data[field] = value
    4. Return data dictionary
END FUNCTION
```

**Field Processing**:
- Trim whitespace from all fields
- Convert empty strings to None (NULL in database)
- Preserve newlines in textarea fields (education, skills, descriptions)

---

### 7.2 Text Formatting

**Purpose**: Format text for display

**Algorithm** (Jinja2 filters):
```
FUNCTION format_text(text):
    1. IF text is None: return empty string
    2. Escape HTML special characters (Jinja2 auto-escapes)
    3. Preserve newlines (use <br> or white-space: pre-line)
    4. Return formatted text
END FUNCTION

FUNCTION truncate_text(text, max_length):
    1. IF text is None: return empty string
    2. IF length(text) <= max_length: return text
    3. Truncate to max_length
    4. Append "..." (ellipsis)
    5. Return truncated text
END FUNCTION
```

**Use Cases**:
- Education: Preserve newlines
- Skills: Parse into list
- Project descriptions: Preserve newlines, optionally truncate
- Certification names: Display as-is

---

## 8. State Management

### 8.1 Client-Side State

**State Variables**:
- `currentStep` (integer): Current form step (1-5)
- `formState` (object): Form data for all fields
- `completedSteps` (array): List of completed step numbers
- `modalVisible` (boolean): Template preview modal visibility
- `selectedTemplate` (string): Currently selected template ID

**State Persistence**:
- `sessionStorage`: Form data persists during session
- Cleared on successful submission
- Restored on page load (browser back button)

---

### 8.2 Server-Side State

**State Storage**:
- Database (SQLite): Profile data (29 fields)
- No session storage needed (stateless HTTP)

**State Retrieval**:
- `get_data()`: Retrieve profile from database
- Returns dict or None

---

## 9. Business Logic Summary

**Total Algorithms**: 25+ algorithms defined

**Key Logic Areas**:
1. Multi-step form wizard (4 algorithms)
2. Template selection (2 algorithms)
3. Resume rendering (5 algorithms)
4. Form validation (4 algorithms)
5. Navigation (2 algorithms)
6. Error handling (3 algorithms)
7. Data transformation (2 algorithms)
8. State management (2 algorithms)

**Complexity Level**: Moderate - clear logic with well-defined rules

**Technology-Agnostic**: Logic can be implemented in any language/framework
