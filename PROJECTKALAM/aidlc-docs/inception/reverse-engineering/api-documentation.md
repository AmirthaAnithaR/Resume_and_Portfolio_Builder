# API Documentation

## REST APIs

### GET /
**Purpose**: Display the profile input form

**Method**: GET

**Path**: `/`

**Request**: None

**Response**: 
- **Content-Type**: text/html
- **Body**: Rendered index.html template
- **Status**: 200 OK

**Behavior**:
- If profile exists: Form is pre-populated with existing data
- If no profile: Form is empty
- Always accessible (no authentication)

**Template Context**:
```python
{
    "profile": {
        "name": str,
        "email": str,
        "phone": str,
        "github_url": str | None,
        "linkedin_url": str | None,
        "education": str | None,
        "skills": str | None,
        "project1_title": str | None,
        "project1_desc": str | None,
        "project1_url": str | None,
        # ... (project2, project3)
        "cert1_name": str | None,
        "cert1_org": str | None,
        "cert1_year": str | None,
        # ... (cert2, cert3)
    } | None
}
```

---

### POST /save
**Purpose**: Save or update user profile

**Method**: POST

**Path**: `/save`

**Request**:
- **Content-Type**: application/x-www-form-urlencoded
- **Body**: Form data with 27 fields

**Form Fields**:
```
Required:
- name: str (full name)
- email: str (email address)
- phone: str (phone number)

Optional:
- github_url: str (GitHub profile URL)
- linkedin_url: str (LinkedIn profile URL)
- education: str (education details)
- skills: str (comma-separated skills)
- project1_title, project1_desc, project1_url: str
- project2_title, project2_desc, project2_url: str
- project3_title, project3_desc, project3_url: str
- cert1_name, cert1_org, cert1_year: str
- cert2_name, cert2_org, cert2_year: str
- cert3_name, cert3_org, cert3_year: str
```

**Response**:
- **Status**: 302 Found (redirect)
- **Location**: `/view`

**Business Logic**:
1. Extract all form fields
2. Strip whitespace from each field
3. Check if profile exists (id=1)
4. If exists: UPDATE all fields
5. If not exists: INSERT new row with id=1
6. Redirect to /view (POST-Redirect-GET pattern)

**Error Handling**:
- No server-side validation (relies on client-side validation)
- Database errors not explicitly handled (would raise exception)

---

### GET /view
**Purpose**: Display the generated resume and portfolio

**Method**: GET

**Path**: `/view`

**Request**: None

**Response**:
- **Content-Type**: text/html
- **Body**: Rendered view.html template
- **Status**: 200 OK (if profile exists) or 302 Found (redirect if no profile)

**Behavior**:
- If profile exists: Render resume/portfolio page
- If no profile: Redirect to / (form page)

**Template Context**:
```python
{
    "profile": {
        "name": str,
        "email": str,
        "phone": str,
        "github_url": str | None,
        "linkedin_url": str | None,
        "education": str | None,
        "skills": str | None,
        "project1_title": str | None,
        "project1_desc": str | None,
        "project1_url": str | None,
        # ... (project2, project3)
        "cert1_name": str | None,
        "cert1_org": str | None,
        "cert1_year": str | None,
        # ... (cert2, cert3)
    }
}
```

**Guard Clause**: BR-10 - Redirect to form if no profile exists

---

## Internal APIs (Python Functions)

### database.init_db()
**Purpose**: Initialize the SQLite database and create the profile table

**Signature**:
```python
def init_db() -> None
```

**Parameters**: None

**Returns**: None

**Behavior**:
- Creates `resume_portfolio.db` if it doesn't exist
- Executes CREATE TABLE IF NOT EXISTS
- Safe to call multiple times (idempotent)
- Prints confirmation message to console

**Side Effects**:
- Creates database file in current directory
- Creates `profile` table with 27 columns

---

### database.save_data(data)
**Purpose**: Insert a new profile into the database

**Signature**:
```python
def save_data(data: dict) -> None
```

**Parameters**:
- `data` (dict): Profile data with keys matching column names

**Returns**: None

**Behavior**:
- Fills missing keys with None via `_fill_defaults()`
- Inserts row with id=1
- Commits transaction
- Prints confirmation message

**Preconditions**:
- No profile with id=1 exists (otherwise raises IntegrityError)

**Side Effects**:
- Inserts one row into `profile` table
- Commits database transaction

---

### database.get_data()
**Purpose**: Retrieve the stored profile from the database

**Signature**:
```python
def get_data() -> dict | None
```

**Parameters**: None

**Returns**:
- `dict`: Profile data if exists
- `None`: If no profile found

**Behavior**:
- Queries for row with id=1
- Converts sqlite3.Row to plain dict
- Returns None if no row found

**Side Effects**: None (read-only)

---

### database.update_data(data)
**Purpose**: Update the existing profile with new data

**Signature**:
```python
def update_data(data: dict) -> None
```

**Parameters**:
- `data` (dict): New profile data with keys matching column names

**Returns**: None

**Behavior**:
- Fills missing keys with None via `_fill_defaults()`
- Updates all 27 columns for row with id=1
- Commits transaction
- Prints confirmation message

**Preconditions**:
- Profile with id=1 must exist (otherwise UPDATE affects 0 rows)

**Side Effects**:
- Updates one row in `profile` table
- Commits database transaction

---

### database._fill_defaults(data)
**Purpose**: Ensure all expected keys exist in the data dictionary

**Signature**:
```python
def _fill_defaults(data: dict) -> dict
```

**Parameters**:
- `data` (dict): Raw form data (may have missing keys)

**Returns**:
- `dict`: New dictionary with all 27 keys present

**Behavior**:
- Iterates through expected_keys list
- For each key: uses value from data if present, else None
- Converts empty strings to None for optional fields

