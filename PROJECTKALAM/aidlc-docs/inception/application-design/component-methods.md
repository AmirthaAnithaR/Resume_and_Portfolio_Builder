# Component Methods

## Overview
This document defines method signatures for all components, their purposes, inputs, and outputs. Detailed business rules will be defined later in Functional Design.

---

## Backend Component Methods (app.py)

### Route Handler Methods

#### 1. `index()`
**Route**: `GET /`  
**Purpose**: Display landing page or redirect based on application state  
**Input**: None  
**Output**: Rendered landing.html template  
**Business Logic**: Show landing page to all users

---

#### 2. `form()`
**Route**: `GET /form`  
**Purpose**: Display multi-step form for profile input  
**Input**: None (checks for existing profile via `get_data()`)  
**Output**: Rendered form.html template with profile data (if exists)  
**Business Logic**: Pre-populate form if profile exists (edit mode)

---

#### 3. `save()`
**Route**: `POST /save`  
**Purpose**: Save or update user profile data  
**Input**: Form data from request.form (27+ fields)  
**Output**: Redirect to template selection page (`/select-template`)  
**Business Logic**:
- Extract all form fields
- Strip whitespace
- Check if profile exists
- Call `save_data()` or `update_data()`
- Redirect to template selection

---

#### 4. `select_template()`
**Route**: `GET /select-template`  
**Purpose**: Display template selection page with 3 template options  
**Input**: None (retrieves profile via `get_data()`)  
**Output**: Rendered template-selection.html with profile data  
**Business Logic**:
- Retrieve profile data
- If no profile, redirect to form
- Pass profile data to template for preview

---

#### 5. `save_template_choice()`
**Route**: `POST /save-template` or `GET /select-template?template=X`  
**Purpose**: Save user's template choice and redirect to final resume  
**Input**: Template choice (template1, template2, or template3)  
**Output**: Redirect to `/view`  
**Business Logic**:
- Extract template choice from request
- Update profile with template_choice field
- Call `update_data()`
- Redirect to view page

---

#### 6. `view()`
**Route**: `GET /view`  
**Purpose**: Display final resume + portfolio page  
**Input**: None (retrieves profile via `get_data()`)  
**Output**: Rendered view.html with profile data and template choice  
**Business Logic**:
- Retrieve profile data
- If no profile, redirect to landing page
- Determine template choice (default to template1 if not set)
- Pass profile and template_choice to view.html

---

### Helper Methods (if needed)

#### 7. `get_template_name(template_choice)`
**Purpose**: Map template choice to template filename  
**Input**: `template_choice` (str: "template1", "template2", "template3")  
**Output**: Template filename (str: "resume-template1.html", etc.)  
**Business Logic**: Simple mapping or default to template1

---

## Database Component Methods (database.py)

### Existing Methods (Enhanced)

#### 8. `init_db()`
**Purpose**: Initialize database and create profile table  
**Input**: None  
**Output**: None (side effect: creates table)  
**Business Logic**:
- Execute CREATE TABLE IF NOT EXISTS
- Include new optional fields (template_choice, summary)
- Safe to call multiple times

---

#### 9. `save_data(data)`
**Purpose**: Insert new profile into database  
**Input**: `data` (dict with profile fields)  
**Output**: None (side effect: inserts row)  
**Business Logic**:
- Fill defaults for missing fields
- Insert row with id=1
- Include new optional fields

---

#### 10. `get_data()`
**Purpose**: Retrieve profile from database  
**Input**: None  
**Output**: dict with profile data or None  
**Business Logic**:
- Query for row with id=1
- Convert to dict
- Return None if no profile exists

---

#### 11. `update_data(data)`
**Purpose**: Update existing profile in database  
**Input**: `data` (dict with profile fields)  
**Output**: None (side effect: updates row)  
**Business Logic**:
- Fill defaults for missing fields
- Update all fields for row with id=1
- Include new optional fields

---

#### 12. `_fill_defaults(data)`
**Purpose**: Ensure all expected keys exist in data dict  
**Input**: `data` (dict with partial profile fields)  
**Output**: dict with all keys present (None for missing)  
**Business Logic**:
- Iterate through expected keys (27 existing + 2 new)
- Set missing keys to None
- Convert empty strings to None

---

### New Methods (Optional)

#### 13. `update_template_choice(template_choice)`
**Purpose**: Update only the template_choice field  
**Input**: `template_choice` (str)  
**Output**: None (side effect: updates field)  
**Business Logic**:
- Execute UPDATE query for template_choice only
- More efficient than updating all fields

---

## Frontend JavaScript Methods

### Form Wizard Component (form-wizard.js)

#### 14. `initFormWizard()`
**Purpose**: Initialize form wizard on page load  
**Input**: None  
**Output**: None (side effect: sets up event listeners)  
**Business Logic**:
- Attach event listeners to Next/Back/Submit buttons
- Show first step
- Initialize progress indicator

---

