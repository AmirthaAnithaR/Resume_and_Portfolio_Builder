# Functional Design Plan: AI CV Builder (Resume Portfolio)

## Unit Information
- **Unit Name**: resume-portfolio
- **Unit Type**: Full-stack web application (Frontend redesign with minimal backend changes)
- **Scope**: Landing page, multi-step form, template selection, three resume templates, final resume view

---

## Functional Design Checklist

### Phase 1: Business Logic Modeling
- [ ] Define page navigation flow and routing logic
- [ ] Define multi-step form wizard state management
- [ ] Define template selection and preview logic
- [ ] Define resume rendering logic for three templates
- [ ] Define data transformation logic (form data → resume display)

### Phase 2: Domain Model Design
- [ ] Define Profile entity structure (existing + new fields)
- [ ] Define FormState entity (client-side state)
- [ ] Define TemplateChoice entity
- [ ] Define validation rules for all entities

### Phase 3: Business Rules Definition
- [ ] Define form validation rules (required fields, formats)
- [ ] Define navigation rules (when to allow/prevent transitions)
- [ ] Define template selection rules
- [ ] Define data persistence rules
- [ ] Define error handling rules

### Phase 4: Frontend Components Design
- [ ] Define component hierarchy and structure
- [ ] Define props and state for each component
- [ ] Define user interaction flows
- [ ] Define form validation rules per step
- [ ] Define API integration points

---

## Clarifying Questions

### Business Logic Modeling

#### Q1: Page Navigation Flow
When a user visits the root URL `/`, what should be the default behavior?

**Context**: The requirements mention both a landing page and a form page. We need to clarify the routing strategy.

**Options**:
A) Always show landing page first, regardless of profile state
B) Show landing page if no profile exists, redirect to /view if profile exists
C) Show landing page for first visit, then remember preference (cookie/session)
D) Make landing page optional - go directly to form page

[Answer]: a

---

#### Q2: Multi-Step Form State Persistence
How should form data be persisted as users navigate between steps?

**Context**: Users need to move back and forth between form steps without losing data.

**Options**:
A) Client-side only (JavaScript object in memory, lost on page refresh)
B) Client-side with sessionStorage (persists during session, lost on browser close)
C) Client-side with localStorage (persists across sessions)
D) Server-side (save draft to database on each step)

[Answer]: c

---

#### Q3: Form Edit Mode Behavior
When a user with an existing profile clicks "Edit Details", should they see the multi-step wizard or a single-page form?

**Context**: Edit mode needs to balance ease of use with consistency.

**Options**:
A) Show multi-step wizard (consistent with create flow)
B) Show single-page form with all fields (faster for editing)
C) Show multi-step wizard but allow "Save" at any step
D) Let user choose between wizard and single-page view

[Answer]: a

---

#### Q4: Template Preview Data Source
When showing template previews on the selection page, what data should be used?

**Context**: Template previews need to show realistic content.

**Options**:
A) User's actual data (just submitted from form)
B) Placeholder/sample data (generic example)
C) Mix: User's name + sample data for other fields
D) User's data with fallback to sample data for empty fields

[Answer]: d

---

#### Q5: Template Change Behavior
When a user clicks "Change Template" from the final resume page, what should happen?

**Context**: Users may want to try different templates after seeing the result.

**Options**:
A) Return to template selection page, show previews again
B) Show modal with template options on current page
C) Cycle through templates without leaving page (Next/Previous buttons)
D) Return to template selection with current template highlighted

[Answer]: d

---

### Domain Model Design

#### Q6: Optional Fields Handling
How should optional fields (GitHub, LinkedIn, project URLs, certifications) be handled in the domain model?

**Context**: Not all users will fill all optional fields.

**Options**:
A) Store as NULL in database, skip rendering if NULL
B) Store as empty string "", skip rendering if empty
C) Store as NULL, convert to empty string in application layer
D) Store with special marker value (e.g., "N/A")

[Answer]: a

---

#### Q7: Skills Data Format
How should skills be stored and parsed?

**Context**: Skills need to be displayed as badges/pills in some templates.

**Options**:
A) Comma-separated string (e.g., "Python, JavaScript, SQL")
B) Newline-separated string (one skill per line)
C) JSON array stored as TEXT (e.g., '["Python", "JavaScript"]')
D) Accept both comma and newline, parse intelligently

[Answer]: d

---

#### Q8: Project Data Structure
How should project data be validated and stored?

**Context**: Users can enter up to 3 projects, each with title, description, and URL.

