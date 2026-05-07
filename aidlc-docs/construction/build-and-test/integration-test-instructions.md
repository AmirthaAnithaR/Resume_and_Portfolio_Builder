# Integration Test Instructions
# Resume + Portfolio Builder

---

## Purpose

Integration tests verify that all components work together correctly as a complete system — the form, Flask routes, database layer, and templates all interacting end-to-end.

Since this is a single-process local application (no microservices, no external APIs), integration testing means running the full Flask app and exercising complete user workflows.

---

## Setup

The Flask test client (used in unit tests) also serves as the integration test harness — it exercises the full request/response cycle including template rendering and database I/O.

```bash
cd resume-portfolio-builder
pip install pytest==8.2.0   # if not already installed
```

---

## Integration Test Scenarios

### Scenario 1: Complete First-Time User Flow

**Description**: User visits for the first time, fills the form, submits, and sees their resume and portfolio.

**Test Steps**:
1. `GET /` → expect 200, empty form
2. `POST /save` with full profile data → expect redirect to `/view`
3. `GET /view` → expect 200, name visible, resume section present, portfolio section present

**Expected Results**:
- Data persisted to SQLite
- Resume shows all entered fields
- Portfolio shows skills as badges
- GitHub/LinkedIn links visible (if provided)

---

### Scenario 2: Edit and Re-submit Flow

**Description**: User returns to the form, changes their name and email, re-submits.

**Test Steps**:
1. `POST /save` with original data
2. `GET /` → form must be pre-populated with original data
3. `POST /save` with updated name/email
4. `GET /view` → updated name/email must appear

**Expected Results**:
- Only one row in the database (no duplicates)
- View page reflects the updated values

---

### Scenario 3: Optional Fields — Absent Then Added

**Description**: User submits without GitHub/LinkedIn, then edits and adds them.

**Test Steps**:
1. `POST /save` with `github_url=""`, `linkedin_url=""`
2. `GET /view` → GitHub/LinkedIn links must NOT appear
3. `POST /save` with `github_url="https://github.com/test"`, `linkedin_url="https://linkedin.com/in/test"`
4. `GET /view` → GitHub/LinkedIn links must appear

**Expected Results**:
- BR-05: Empty strings stored as NULL
- BR-06: Links conditionally rendered based on NULL vs value

---

### Scenario 4: View Guard — No Data

**Description**: User navigates directly to `/view` before submitting any data.

**Test Steps**:
1. Fresh database (no profile)
2. `GET /view` → expect redirect to `/`
3. `GET /` → expect 200, empty form

**Expected Results**:
- BR-10 enforced: no crash, clean redirect

---

### Scenario 5: PDF Print Scope

**Description**: Verify print CSS hides the correct elements.

**Manual Test Steps**:
1. Run the app and submit sample data
2. Navigate to `/view`
3. Open browser DevTools → Rendering → Emulate CSS media: print
4. Verify `.portfolio-section` is hidden
5. Verify `.navbar` is hidden
6. Verify `.btn-download` and `.btn-edit` are hidden
7. Verify `.resume-section` is fully visible

**Expected Results**:
- Only the resume section is visible in print preview

---

## Run Integration Tests

Add this file as `resume-portfolio-builder/test_integration.py`:

```python
"""
test_integration.py — Integration tests for Resume + Portfolio Builder
Run with: pytest test_integration.py -v
"""

import pytest
from database import init_db, save_data, get_data
import app as flask_app

FULL_PROFILE = {
    "name": "Ayesha Khan", "email": "ayesha@email.com", "phone": "+92-300-1234567",
    "github_url": "https://github.com/ayeshakhan",
    "linkedin_url": "https://linkedin.com/in/ayeshakhan",
    "education": "BS CS, FAST-NUCES, 2024", "skills": "Python, HTML, CSS",
    "project1_title": "Student Portal", "project1_desc": "Web app", "project1_url": "",
    "project2_title": "", "project2_desc": "", "project2_url": "",
    "project3_title": "", "project3_desc": "", "project3_url": "",
    "cert1_name": "Python for Everybody", "cert1_org": "Coursera", "cert1_year": "2023",
    "cert2_name": "", "cert2_org": "", "cert2_year": "",
    "cert3_name": "", "cert3_org": "", "cert3_year": "",
}

@pytest.fixture
def client(monkeypatch, tmp_path):
    test_db = str(tmp_path / "integration_test.db")
    monkeypatch.setattr("database.DB_PATH", test_db)
    init_db()
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c


def test_full_first_time_user_flow(client):
    """Scenario 1: empty form → submit → view resume + portfolio."""
    r1 = client.get("/")
    assert r1.status_code == 200
    assert b"profile-form" in r1.data

    r2 = client.post("/save", data=FULL_PROFILE)
    assert r2.status_code == 302
    assert "/view" in r2.headers["Location"]

    r3 = client.get("/view")
    assert r3.status_code == 200
    assert b"Ayesha Khan" in r3.data
    assert b"resume-section" in r3.data
    assert b"portfolio-section" in r3.data


def test_edit_and_resubmit_flow(client):
    """Scenario 2: submit → edit → resubmit → updated data shown."""
    client.post("/save", data=FULL_PROFILE)

    r_form = client.get("/")
    assert b"Ayesha Khan" in r_form.data   # pre-populated

    updated = dict(FULL_PROFILE)
    updated["name"] = "Sara Ahmed"
    client.post("/save", data=updated)

    r_view = client.get("/view")
    assert b"Sara Ahmed" in r_view.data
    assert b"Ayesha Khan" not in r_view.data

    profile = get_data()
    assert profile["id"] == 1   # still one row


def test_optional_fields_absent_then_added(client):
    """Scenario 3: no GitHub → submit → no link; add GitHub → submit → link shown."""
    no_github = dict(FULL_PROFILE)
    no_github["github_url"] = ""
    client.post("/save", data=no_github)
    r1 = client.get("/view")
    assert b"github.com/ayeshakhan" not in r1.data

    with_github = dict(FULL_PROFILE)
    with_github["github_url"] = "https://github.com/ayeshakhan"
    client.post("/save", data=with_github)
    r2 = client.get("/view")
    assert b"github.com/ayeshakhan" in r2.data


def test_view_guard_no_data(client):
    """Scenario 4: GET /view with no data must redirect to /."""
    r = client.get("/view")
    assert r.status_code == 302
    assert "/" in r.headers["Location"]
```

```bash
pytest test_integration.py -v
```

**Expected output:**
```
test_integration.py::test_full_first_time_user_flow PASSED
test_integration.py::test_edit_and_resubmit_flow PASSED
test_integration.py::test_optional_fields_absent_then_added PASSED
test_integration.py::test_view_guard_no_data PASSED
========================= 4 passed in X.XXs =========================
```
