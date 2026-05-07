# Services

## Overview
This document defines service layer components for orchestration and business logic coordination. Services are optional helper modules that organize complex logic.

---

## Service Architecture Decision

**Approach**: **Minimal Service Layer** - Keep logic in route handlers and helper functions

**Rationale**:
- Beginner-friendly requirement favors simplicity
- Flask application is small and straightforward
- Avoid over-engineering for a learning project
- Business logic is not complex enough to warrant separate service classes

**Pattern**: Helper functions in app.py or separate utils module (if needed)

---

## Helper Functions (Instead of Services)

### 1. Template Selection Helpers

#### `get_template_filename(template_choice)`
**Purpose**: Map template choice to template filename  
**Location**: app.py (helper function)  
**Input**: `template_choice` (str: "template1", "template2", "template3" or None)  
**Output**: Template filename (str: "resume-template1.html", etc.)  
**Logic**:
```python
def get_template_filename(template_choice):
    """Map template choice to filename, default to template1"""
    template_map = {
        'template1': 'resume-template1.html',
        'template2': 'resume-template2.html',
        'template3': 'resume-template3.html',
    }
    return template_map.get(template_choice, 'resume-template1.html')
```

---

#### `get_default_template_choice()`
**Purpose**: Return default template if user hasn't selected one  
**Location**: app.py (helper function)  
**Input**: None  
**Output**: Default template choice (str: "template1")  
**Logic**:
```python
def get_default_template_choice():
    """Return default template choice"""
    return 'template1'
```

---

### 2. Form Data Helpers

#### `extract_form_data(request_form)`
**Purpose**: Extract and clean form data from request  
**Location**: app.py (helper function)  
**Input**: `request.form` (ImmutableMultiDict)  
**Output**: dict with cleaned form data  
**Logic**:
```python
def extract_form_data(request_form):
    """Extract all form fields and strip whitespace"""
    fields = [
        'name', 'email', 'phone', 'github_url', 'linkedin_url',
        'education', 'skills',
        'project1_title', 'project1_desc', 'project1_url',
        'project2_title', 'project2_desc', 'project2_url',
        'project3_title', 'project3_desc', 'project3_url',
        'cert1_name', 'cert1_org', 'cert1_year',
        'cert2_name', 'cert2_org', 'cert2_year',
        'cert3_name', 'cert3_org', 'cert3_year',
        'summary',  # New optional field
    ]
    
    data = {}
    for field in fields:
        value = request_form.get(field, '').strip()
        data[field] = value if value else None
    
    return data
```

---

### 3. Validation Helpers (Optional Server-Side)

#### `validate_required_fields(data)`
**Purpose**: Validate required fields on server-side  
**Location**: app.py (helper function) - OPTIONAL  
**Input**: `data` (dict with form data)  
**Output**: tuple (bool is_valid, list errors)  
**Logic**:
```python
def validate_required_fields(data):
    """Validate required fields (server-side backup)"""
    errors = []
    
    if not data.get('name'):
        errors.append('Name is required')
    if not data.get('email'):
        errors.append('Email is required')
    if not data.get('phone'):
        errors.append('Phone is required')
    
    # Email format validation (basic)
    if data.get('email') and '@' not in data['email']:
        errors.append('Invalid email format')
    
    return (len(errors) == 0, errors)
```

**Note**: This is optional since client-side validation is primary. Can be added for security.

---

### 4. Data Formatting Helpers

#### `format_skills_list(skills_text)`
**Purpose**: Parse skills text into list  
**Location**: Could be Jinja2 filter or Python helper  
**Input**: `skills_text` (str: comma or newline separated)  
**Output**: list of skill strings  
**Logic**:
```python
def format_skills_list(skills_text):
    """Parse skills text into list"""
    if not skills_text:
        return []
    
    # Try comma-separated first
    if ',' in skills_text:
        skills = [s.strip() for s in skills_text.split(',')]
    else:
        # Try newline-separated
        skills = [s.strip() for s in skills_text.split('\n')]
    
    # Filter out empty strings
    return [s for s in skills if s]
```

