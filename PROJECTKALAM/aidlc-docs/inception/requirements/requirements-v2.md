# Requirements Document: Resume Versions & Advanced Customization

## Intent Analysis Summary

### User Request
Add two major features to the existing AI CV Builder:
1. **Resume Versions & Management**: Allow users to create multiple resume versions for different jobs
2. **Advanced Customization**: Add color themes, font selection, section reordering, custom sections, and profile photo upload

### Request Type
**Enhancement** - Major feature additions to existing application

### Scope Estimate
**Multiple Components** - Changes across database schema, backend routes, frontend UI, and file handling

### Complexity Estimate
**Complex** - Significant database changes, new UI components, file upload handling, and version management logic

---

## Design Decisions (AI-Selected for Speed)

### Resume Versions & Management
- **Version Limit**: Unlimited versions per user
- **Storage**: Complete profile data per version with metadata (name, description, dates)
- **Naming**: Required unique name per version + optional description
- **Default**: User marks one version as default
- **History**: Track creation and last modified timestamps only (no detailed change history)
- **Comparison**: Simple side-by-side view without diff highlighting
- **Clone**: Create duplicate and prompt user to edit name
- **Archive**: Archive + soft delete (30-day trash)
- **UI**: "My Resumes" dashboard + dropdown for quick switching
- **Display**: Version name, thumbnail preview, template, dates, actions

### Advanced Customization
- **Color Themes**: 5 pre-defined professional themes + custom color picker
- **Theme Scope**: Per resume version (each version has its own theme)
- **Theme Elements**: Resume content + navigation bar + buttons
- **Fonts**: 5 professional font pairings (pre-defined combinations)
- **Font Scope**: Per resume version
- **Section Reordering**: All sections reorderable (Personal Info can move too)
- **Reorder UI**: Drag-and-drop with visual handles
- **Section Order Scope**: Per resume version
- **Custom Sections**: Awards, Publications, Languages, Hobbies, Volunteer Work, Memberships + ability to create custom
- **Custom Section Structure**: Flexible - user chooses text area or structured fields
- **Custom Section Icons**: User selects from icon library
- **Profile Photo**: Display in resume header, max 5MB, auto-crop to square
- **Photo Scope**: Per resume version (each version can have different photo)
- **Logo**: Both image logo and text-based branding supported
- **Logo Placement**: User chooses (header, footer, or hidden)
- **Customization UI**: Settings panel/sidebar that slides in
- **Preview**: Live preview as user makes changes
- **Export/Import**: Both export settings as JSON and copy from another version

### Technical Implementation
- **Database**: New `resume_versions` table with complete profile data + metadata
- **Customization Storage**: JSON blob column in `resume_versions` for flexible settings
- **File Storage**: `static/uploads/user_{id}/` directory (per-user folders)
- **URL Structure**: `/view` (default) and `/view/{version_id}` (specific version)
- **Backward Compatibility**: Auto-migrate existing profiles to "My First Resume" (default version)

### Extensions
- **Security Baseline**: ENABLED (essential for file uploads)
- **Property-Based Testing**: DISABLED (use standard unit tests for speed)

---

## Functional Requirements

### FR-01: Resume Version Management Dashboard
**Priority**: High  
**Description**: Create a dashboard where users can view, manage, and switch between resume versions

**Acceptance Criteria**:
- New route `/my-resumes` displays all user's resume versions
- Each version shows: thumbnail preview, name, description, template choice, creation date, last modified date
- Actions available: View, Edit, Clone, Archive, Delete
- "Create New Version" button to start a new resume
- Default version is marked with a badge
- Responsive grid layout (3 columns desktop, 2 tablet, 1 mobile)

---

### FR-02: Create New Resume Version
**Priority**: High  
**Description**: Allow users to create a new resume version from scratch or by cloning

**Acceptance Criteria**:
- "Create New Version" button opens modal/form
- User enters: Version name (required), Description (optional), Target job/company (optional)
- User selects starting point: Blank resume, Clone from existing version, Use default template
- System creates new version and redirects to form page for that version
- New version is automatically set as active/current version

---

### FR-03: Clone Resume Version
**Priority**: High  
**Description**: Duplicate an existing resume version with all data and customizations

**Acceptance Criteria**:
- "Clone" button on each version card
- Opens modal prompting for new version name (pre-filled with "Copy of [Original Name]")
- User can edit name and description before cloning
- System creates exact duplicate including: profile data, template choice, customization settings, photo
- Cloned version becomes the active version
- User is redirected to view the cloned version

---

### FR-04: Set Default Resume Version
**Priority**: Medium  
**Description**: Allow users to mark one version as their default/primary resume

**Acceptance Criteria**:
- "Set as Default" action on each version card
- Default version is marked with "Default" badge
- When user visits `/view` without version ID, default version is shown
- Only one version can be default at a time
- If user deletes default version, system prompts to select new default

---

