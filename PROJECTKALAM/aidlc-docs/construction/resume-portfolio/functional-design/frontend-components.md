# Frontend Components
# Resume + Portfolio Builder

---

## Component 1: Navigation Bar

**Present on**: Both pages

**Elements**:
- App title / logo text: "Resume + Portfolio Builder"
- Link: "Home" → `/`
- Link: "View Resume" → `/view`

**CSS class**: `.navbar`

---

## Component 2: Input Form (`index.html`)

**Route**: `GET /`  |  **Submits to**: `POST /save`

### Form Sections & Fields

```
[Personal Information]
  - Name *              <input type="text"  name="name">
  - Email *             <input type="email" name="email">
  - Phone *             <input type="tel"   name="phone">
  - GitHub URL          <input type="url"   name="github_url">
  - LinkedIn URL        <input type="url"   name="linkedin_url">

[Education]
  - Education           <textarea name="education">

[Skills]
  - Skills              <textarea name="skills">
                        placeholder: "Python, HTML, CSS, JavaScript..."

[Projects]  (3 fixed groups)
  Project 1:
    - Title             <input type="text" name="project1_title">
    - Description       <textarea         name="project1_desc">
    - Link (optional)   <input type="url" name="project1_url">
  Project 2: (same pattern, project2_*)
  Project 3: (same pattern, project3_*)

[Certifications]  (3 fixed groups)
  Certification 1:
    - Name              <input type="text" name="cert1_name">
    - Organization      <input type="text" name="cert1_org">
    - Year              <input type="text" name="cert1_year">
  Certification 2: (same pattern, cert2_*)
  Certification 3: (same pattern, cert3_*)

[Submit Button]
  <button type="submit">Generate Resume & Portfolio</button>
```

### Pre-population Pattern (Jinja2)

```html
<!-- Required field -->
<input type="text" name="name"
       value="{{ profile.name if profile else '' }}"
       id="name" required>

<!-- Optional field -->
<input type="url" name="github_url"
       value="{{ profile.github_url or '' }}"
       id="github_url">

<!-- Textarea -->
<textarea name="education" id="education">
  {{- profile.education if profile else '' -}}
</textarea>
```

### Validation State (managed by form.js)

| Field | Validation | Error Element ID |
|---|---|---|
| `name` | Non-empty | `#name-error` |
| `email` | Non-empty + regex | `#email-error` |
| `phone` | Non-empty | `#phone-error` |
| `github_url` | URL regex (if non-empty) | `#github-error` |
| `linkedin_url` | URL regex (if non-empty) | `#linkedin-error` |
| `project1_url` | URL regex (if non-empty) | `#project1-url-error` |
| `project2_url` | URL regex (if non-empty) | `#project2-url-error` |
| `project3_url` | URL regex (if non-empty) | `#project3-url-error` |

Error elements are `<span class="error-msg" id="...">` placed immediately after each input.

---

## Component 3: Resume Section (`view.html`)

**CSS class**: `.resume-section`

### Layout

```
+------------------------------------------+
|  [Name]                                  |
|  [Email] | [Phone]                        |
|  [GitHub link?]  [LinkedIn link?]         |
+------------------------------------------+
|  EDUCATION                               |
|  [education text]                        |
+------------------------------------------+
|  SKILLS                                  |
|  [skills text]                           |
+------------------------------------------+
|  PROJECTS                                |
|  Project 1: [title] — [desc] [link?]     |
|  Project 2: [title] — [desc] [link?]     |
|  Project 3: [title] — [desc] [link?]     |
+------------------------------------------+
|  CERTIFICATIONS                          |
|  [cert1_name], [cert1_org], [cert1_year] |
|  [cert2_name], [cert2_org], [cert2_year] |
|  [cert3_name], [cert3_org], [cert3_year] |
+------------------------------------------+
|  [Download as PDF]  [Edit Details]       |
+------------------------------------------+
```

### Conditional Rendering Rules

```html
{% if profile.github_url %}
  <a href="{{ profile.github_url }}" target="_blank">GitHub</a>
{% endif %}

{% if profile.linkedin_url %}
  <a href="{{ profile.linkedin_url }}" target="_blank">LinkedIn</a>
{% endif %}

{% if profile.project1_title %}
  <div class="project-item">
    <strong>{{ profile.project1_title }}</strong> — {{ profile.project1_desc }}
    {% if profile.project1_url %}
      <a href="{{ profile.project1_url }}" target="_blank">View Project</a>
    {% endif %}
  </div>
{% endif %}
```

---

## Component 4: Portfolio Section (`view.html`)

**CSS class**: `.portfolio-section`  
**Hidden in print** via `print.css`

### Sections

| Section | Content | CSS class |
|---|---|---|
| About Me | Name, email, phone, GitHub link, LinkedIn link | `.portfolio-about` |
| Education | education text | `.portfolio-education` |
| Skills | Skills rendered as badge/tag spans | `.portfolio-skills` |
| Projects | 3 project cards (title, desc, optional link) | `.portfolio-projects` |
| Contact | Email, phone, GitHub link, LinkedIn link | `.portfolio-contact` |

### Skills Badge Rendering

```html
{% for skill in profile.skills.replace('\n', ',').split(',') %}
  {% set skill_clean = skill.strip() %}
  {% if skill_clean %}
    <span class="skill-badge">{{ skill_clean }}</span>
  {% endif %}
{% endfor %}
```

---

## Component 5: Action Buttons (`view.html`)

| Button | Label | Action | Hidden in Print |
|---|---|---|---|
| Download PDF | "Download as PDF" | `onclick="window.print()"` | Yes |
| Edit | "Edit Details" | `href="/"` | Yes |

**CSS classes**: `.btn-download`, `.btn-edit`

---

## User Interaction Flows

### Flow 1: First Visit
```
/ (empty form) → fill fields → submit → /view (resume + portfolio)
```

### Flow 2: Edit
```
/view → click "Edit Details" → / (pre-populated form) → modify → submit → /view (updated)
```

### Flow 3: PDF Download
```
/view → click "Download as PDF" → browser print dialog → save PDF
```

### Flow 4: Navigation
```
Any page → click "Home" in navbar → /
Any page → click "View Resume" in navbar → /view (or redirect to / if no data)
```
