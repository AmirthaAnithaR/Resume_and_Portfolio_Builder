# Requirements Document: AI CV Builder Redesign

## Intent Analysis Summary

### User Request
Redesign the existing Resume + Portfolio Builder project into a professional AI CV Builder website with a premium landing page, multi-step form flow, template selection, and enhanced UI/UX. Update frontend and UI flow only while keeping backend/database compatible.

### Request Type
**Enhancement** - Major frontend redesign of existing application

### Scope Estimate
**Multiple Components** - Changes across multiple frontend components (templates, CSS, JavaScript) with minimal backend changes (new routes only)

### Complexity Estimate
**Moderate** - Clear implementation path with well-defined requirements, but involves multiple new pages, multi-step flow, and three distinct resume templates

---

## Project Overview

### Current State
- **Application**: Flask-based Resume + Portfolio Builder
- **Architecture**: MVC pattern with Flask + SQLite
- **Status**: Backend complete and tested (27/27 tests passing)
- **Issue**: Frontend incomplete (view.html is placeholder), basic UI, no landing page, no template selection

### Desired State
- **Professional AI CV Builder** with premium UI/UX
- **Multi-page flow**: Landing → Multi-step Form → Template Selection → Final Resume
- **Three resume templates**: Corporate Professional, Modern Developer, Creative Portfolio
- **Enhanced features**: Smooth transitions, responsive design, sticky navigation
- **Branding**: "My CV Creator" with white + navy + teal theme

### Redesign Scope
- ✅ **Frontend Only**: Templates, CSS, JavaScript
- ✅ **New Pages**: Landing page, template selection page
- ✅ **Enhanced Pages**: Form page (multi-step), resume view page
- ✅ **Backend**: Minimal changes (add new routes, optional database fields)
- ❌ **No Changes**: Core backend logic, database structure (mostly unchanged)

---

## Functional Requirements

### FR-01: Landing Page
**Priority**: High  
**Description**: Create a premium landing page as the entry point to the application

**Acceptance Criteria**:
- Display when user visits root URL (/)
- Include hero section with:
  - Main heading: "Welcome to My CV Creator"
  - Subheading: "Create a compelling CV with AI assistance in minutes."
  - Description: "Online resume builder with AI assistance. Seamlessly create an exceptional resume with smart formatting, professional templates, and personalized content."
  - Professional resume/document illustration or icon
  - Prominent "Get Started" button
- Include features section explaining "Why use our CV builder?"
- Include testimonials or sample resume examples
- Fully responsive design (mobile, tablet, desktop)
- Premium theme: white + navy + teal color scheme
- Sticky navigation bar with logo and links

**User Flow**:
```
User visits / → Landing page loads → User clicks "Get Started" → Navigate to form page
```

---

### FR-02: Multi-Step Form Flow
**Priority**: High  
**Description**: Transform the single-page form into a multi-step wizard with progress indication

**Acceptance Criteria**:
- Display form in multiple steps:
  - **Step 1**: Personal Information (name, email, phone, GitHub, LinkedIn)
  - **Step 2**: Education (education details)
  - **Step 3**: Skills (skills list)
  - **Step 4**: Projects (3 projects with title, description, URL)
  - **Step 5**: Certifications (3 certifications with name, org, year)
- Show progress indicator at top (e.g., "Step 1 of 5")
- Provide "Next" and "Back" buttons for navigation between steps
- Validate current step before allowing "Next"
- Show "Submit" button on final step
- Include "Back to Home" link in navigation
- Maintain clean, modern, mobile-responsive design
- Pre-populate form fields if profile exists (edit mode)

**User Flow**:
```
User clicks "Get Started" → Step 1 (Personal Info) → Next → Step 2 (Education) → Next → 
Step 3 (Skills) → Next → Step 4 (Projects) → Next → Step 5 (Certifications) → Submit → 
Navigate to template selection page
```

**Business Rules**:
- BR-01: Required fields (name, email, phone) must be validated before proceeding
- BR-02: Email must match valid format
- BR-03: URLs must start with http:// or https:// (if provided)
- BR-04: User can navigate back to previous steps without losing data
- BR-05: Form data persists across steps (client-side state management)

