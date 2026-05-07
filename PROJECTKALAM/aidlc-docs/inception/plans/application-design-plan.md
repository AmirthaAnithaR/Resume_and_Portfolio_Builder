# Application Design Plan: AI CV Builder

## Overview
This plan outlines the application design for the AI CV Builder redesign, focusing on component identification, responsibilities, methods, services, and dependencies.

## Design Scope
- **Frontend Components**: Landing page, multi-step form wizard, template selection, three resume templates, navigation system
- **Backend Components**: Route handlers, template rendering, optional database schema updates
- **Service Layer**: Form state management, template selection logic, resume rendering service

---

## Design Questions

Please answer the following questions to guide the application design. Fill in your answer after each [Answer]: tag.

### Section 1: Component Organization

#### Question 1: Page Component Structure
How should the page components be organized?

A) Each page as a separate Jinja2 template with shared base template (template inheritance)
B) Modular components with includes ({% include %}) for reusable sections
C) Both - base template inheritance + includes for shared components (nav, footer, form sections)
D) Single-page application approach with JavaScript-driven view switching

[Answer]: C

#### Question 2: Form Step Components
How should the multi-step form be structured?

A) Single template with JavaScript showing/hiding steps (client-side only)
B) Separate template for each step with server-side navigation
C) Single template with step components as Jinja2 macros
D) Hybrid - single template with JavaScript step management + server-side validation

[Answer]: D

#### Question 3: Resume Template Components
How should the three resume templates be organized?

A) Three completely separate template files (no shared code)
B) Base resume template with template-specific overrides (template inheritance)
C) Shared component library with template-specific layouts
D) Single template with conditional rendering based on template choice

[Answer]: B

---

### Section 2: Component Methods and Responsibilities

#### Question 4: Form State Management
Where should the multi-step form state be managed?

A) Client-side only (JavaScript object in memory)
B) Client-side with sessionStorage/localStorage persistence
C) Server-side session storage
D) Hybrid - client-side for UX + server-side for validation

[Answer]: D

#### Question 5: Template Preview Logic
How should the template preview functionality work?

A) Generate full HTML preview on server, send to client
B) Client-side JavaScript renders preview from form data
C) Server-side API endpoint returns preview HTML fragment
D) Pre-rendered thumbnails + modal with live preview on demand

[Answer]: D

#### Question 6: Navigation State Management
How should navigation state (current page, active link) be managed?

A) Server-side - Flask passes current page to template
B) Client-side - JavaScript detects current URL and updates nav
C) Both - server sets initial state, client handles interactions
D) URL-based - CSS :target or JavaScript URL parsing

[Answer]: C

---

### Section 3: Service Layer Design

#### Question 7: Resume Rendering Service
Should there be a dedicated service for resume rendering?

A) Yes - separate ResumeRenderer service class with render() method
B) No - render logic directly in Flask route handlers
C) Partial - helper functions in a utils module
D) Template-based - all logic in Jinja2 templates with filters

[Answer]: C

#### Question 8: Form Validation Service
How should form validation be organized?

A) Client-side only (JavaScript validation in form.js)
B) Server-side only (Python validation in app.py)
C) Both - client-side for UX + server-side for security
D) Shared validation rules (JSON schema or similar) used by both client and server

[Answer]: C

#### Question 9: Template Selection Service
Should template selection logic be centralized?

A) Yes - TemplateSelector service handles selection, preview, and rendering
B) No - logic distributed across route handlers
C) Partial - helper functions for template mapping and data binding
D) Configuration-driven - template metadata in JSON/dict, generic renderer

[Answer]: D

---

### Section 4: Component Dependencies

#### Question 10: Template-to-Backend Dependency
How should templates depend on backend data?

A) Direct - templates expect specific data structure from Flask
B) Adapter pattern - backend adapts data to template-specific format
C) View models - dedicated data classes for each template
D) Flexible - templates handle missing/optional data gracefully

[Answer]: D

#### Question 11: JavaScript-to-Backend Communication
How should JavaScript communicate with backend for dynamic features?

A) Form submissions only (no AJAX/fetch)
B) AJAX/fetch for specific features (template preview, validation)
C) RESTful API endpoints for all dynamic interactions
D) Minimal - prefer full page reloads over AJAX

[Answer]: B

#### Question 12: CSS-to-Component Coupling
How should CSS be organized relative to components?

A) Single global stylesheet (style.css) for all components
B) Component-specific stylesheets (landing.css, form.css, etc.)
C) Hybrid - global base styles + component-specific overrides
D) Utility-first approach (similar to Tailwind, but custom)

[Answer]: C

---

### Section 5: Design Patterns and Architecture

#### Question 13: Backend Routing Pattern
How should new routes be organized in app.py?

A) Flat structure - all routes in app.py
B) Blueprint pattern - group related routes (landing_bp, form_bp, etc.)
C) Class-based views - route handlers as class methods
D) Keep flat for simplicity (beginner-friendly requirement)

[Answer]: D

#### Question 14: Data Access Pattern
Should database access be modified?

A) Keep existing pattern (database.py functions)
B) Add repository pattern with classes
C) Add ORM (SQLAlchemy) for better abstraction
D) Keep existing + add helper functions for new fields

[Answer]: D

#### Question 15: Error Handling Pattern
How should errors be handled across the application?

A) Try-except in route handlers, render error template
B) Flask error handlers (@app.errorhandler)
C) Custom error middleware
D) Minimal - let Flask default error handling work

[Answer]: B

---

## Application Design Execution Plan

Once questions are answered, execute the following steps:

### Phase 1: Component Identification
- [ ] Identify all page components (landing, form, template selection, resume templates, final resume)
- [ ] Identify shared components (navigation, footer, form sections)
- [ ] Identify backend components (route handlers, services, utilities)
- [ ] Document component responsibilities and boundaries

### Phase 2: Component Methods Definition
- [ ] Define route handler methods (GET/POST for each page)
- [ ] Define service methods (form validation, template rendering, state management)
- [ ] Define utility methods (data formatting, template selection, preview generation)
- [ ] Document method signatures and high-level purpose

### Phase 3: Service Layer Design
- [ ] Design form state management service (if needed)
- [ ] Design template rendering service (if needed)
- [ ] Design validation service (if needed)
- [ ] Document service responsibilities and interactions

### Phase 4: Component Dependencies
- [ ] Map template-to-backend dependencies
- [ ] Map JavaScript-to-backend dependencies
- [ ] Map CSS-to-component dependencies
- [ ] Create dependency matrix and communication patterns

### Phase 5: Design Validation
- [ ] Verify all components have clear responsibilities
- [ ] Verify no circular dependencies
- [ ] Verify design supports all functional requirements (FR-01 to FR-11)
- [ ] Verify design is beginner-friendly (maintainability requirement)

### Phase 6: Generate Design Artifacts
- [ ] Generate components.md (component definitions and responsibilities)
- [ ] Generate component-methods.md (method signatures and purposes)
- [ ] Generate services.md (service definitions and orchestration)
- [ ] Generate component-dependency.md (dependency relationships and patterns)
- [ ] Generate application-design.md (consolidated design document)

---

## Instructions

1. Please answer all questions (Question 1-15) by filling in the letter choice after each [Answer]: tag
2. If you have additional design preferences not covered by the options, add them after your answer
3. Once you've answered all questions, let me know and I'll analyze your responses
4. I may ask follow-up questions if any answers need clarification
5. After all questions are resolved, I'll execute the design plan and generate the artifacts

**Note**: Your answers will guide the component structure, service layer design, and overall architecture of the redesigned application.
