# Requirements Verification Questions - Resume Versions & Advanced Customization

**Purpose**: Clarify requirements for implementing Resume Version Management and Advanced Customization features

**Instructions**: Please answer all questions by filling in the `[Answer]:` tag with your choice (A, B, C, D, or X for custom response). For questions requiring additional details, provide them after the answer tag.

---

## FEATURE 1: RESUME VERSIONS & MANAGEMENT

### Version Management Core

**Q1: How many resume versions should a user be able to create?**
- A) Unlimited versions (no limit)
- B) Limited to 5 versions per user
- C) Limited to 10 versions per user
- D) Limited to 3 versions (free tier) with option to upgrade
- X) Other (please specify)

[Answer]:5

---

**Q2: What information should be stored for each resume version?**
- A) Complete copy of all profile data (name, email, education, skills, projects, certifications, template choice)
- B) Only differences from the "master" profile (delta storage)
- C) Complete profile data + metadata (version name, description, target job/company, creation date, last modified)
- D) Complete profile data + metadata + tags/categories for organization
- X) Other (please specify)

[Answer]:a

---

**Q3: Should users be able to name/label their resume versions?**
- A) Yes, required - each version must have a unique name (e.g., "Software Engineer Resume", "Data Analyst Resume")
- B) Yes, optional - users can optionally name versions, otherwise auto-generate names (e.g., "Resume Version 1", "Resume Version 2")
- C) No - use auto-generated names only with timestamps
- D) Yes, with both name and description fields
- X) Other (please specify)

[Answer]:c

---

**Q4: How should the "default" or "active" resume be determined?**
- A) User explicitly marks one version as "default" (shown when visiting /view without version ID)
- B) Most recently modified version is automatically the default
- C) Most recently created version is the default
- D) No default concept - user must always select a version explicitly
- X) Other (please specify)

[Answer]:a

---

### Version History & Change Tracking

**Q5: Should the system track version history (changes over time to a single resume version)?**
- A) Yes - full history tracking with ability to revert to any previous state (like Git commits)
- B) Yes - limited history (keep last 5 changes only)
- C) Yes - track creation and last modified timestamps only (no detailed change history)
- D) No - each "version" is independent, no history within a version
- X) Other (please specify)

[Answer]:b

---

**Q6: If history tracking is enabled (Q5 = A or B), what should be tracked?**
- A) Automatic snapshots on every save
- B) Manual snapshots - user clicks "Save Snapshot" to create a restore point
- C) Automatic snapshots + change descriptions (user provides description of what changed)
- D) Detailed field-level change tracking (show which fields changed, old vs new values)
- X) Other (please specify)

[Answer]:a

---

**Q7: Should users be able to compare two resume versions side-by-side?**
- A) Yes - visual diff showing what's different between two versions (highlight changes)
- B) Yes - simple side-by-side view without highlighting differences
- C) No - users can view versions separately but no comparison feature
- D) Yes - with A/B testing metrics (track which version performs better)
- X) Other (please specify)

[Answer]:a

---

### Clone & Duplicate

**Q8: How should the "Clone Resume" feature work?**
- A) Create exact duplicate with auto-generated name (e.g., "Copy of Software Engineer Resume")
- B) Create duplicate and immediately prompt user to edit name and description
- C) Create duplicate and open in edit mode so user can modify before saving
- D) Clone with options: copy everything, or copy only selected sections
- X) Other (please specify)

[Answer]:a

---

### Archive & Delete

**Q9: Should there be an "Archive" feature separate from "Delete"?**
- A) Yes - Archive hides versions from main list but keeps them recoverable; Delete permanently removes
- B) No - Only "Delete" with confirmation dialog
- C) Yes - Archive only (no permanent delete option for safety)
- D) Yes - Archive + soft delete (deleted items go to "Trash" for 30 days before permanent deletion)
- X) Other (please specify)

[Answer]:a

---

**Q10: What should happen when a user tries to delete their only remaining resume version?**
- A) Allow deletion (user can create new resume later)
- B) Prevent deletion with error message "You must have at least one resume version"
- C) Allow deletion but automatically create a blank template
- D) Warn user but allow deletion if they confirm
- X) Other (please specify)

[Answer]:a

---

### Version Management UI

**Q11: Where should users manage their resume versions?**
- A) New "My Resumes" dashboard page listing all versions with actions (view, edit, clone, delete)
- B) Dropdown menu in navigation bar to switch between versions
- C) Both A and B - dashboard for management + dropdown for quick switching
- D) Modal/popup accessible from any page
- X) Other (please specify)

[Answer]:a and b

---

**Q12: What information should be displayed in the resume versions list?**
- A) Version name, template choice, last modified date, actions (view/edit/clone/delete)
- B) Version name, thumbnail preview, template choice, creation date, last modified date, actions
- C) Version name, description, target job/company, template choice, dates, tags, actions
- D) Minimal - just version name and actions
- X) Other (please specify)

[Answer]:a

---

---

