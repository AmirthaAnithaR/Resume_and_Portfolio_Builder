# Domain Entities

## Overview
This document defines the domain entities for the AI CV Builder application, including their fields, types, constraints, and relationships.

---

## 1. Profile Entity

**Purpose**: Represents a user's complete profile data for resume and portfolio generation

**Persistence**: SQLite database (single row, id=1)

**Fields**:

### 1.1 Primary Key
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, NOT NULL | Always 1 (single-user design) |

### 1.2 Personal Information (5 fields)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| name | TEXT | NOT NULL | Full name (required) |
| email | TEXT | NOT NULL | Email address (required, validated format) |
| phone | TEXT | NOT NULL | Phone number (required) |
| github_url | TEXT | NULL | GitHub profile URL (optional, validated format) |
| linkedin_url | TEXT | NULL | LinkedIn profile URL (optional, validated format) |

### 1.3 Education and Skills (2 fields)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| education | TEXT | NULL | Education details (multi-line text) |
| skills | TEXT | NULL | Skills list (comma or newline separated) |

### 1.4 Projects (9 fields - 3 projects)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| project1_title | TEXT | NULL | Project 1 title |
| project1_desc | TEXT | NULL | Project 1 description (multi-line) |
| project1_url | TEXT | NULL | Project 1 URL (optional, validated format) |
| project2_title | TEXT | NULL | Project 2 title |
| project2_desc | TEXT | NULL | Project 2 description (multi-line) |
| project2_url | TEXT | NULL | Project 2 URL (optional, validated format) |
| project3_title | TEXT | NULL | Project 3 title |
| project3_desc | TEXT | NULL | Project 3 description (multi-line) |
| project3_url | TEXT | NULL | Project 3 URL (optional, validated format) |

### 1.5 Certifications (9 fields - 3 certifications)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| cert1_name | TEXT | NULL | Certification 1 name |
| cert1_org | TEXT | NULL | Certification 1 organization |
| cert1_year | TEXT | NULL | Certification 1 year |
| cert2_name | TEXT | NULL | Certification 2 name |
| cert2_org | TEXT | NULL | Certification 2 organization |
| cert2_year | TEXT | NULL | Certification 2 year |
| cert3_name | TEXT | NULL | Certification 3 name |
| cert3_org | TEXT | NULL | Certification 3 organization |
| cert3_year | TEXT | NULL | Certification 3 year |

### 1.6 Template Selection (1 field)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| template_choice | TEXT | NULL | Selected template ("template1", "template2", "template3") |

### 1.7 Professional Summary (1 field)
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| summary | TEXT | NULL | Professional summary/objective (optional, future enhancement) |

**Total Fields**: 29 (27 existing + 2 new)

**Business Rules**:
- Only one profile exists (id=1)
- Required fields: name, email, phone
- Optional fields: All others (NULL allowed)
- Empty strings converted to NULL on save

---

## 2. FormStep Entity

**Purpose**: Represents a step in the multi-step form wizard

**Persistence**: Client-side only (JavaScript object)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| stepNumber | Integer | 1-5 | Step number in wizard |
| stepName | String | NOT NULL | Step name (e.g., "Personal Information") |
| fields | Array<String> | NOT NULL | List of field names in this step |
| isValid | Boolean | NOT NULL | Whether step has been validated |
| isCompleted | Boolean | NOT NULL | Whether step has been completed |

**Step Definitions**:

### Step 1: Personal Information
- **Fields**: name, email, phone, github_url, linkedin_url
- **Required**: name, email, phone
- **Validation**: Email format, URL format (optional fields)

### Step 2: Education
- **Fields**: education
- **Required**: None
- **Validation**: None

### Step 3: Skills
- **Fields**: skills
- **Required**: None
- **Validation**: None

### Step 4: Projects
- **Fields**: project1_title, project1_desc, project1_url, project2_title, project2_desc, project2_url, project3_title, project3_desc, project3_url
- **Required**: None
- **Validation**: URL format (optional project URLs)

### Step 5: Certifications
- **Fields**: cert1_name, cert1_org, cert1_year, cert2_name, cert2_org, cert2_year, cert3_name, cert3_org, cert3_year
- **Required**: None
- **Validation**: None

**Business Rules**:
- Steps must be completed in order (1 → 2 → 3 → 4 → 5)
- User can navigate back to previous steps without validation
- User cannot navigate forward without validating current step
- Form data persists across steps (in-memory or sessionStorage)

---

## 3. ResumeTemplate Entity

**Purpose**: Represents a resume template option

