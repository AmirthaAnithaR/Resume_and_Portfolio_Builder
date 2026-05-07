# Code Generation Plan: Resume Versions & Advanced Customization

## Implementation Strategy

**Approach**: Incremental implementation in logical phases
**Priority**: Core version management first, then customization features
**Testing**: Manual testing after each phase

---

## Phase 1: Database Schema & Migration (CRITICAL FOUNDATION)

### Step 1: Update database.py - Add resume_versions table
- [x] Create `resume_versions` table schema
- [x] Add migration function to migrate existing profiles
- [x] Add CRUD functions for resume versions
- [x] Add file upload helper functions
- [x] Test database operations

**Files**: `resume-portfolio-builder/database.py` ✅ COMPLETE

---

## Phase 2: Version Management Backend (CORE FUNCTIONALITY)

### Step 2: Update app.py - Add version management routes
- [x] Add `/my-resumes` route (dashboard)
- [x] Add `/create-version` route (create new version)
- [x] Add `/clone-version/<id>` route (clone version)
- [x] Add `/set-default/<id>` route (set default)
- [x] Add `/archive-version/<id>` route (archive)
- [x] Add `/delete-version/<id>` route (soft delete)
- [x] Add `/restore-version/<id>` route (restore from trash)
- [x] Update `/view` and `/view/<version_id>` routes
- [x] Update `/form` and `/save` routes to work with versions

**Files**: `resume-portfolio-builder/app.py` ✅ COMPLETE

---

## Phase 3: Version Management Frontend (USER INTERFACE)

### Step 3: Create dashboard template
- [x] Create `templates/my-resumes.html` (dashboard with version cards)
- [x] Add version card component with thumbnail, name, dates, actions
- [x] Add "Create New Version" modal
- [x] Add "Clone Version" modal
- [x] Add tabs: Active, Archived, Trash
- [x] Add version dropdown to base.html navigation

**Files**: 
- `resume-portfolio-builder/templates/my-resumes.html` ✅ COMPLETE
- `resume-portfolio-builder/templates/base.html` (updated navigation) ✅ COMPLETE

### Step 4: Create dashboard CSS and JavaScript
- [x] Add dashboard styles to `static/css/style.css`
- [x] Create version management JavaScript (included in my-resumes.html)

**Files**:
- `resume-portfolio-builder/static/css/style.css` (appended) ✅ COMPLETE
- JavaScript included inline in my-resumes.html ✅ COMPLETE

---

## Phase 4: Customization Backend (SETTINGS STORAGE)

### Step 5: Add customization routes to app.py
- [ ] Add `/customize/<version_id>` route (get customization settings)
- [ ] Add `/save-customization/<version_id>` route (save settings)
- [ ] Add `/upload-photo/<version_id>` route (photo upload)
- [ ] Add `/upload-logo/<version_id>` route (logo upload)
- [ ] Add `/export-settings/<version_id>` route (export JSON)
- [ ] Add `/import-settings/<version_id>` route (import JSON)

**Files**: `resume-portfolio-builder/app.py`

---

## Phase 5: Customization Frontend (SETTINGS PANEL)

### Step 6: Create customization panel component
- [ ] Create `templates/components/customization-panel.html` (slide-in panel)
- [ ] Add tabs: Colors, Fonts, Layout, Sections, Photo, Logo
- [ ] Add color theme selector (5 themes + custom picker)
- [ ] Add font selector (5 pairings with preview)
- [ ] Add section reordering interface (drag-drop)
- [ ] Add custom section creator
- [ ] Add photo upload with crop tool
- [ ] Add logo upload/text branding

**Files**: `resume-portfolio-builder/templates/components/customization-panel.html`

### Step 7: Create customization JavaScript
- [ ] Create `static/js/customization.js` (panel logic, live preview, AJAX)
- [ ] Add color picker integration
- [ ] Add drag-and-drop library (SortableJS)
- [ ] Add image crop library (Cropper.js)
- [ ] Add live preview updates

