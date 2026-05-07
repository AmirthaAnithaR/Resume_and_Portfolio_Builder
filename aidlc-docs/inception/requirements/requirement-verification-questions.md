# Requirements Verification Questions

Please answer the following questions to clarify the requirements for the AI CV Builder redesign. Fill in your answer after each [Answer]: tag using the letter choice (A, B, C, D, etc.) or provide a custom response for option X.

---

## Section 1: Landing Page Requirements

### Question 1
What should happen when a user visits the root URL (/) for the first time?

A) Show the landing page with "Get Started" button
B) Show the form directly (skip landing page)
C) Show a login/authentication page first
D) Show a dashboard with multiple options
X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 2
Should the landing page include any additional sections beyond the hero section (heading, subheading, description, "Get Started" button)?

A) No, keep it minimal - just hero section with "Get Started" button
B) Yes, add features section (e.g., "Why use our CV builder?")
C) Yes, add testimonials or sample resumes
D) Yes, add both features section and examples/testimonials
X) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 3
What should the landing page illustration/icon represent?

A) Professional resume/document icon
B) AI/technology theme (robot, brain, sparkles)
C) Career success theme (briefcase, trophy, growth chart)
D) Abstract modern design (geometric shapes, gradients)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Section 2: Form Page Flow

### Question 4
After clicking "Get Started" on the landing page, should the form page:

A) Show all form sections at once (current behavior - single page form)
B) Show form sections in a multi-step wizard (Step 1: Personal Info, Step 2: Education, etc.)
C) Show a progress indicator but keep all sections visible (scroll-based)
D) Show sections one at a time with "Next" buttons (accordion style)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 5
Should the form page have a "Back to Home" or "Cancel" option?

A) Yes, add a "Back to Home" link in the navigation
B) Yes, add a "Cancel" button that shows a confirmation dialog
C) No, users should complete the form or use browser back button
D) Yes, add both navigation link and cancel button
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Section 3: Template Selection

### Question 6
When should the template selection page appear?

A) After form submission (as specified in your request)
B) Before filling the form (user chooses template first, then fills form)
C) Both - preview before form, confirm after form submission
D) Make it optional - provide a default template and allow users to change later
X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 7
How should the 3 resume templates be displayed on the template selection page?

A) Side-by-side cards with thumbnail previews (3 columns on desktop, stack on mobile)
B) Vertical list with larger previews (one per row)
C) Carousel/slider format (one template visible at a time, swipe to see others)
D) Grid with modal popup for full preview when clicked
X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 8
Should users be able to preview the template with their actual data before selecting?

A) Yes, show live preview with their entered data
B) No, show generic placeholder data in template previews
C) Yes, but only show a quick preview modal when hovering/clicking
D) Provide both - thumbnail with placeholder, click for live preview
X) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Section 4: Resume Templates Design

### Question 9
For Template 1 (Corporate Professional Resume - ATS-friendly), what level of visual styling should it have?

A) Minimal - black text on white, simple lines, no colors (maximum ATS compatibility)
B) Conservative - navy/grey accents, subtle borders, professional fonts
C) Balanced - some color accents (navy/teal), icons for sections, modern but clean
D) Let me see options and choose during design phase
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 10
For Template 2 (Modern Developer Resume), should it include:

A) Skills badges only (colored pills/tags for each skill)
B) Project cards with tech stack tags
C) Both skills badges and project cards with visual hierarchy
D) Skills badges, project cards, and GitHub contribution graph/stats
X) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 11
For Template 3 (Creative Portfolio Resume), how creative should the layout be?

A) Moderately creative - asymmetric layout, bold colors, unique typography
B) Highly creative - unconventional sections, artistic elements, standout design
C) Balanced creativity - modern design with some unique elements but still professional
D) Let me see options and choose during design phase
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Section 5: Final Resume + Portfolio Page

### Question 12
After selecting a template, what should the final page display?

A) Only the resume in the selected template
B) Resume + separate portfolio section below (two distinct sections on same page)
C) Tabbed interface (Resume tab, Portfolio tab)
D) Resume with portfolio projects integrated into the resume layout
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 13
What actions should be available on the final resume page?