**Persistence**: Static definition (no database storage)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| templateId | String | NOT NULL, UNIQUE | Template identifier ("template1", "template2", "template3") |
| templateName | String | NOT NULL | Display name (e.g., "Corporate Professional Resume") |
| description | String | NOT NULL | Brief description of template style |
| filename | String | NOT NULL | Template file name (e.g., "resume-template1.html") |
| styleType | String | NOT NULL | Style category ("conservative", "modern", "creative") |
| thumbnailUrl | String | NULL | Thumbnail image URL (optional) |

**Template Definitions**:

### Template 1: Corporate Professional Resume
- **templateId**: "template1"
- **templateName**: "Corporate Professional Resume"
- **description**: "Clean ATS-friendly design with conservative professional styling"
- **filename**: "resume-template1.html"
- **styleType**: "conservative"
- **Features**: Single-column, navy/grey accents, professional fonts, ATS-compatible

### Template 2: Modern Developer Resume
- **templateId**: "template2"
- **templateName**: "Modern Developer Resume"
- **description**: "Modern design with skills badges and project cards"
- **filename**: "resume-template2.html"
- **styleType**: "modern"
- **Features**: Skills badges, project cards, two-column layout, tech-focused

### Template 3: Creative Portfolio Resume
- **templateId**: "template3"
- **templateName**: "Creative Portfolio Resume"
- **description**: "Stylish visual layout with balanced creativity"
- **filename**: "resume-template3.html"
- **styleType**: "creative"
- **Features**: Asymmetric layout, creative icons, visual hierarchy, unique design

**Business Rules**:
- User must select one template
- Template choice is saved with profile
- User can change template later
- Template change preserves all profile data

---

## 4. ValidationError Entity

**Purpose**: Represents a validation error for a form field

**Persistence**: Client-side only (JavaScript object)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| fieldId | String | NOT NULL | HTML element ID of invalid field |
| errorId | String | NOT NULL | HTML element ID of error message span |
| message | String | NOT NULL | Error message to display |
| errorType | String | NOT NULL | Type of error ("required", "format", "constraint") |

**Error Types**:

### Required Field Error
- **errorType**: "required"
- **message**: "[Field name] is required"
- **Fields**: name, email, phone

### Email Format Error
- **errorType**: "format"
- **message**: "Please enter a valid email address"
- **Fields**: email

### URL Format Error
- **errorType**: "format"
- **message**: "URL must start with http:// or https://"
- **Fields**: github_url, linkedin_url, project1_url, project2_url, project3_url

**Business Rules**:
- Errors are displayed below the invalid field
- Invalid fields get red border (input-error class)
- Errors are cleared when user corrects the field
- Multiple errors can exist simultaneously
- First error is scrolled into view on validation failure

---

## 5. Project Entity (Derived)

**Purpose**: Represents a single project (derived from Profile entity)

**Persistence**: Part of Profile entity (not separate table)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| title | String | NULL | Project title |
| description | String | NULL | Project description (multi-line) |
| url | String | NULL | Project URL (optional) |

**Derivation Logic**:
```
FOR i = 1 to 3:
    IF profile['project' + i + '_title'] is not empty OR profile['project' + i + '_desc'] is not empty:
        Create Project entity with:
            title = profile['project' + i + '_title']
            description = profile['project' + i + '_desc']
            url = profile['project' + i + '_url']
```

**Business Rules**:
- Project is shown if title OR description is provided
- URL is optional (can be NULL)
- Empty projects are hidden in resume
- Maximum 3 projects per profile

---

## 6. Certification Entity (Derived)

**Purpose**: Represents a single certification (derived from Profile entity)

**Persistence**: Part of Profile entity (not separate table)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| name | String | NULL | Certification name |
| organization | String | NULL | Issuing organization |
| year | String | NULL | Year obtained |

**Derivation Logic**:
```
FOR i = 1 to 3:
    IF profile['cert' + i + '_name'] is not empty:
        Create Certification entity with:
            name = profile['cert' + i + '_name']
            organization = profile['cert' + i + '_org']
            year = profile['cert' + i + '_year']
```

**Business Rules**:
- Certification is shown if name is provided
- Organization and year are optional (can be NULL)
- Empty certifications are hidden in resume
- Maximum 3 certifications per profile

---

## 7. Skill Entity (Derived)

**Purpose**: Represents a single skill (derived from Profile entity)

**Persistence**: Part of Profile entity (not separate table)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| name | String | NOT NULL | Skill name |

**Derivation Logic**:
```
IF profile['skills'] contains comma:
    Split by comma → Array of skills
ELSE IF profile['skills'] contains newline:
    Split by newline → Array of skills
ELSE:
    Single skill → Array with one element
```

**Business Rules**:
- Skills are parsed from comma-separated or newline-separated text
- Each skill is trimmed of whitespace
- Empty skills are filtered out
- Skills are displayed as list, badges, or visual representation (template-dependent)

---

## Entity Relationships