## FEATURE 2: ADVANCED CUSTOMIZATION

### Color Theme Selector

**Q13: How many color themes should be available?**
- A) 5 pre-defined themes (e.g., Navy Blue, Forest Green, Burgundy, Charcoal, Teal)
- B) 10 pre-defined themes covering various professional colors
- C) 3 pre-defined themes + custom color picker (user can choose any color)
- D) Unlimited - full custom color picker for primary, secondary, and accent colors
- X) Other (please specify)

[Answer]:

---

**Q14: Should color themes be applied per resume version or globally?**
- A) Per resume version - each version can have its own color theme
- B) Globally - one color theme applies to all resume versions
- C) Per template - each template (Corporate, Modern, Creative) has its own theme
- D) Hybrid - default global theme, but can override per version
- X) Other (please specify)

[Answer]:

---

**Q15: What elements should be affected by the color theme?**
- A) Only resume content (headings, section dividers, skill badges)
- B) Resume content + navigation bar
- C) Resume content + navigation bar + buttons and UI elements
- D) Everything - full application theming including landing page, forms, etc.
- X) Other (please specify)

[Answer]:

---

### Font Selector

**Q16: How many font combinations should be available?**
- A) 3 professional font pairings (e.g., Arial/Helvetica, Roboto/Open Sans, Georgia/Times)
- B) 5 font pairings covering different styles (modern, classic, creative)
- C) 10+ font pairings with preview
- D) Custom font selector - user can choose any Google Font
- X) Other (please specify)

[Answer]:

---

**Q17: Should font selection be separate for headings and body text?**
- A) Yes - separate selectors for heading font and body font
- B) No - pre-defined pairings only (heading + body together)
- C) Yes - separate selectors + font size controls
- D) Advanced - separate selectors for headings, subheadings, body, and captions
- X) Other (please specify)

[Answer]:

---

**Q18: Should font choices be applied per resume version or globally?**
- A) Per resume version - each version can have its own fonts
- B) Globally - one font choice applies to all versions
- C) Per template - each template has its own font settings
- D) Hybrid - default global fonts, but can override per version
- X) Other (please specify)

[Answer]:

---

### Section Reordering

**Q19: Which sections should be reorderable?**
- A) All sections (Education, Skills, Projects, Certifications)
- B) Only main content sections (Education, Skills, Projects, Certifications) - Personal Info always stays at top
- C) All sections including Personal Info
- D) Predefined layouts only (no custom reordering)
- X) Other (please specify)

[Answer]:

---

**Q20: How should the drag-and-drop reordering interface work?**
- A) Drag handles on each section - click and drag to reorder
- B) Up/Down arrow buttons to move sections
- C) Both drag-and-drop and arrow buttons
- D) Visual editor with live preview as you reorder
- X) Other (please specify)

[Answer]:

---

**Q21: Should section order be saved per resume version or globally?**
- A) Per resume version - each version can have different section order
- B) Globally - one section order applies to all versions
- C) Per template - each template has its own default order
- D) Hybrid - default global order, but can override per version
- X) Other (please specify)

[Answer]:

---

### Custom Sections

**Q22: What custom sections should be supported?**
- A) Awards, Publications, Languages, Hobbies
- B) Awards, Publications, Languages, Hobbies, Volunteer Work, Professional Memberships
- C) Pre-defined list (A or B) + ability to create completely custom sections with custom names
- D) Unlimited custom sections - user can add any section with any name and content
- X) Other (please specify)

[Answer]:

---

**Q23: What data structure should custom sections use?**
- A) Simple text area (free-form text)
- B) Structured fields similar to Projects (title, description, date, URL)
- C) Flexible - user chooses between text area or structured fields when creating section
- D) Rich text editor with formatting (bold, italic, lists, links)
- X) Other (please specify)

[Answer]:

---

**Q24: Should custom sections have icons?**
- A) Yes - user selects from icon library when creating section
- B) Yes - auto-assign icons based on section name
- C) No - text labels only
- D) Optional - user can choose icon or leave blank
- X) Other (please specify)

[Answer]:

---

### Profile Photo Upload

**Q25: Where should the profile photo be displayed?**
- A) In resume header (top of resume, next to name and contact info)
- B) In resume header + portfolio section
- C) Optional per template - some templates show photo, others don't
- D) User chooses where to display photo (header, sidebar, or hidden)
- X) Other (please specify)

[Answer]:

---

**Q26: What file upload requirements should be enforced?**
- A) Image files only (JPG, PNG), max 2MB, minimum 200x200px
- B) Image files only (JPG, PNG, GIF), max 5MB, minimum 300x300px
- C) Image files with automatic cropping to square aspect ratio
- D) Image files with crop/resize tool before upload
- X) Other (please specify)

[Answer]:

---

**Q27: Should profile photos be stored per resume version or globally?**
- A) Per resume version - each version can have different photo (or no photo)
- B) Globally - one photo applies to all versions
- C) Hybrid - default global photo, but can override per version
- D) Multiple photos in library - user selects which photo to use per version
- X) Other (please specify)