#### 15. `showStep(stepNumber)`
**Purpose**: Display specific form step  
**Input**: `stepNumber` (int: 1-5)  
**Output**: None (side effect: updates DOM)  
**Business Logic**:
- Hide all steps
- Show step with matching data-step attribute
- Update progress indicator
- Update button visibility (hide Back on step 1, show Submit on step 5)
- Scroll to top

---

#### 16. `nextStep()`
**Purpose**: Validate current step and move to next  
**Input**: None (reads current step from DOM)  
**Output**: None (side effect: changes step or shows errors)  
**Business Logic**:
- Get current step number
- Validate current step fields
- If valid: save form state, increment step, call showStep()
- If invalid: show error messages, prevent navigation

---

#### 17. `prevStep()`
**Purpose**: Move to previous step  
**Input**: None (reads current step from DOM)  
**Output**: None (side effect: changes step)  
**Business Logic**:
- Get current step number
- Decrement step number
- Call showStep()
- No validation needed for going back

---

#### 18. `validateStep(stepNumber)`
**Purpose**: Validate all fields in a specific step  
**Input**: `stepNumber` (int: 1-5)  
**Output**: boolean (true if valid, false if invalid)  
**Business Logic**:
- Get all input fields in step
- Validate required fields (step 1: name, email, phone)
- Validate email format (step 1)
- Validate URL format (step 1: GitHub, LinkedIn; step 4: project URLs)
- Return true if all valid, false otherwise

---

#### 19. `saveFormState()`
**Purpose**: Save current form data to memory  
**Input**: None (reads from form fields)  
**Output**: None (side effect: updates formState object)  
**Business Logic**:
- Iterate through all form fields
- Store field values in formState object
- Persist to sessionStorage (optional)

---

#### 20. `restoreFormState()`
**Purpose**: Restore form data from memory  
**Input**: None (reads from formState object)  
**Output**: None (side effect: populates form fields)  
**Business Logic**:
- Iterate through formState object
- Set form field values
- Restore from sessionStorage if available

---

#### 21. `updateProgress(stepNumber)`
**Purpose**: Update progress indicator  
**Input**: `stepNumber` (int: 1-5)  
**Output**: None (side effect: updates DOM)  
**Business Logic**:
- Update progress text ("Step X of 5")
- Update progress bar width (X/5 * 100%)
- Highlight completed steps

---

### Form Validation Component (form.js)

#### 22. `validateForm(event)`
**Purpose**: Validate entire form before submission  
**Input**: `event` (form submit event)  
**Output**: None (side effect: prevents submission if invalid)  
**Business Logic**:
- Clear previous errors
- Validate all required fields
- Validate email format
- Validate URL format
- If invalid: prevent submission, show errors, scroll to first error
- If valid: allow submission

---

#### 23. `validateRequired(fieldId, errorId, message)`
**Purpose**: Check if required field has value  
**Input**: `fieldId` (str), `errorId` (str), `message` (str)  
**Output**: boolean (true if valid, false if empty)  
**Business Logic**:
- Get field value
- Trim whitespace
- If empty: show error, return false
- If not empty: return true

---

#### 24. `validateEmail(value)`
**Purpose**: Validate email format  
**Input**: `value` (str)  
**Output**: boolean (true if valid email format)  
**Business Logic**:
- Test value against email regex
- Return true/false

---