---

### FR-03: Template Selection Page
**Priority**: High  
**Description**: Allow users to choose from 3 professional resume templates after form submission

**Acceptance Criteria**:
- Display after form submission (POST /save completes)
- Show 3 resume templates side-by-side:
  - **Template 1**: Corporate Professional Resume (ATS-friendly)
  - **Template 2**: Modern Developer Resume
  - **Template 3**: Creative Portfolio Resume
- Display as cards with thumbnail previews (3 columns on desktop, stack on mobile)
- Each card shows:
  - Template preview (thumbnail with placeholder data)
  - Template name
  - Brief description
  - "Use Template" button
- Clicking template card shows modal with live preview using user's actual data
- Clicking "Use Template" button saves selection and navigates to final resume page
- Responsive design (mobile, tablet, desktop)
- Smooth transitions and hover effects

**User Flow**:
```
User submits form → Template selection page loads → User views thumbnails → 
User clicks template for preview → Modal shows live preview with user data → 
User clicks "Use Template" → Navigate to final resume page with selected template
```

**Business Rules**:
- BR-06: Template selection is required (no default template)
- BR-07: Template choice is saved with profile data
- BR-08: User can change template later from final resume page

---

### FR-04: Resume Template 1 - Corporate Professional
**Priority**: High  
**Description**: ATS-friendly resume template with conservative professional styling

**Acceptance Criteria**:
- **Design Style**: Conservative with navy/grey accents, subtle borders, professional fonts
- **Layout**: Single-column, clean sections, maximum readability
- **Sections**:
  - Header: Name, contact info (email, phone, GitHub, LinkedIn)
  - Education: Institution, degree, year
  - Skills: Listed format (not badges)
  - Projects: Title, description, URL (if provided)
  - Certifications: Name, organization, year