A) Download as PDF only
B) Download as PDF + Edit Details (go back to form)
C) Download as PDF + Edit Details + Change Template
D) Download as PDF + Edit Details + Change Template + Share Link
X) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 14
For the "Download as PDF" feature, should it:

A) Use browser's print-to-PDF (window.print() with print.css)
B) Generate PDF on server-side (requires new Python library like WeasyPrint)
C) Provide both options (Quick Print + High-Quality PDF)
D) Just provide print option for now, PDF generation can be added later
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Section 6: Navigation and User Flow

### Question 15
Should there be a persistent navigation bar on all pages?

A) Yes, sticky navigation on all pages with logo and links (Home, View Resume, Edit)
B) Yes, but minimal on landing page, full navigation on other pages
C) No, use contextual navigation (buttons/links specific to each page)
D) Yes, sticky navigation with additional features (theme toggle, help, etc.)
X) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 16
If a user visits /view directly (without going through the flow), what should happen?

A) Redirect to landing page if no profile exists, show resume if profile exists (current behavior)
B) Always redirect to landing page to enforce the flow
C) Show a "Get Started" prompt on the view page if no profile exists
D) Show the form page directly if no profile exists
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Section 7: Responsive Design and Transitions

### Question 17
For mobile responsiveness, should the resume templates:

A) Use the same layout as desktop, just scaled down
B) Have a simplified mobile-specific layout (single column, reduced sections)
C) Be optimized for mobile viewing but maintain all content
D) Provide a mobile-optimized view with option to see desktop version
X) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 18
What type of page transitions do you want between pages?

A) Instant navigation (no transitions, standard page loads)
B) Fade in/out transitions (smooth opacity changes)
C) Slide transitions (pages slide in from right/left)
D) Modern SPA-style transitions (fade + slight movement)
X) Other (please describe after [Answer]: tag below)

[Answer]: D

### Question 19
Should there be loading states or animations when:

A) No loading states needed (pages load instantly on localhost)
B) Show loading spinner when generating resume preview
C) Show skeleton screens while content loads
D) Show progress indicators for multi-step processes
X) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Section 8: AI Assistance Features

### Question 20
You mentioned "AI assistance" in the description. What AI features should be included in this redesign?

A) No actual AI features yet - just branding/messaging about AI assistance
B) AI-powered content suggestions (requires OpenAI API integration)
C) AI resume review/feedback (requires AI integration)
D) AI features are future enhancement - focus on UI/UX redesign first
X) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Section 9: Color Theme and Branding

### Question 21
You specified "white + navy + teal premium theme". Should this color scheme:

A) Be applied consistently across all pages and templates
B) Be used for the app interface, but templates can have their own color schemes
C) Be the primary theme with option for users to customize colors
D) Include additional accent colors beyond navy and teal
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 22
What should the application name/branding be?

A) "My CV Creator" (as specified in your request)
B) "AI CV Builder" (as mentioned in your request)
C) "Resume + Portfolio Builder" (current name)
D) Let me decide during design phase
X) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Section 10: Data and Backend Compatibility

### Question 23
Should the existing database schema (27 fields: personal info, education, skills, 3 projects, 3 certifications) remain unchanged?

A) Yes, keep exactly as-is (backend compatibility requirement)
B) Yes, but add optional fields if needed (e.g., summary, objective)
C) Modify schema to support more projects/certifications (dynamic lists)
D) Keep schema but add new table for template preferences
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 24
Should the application support multiple resume versions or profiles?

A) No, keep single-user, single-profile design (current behavior)
B) Yes, allow multiple resume versions (e.g., "Software Engineer Resume", "Data Analyst Resume")
C) Yes, allow saving different template choices for the same data
D) Future enhancement - keep single profile for now
X) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Section 11: Extension Configuration

### Question 25: Security Extensions
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)
B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)
X) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 26: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)
B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)
C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)
X) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Instructions

1. Please fill in your answer for each question using the letter choice (A, B, C, D, or X)
2. If you choose X (Other), provide a detailed description after the [Answer]: tag
3. Once you've answered all questions, let me know and I'll analyze your responses
4. I may ask follow-up questions if any answers need clarification

**Note**: Your answers will help me create a detailed requirements document that ensures the redesign meets your exact vision.