[Answer]:

---

### Logo/Branding

**Q28: What type of logo/branding should be supported?**
- A) Personal logo image upload (similar to profile photo)
- B) Text-based personal brand (e.g., initials or name in stylized format)
- C) Both image logo and text-based branding
- D) No logo feature (focus on profile photo only)
- X) Other (please specify)

[Answer]:

---

**Q29: Where should the logo/branding be displayed?**
- A) Resume header (top corner or next to name)
- B) Resume footer (bottom of each page)
- C) Both header and footer
- D) User chooses placement (header, footer, or hidden)
- X) Other (please specify)

[Answer]:

---

### Customization UI/UX

**Q30: How should users access customization options?**
- A) Dedicated "Customize" page with all options (colors, fonts, sections, photo, logo)
- B) Inline editing - customize directly on the resume view page
- C) Settings panel/sidebar that slides in from the side
- D) Step-by-step wizard for customization
- X) Other (please specify)

[Answer]:

---

**Q31: Should there be a "Preview" mode before applying customizations?**
- A) Yes - live preview as user makes changes (real-time updates)
- B) Yes - preview button to see changes before saving
- C) No - changes apply immediately
- D) Yes - side-by-side preview (original vs customized)
- X) Other (please specify)

[Answer]:

---

**Q32: Should customization settings be exportable/importable?**
- A) Yes - export theme settings as JSON file, import to apply to other versions
- B) Yes - "Copy settings from another version" feature
- C) No - manual customization only
- D) Yes - both export/import and copy from version
- X) Other (please specify)

[Answer]:

---

---

## TECHNICAL & IMPLEMENTATION QUESTIONS

### Database Schema

**Q33: How should resume versions be stored in the database?**
- A) New table `resume_versions` with foreign key to `users` table, stores complete profile data per version
- B) Keep existing `profile` table as "master", new `resume_versions` table stores only differences
- C) New table `resume_versions` + new table `version_history` for change tracking
- D) Completely restructure - make current `profile` table into `resume_versions` with version_id
- X) Other (please specify)

[Answer]:

---

**Q34: How should customization settings be stored?**
- A) New columns in `resume_versions` table (color_theme, font_choice, section_order, etc.)
- B) New table `customization_settings` with foreign key to `resume_versions`
- C) JSON blob column in `resume_versions` table for flexible settings storage
- D) Separate tables for each customization type (themes, fonts, sections, etc.)
- X) Other (please specify)

[Answer]:

---

**Q35: How should file uploads (photos, logos) be handled?**
- A) Store files in `static/uploads/` directory, store file paths in database
- B) Store files in `static/uploads/user_{id}/` directory (per-user folders)
- C) Convert images to base64 and store directly in database
- D) Use cloud storage (AWS S3, Cloudinary) for file storage
- X) Other (please specify)

[Answer]:

---

### URL Structure

**Q36: How should URLs be structured for resume versions?**
- A) `/view/{version_id}` - view specific version by ID
- B) `/view?version={version_id}` - query parameter for version
- C) `/resumes/{version_id}` - dedicated resumes endpoint
- D) `/view` (default version) and `/view/{version_id}` (specific version)
- X) Other (please specify)

[Answer]:

---

### Backward Compatibility

**Q37: What should happen to existing user profiles when this feature is deployed?**
- A) Migrate existing profiles to "Version 1" automatically (default version)
- B) Keep existing profiles as-is, new version system only for new resumes
- C) Prompt users to migrate their profile to the new version system on next login
- D) Automatic migration + create backup of original profile
- X) Other (please specify)

[Answer]:

---

---

## EXTENSION CONFIGURATION

### Security Baseline Extension

**Q38: Should security baseline rules be enforced for this feature enhancement?**

This extension adds security requirements including:
- Input validation and sanitization
- File upload security (size limits, type validation, malware scanning)
- SQL injection prevention
- XSS protection
- CSRF protection
- Secure file storage

- A) Yes - Enable security baseline extension (recommended for file uploads)
- B) No - Skip security baseline extension (prototype/learning project)

[Answer]:

---

### Property-Based Testing Extension

**Q39: Should property-based testing be required for this feature enhancement?**

This extension requires property-based tests using Hypothesis library for:
- Testing version management logic with random data
- Testing customization settings with various combinations
- Testing file upload handling with edge cases

- A) Yes - Enable property-based testing extension
- B) No - Skip property-based testing extension (use standard unit tests only)

[Answer]:

---

---

## SUMMARY

**Total Questions**: 39 questions covering:
- Resume Version Management (12 questions)
- Advanced Customization (20 questions)
- Technical Implementation (5 questions)
- Extension Configuration (2 questions)

**Next Steps**:
1. Answer all questions above
2. I will analyze answers for ambiguities
3. I will create follow-up questions if needed
4. Once all ambiguities are resolved, I will generate comprehensive requirements document

---

**Please answer all questions and let me know when you're done!**