**Options**:
A) All fields required for each project (if project1_title exists, project1_desc and project1_url required)
B) Only title required, description and URL optional
C) Title and description required, URL optional
D) All fields optional (allow partial project entries)

[Answer]: c

---

#### Q9: Template Choice Default
What should happen if a user's profile doesn't have a template_choice saved?

**Context**: Existing profiles or edge cases where template selection is skipped.

**Options**:
A) Default to template1 (Corporate Professional)
B) Force user to select template before viewing resume
C) Show all three templates stacked on view page
D) Randomly select a template

[Answer]: a

---

### Business Rules Definition

#### Q10: Email Validation Rule
What level of email validation should be enforced?

**Context**: Email is a required field and needs proper validation.

**Options**:
A) Basic regex (contains @ and .)
B) Strict RFC 5322 compliant regex
C) HTML5 input type="email" validation only
D) Basic regex + DNS check (verify domain exists)

[Answer]: a

---

#### Q11: URL Validation Rule
What level of URL validation should be enforced for GitHub, LinkedIn, and project URLs?

**Context**: URLs are optional but should be valid if provided.

**Options**:
A) Must start with http:// or https://
B) Must start with http:// or https:// and match URL pattern
C) Accept URLs without protocol, auto-prepend https://
D) No validation, accept any text

[Answer]: c
---

#### Q12: Required Fields Per Step
Which fields should be required in each form step?

**Context**: Need to define validation rules for each step.

**Step 1 (Personal Info)**:a
A) Name, email, phone required; GitHub, LinkedIn optional
B) All fields required
C) Only name and email required
D) Only name required

**Step 2 (Education)**:a
A) Required (cannot be empty)
B) Optional (can skip)

**Step 3 (Skills)**:a
A) Required (at least one skill)
B) Optional (can skip)

**Step 4 (Projects)**:b
A) At least one project required
B) All three projects required
C) Optional (can skip all)

**Step 5 (Certifications)**:b
A) At least one certification required
B) All three certifications required
C) Optional (can skip all)

[Answer]: 

---

#### Q13: Navigation Rules - Back Button
When a user clicks "Back" in the multi-step form, should validation be enforced?

**Context**: Users may want to go back to fix errors.

**Options**:
A) No validation, always allow going back
B) Validate current step before allowing back
C) Save current step data (even if invalid) before going back
D) Warn user about unsaved changes before going back

[Answer]: a

---

#### Q14: Form Submission Behavior
What should happen after the user clicks "Submit" on the final form step?

**Context**: Need to define the complete submission flow.

**Options**:
A) Save data → Redirect to template selection immediately
B) Save data → Show success message → Redirect to template selection after 2 seconds
C) Save data → Show loading spinner → Redirect to template selection
D) Save data → Redirect to view page with default template (skip template selection)

[Answer]: c

---

#### Q15: Error Handling - Save Failure
What should happen if saving profile data fails (database error)?

**Context**: Need to handle edge cases gracefully.

**Options**:
A) Show error message, stay on current page, allow retry
B) Show error message, redirect to form page
C) Show generic error page with "Try Again" button
D) Log error silently, redirect to landing page

[Answer]: a

---

### Frontend Components Design

#### Q16: Form Step Component Structure
How should form steps be structured in the HTML?

**Context**: Need to decide on the DOM structure for the multi-step wizard.

**Options**:
A) All steps in one form, show/hide with CSS (display: none)
B) All steps in one form, show/hide with JavaScript (remove/add from DOM)
C) Separate forms for each step, submit each step individually
D) Single form with dynamic content replacement (SPA-style)

[Answer]: a

---

#### Q17: Progress Indicator Design
What information should the progress indicator show?

**Context**: Users need to know their position in the form flow.

**Options**:
A) Step number only (e.g., "Step 2 of 5")
B) Step number + step name (e.g., "Step 2 of 5: Education")
C) Visual progress bar + step number
D) Visual progress bar + step number + step name + completed steps checkmarks

[Answer]: d

---

#### Q18: Template Preview Modal Behavior
How should the template preview modal work?

**Context**: Users can click template cards to see a preview.

**Options**:
A) Modal shows full-size preview, scrollable, with "Use Template" and "Close" buttons
B) Modal shows thumbnail preview with "Use Template" and "Close" buttons
C) Modal shows side-by-side comparison of all templates
D) No modal - clicking card directly selects template

[Answer]: a

---