#### 25. `validateUrl(value)`
**Purpose**: Validate URL format  
**Input**: `value` (str)  
**Output**: boolean (true if valid URL format)  
**Business Logic**:
- Test value against URL regex (http:// or https://)
- Return true/false

---

#### 26. `validateOptionalUrl(fieldId, errorId, message)`
**Purpose**: Validate URL format if field is non-empty  
**Input**: `fieldId` (str), `errorId` (str), `message` (str)  
**Output**: boolean (true if empty or valid URL)  
**Business Logic**:
- Get field value
- If empty: return true (optional field)
- If not empty: validate URL format
- If invalid: show error, return false

---

#### 27. `showError(fieldId, errorId, message)`
**Purpose**: Display error message for field  
**Input**: `fieldId` (str), `errorId` (str), `message` (str)  
**Output**: None (side effect: updates DOM)  
**Business Logic**:
- Add error class to input field
- Set error message text in error span

---

#### 28. `clearErrors()`
**Purpose**: Clear all error messages  
**Input**: None  
**Output**: None (side effect: updates DOM)  
**Business Logic**:
- Remove error class from all inputs
- Clear all error message spans

---

### Template Preview Component (template-preview.js)

#### 29. `initTemplatePreview()`
**Purpose**: Initialize template preview functionality  
**Input**: None  
**Output**: None (side effect: sets up event listeners)  
**Business Logic**:
- Attach click listeners to template cards
- Attach click listener to modal close button
- Attach click listeners to "Use Template" buttons

---

#### 30. `showPreview(templateId)`
**Purpose**: Show modal with template preview  
**Input**: `templateId` (str: "template1", "template2", "template3")  
**Output**: None (side effect: shows modal)  
**Business Logic**:
- Get profile data from page or API
- Render preview HTML for selected template
- Insert preview HTML into modal
- Show modal (add visible class)

---

#### 31. `closePreview()`
**Purpose**: Close preview modal  
**Input**: None  
**Output**: None (side effect: hides modal)  
**Business Logic**:
- Hide modal (remove visible class)
- Clear modal content

---

#### 32. `selectTemplate(templateId)`
**Purpose**: Save template choice and navigate to final resume  
**Input**: `templateId` (str: "template1", "template2", "template3")  
**Output**: None (side effect: navigates to /view)  
**Business Logic**:
- Send POST request to /save-template with templateId
- Or navigate to /view?template=templateId
- Redirect to final resume page

---

#### 33. `renderPreview(templateId, profileData)`
**Purpose**: Generate preview HTML for template  
**Input**: `templateId` (str), `profileData` (object)  
**Output**: HTML string  
**Business Logic**:
- Based on templateId, generate HTML structure
- Populate with profileData
- Return HTML string for insertion into modal

---

## Template Component Methods (Jinja2 Macros)

### Form Step Macros (form.html)

#### 34. `render_step_1(profile)`
**Purpose**: Render Personal Information step  
**Input**: `profile` (dict or None)  
**Output**: HTML for step 1 fields  
**Business Logic**:
- Render name, email, phone, GitHub, LinkedIn fields
- Pre-populate if profile exists

---

#### 35. `render_step_2(profile)`
**Purpose**: Render Education step  
**Input**: `profile` (dict or None)  
**Output**: HTML for step 2 fields  
**Business Logic**:
- Render education textarea
- Pre-populate if profile exists

---

#### 36. `render_step_3(profile)`
**Purpose**: Render Skills step  
**Input**: `profile` (dict or None)  
**Output**: HTML for step 3 fields  
**Business Logic**:
- Render skills textarea
- Pre-populate if profile exists

---

#### 37. `render_step_4(profile)`
**Purpose**: Render Projects step  
**Input**: `profile` (dict or None)  
**Output**: HTML for step 4 fields  
**Business Logic**:
- Render 3 project sections (title, description, URL)
- Pre-populate if profile exists

---

#### 38. `render_step_5(profile)`
**Purpose**: Render Certifications step  
**Input**: `profile` (dict or None)  
**Output**: HTML for step 5 fields  
**Business Logic**:
- Render 3 certification sections (name, org, year)
- Pre-populate if profile exists

---

### Resume Template Macros (resume-template*.html)

#### 39. `render_header(profile)`
**Purpose**: Render resume header with name and contact info  
**Input**: `profile` (dict)  
**Output**: HTML for header section  
**Business Logic**:
- Display name prominently
- Display email, phone, GitHub, LinkedIn (if provided)

---

#### 40. `render_education(profile)`
**Purpose**: Render education section  
**Input**: `profile` (dict)  
**Output**: HTML for education section  
**Business Logic**:
- Display education text
- Handle newlines and formatting

---

#### 41. `render_skills(profile, style)`
**Purpose**: Render skills section  
**Input**: `profile` (dict), `style` (str: "list", "badges", "visual")  
**Output**: HTML for skills section  
**Business Logic**:
- Parse skills (comma-separated or newline-separated)
- Render based on style (list, badges, or visual)

---

#### 42. `render_projects(profile, style)`
**Purpose**: Render projects section  
**Input**: `profile` (dict), `style` (str: "list", "cards", "portfolio")  
**Output**: HTML for projects section  
**Business Logic**:
- Iterate through 3 projects
- Skip empty projects
- Render based on style (list, cards, or portfolio)

---

#### 43. `render_certifications(profile, style)`
**Purpose**: Render certifications section  
**Input**: `profile` (dict), `style` (str: "list", "timeline", "badges")  
**Output**: HTML for certifications section  
**Business Logic**:
- Iterate through 3 certifications
- Skip empty certifications
- Render based on style (list, timeline, or badges)

---

## Method Summary

| Component | Method Count | Key Methods |
|-----------|--------------|-------------|
| Route Handlers (app.py) | 7 | index(), form(), save(), select_template(), save_template_choice(), view() |
| Database (database.py) | 6 | init_db(), save_data(), get_data(), update_data(), _fill_defaults(), update_template_choice() |
| Form Wizard (form-wizard.js) | 8 | initFormWizard(), showStep(), nextStep(), prevStep(), validateStep(), saveFormState(), restoreFormState(), updateProgress() |
| Form Validation (form.js) | 7 | validateForm(), validateRequired(), validateEmail(), validateUrl(), validateOptionalUrl(), showError(), clearErrors() |
| Template Preview (template-preview.js) | 5 | initTemplatePreview(), showPreview(), closePreview(), selectTemplate(), renderPreview() |
| Template Macros (Jinja2) | 10 | render_step_1-5(), render_header(), render_education(), render_skills(), render_projects(), render_certifications() |

**Total Methods**: 43 methods across all components

---

## Notes

- **Detailed business rules** will be defined in Functional Design (CONSTRUCTION phase)
- **Method signatures** may be refined during implementation
- **Helper methods** may be added as needed during Code Generation
- **Error handling** will be detailed in Functional Design
- **Validation rules** will be specified in Functional Design
