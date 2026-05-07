"""
test_app.py — Resume + Portfolio Builder
-----------------------------------------
Unit tests for Flask routes in app.py.
Uses Flask's built-in test client — no real HTTP server needed.
The in-memory SQLite connection is managed by conftest.py.
Each test gets a clean (empty) profile table via the autouse clean_db fixture.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# conftest.py has already patched database.get_connection before this import
from app import app as flask_app
import database


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Create a Flask test client. DB cleanup is handled by conftest clean_db."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Sample form data (mirrors what the HTML form POSTs)
# ---------------------------------------------------------------------------

FORM_DATA = {
    "name":           "Ayesha Khan",
    "email":          "ayesha@email.com",
    "phone":          "+92-300-1234567",
    "github_url":     "https://github.com/ayeshakhan",
    "linkedin_url":   "",                              # intentionally blank
    "education":      "BS CS, FAST, 2024",
    "skills":         "Python, HTML",
    "project1_title": "Portal",
    "project1_desc":  "A portal app",
    "project1_url":   "",
    "project2_title": "",
    "project2_desc":  "",
    "project2_url":   "",
    "project3_title": "",
    "project3_desc":  "",
    "project3_url":   "",
    "cert1_name":     "Python for Everybody",
    "cert1_org":      "Coursera",
    "cert1_year":     "2023",
    "cert2_name":     "",
    "cert2_org":      "",
    "cert2_year":     "",
    "cert3_name":     "",
    "cert3_org":      "",
    "cert3_year":     "",
}


# ---------------------------------------------------------------------------
# Tests: GET / — Home / Form page
# ---------------------------------------------------------------------------

def test_index_returns_200(client):
    """GET / returns HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_index_renders_form(client):
    """GET / renders the profile input form."""
    response = client.get("/")
    assert b"profile-form" in response.data


def test_index_shows_empty_form_heading_when_no_data(client):
    """GET / shows 'Enter Your Details' heading when no profile saved yet."""
    response = client.get("/")
    assert b"Enter Your Details" in response.data


def test_index_prepopulates_form_when_data_exists(client):
    """GET / pre-populates form with stored data on return visit (BR-08)."""
    client.post("/save", data=FORM_DATA)
    response = client.get("/")
    assert b"Ayesha Khan" in response.data
    assert b"Edit Your Details" in response.data


# ---------------------------------------------------------------------------
# Tests: POST /save — Form submission
# ---------------------------------------------------------------------------

def test_save_redirects_to_view(client):
    """POST /save redirects to /view after saving (BR-09)."""
    response = client.post("/save", data=FORM_DATA)
    assert response.status_code == 302
    assert "/view" in response.headers["Location"]


def test_save_persists_data_to_database(client):
    """POST /save stores the submitted data in SQLite (FR-02)."""
    client.post("/save", data=FORM_DATA)
    profile = database.get_data()
    assert profile is not None
    assert profile["name"] == "Ayesha Khan"
    assert profile["email"] == "ayesha@email.com"


def test_save_updates_existing_data_on_resubmit(client):
    """POST /save overwrites existing data on re-submit (BR-04)."""
    client.post("/save", data=FORM_DATA)

    updated = FORM_DATA.copy()
    updated["name"] = "Sara Ahmed"
    client.post("/save", data=updated)

    profile = database.get_data()
    assert profile["name"] == "Sara Ahmed"


# ---------------------------------------------------------------------------
# Tests: GET /view — Resume + Portfolio page
# ---------------------------------------------------------------------------

def test_view_redirects_to_home_when_no_data(client):
    """GET /view redirects to / when no profile exists (BR-10)."""
    response = client.get("/view")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_view_returns_200_when_data_exists(client):
    """GET /view returns HTTP 200 when a profile exists."""
    client.post("/save", data=FORM_DATA)
    response = client.get("/view")
    assert response.status_code == 200


def test_view_renders_resume_name(client):
    """GET /view renders the user's name in the resume section (FR-03)."""
    client.post("/save", data=FORM_DATA)
    response = client.get("/view")
    assert b"Ayesha Khan" in response.data


def test_view_renders_github_link_when_provided(client):
    """GET /view renders GitHub link when github_url is set (BR-06)."""
    client.post("/save", data=FORM_DATA)
    response = client.get("/view")
    assert b"github.com/ayeshakhan" in response.data


def test_view_omits_linkedin_link_when_not_provided(client):
    """GET /view does not render LinkedIn link when linkedin_url is NULL (BR-06)."""
    client.post("/save", data=FORM_DATA)   # linkedin_url is "" in FORM_DATA
    response = client.get("/view")
    assert b"resume-linkedin-link" not in response.data
    assert b"portfolio-linkedin-link" not in response.data