**Side Effects**: None (pure function)

---

## Data Models

### Profile Model
**Table**: `profile`

**Schema**:
```sql
CREATE TABLE profile (
    id              INTEGER PRIMARY KEY,   -- Always 1 (single-user)
    
    -- Personal Information
    name            TEXT    NOT NULL,
    email           TEXT    NOT NULL,
    phone           TEXT    NOT NULL,
    github_url      TEXT,
    linkedin_url    TEXT,
    
    -- Education
    education       TEXT,
    
    -- Skills
    skills          TEXT,
    
    -- Project 1
    project1_title  TEXT,
    project1_desc   TEXT,
    project1_url    TEXT,
    
    -- Project 2
    project2_title  TEXT,
    project2_desc   TEXT,
    project2_url    TEXT,
    
    -- Project 3
    project3_title  TEXT,
    project3_desc   TEXT,
    project3_url    TEXT,
    
    -- Certification 1
    cert1_name      TEXT,
    cert1_org       TEXT,
    cert1_year      TEXT,
    
    -- Certification 2
    cert2_name      TEXT,
    cert2_org       TEXT,
    cert2_year      TEXT,
    
    -- Certification 3
    cert3_name      TEXT,
    cert3_org       TEXT,
    cert3_year      TEXT
);
```

**Fields**:
- **id** (INTEGER, PRIMARY KEY): Always 1 (single-user constraint)
- **name** (TEXT, NOT NULL): User's full name
- **email** (TEXT, NOT NULL): Email address
- **phone** (TEXT, NOT NULL): Phone number
- **github_url** (TEXT, nullable): GitHub profile URL
- **linkedin_url** (TEXT, nullable): LinkedIn profile URL
- **education** (TEXT, nullable): Free-text education details
- **skills** (TEXT, nullable): Comma-separated skills list
- **project[1-3]_title** (TEXT, nullable): Project title
- **project[1-3]_desc** (TEXT, nullable): Project description
- **project[1-3]_url** (TEXT, nullable): Project URL
- **cert[1-3]_name** (TEXT, nullable): Certification name
- **cert[1-3]_org** (TEXT, nullable): Issuing organization
- **cert[1-3]_year** (TEXT, nullable): Year obtained

**Relationships**: None (single table, no foreign keys)

**Validation**:
- **Database Level**: NOT NULL constraints on name, email, phone
- **Application Level**: Client-side validation in form.js
- **Business Rules**:
  - BR-01: Required fields must be non-empty
  - BR-02: Email must match valid format
  - BR-03: URLs must start with http:// or https://

**Indexes**: None (single-row table, no performance concerns)

**Constraints**:
- PRIMARY KEY on id (enforces uniqueness)
- Single-user design: Only id=1 is ever used

---

## Client-Side Validation API (form.js)

### validateForm(event)
**Purpose**: Validate form before submission

**Signature**:
```javascript
function validateForm(event: Event): void
```

**Parameters**:
- `event` (Event): Form submit event

**Returns**: void

**Behavior**:
1. Clear previous error messages
2. Validate required fields (name, email, phone)
3. Validate email format
4. Validate optional URL fields (if non-empty)
5. If any validation fails:
   - Prevent form submission (event.preventDefault())
   - Scroll to first error
6. If all pass: Allow form submission

**Side Effects**:
- Adds/removes `.input-error` class on inputs
- Updates error message spans
- Prevents default form submission if invalid

---

### validateRequired(fieldId, errorId, message)
**Purpose**: Check that a required field is non-empty

**Signature**:
```javascript
function validateRequired(
    fieldId: string, 
    errorId: string, 
    message: string
): boolean
```

**Parameters**:
- `fieldId`: ID of input element
- `errorId`: ID of error span element
- `message`: Error message to display

**Returns**:
- `true`: Field has value
- `false`: Field is empty

---

### validateOptionalUrl(fieldId, errorId, message)
**Purpose**: Validate URL format if field is non-empty

**Signature**:
```javascript
function validateOptionalUrl(
    fieldId: string, 
    errorId: string, 
    message: string
): boolean
```

**Parameters**:
- `fieldId`: ID of input element
- `errorId`: ID of error span element
- `message`: Error message to display

**Returns**:
- `true`: Field is empty OR valid URL
- `false`: Field has invalid URL format

---

### validateEmail(value)
**Purpose**: Test if string matches email format

**Signature**:
```javascript
function validateEmail(value: string): boolean
```

**Parameters**:
- `value`: Email string to test

**Returns**:
- `true`: Valid email format
- `false`: Invalid format

**Regex**: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`

---

### validateUrl(value)
**Purpose**: Test if string is valid http/https URL

**Signature**:
```javascript
function validateUrl(value: string): boolean
```

**Parameters**:
- `value`: URL string to test

**Returns**:
- `true`: Starts with http:// or https://
- `false`: Invalid URL format

**Regex**: `/^https?:\/\/.+/`

---

## API Flow Diagrams

### Create Profile Flow
```
User fills form
    |
    v
Client validation (form.js)
    |
    +-- Invalid --> Show errors, block submission
    |
    v
POST /save
    |
    v
Extract form data (app.py)
    |
    v
Check if profile exists (get_data())
    |
    +-- Exists --> update_data() --> UPDATE SQL
    |
    +-- Not exists --> save_data() --> INSERT SQL
    |
    v
Redirect 302 to /view
    |
    v
GET /view
    |
    v
Render resume page
```

### View Resume Flow
```
User clicks "View Resume"
    |
    v
GET /view
    |
    v
get_data()
    |
    +-- Profile exists --> Render view.html with data
    |
    +-- No profile --> Redirect 302 to / (form)
```
