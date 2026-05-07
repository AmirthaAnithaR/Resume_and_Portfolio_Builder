# Functional Design Plan: AI CV Builder

## Overview
This plan outlines the detailed functional design for the AI CV Builder redesign, focusing on business logic, domain models, business rules, and frontend component structure.

## Unit Context
**Unit Name**: AI CV Builder (Single Unit)  
**Scope**: Complete frontend redesign with multi-step form, template selection, and three resume templates  
**Responsibilities**: User profile management, template selection, resume rendering, portfolio display

---

## Functional Design Execution Plan

### Phase 1: Business Logic Modeling
- [ ] Define multi-step form wizard logic (step navigation, validation, state management)
- [ ] Define template selection logic (preview generation, template choice persistence)
- [ ] Define resume rendering logic (data binding, template inclusion, conditional display)
- [ ] Define form validation logic (client-side rules, error handling)
- [ ] Define data transformation logic (skills parsing, project filtering, text formatting)

### Phase 2: Domain Model Definition
- [ ] Define Profile entity (all 29 fields with types and constraints)
- [ ] Define FormStep entity (step number, fields, validation rules)
- [ ] Define ResumeTemplate entity (template ID, name, description, style)
- [ ] Define ValidationError entity (field, message, type)
- [ ] Define entity relationships and data flow

### Phase 3: Business Rules Specification
- [ ] Define required field rules (name, email, phone must be non-empty)
- [ ] Define email validation rules (format: xxx@xxx.xxx)
- [ ] Define URL validation rules (must start with http:// or https://)
- [ ] Define template selection rules (must choose one of three templates)
- [ ] Define form step progression rules (validate before next, no validation for back)
- [ ] Define data persistence rules (save on submit, update on re-submit)
- [ ] Define redirect rules (form → template selection → final resume)

### Phase 4: Frontend Component Design
- [ ] Define component hierarchy (pages, sections, form steps, buttons)
- [ ] Define component props and state (what data each component needs)
- [ ] Define user interaction flows (click, input, submit, navigate)
- [ ] Define form validation flows (validate on blur, on submit, show errors)
- [ ] Define API integration points (which routes each component calls)

### Phase 5: Data Flow Design
- [ ] Define form data flow (user input → validation → state → submission → database)
- [ ] Define template selection flow (user choice → preview → save → redirect)
- [ ] Define resume rendering flow (database → template → display)
- [ ] Define navigation flow (page transitions, redirects, back button)

### Phase 6: Error Handling Design
- [ ] Define validation error handling (show errors, prevent submission)
- [ ] Define database error handling (connection errors, save failures)
- [ ] Define navigation error handling (missing profile, invalid routes)
- [ ] Define JavaScript error handling (graceful degradation)

### Phase 7: Generate Artifacts
- [x] Generate business-logic-model.md (detailed business logic and algorithms)
- [ ] Generate domain-entities.md (entity definitions with fields and relationships)
- [ ] Generate business-rules.md (all business rules and validation logic)
- [ ] Generate frontend-components.md (component structure, props, state, interactions)

---

## Design Questions

Since you requested immediate execution ("NOW"), I'll proceed with reasonable design decisions based on requirements and best practices. However, if you'd like to provide input on any of these areas, please let me know:

### Business Logic Questions (Optional Input)

#### Question 1: Form Step Validation Timing
When should form step validation occur?

A) On blur (when user leaves a field)
B) On submit (when user clicks Next/Submit)
C) Both - on blur for immediate feedback + on submit for final check
D) Real-time (as user types)

**Default Decision**: C (Both - on blur + on submit) for best UX

---

#### Question 2: Form State Persistence
How should form state be persisted across steps?

A) In-memory JavaScript object only (lost on page refresh)
B) sessionStorage (persists during session, lost on browser close)
C) localStorage (persists across sessions)
D) Server-side session storage

**Default Decision**: B (sessionStorage) for balance of persistence and privacy

---

#### Question 3: Template Preview Data
What data should be shown in template preview?

A) User's actual data from form
B) Placeholder/sample data
C) Mix - user's data where available, placeholder for empty fields
D) User's data with option to toggle to sample data

**Default Decision**: C (Mix) for realistic preview while handling empty fields

---

#### Question 4: Skills Parsing Logic
How should skills text be parsed into individual skills?

A) Comma-separated only (e.g., "Python, JavaScript, SQL")
B) Newline-separated only (one skill per line)
C) Both - try comma first, fall back to newline
D) Smart parsing (detect delimiter automatically)

**Default Decision**: C (Both) for flexibility

---

#### Question 5: Empty Project/Certification Handling
How should empty projects or certifications be handled?

A) Show all 3 slots even if empty (with "Not provided" text)
B) Hide empty slots (only show filled ones)
C) Show empty slots in form, hide in resume
D) Require at least one project and one certification

**Default Decision**: B (Hide empty slots) for cleaner resume appearance

---

#### Question 6: Template Change Behavior
When user changes template, should form data be preserved?

A) Yes, always preserve all form data
B) Yes, but warn user before changing
C) No, reset form data when changing template
D) Preserve data but reset template-specific styling

**Default Decision**: A (Always preserve) - template is just presentation

---

#### Question 7: Navigation Guard
Should there be a warning when user tries to leave form with unsaved changes?

A) Yes, show browser confirmation dialog
B) Yes, show custom modal with save option
C) No, allow navigation without warning
D) Only warn on form page, not on other pages

**Default Decision**: C (No warning) for simplicity, form auto-saves on submit

---

#### Question 8: PDF Download Behavior
How should PDF download work?

A) Open print dialog immediately (window.print())
B) Show preview first, then print dialog
C) Generate PDF on server and download
D) Show instructions for saving as PDF

**Default Decision**: A (window.print()) for simplicity and browser compatibility

---

## Notes

- **Default decisions** are based on requirements, best practices, and beginner-friendly approach
- **User can override** any default decision by providing input
- **Functional design** will proceed with defaults unless user specifies otherwise
- **Business rules** will be comprehensive and cover all edge cases
- **Frontend components** will be detailed with props, state, and interactions

---

## Instructions

1. If you want to provide input on any design questions, please answer them
2. If you're satisfied with the default decisions, I'll proceed immediately
3. I'll generate comprehensive functional design artifacts based on requirements and defaults
4. You can request changes after reviewing the artifacts

**Ready to proceed with functional design generation using default decisions.**