**Files**: `resume-portfolio-builder/static/js/customization.js`

### Step 8: Create customization CSS
- [ ] Add customization panel styles
- [ ] Add color theme CSS variables
- [ ] Add font loading from Google Fonts
- [ ] Add drag-drop visual feedback
- [ ] Add responsive styles for mobile

**Files**: `resume-portfolio-builder/static/css/style.css` (append)

---

## Phase 6: Apply Customizations to Templates (VISUAL RENDERING)

### Step 9: Update resume templates to use customization settings
- [ ] Update `templates/resume-template1.html` (apply colors, fonts, section order, photo, logo)
- [ ] Update `templates/resume-template2.html` (apply customizations)
- [ ] Update `templates/resume-template3.html` (apply customizations)
- [ ] Update `templates/view.html` (load customization settings, render custom sections)
- [ ] Add dynamic CSS generation based on customization settings

**Files**:
- `resume-portfolio-builder/templates/resume-template1.html`
- `resume-portfolio-builder/templates/resume-template2.html`
- `resume-portfolio-builder/templates/resume-template3.html`
- `resume-portfolio-builder/templates/view.html`

---

## Phase 7: File Upload Security (CRITICAL SECURITY)

### Step 10: Add file upload validation and security
- [ ] Add file type validation (whitelist JPG, PNG, GIF)
- [ ] Add file size validation (max 5MB)
- [ ] Add image content validation (verify actual image)
- [ ] Add filename sanitization
- [ ] Create upload directories with proper permissions
- [ ] Add file cleanup for deleted versions

**Files**: `resume-portfolio-builder/database.py` (helper functions)

---

## Phase 8: Migration & Backward Compatibility (DATA MIGRATION)

### Step 11: Create migration script and update init
- [ ] Add migration function in database.py
- [ ] Run migration on app startup (check if already migrated)
- [ ] Update `init_db()` to create resume_versions table
- [ ] Test migration with existing database

**Files**: `resume-portfolio-builder/database.py`

---

## Phase 9: Testing & Documentation (VALIDATION)

### Step 12: Create test files and documentation
- [ ] Create `tests/test_versions.py` (version management tests)
- [ ] Create `tests/test_customization.py` (customization tests)
- [ ] Create `tests/test_file_upload.py` (file upload security tests)
- [ ] Update `README.md` with new features
- [ ] Create `CUSTOMIZATION_GUIDE.md` (user guide)

**Files**:
- `resume-portfolio-builder/tests/test_versions.py`
- `resume-portfolio-builder/tests/test_customization.py`
- `resume-portfolio-builder/tests/test_file_upload.py`
- `resume-portfolio-builder/README.md` (update)
- `resume-portfolio-builder/CUSTOMIZATION_GUIDE.md` (new)

---

## Summary

**Total Steps**: 12 steps across 9 phases
**Estimated Files**: 20+ files (new + updated)
**Implementation Order**: Database → Backend → Frontend → Security → Migration → Testing

**Critical Path**:
1. Database schema (foundation)
2. Version management backend (core logic)
3. Version management frontend (user interface)
4. Customization backend (settings storage)
5. Customization frontend (settings UI)
6. Apply customizations (visual rendering)
7. Security (file uploads)
8. Migration (data migration)
9. Testing (validation)

---

## Dependencies

- **Python Libraries**: Pillow (image processing), werkzeug (file handling)
- **JavaScript Libraries**: SortableJS (drag-drop), Cropper.js (image crop), Pickr (color picker)
- **CSS**: Google Fonts API, Font Awesome icons

---

## Risk Mitigation

- **Database Migration**: Backup existing database before migration
- **File Storage**: Create upload directories with proper permissions
- **Security**: Validate all file uploads, sanitize filenames
- **Performance**: Add database indexes, optimize queries
- **Backward Compatibility**: Keep existing routes working, graceful fallbacks

---

**Ready to start implementation!**