**Alternative**: Implement as Jinja2 filter in templates

---

#### `truncate_text(text, max_length)`
**Purpose**: Truncate long text with ellipsis  
**Location**: Jinja2 filter (built-in) or custom filter  
**Input**: `text` (str), `max_length` (int)  
**Output**: Truncated string  
**Logic**: Use Jinja2's built-in `truncate` filter or create custom

---

## Service Layer Summary

**Decision**: **No formal service layer** - use helper functions instead

**Rationale**:
- ✅ Simpler architecture (beginner-friendly)
- ✅ Less boilerplate code
- ✅ Easier to understand and maintain
- ✅ Sufficient for application complexity
- ✅ Follows Flask best practices for small apps

**Helper Functions Location**:
- **app.py**: Route-related helpers (template selection, form data extraction)
- **database.py**: Data access helpers (already exists)
- **Jinja2 filters**: Template-related helpers (text formatting, list parsing)
- **JavaScript**: Client-side helpers (form wizard, validation, preview)

---

## Orchestration Patterns

### Pattern 1: Form Submission Flow
```
User submits form
    ↓
POST /save route handler
    ↓
extract_form_data(request.form)  [Helper function]
    ↓
validate_required_fields(data)  [Optional helper]
    ↓
get_data()  [Database function]
    ↓
save_data(data) or update_data(data)  [Database function]
    ↓
Redirect to /select-template
```

**Orchestration**: Route handler coordinates helper functions and database calls

---

### Pattern 2: Template Selection Flow
```
User selects template
    ↓
GET /select-template?template=X route handler
    ↓
get_data()  [Database function]
    ↓
Update data['template_choice'] = X
    ↓
update_data(data)  [Database function]
    ↓
Redirect to /view
```

**Orchestration**: Route handler coordinates database calls

---

### Pattern 3: Resume Rendering Flow
```
User visits /view
    ↓
GET /view route handler
    ↓
get_data()  [Database function]
    ↓
get_template_filename(profile['template_choice'])  [Helper function]
    ↓
render_template('view.html', profile=profile, template_file=template_file)
    ↓
view.html includes selected resume template
    ↓
Resume template renders with profile data
```

**Orchestration**: Route handler + Jinja2 template engine

---

## Alternative: Service Classes (Not Recommended)

If the application grows more complex in the future, consider these service classes:

### ResumeService (Future Enhancement)
```python
class ResumeService:
    """Service for resume-related operations"""
    
    def get_resume_data(self, profile_id):
        """Get profile data for resume"""
        pass
    
    def render_resume(self, profile, template_choice):
        """Render resume with selected template"""
        pass
    
    def generate_pdf(self, profile, template_choice):
        """Generate PDF from resume (future)"""
        pass
```

### TemplateService (Future Enhancement)
```python
class TemplateService:
    """Service for template-related operations"""
    
    def get_available_templates(self):
        """Get list of available templates"""
        pass
    
    def get_template_metadata(self, template_id):
        """Get template name, description, preview"""
        pass
    
    def render_preview(self, template_id, profile):
        """Render template preview"""
        pass
```

### ValidationService (Future Enhancement)
```python
class ValidationService:
    """Service for validation operations"""
    
    def validate_profile_data(self, data):
        """Validate all profile fields"""
        pass
    
    def validate_email(self, email):
        """Validate email format"""
        pass
    
    def validate_url(self, url):
        """Validate URL format"""
        pass
```

**Note**: These are **NOT** implemented in the current design. Keep it simple with helper functions.

---

## Summary

**Service Layer Approach**: Minimal - use helper functions instead of service classes

**Helper Functions**:
- Template selection helpers (2 functions)
- Form data helpers (1 function)
- Validation helpers (1 optional function)
- Data formatting helpers (2 functions, possibly as Jinja2 filters)

**Orchestration**: Route handlers coordinate helper functions and database calls

**Future Enhancement**: If application grows, refactor helper functions into service classes

**Rationale**: Simplicity and beginner-friendliness over architectural purity