### FR-05: Archive Resume Version
**Priority**: Medium  
**Description**: Hide resume versions from main list without permanently deleting

**Acceptance Criteria**:
- "Archive" action on each version card
- Archived versions move to "Archived" tab in dashboard
- Archived versions can be restored or permanently deleted
- Archived versions don't appear in version dropdown or main list
- User can view archived versions by clicking "Archived" tab

---

### FR-06: Delete Resume Version (Soft Delete)
**Priority**: Medium  
**Description**: Move deleted versions to trash for 30 days before permanent deletion

**Acceptance Criteria**:
- "Delete" action shows confirmation dialog
- Deleted versions move to "Trash" tab
- Trash items show deletion date and days remaining
- User can restore from trash or permanently delete
- After 30 days, system automatically purges trash items
- Cannot delete if it's the only remaining version

---

### FR-07: Version Switching Dropdown
**Priority**: High  
**Description**: Quick version switcher in navigation bar

**Acceptance Criteria**:
- Dropdown in navigation shows current version name
- Lists all active (non-archived) versions
- Clicking a version switches to that version's view
- Shows version count (e.g., "My Resumes (5)")
- Link to "Manage All Versions" opens dashboard

---

### FR-08: Color Theme Selector
**Priority**: High  
**Description**: Allow users to choose from pre-defined color themes or create custom

**Acceptance Criteria**:
- 5 pre-defined themes: Navy Professional, Forest Green, Burgundy Executive, Charcoal Modern, Teal Creative
- Custom color picker for primary, secondary, and accent colors
- Live preview as user selects colors
- Theme applies to: resume headings, section dividers, skill badges, navigation bar, buttons
- Theme saved per resume version
- Color picker shows hex codes and allows manual entry

---

### FR-09: Font Selector
**Priority**: High  
**Description**: Choose from professional font pairings

**Acceptance Criteria**:
- 5 font pairings:
  1. Classic Professional (Arial + Helvetica)
  2. Modern Clean (Roboto + Open Sans)
  3. Executive Serif (Georgia + Times New Roman)
  4. Tech Sans (Inter + Lato)
  5. Creative Modern (Montserrat + Raleway)
- Preview shows sample text in each font pairing
- Fonts apply to headings and body text
- Font choice saved per resume version
- Fonts load from Google Fonts CDN

---

### FR-10: Section Reordering
**Priority**: High  
**Description**: Drag-and-drop to reorder resume sections

**Acceptance Criteria**:
- "Customize Layout" button opens section reordering interface
- All sections draggable: Personal Info, Education, Skills, Projects, Certifications, Custom Sections
- Visual drag handles on each section
- Live preview shows new order as user drags
- "Reset to Default" button restores original order
- Section order saved per resume version
- Mobile: Use up/down arrow buttons instead of drag-and-drop

---

### FR-11: Custom Sections
**Priority**: High  
**Description**: Add custom sections like Awards, Publications, Languages, Hobbies

**Acceptance Criteria**:
- "Add Custom Section" button in customization panel
- Pre-defined section types: Awards, Publications, Languages, Hobbies, Volunteer Work, Professional Memberships
- Option to create completely custom section with custom name
- User chooses data structure:
  - Simple text area (free-form)
  - Structured fields (title, organization, date, description, URL)
- User selects icon from icon library (50+ professional icons)
- Custom sections appear in section reordering interface
- Custom sections can be edited, hidden, or deleted
- Custom sections saved per resume version

---

### FR-12: Profile Photo Upload
**Priority**: High  
**Description**: Upload and display professional headshot on resume

**Acceptance Criteria**:
- "Upload Photo" button in customization panel
- Accepts JPG, PNG, GIF files, max 5MB
- Image cropping tool to select square area
- Preview before saving
- Photo displays in resume header (next to name)
- Photo is optional - can be hidden or removed
- Photo saved per resume version (each version can have different photo)
- Photos stored in `static/uploads/user_{id}/photos/`

---

### FR-13: Logo/Branding Upload
**Priority**: Medium  
**Description**: Add personal logo or text-based branding

**Acceptance Criteria**:
- "Add Logo" option in customization panel
- Two modes: Image upload or Text-based branding
- Image upload: Same requirements as profile photo (max 5MB, JPG/PNG)
- Text-based: User enters text (e.g., initials) and chooses font/color
- User chooses placement: Header (top corner), Footer (bottom), or Hidden
- Logo saved per resume version
- Logos stored in `static/uploads/user_{id}/logos/`

---

### FR-14: Customization Settings Panel
**Priority**: High  
**Description**: Unified interface for all customization options

**Acceptance Criteria**:
- "Customize" button in navigation opens slide-in panel from right
- Panel has tabs: Colors, Fonts, Layout, Sections, Photo, Logo
- Live preview on left side as user makes changes
- "Save Changes" button at bottom of panel
- "Cancel" button discards unsaved changes
- "Reset to Default" button restores template defaults
- Panel is responsive (full-screen modal on mobile)