- **Color Scheme**: Navy (#1a3c5e) and grey accents on white background
- **Typography**: Professional sans-serif fonts (e.g., Arial, Helvetica)
- **ATS Compatibility**: Simple structure, no complex layouts, machine-readable
- **Responsive**: Optimized for mobile viewing, maintains all content
- **Print-Friendly**: Clean print layout via print.css

---

### FR-05: Resume Template 2 - Modern Developer
**Priority**: High  
**Description**: Modern resume template designed for developers with visual hierarchy

**Acceptance Criteria**:
- **Design Style**: Modern with skills badges and project cards
- **Layout**: Two-column or card-based layout
- **Sections**:
  - Header: Name, contact info with icons
  - Skills: Colored pills/badges for each skill (teal/navy theme)
  - Projects: Card format with:
    - Project title
    - Description
    - Tech stack tags (if skills mentioned in description)
    - Project URL link
  - Education: Compact format
  - Certifications: Timeline or list format
- **Color Scheme**: Navy + teal + white with accent colors for badges
- **Typography**: Modern sans-serif (e.g., Inter, Roboto)
- **Visual Elements**: Icons for sections, badges for skills, cards for projects
- **Responsive**: Optimized for mobile viewing, maintains all content
- **Print-Friendly**: Simplified layout for printing

---

### FR-06: Resume Template 3 - Creative Portfolio
**Priority**: High  
**Description**: Creative resume template with modern design and unique elements

**Acceptance Criteria**:
- **Design Style**: Balanced creativity - modern design with unique elements but still professional
- **Layout**: Asymmetric or grid-based layout with visual interest
- **Sections**:
  - Header: Large name, creative contact display
  - About/Summary: If provided (optional field)
  - Skills: Visual representation (badges, bars, or creative display)
  - Projects: Portfolio-style cards with emphasis on visual hierarchy
  - Education: Integrated into layout
  - Certifications: Creative timeline or badge display
- **Color Scheme**: Bold use of navy + teal + white with gradients or accents
- **Typography**: Mix of fonts (heading + body), modern and stylish
- **Visual Elements**: Unique section dividers, creative icons, visual hierarchy
- **Responsive**: Optimized for mobile viewing, maintains all content
- **Print-Friendly**: Simplified but maintains creative elements

---

### FR-07: Final Resume + Portfolio Page
**Priority**: High  
**Description**: Display the generated resume in selected template with portfolio section below

**Acceptance Criteria**:
- Display resume in user's selected template at top of page
- Display separate portfolio section below resume with:
  - Projects showcase (expanded view of projects)
  - Skills visualization
  - Certifications timeline
- Action buttons at top or bottom:
  - **Download as PDF**: Triggers browser print dialog (window.print())
  - **Edit Details**: Returns to form page (pre-populated)
  - **Change Template**: Returns to template selection page
  - **Share Link**: Generates shareable link (future: copy URL to clipboard)
- Sticky navigation bar with "My CV Creator" branding
- Responsive design (mobile, tablet, desktop)
- Smooth scroll between resume and portfolio sections

**User Flow**:
```
User selects template → Final page loads with resume + portfolio → 
User reviews content → User clicks action button (Download/Edit/Change Template/Share)
```

**Business Rules**:
- BR-09: If no profile exists and user visits /view directly, redirect to landing page
- BR-10: If profile exists and user visits /view directly, show resume with saved template
- BR-11: Download as PDF uses browser's print functionality with print.css
- BR-12: Edit Details preserves template selection
- BR-13: Share Link copies current page URL to clipboard (or shows URL)

---

### FR-08: Navigation System
**Priority**: Medium  
**Description**: Consistent sticky navigation across all pages

**Acceptance Criteria**:
- Sticky navigation bar on all pages
- Navigation includes:
  - Logo/Brand: "My CV Creator" (links to landing page)
  - Links: Home, View Resume, Edit (contextual based on profile state)
- Navigation styling:
  - Navy background with white text
  - Smooth transitions on hover
  - Hamburger menu on mobile
- Responsive design (mobile, tablet, desktop)
- Active page indicator (highlight current page)

**Navigation Behavior**:
- **Landing Page**: Show "Home" (active) and "View Resume" (if profile exists)
- **Form Page**: Show "Home" and "View Resume" (if profile exists)
- **Template Selection**: Show "Home" and "Back to Form"
- **Final Resume Page**: Show "Home", "Edit", and "Change Template"

---

### FR-09: Responsive Design
**Priority**: High  
**Description**: Ensure all pages and templates are fully responsive

**Acceptance Criteria**:
- **Breakpoints**:
  - Mobile: < 768px
  - Tablet: 768px - 1024px
  - Desktop: > 1024px
- **Mobile Optimizations**:
  - Single-column layouts
  - Hamburger navigation menu
  - Touch-friendly buttons (min 44px height)
  - Optimized font sizes
  - Stack template cards vertically
- **Tablet Optimizations**:
  - Two-column layouts where appropriate
  - Responsive navigation
  - Optimized spacing
- **Desktop Optimizations**:
  - Multi-column layouts
  - Full navigation bar
  - Hover effects
  - Optimal reading width (max-width containers)
- **Resume Templates**: Optimized for mobile viewing but maintain all content

---

### FR-10: Page Transitions and Animations
**Priority**: Medium  
**Description**: Smooth transitions and loading states for enhanced UX

**Acceptance Criteria**:
- **Page Transitions**: Modern SPA-style transitions (fade + slight movement)
- **Loading States**: Show progress indicators for multi-step processes:
  - Form step transitions
  - Template preview loading
  - Resume generation
- **Animations**:
  - Fade-in effects for page content
  - Smooth hover effects on buttons and cards
  - Slide-in effects for navigation menu (mobile)
  - Progress bar animation for form steps
- **Performance**: Animations should be smooth (60fps) and not block user interaction

---

### FR-11: Database Schema Updates (Optional)
**Priority**: Low  
**Description**: Add optional fields to support enhanced features

**Acceptance Criteria**:
- Keep existing 27 fields unchanged (backward compatibility)
- Add optional fields:
  - `template_choice` (TEXT): Stores selected template (template1, template2, template3)
  - `summary` (TEXT): Optional professional summary/objective
  - `profile_photo_url` (TEXT): Optional profile photo URL (future enhancement)
- Migration strategy: ALTER TABLE to add new columns with NULL defaults
- Existing data remains intact
- New fields are optional (NULL allowed)

**Business Rules**:
- BR-14: Existing profiles without template_choice default to template1
- BR-15: Summary field is optional and only shown if provided
- BR-16: Database operations (save, update, get) handle new fields gracefully

---

## Non-Functional Requirements

### NFR-01: Performance
**Priority**: High  
**Description**: Application should load quickly and respond smoothly

**Acceptance Criteria**:
- Page load time < 2 seconds on localhost
- Form step transitions < 300ms
- Template preview generation < 1 second
- Smooth animations (60fps)
- No blocking operations during user interaction

---

### NFR-02: Usability
**Priority**: High  
**Description**: Application should be intuitive and easy to use

**Acceptance Criteria**:
- Clear visual hierarchy on all pages
- Intuitive navigation (users understand flow without instructions)
- Helpful error messages for validation failures
- Progress indication for multi-step processes
- Consistent UI patterns across pages
- Accessible form labels and ARIA attributes
- Keyboard navigation support

---

### NFR-03: Browser Compatibility
**Priority**: High  
**Description**: Application should work on modern browsers

**Acceptance Criteria**:
- **Supported Browsers**:
  - Chrome 90+ ✅
  - Firefox 88+ ✅
  - Safari 14+ ✅
  - Edge 90+ ✅
- **Required Features**:
  - CSS Grid and Flexbox
  - CSS Custom Properties
  - ES6 JavaScript
  - HTML5 form validation
- **Graceful Degradation**: Basic functionality works on older browsers

---

### NFR-04: Maintainability
**Priority**: Medium  
**Description**: Code should be clean, documented, and easy to maintain

**Acceptance Criteria**:
- Consistent code style (existing project conventions)
- Inline comments for complex logic
- Modular CSS (organized by component/page)
- Reusable JavaScript functions
- Clear file organization
- Beginner-friendly code (as specified in original request)

---

### NFR-05: Accessibility
**Priority**: Medium  
**Description**: Application should be accessible to users with disabilities

**Acceptance Criteria**:
- Semantic HTML elements
- Form labels associated with inputs
- ARIA attributes for dynamic content
- Keyboard navigation support
- Sufficient color contrast (WCAG AA)
- Focus indicators on interactive elements
- Alt text for images/icons

---

### NFR-06: Backend Compatibility
**Priority**: High  
**Description**: Maintain compatibility with existing Flask backend

**Acceptance Criteria**:
- Keep existing routes functional (/, /save, /view)
- Add new routes without breaking existing functionality:
  - GET /landing (optional, or use / for landing)
  - GET /form (or keep / for form after landing)
  - GET /select-template (template selection page)
  - POST /save-template (save template choice)
- Database schema changes are additive only (no breaking changes)
- Existing tests continue to pass (27/27)
- No changes to database.py core functions

---

## Technical Constraints

### TC-01: Technology Stack
- **Backend**: Python 3.x + Flask 3.0.3 (unchanged)
- **Database**: SQLite 3.x (unchanged)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript (no frameworks)
- **Template Engine**: Jinja2 (unchanged)
- **No New Dependencies**: Keep requirements.txt minimal (Flask only)

### TC-02: File Structure
- **Backend Files**: Minimal changes to app.py, no changes to database.py
- **Frontend Files**: Update/create templates and static assets
- **New Files**:
  - templates/landing.html
  - templates/form-step.html (or modify index.html)
  - templates/template-selection.html
  - templates/resume-template1.html
  - templates/resume-template2.html
  - templates/resume-template3.html
  - static/js/form-wizard.js (multi-step logic)
  - static/js/template-preview.js (preview functionality)

### TC-03: Development Environment
- **Local Development**: Flask development server (localhost:5000)
- **No Build Step**: Pure Python/HTML/CSS/JS (no compilation)
- **Testing**: Pytest for backend, manual testing for frontend

---

## User Stories (High-Level)

### US-01: First-Time User Journey
**As a** first-time user  
**I want to** see a professional landing page explaining the CV builder  
**So that** I understand what the application does and feel confident using it

**Acceptance Criteria**:
- Landing page loads when visiting root URL
- Clear value proposition and features explained
- "Get Started" button is prominent and clickable
- Smooth transition to form page

---

### US-02: Create Resume with Guided Flow
**As a** user  
**I want to** fill out my information in a step-by-step wizard  
**So that** the process feels manageable and not overwhelming

**Acceptance Criteria**:
- Form is divided into 5 clear steps
- Progress indicator shows current step
- Can navigate back to previous steps
- Validation prevents proceeding with invalid data
- Form data persists across steps

---

### US-03: Choose Resume Template
**As a** user  
**I want to** preview and select from multiple resume templates  
**So that** I can choose a design that matches my style and career field

**Acceptance Criteria**:
- 3 distinct templates are shown with previews
- Can click to see full preview with my data
- Can select template and proceed to final resume
- Template choice is saved with my profile

---

### US-04: View and Download Resume
**As a** user  
**I want to** view my generated resume and download it as PDF  
**So that** I can use it for job applications

**Acceptance Criteria**:
- Resume displays in selected template
- Portfolio section shows projects and skills
- Download button triggers print dialog
- Can edit details or change template
- Can share link to resume

---

### US-05: Edit Existing Resume
**As a** returning user  
**I want to** edit my existing resume information  
**So that** I can keep my resume up-to-date

**Acceptance Criteria**:
- Form pre-populates with existing data
- Can navigate through steps and update information
- Template selection remembers previous choice
- Changes are saved and reflected in resume view

---

## Out of Scope (Future Enhancements)

The following features are explicitly **NOT** included in this redesign:

- ❌ **AI Integration**: No actual AI features (OpenAI API, content suggestions, resume review)
- ❌ **Authentication**: No user login, registration, or multi-user support
- ❌ **Multiple Profiles**: No support for multiple resume versions per user
- ❌ **Server-Side PDF Generation**: No WeasyPrint or ReportLab integration
- ❌ **Dynamic Projects/Certifications**: No ability to add more than 3 projects/certifications
- ❌ **Theme Customization**: No user-selectable color themes
- ❌ **Profile Photos**: No image upload functionality
- ❌ **Social Sharing**: No social media integration
- ❌ **Analytics**: No usage tracking or analytics
- ❌ **Email Export**: No email sending functionality
- ❌ **Cloud Storage**: No cloud backup or sync

---

## Success Criteria

The redesign will be considered successful when:

1. ✅ **Landing Page**: Professional landing page with hero section, features, and testimonials
2. ✅ **Multi-Step Form**: Form wizard with 5 steps and progress indication
3. ✅ **Template Selection**: 3 distinct resume templates with preview functionality
4. ✅ **Final Resume**: Resume + portfolio page with download, edit, and share options
5. ✅ **Responsive Design**: Fully responsive on mobile, tablet, and desktop
6. ✅ **Smooth Transitions**: Modern page transitions and loading states
7. ✅ **Premium UI/UX**: White + navy + teal theme, professional appearance
8. ✅ **Backend Compatible**: Existing backend works with minimal changes
9. ✅ **Tests Pass**: All existing tests continue to pass (27/27)
10. ✅ **Beginner-Friendly**: Code is clean, documented, and easy to understand

---

## Extension Configuration

### Security Baseline Extension
**Status**: ❌ Disabled  
**Rationale**: This is a learning/prototype project, not production-grade. Security rules are not enforced.

### Property-Based Testing Extension
**Status**: ❌ Disabled  
**Rationale**: This is a simple CRUD application with UI focus. Property-based testing rules are not enforced.

---

## Requirements Summary

This redesign transforms the Resume + Portfolio Builder into a professional AI CV Builder with:

- **4 new pages**: Landing, multi-step form, template selection, enhanced resume view
- **3 resume templates**: Corporate Professional, Modern Developer, Creative Portfolio
- **Enhanced UX**: Multi-step wizard, smooth transitions, responsive design, premium theme
- **Minimal backend changes**: New routes, optional database fields, existing logic unchanged
- **No new dependencies**: Pure HTML/CSS/JS, Flask + SQLite only

The focus is on creating a polished, professional frontend experience while maintaining full backend compatibility and keeping the codebase beginner-friendly.