### Relationship Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────┐
│                        Profile Entity                        │
│  (SQLite database, single row, id=1)                        │
│                                                              │
│  - id (PK)                                                   │
│  - Personal Info (5 fields)                                  │
│  - Education & Skills (2 fields)                             │
│  - Projects (9 fields)                                       │
│  - Certifications (9 fields)                                 │
│  - Template Choice (1 field)                                 │
│  - Summary (1 field)                                         │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   │ derives
                   ├──────────────────────────────────────────┐
                   │                                          │
                   ▼                                          ▼
         ┌──────────────────┐                      ┌──────────────────┐
         │  Project Entity  │                      │ Certification    │
         │  (Derived)       │                      │ Entity (Derived) │
         │                  │                      │                  │
         │  - title         │                      │  - name          │
         │  - description   │                      │  - organization  │
         │  - url           │                      │  - year          │
         └──────────────────┘                      └──────────────────┘
                   │
                   │ derives
                   ▼
         ┌──────────────────┐
         │  Skill Entity    │
         │  (Derived)       │
         │                  │
         │  - name          │
         └──────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   ResumeTemplate Entity                      │
│  (Static definition, no database)                           │
│                                                              │
│  - templateId (PK)                                           │
│  - templateName                                              │
│  - description                                               │
│  - filename                                                  │
│  - styleType                                                 │
│  - thumbnailUrl                                              │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   │ referenced by
                   │
         ┌─────────▼─────────┐
         │  Profile Entity   │
         │  template_choice  │
         └───────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    FormStep Entity                           │
│  (Client-side only, JavaScript)                             │
│                                                              │
│  - stepNumber (PK)                                           │
│  - stepName                                                  │
│  - fields (array)                                            │
│  - isValid                                                   │
│  - isCompleted                                               │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   │ validates
                   │
         ┌─────────▼─────────┐
         │  Profile Entity   │
         │  (form fields)    │
         └───────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 ValidationError Entity                       │
│  (Client-side only, JavaScript)                             │
│                                                              │
│  - fieldId                                                   │
│  - errorId                                                   │
│  - message                                                   │
│  - errorType                                                 │
└──────────────────┬───────────────────────────────────────────┘
                   │
                   │ reports errors for
                   │
         ┌─────────▼─────────┐
         │  FormStep Entity  │
         │  (validation)     │
         └───────────────────┘
```

### Relationship Summary

**Profile → Project** (1:N, derived)
- One profile contains up to 3 projects
- Projects are derived from profile fields (project1_*, project2_*, project3_*)

**Profile → Certification** (1:N, derived)
- One profile contains up to 3 certifications
- Certifications are derived from profile fields (cert1_*, cert2_*, cert3_*)

**Profile → Skill** (1:N, derived)
- One profile contains multiple skills
- Skills are derived from profile.skills field (parsed)

**Profile → ResumeTemplate** (N:1, reference)
- One profile references one template via template_choice field
- Template is selected from 3 static template definitions

**FormStep → Profile** (N:1, validation)
- Each form step validates a subset of profile fields
- 5 form steps collectively cover all profile fields

**ValidationError → FormStep** (N:1, reporting)
- Each validation error is associated with a form step
- Multiple errors can exist for a single step

---

## Entity Lifecycle

### Profile Entity Lifecycle

```
[New User] → [Form Page] → [Fill Step 1-5] → [Submit] → [Profile Created (INSERT)]
                                                              ↓
                                                    [Template Selection]
                                                              ↓
                                                    [Select Template]
                                                              ↓
                                                    [Profile Updated (UPDATE)]
                                                              ↓
                                                    [Final Resume Page]
                                                              ↓
                                          [Edit Details] ← [Profile Retrieved (SELECT)]
                                                              ↓
                                                    [Form Page (pre-populated)]
                                                              ↓
                                                    [Update Fields]
                                                              ↓
                                                    [Submit]
                                                              ↓
                                                    [Profile Updated (UPDATE)]
```

### FormStep Entity Lifecycle

```
[Form Page Load] → [Initialize FormStep objects (1-5)]
                              ↓
                    [Show Step 1]
                              ↓
                    [User fills fields]
                              ↓
                    [Click Next]
                              ↓
                    [Validate Step 1] → [If invalid: Show errors, stay on Step 1]
                              ↓
                    [If valid: Mark Step 1 completed, Show Step 2]
                              ↓
                    [Repeat for Steps 2-5]
                              ↓
                    [Submit Form] → [Validate all steps]
                              ↓
                    [If all valid: Submit to server]
