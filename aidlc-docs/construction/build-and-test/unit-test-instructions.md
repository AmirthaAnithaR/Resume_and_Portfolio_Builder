# Unit Test Instructions
# Resume + Portfolio Builder

---

## Overview

Unit tests verify each component in isolation. For this project the most valuable unit tests cover:

1. **`database.py`** — CRUD functions and NULL normalization logic
2. **`app.py`** — Flask route behaviour (form rendering, save/update decision, redirects)
3. **`form.js`** — Client-side validation logic

---

## Setup

Install the test dependency (pytest):

```bash
cd resume-portfolio-builder
pip install pytest==8.2.0
```

Create the test file:

```bash
# Windows
type nul > test_app.py

# macOS / Linux
touch test_app.py
```

---

## Test File: `test_app.py`

Copy this complete test file into `resume-portfolio-builder/test_app.py`:

```python
"""
test_app.py — Unit tests for Resume + Portfolio Builder
Run with: pytest test_app.py -v
"""

import pytest
import os
import tempfile
from database import init_db, save_data, get_data, update_data, _fill_defaults, DB_PATH
import app as flask_app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def temp_db(monkeypatch, tmp_path):
    """
    Redirect the database to a temporary file for each test.
    Ensures tests don't affect the real resume_portfolio.db.
    """
    test_db = str(tmp_path / "test.db")
    monkeypatch.setattr("database.DB_PATH", test_db)
    init_db()
    yield test_db


@pytest.fixture
def client(temp_db):
    """
    Flask test client with a fresh temporary database.
    """
    flask_app.app.config["TESTING"] = True
    flask_app.app.config["WTF_CSRF_ENABLED"] = False
    with flask_app.app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE_DATA = {
    "name": "Ayesha Khan",
    "email": "ayesha@email.com",
    "phone": "+92-300-1234567",
    "github_url": "https://github.com/ayeshakhan",
    "linkedin_url": "https://linkedin.com/in/ayeshakhan",
    "education": "BS Computer Science, FAST-NUCES, 2024",
    "skills": "Python, HTML, CSS",
    "project1_title": "Student Portal",
    "project1_desc": "A web app for managing student records",
    "project1_url": "https://github.com/ayeshakhan/portal",
    "project2_title": "Weather App",
    "project2_desc": "Fetches live weather data",
    "project2_url": "",
    "project3_title": "",
    "project3_desc": "",
    "project3_url": "",
    "cert1_name": "Python for Everybody",
    "cert1_org": "Coursera",
    "cert1_year": "2023",
    "cert2_name": "",
    "cert2_org": "",
    "cert2_year": "",
    "cert3_name": "",
    "cert3_org": "",
    "cert3_year": "",
}


# ---------------------------------------------------------------------------
# database.py — Unit Tests
# ---------------------------------------------------------------------------

class TestFillDefaults:
    """Tests for the _fill_defaults() normalization helper."""

    def test_empty_string_becomes_none(self):
        """BR-05: Empty strings must be converted to None."""
        data = {"name": "Ali", "email": "ali@test.com", "phone": "123",
                "github_url": "", "linkedin_url": ""}
        result = _fill_defaults(data)
        assert result["github_url"] is None
        assert result["linkedin_url"] is None

    def test_non_empty_value_preserved(self):
        """Non-empty values must not be changed."""
        data = {"name": "Ali", "email": "ali@test.com", "phone": "123",
                "github_url": "https://github.com/ali"}
        result = _fill_defaults(data)
        assert result["github_url"] == "https://github.com/ali"

    def test_missing_key_becomes_none(self):
        """Keys absent from input dict must default to None."""
        result = _fill_defaults({"name": "Ali", "email": "a@b.com", "phone": "1"})
        assert result["project1_url"] is None
        assert result["cert3_year"] is None

    def test_all_expected_keys_present(self):
        """Output dict must contain all 25 expected column keys."""
        result = _fill_defaults({})
        expected_keys = [
            "name", "email", "phone", "github_url", "linkedin_url",
            "education", "skills",
            "project1_title", "project1_desc", "project1_url",
            "project2_title", "project2_desc", "project2_url",
            "project3_title", "project3_desc", "project3_url",
            "cert1_name", "cert1_org", "cert1_year",
            "cert2_name", "cert2_org", "cert2_year",
            "cert3_name", "cert3_org", "cert3_year",
        ]
        for key in expected_keys:
            assert key in result


class TestDatabaseCRUD:
    """Tests for save_data(), get_data(), update_data()."""

    def test_get_data_returns_none_when_empty(self, temp_db):
        """BR-10 dependency: get_data() returns None before any save."""
        assert get_data() is None

    def test_save_data_persists_profile(self, temp_db):
        """save_data() must store the profile and get_data() must retrieve it."""
        save_data(SAMPLE_DATA)
        profile = get_data()
        assert profile is not None
        assert profile["name"] == "Ayesha Khan"
        assert profile["email"] == "ayesha@email.com"

    def test_save_data_stores_optional_fields(self, temp_db):
        """Optional fields with values must be stored correctly."""
        save_data(SAMPLE_DATA)
        profile = get_data()
        assert profile["github_url"] == "https://github.com/ayeshakhan"
        assert profile["project1_title"] == "Student Portal"

    def test_save_data_stores_null_for_empty_optional(self, temp_db):
        """BR-05: Empty optional fields must be stored as NULL."""
        save_data(SAMPLE_DATA)
        profile = get_data()
        assert profile["project2_url"] is None   # was "" in SAMPLE_DATA
        assert profile["project3_title"] is None

    def test_update_data_overwrites_profile(self, temp_db):
        """BR-04: update_data() must overwrite all fields."""
        save_data(SAMPLE_DATA)
        updated = dict(SAMPLE_DATA)
        updated["name"] = "Sara Ahmed"
        updated["email"] = "sara@email.com"
        update_data(updated)
        profile = get_data()
        assert profile["name"] == "Sara Ahmed"
        assert profile["email"] == "sara@email.com"

    def test_update_data_clears_removed_optional_field(self, temp_db):
        """Removing an optional field on re-submit must store NULL."""
        save_data(SAMPLE_DATA)
        updated = dict(SAMPLE_DATA)
        updated["github_url"] = ""   # user cleared the field
        update_data(updated)
        profile = get_data()
        assert profile["github_url"] is None

    def test_single_profile_constraint(self, temp_db):
        """BR-07: Only one profile row should ever exist."""
        save_data(SAMPLE_DATA)
        update_data(SAMPLE_DATA)   # should update, not insert second row
        profile = get_data()
        assert profile["id"] == 1


# ---------------------------------------------------------------------------
# app.py — Flask Route Tests
# ---------------------------------------------------------------------------

class TestIndexRoute:
    """Tests for GET /"""

    def test_index_returns_200(self, client):
        """Home page must return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_index_shows_form(self, client):
        """Home page must contain the form element."""
        response = client.get("/")
        assert b"profile-form" in response.data

    def test_index_prepopulates_when_data_exists(self, client, temp_db):
        """BR-08: Form must be pre-populated when profile exists."""
        save_data(SAMPLE_DATA)
        response = client.get("/")
        assert b"Ayesha Khan" in response.data


class TestSaveRoute:
    """Tests for POST /save"""

    def test_save_redirects_to_view(self, client):
        """BR-09: POST /save must redirect to /view."""
        response = client.post("/save", data=SAMPLE_DATA)
        assert response.status_code == 302
        assert "/view" in response.headers["Location"]

    def test_save_persists_data(self, client, temp_db):
        """POST /save must store data in the database."""
        client.post("/save", data=SAMPLE_DATA)
        profile = get_data()
        assert profile is not None
        assert profile["name"] == "Ayesha Khan"

    def test_save_calls_update_on_resubmit(self, client, temp_db):
        """BR-04: Second POST /save must update, not duplicate."""
        client.post("/save", data=SAMPLE_DATA)
        updated = dict(SAMPLE_DATA)
        updated["name"] = "Sara Ahmed"
        client.post("/save", data=updated)
        profile = get_data()
        assert profile["name"] == "Sara Ahmed"
        assert profile["id"] == 1   # still only one row


class TestViewRoute:
    """Tests for GET /view"""

    def test_view_redirects_when_no_data(self, client):
        """BR-10: GET /view must redirect to / when no profile exists."""
        response = client.get("/view")
        assert response.status_code == 302
        assert "/" in response.headers["Location"]

    def test_view_returns_200_when_data_exists(self, client, temp_db):
        """GET /view must return 200 when profile exists."""
        save_data(SAMPLE_DATA)
        response = client.get("/view")
        assert response.status_code == 200

    def test_view_shows_name(self, client, temp_db):
        """Resume page must display the stored name."""
        save_data(SAMPLE_DATA)
        response = client.get("/view")
        assert b"Ayesha Khan" in response.data

    def test_view_shows_github_link_when_present(self, client, temp_db):
        """BR-06: GitHub link must appear when github_url is stored."""
        save_data(SAMPLE_DATA)
        response = client.get("/view")
        assert b"github.com/ayeshakhan" in response.data

    def test_view_hides_github_link_when_absent(self, client, temp_db):
        """BR-06: GitHub link must NOT appear when github_url is NULL."""
        data = dict(SAMPLE_DATA)
        data["github_url"] = ""
        save_data(data)
        response = client.get("/view")
        assert b"github.com/ayeshakhan" not in response.data

    def test_view_shows_portfolio_section(self, client, temp_db):
        """Portfolio section must be present on the view page."""
        save_data(SAMPLE_DATA)
        response = client.get("/view")
        assert b"portfolio-section" in response.data
```