---

### FR-15: Export/Import Customization Settings
**Priority**: Low  
**Description**: Save and reuse customization settings across versions

**Acceptance Criteria**:
- "Export Settings" button downloads JSON file with all customization settings
- "Import Settings" button uploads JSON file and applies settings
- "Copy from Version" dropdown allows copying settings from another version
- Confirmation dialog before applying imported settings
- Export includes: colors, fonts, section order, custom sections (but not photos/logos)

---

## Non-Functional Requirements

### NFR-01: Performance
**Priority**: High  
**Description**: Application should remain fast with multiple versions and customizations

**Acceptance Criteria**:
- Dashboard loads all versions in < 2 seconds
- Version switching < 500ms
- Live preview updates < 300ms
- Image upload and processing < 3 seconds
- Database queries optimized with indexes

---

### NFR-02: Security
**Priority**: High  
**Description**: Secure file uploads and user data

**Acceptance Criteria**:
- File upload validation (type, size, content)
- Sanitize file names to prevent directory traversal
- Store files outside web root or with restricted access
- Validate image files are actual images (not malicious files)
- SQL injection prevention (parameterized queries)
- XSS protection (escape user input)
- CSRF protection on all forms

---

### NFR-03: Usability
**Priority**: High  
**Description**: Intuitive interface for version management and customization

**Acceptance Criteria**:
- Clear visual hierarchy in dashboard
- Helpful tooltips and hints
- Confirmation dialogs for destructive actions
- Undo capability for customization changes
- Keyboard shortcuts for power users
- Accessible (WCAG AA compliance)

---

### NFR-04: Data Integrity
**Priority**: High  
**Description**: Prevent data loss and ensure consistency

**Acceptance Criteria**:
- Auto-save customization changes every 30 seconds
- Soft delete with 30-day recovery period
- Database transactions for multi-step operations
- Backup existing profile before migration
- Validation before saving (required fields, data types)

---

## Database Schema Changes

### New Table: resume_versions

```sql
CREATE TABLE resume_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    version_name TEXT NOT NULL,
    description TEXT,
    target_job TEXT,
    is_default INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0,
    is_deleted INTEGER DEFAULT 0,
    deleted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Profile data (same as current profile table)
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    github_url TEXT,
    linkedin_url TEXT,
    education TEXT,
    skills TEXT,
    project1_title TEXT,
    project1_desc TEXT,
    project1_url TEXT,
    project2_title TEXT,
    project2_desc TEXT,
    project2_url TEXT,
    project3_title TEXT,
    project3_desc TEXT,
    project3_url TEXT,
    cert1_name TEXT,
    cert1_org TEXT,
    cert1_year TEXT,
    cert2_name TEXT,
    cert2_org TEXT,
    cert2_year TEXT,
    cert3_name TEXT,
    cert3_org TEXT,
    cert3_year TEXT,
    template_choice TEXT DEFAULT 'template1',
    
    -- Customization settings (JSON blob)
    customization_settings TEXT,
    
    -- File paths
    profile_photo_path TEXT,
    logo_path TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Migration Strategy
1. Create `resume_versions` table
2. Migrate existing `profile` records to `resume_versions` with version_name="My First Resume", is_default=1
3. Keep `profile` table for backward compatibility (deprecated)
4. Add indexes on user_id, is_default, is_archived, is_deleted

---

## Success Criteria

The feature enhancement will be considered successful when:

1. ✅ Users can create unlimited resume versions
2. ✅ Users can clone, archive, and delete versions
3. ✅ Users can set a default version
4. ✅ Users can switch between versions via dropdown
5. ✅ Users can customize colors per version (5 themes + custom)
6. ✅ Users can select fonts per version (5 pairings)
7. ✅ Users can reorder sections via drag-and-drop
8. ✅ Users can add custom sections (Awards, Languages, etc.)
9. ✅ Users can upload profile photos per version
10. ✅ Users can add logos/branding per version
11. ✅ Customization panel provides live preview
12. ✅ All existing functionality continues to work
13. ✅ Existing user profiles are migrated automatically
14. ✅ File uploads are secure and validated
15. ✅ Dashboard is responsive and performant

---

## Out of Scope (Future Enhancements)

- ❌ Detailed version history with change tracking
- ❌ A/B testing metrics and analytics
- ❌ Collaborative editing and sharing
- ❌ AI-powered customization suggestions
- ❌ Advanced image editing (filters, effects)
- ❌ Video resume support
- ❌ Integration with job boards
- ❌ Resume scoring and optimization

---

## Extension Configuration

### Security Baseline Extension
**Status**: ✅ ENABLED  
**Rationale**: File upload functionality requires security validation, input sanitization, and secure storage

### Property-Based Testing Extension
**Status**: ❌ DISABLED  
**Rationale**: Standard unit tests sufficient for this feature; property-based testing would slow development

---