```

### ResumeTemplate Entity Lifecycle

```
[Template Selection Page Load] → [Load 3 static template definitions]
                                            ↓
                                  [Display template cards]
                                            ↓
                                  [User clicks template card]
                                            ↓
                                  [Show preview modal]
                                            ↓
                                  [User clicks "Use Template"]
                                            ↓
                                  [Save template_choice to Profile]
                                            ↓
                                  [Redirect to Final Resume Page]
                                            ↓
                                  [Load selected template file]
```

### ValidationError Entity Lifecycle

```
[User fills form field] → [Blur event or Submit event]
                                    ↓
                          [Validate field]
                                    ↓
                          [If invalid: Create ValidationError object]
                                    ↓
                          [Display error message]
                                    ↓
                          [Add error class to field]
                                    ↓
                          [User corrects field]
                                    ↓
                          [Clear ValidationError object]
                                    ↓
                          [Remove error message and class]
```

---

## Entity Summary

| Entity | Type | Persistence | Fields | Purpose |
|--------|------|-------------|--------|---------|
| Profile | Core | SQLite database | 29 | User's complete profile data |
| FormStep | UI | Client-side (JS) | 5 | Multi-step form wizard state |
| ResumeTemplate | Static | None (static) | 6 | Template definition and metadata |
| ValidationError | UI | Client-side (JS) | 4 | Form validation error reporting |
| Project | Derived | Part of Profile | 3 | Individual project (derived from Profile) |
| Certification | Derived | Part of Profile | 3 | Individual certification (derived from Profile) |
| Skill | Derived | Part of Profile | 1 | Individual skill (derived from Profile) |

**Total Entities**: 7 (1 core, 2 UI, 1 static, 3 derived)

---

## Data Flow

### Form Submission Flow

```
User Input (Form) → FormStep Validation → Profile Entity (in-memory)
                                                ↓
                                    POST /save (HTTP)
                                                ↓
                                    Flask Route Handler
                                                ↓
                                    Extract Form Data
                                                ↓
                                    Profile Entity (dict)
                                                ↓
                                    save_data() or update_data()
                                                ↓
                                    SQLite Database (INSERT/UPDATE)
                                                ↓
                                    Profile Entity (persisted)
```

### Resume Rendering Flow

```
GET /view (HTTP) → Flask Route Handler
                            ↓
                    get_data() (database.py)
                            ↓
                    Profile Entity (dict)
                            ↓
                    Parse Skills → Skill Entities (array)
                            ↓
                    Filter Projects → Project Entities (array)
                            ↓
                    Filter Certifications → Certification Entities (array)
                            ↓
                    Get ResumeTemplate (static definition)
                            ↓
                    Render Template (Jinja2)
                            ↓
                    HTML Response (resume + portfolio)
```

---

## Entity Constraints and Invariants

### Profile Entity Constraints
- **Uniqueness**: Only one profile exists (id=1)
- **Required Fields**: name, email, phone must not be NULL
- **Email Format**: Must match regex `^[^\s@]+@[^\s@]+\.[^\s@]+$`
- **URL Format**: URLs must start with `http://` or `https://`
- **Template Choice**: Must be "template1", "template2", or "template3" (if not NULL)

### FormStep Entity Constraints
- **Step Order**: Steps must be 1-5 (no gaps)
- **Validation Order**: Step N cannot be validated until Step N-1 is completed
- **Field Coverage**: All profile fields must be covered by exactly one step

### ResumeTemplate Entity Constraints
- **Template Count**: Exactly 3 templates must be defined
- **Unique IDs**: Template IDs must be unique
- **File Existence**: Template files must exist in templates/ directory

### ValidationError Entity Constraints
- **Field Existence**: fieldId and errorId must reference existing HTML elements
- **Error Type**: errorType must be "required", "format", or "constraint"

---

## Entity Extensions (Future)

### Potential Future Entities

**User Entity** (Multi-user support):
- user_id (PK)
- username
- password_hash
- email
- created_at

**ProfileVersion Entity** (Version history):
- version_id (PK)
- profile_id (FK)
- version_number
- created_at
- profile_data (JSON)

**TemplateCustomization Entity** (Custom themes):
- customization_id (PK)
- profile_id (FK)
- template_id (FK)
- color_scheme (JSON)
- font_choices (JSON)

**AIAssistance Entity** (AI-generated content):
- assistance_id (PK)
- profile_id (FK)
- field_name
- ai_suggestion
- user_accepted (boolean)

---

## Conclusion

This domain model provides a clear, technology-agnostic representation of the AI CV Builder's data structures. The design balances simplicity (single-user, flat structure) with extensibility (derived entities, optional fields) to meet current requirements while allowing future enhancements.

**Key Design Principles**:
- **Simplicity**: Single profile, flat structure, minimal relationships
- **Flexibility**: Optional fields, derived entities, template choice
- **Validation**: Clear constraints and business rules
- **Extensibility**: Room for future enhancements (multi-user, versioning, AI)