---

## Run the Tests

```bash
cd resume-portfolio-builder
pytest test_app.py -v
```

**Expected output:**
```
test_app.py::TestFillDefaults::test_empty_string_becomes_none PASSED
test_app.py::TestFillDefaults::test_non_empty_value_preserved PASSED
test_app.py::TestFillDefaults::test_missing_key_becomes_none PASSED
test_app.py::TestFillDefaults::test_all_expected_keys_present PASSED
test_app.py::TestDatabaseCRUD::test_get_data_returns_none_when_empty PASSED
test_app.py::TestDatabaseCRUD::test_save_data_persists_profile PASSED
...
========================= 20 passed in X.XXs =========================
```

---

## Run with Coverage (Optional)

```bash
pip install pytest-cov==5.0.0
pytest test_app.py -v --cov=. --cov-report=term-missing
```

---

## Manual Validation Checklist

Run the app (`python app.py`) and verify these manually:

- [ ] Home page loads at `http://localhost:5000`
- [ ] Form shows empty fields on first visit
- [ ] Submitting without Name/Email/Phone shows inline error messages
- [ ] Submitting with an invalid email shows an error
- [ ] Submitting with an invalid URL (no https://) shows an error
- [ ] Valid form submission redirects to `/view`
- [ ] Resume section shows all entered data
- [ ] GitHub/LinkedIn links appear only when filled in
- [ ] Portfolio section shows skills as coloured badges
- [ ] "Edit Details" returns to pre-populated form
- [ ] Re-submitting updated data shows new values on `/view`
- [ ] "Download as PDF" opens browser print dialog
- [ ] PDF output contains only the resume (no portfolio, no navbar)