#### Q19: Resume Template Conditional Rendering
How should resume templates handle missing optional data?

**Context**: Not all users will have GitHub, LinkedIn, projects, or certifications.

**Options**:
A) Hide entire section if all fields are empty (e.g., hide Projects section if no projects)
B) Show section with "Not provided" message
C) Show section header but leave content area blank
D) Hide individual items but keep section visible

[Answer]: a

---

#### Q20: Skills Display Logic
How should skills be displayed in different templates?

**Context**: Template 1 uses list, Template 2 uses badges, Template 3 uses visual display.

**Options**:
A) Parse skills string, split by comma or newline, render as array
B) Display skills as-is (raw text) in all templates
C) Parse skills, limit to first 10 skills, show "..." if more
D) Parse skills, categorize by type (languages, frameworks, tools)

[Answer]: a

---

#### Q21: Download PDF Behavior
How should the "Download as PDF" button work?

**Context**: Users want to save their resume as PDF.

**Options**:
A) Trigger browser print dialog (window.print()), user saves as PDF
B) Generate PDF on server-side, download file
C) Use client-side PDF library (e.g., jsPDF) to generate PDF
D) Show print-optimized view, instruct user to print manually

[Answer]: a

---

#### Q22: Mobile Navigation Menu
How should the navigation menu work on mobile devices?

**Context**: Mobile screens need a hamburger menu.

**Options**:
A) Hamburger icon, slide-in menu from left
B) Hamburger icon, slide-in menu from right
C) Hamburger icon, dropdown menu below navbar
D) Hamburger icon, full-screen overlay menu

[Answer]: d

---

#### Q23: Form Validation Feedback
How should validation errors be displayed to users?

**Context**: Users need clear feedback when validation fails.

**Options**:
A) Inline error messages below each field (red text)
B) Inline error messages + red border on invalid fields
C) Inline error messages + red border + icon (X or !)
D) Summary error message at top of form + inline messages

[Answer]: b

---

#### Q24: Template Card Hover Effect
What should happen when a user hovers over a template card?

**Context**: Need to provide visual feedback for interactivity.

**Options**:
A) Scale up slightly (transform: scale(1.05))
B) Add shadow effect (box-shadow)
C) Change border color to accent color (teal)
D) All of the above (scale + shadow + border)

[Answer]: d

---

#### Q25: Loading States
When should loading indicators be shown?

**Context**: Users need feedback during asynchronous operations.

**Options**:
A) Show spinner when saving form data
B) Show spinner when loading template preview
C) Show spinner when navigating between pages
D) All of the above

[Answer]: d

---

### Data Flow and Integration

#### Q26: API Endpoints
Which API endpoints need to be created or modified?

**Context**: Need to define backend routes for the new flow.

**Current Routes**:
- GET / (landing or form)
- GET /form (form page)
- POST /save (save profile)
- GET /view (view resume)

**New Routes Needed**:
A) GET /landing, GET /select-template, POST /save-template
B) GET /select-template, POST /save-template
C) GET /select-template only (save template via query param)
D) No new routes needed (use existing routes)

[Answer]: b

---

#### Q27: Form Data Submission Method
How should form data be submitted to the backend?

**Context**: Need to decide on submission approach.

**Options**:
A) Traditional form POST (full page reload)
B) AJAX POST (no page reload, redirect via JavaScript)
C) Fetch API POST (modern approach, no page reload)
D) FormData API with Fetch (supports file uploads if needed later)

[Answer]: d

---

#### Q28: Template Preview Data Fetching
How should template preview data be fetched?

**Context**: Preview modal needs user data to render template.

**Options**:
A) Pass data via JavaScript (embedded in page on load)
B) Fetch data via AJAX when modal opens
C) Store data in sessionStorage, retrieve when needed
D) Re-submit form data when opening preview

[Answer]: a

---

---

## Instructions for User

Please answer all questions above by filling in the `[Answer]:` tags with your chosen option letter (A, B, C, or D) or a custom answer if none of the options fit.

**Example**:
```
[Answer]: A
```

or

```
[Answer]: B - but with a slight modification: use localStorage only for draft saves, not final submission
```

Once you've answered all questions, reply with **"completed"** and I will analyze your answers and proceed with generating the functional design artifacts.

---

## Notes

- These questions are designed to clarify business logic, domain model, business rules, and frontend component design
- Your answers will directly inform the functional design artifacts
- If any question is unclear or you need more context, please ask before answering
- You can provide custom answers if the provided options don't match your vision
