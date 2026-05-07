"""
test_database.py — Resume + Portfolio Builder
----------------------------------------------
Unit tests for database.py CRUD functions.
The in-memory SQLite connection is managed by conftest.py.
Each test gets a clean (empty) profile table via the autouse clean_db fixture.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

SAMPLE = {
    "name":           "Ayesha Khan",
    "email":          "ayesha@email.com",
    "phone":          "+92-300-1234567",
    "github_url":     "https://github.com/ayeshakhan",
    "linkedin_url":   "https://linkedin.com/in/ayeshakhan",
    "education":      "BS Computer Science, FAST-NUCES, 2024",
    "skills":         "Python, HTML, CSS",
    "project1_title": "Student Portal",
    "project1_desc":  "A web app for student records",
    "project1_url":   "https://github.com/ayeshakhan/portal",
    "project2_title": "Weather App",
    "project2_desc":  "Live weather data app",
    "project2_url":   "",          # empty string — should become NULL (BR-05)
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
# Tests: init_db
# ---------------------------------------------------------------------------

def test_init_db_creates_table():
    """init_db() should create the profile table (called by conftest session fixture)."""
    conn = database.get_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='profile'"
    )
    assert cursor.fetchone() is not None


# ---------------------------------------------------------------------------
# Tests: get_data (empty state)
# ---------------------------------------------------------------------------

def test_get_data_returns_none_when_empty():
    """get_data() returns None when no profile has been saved (BR-10 support)."""
    assert database.get_data() is None


# ---------------------------------------------------------------------------
# Tests: save_data
# ---------------------------------------------------------------------------

def test_save_data_inserts_record():
    """save_data() inserts a profile row with id=1 (BR-07)."""
    database.save_data(SAMPLE)
    profile = database.get_data()
    assert profile is not None
    assert profile["id"] == 1


def test_save_data_stores_required_fields():
    """save_data() correctly stores name, email, phone (BR-01)."""
    database.save_data(SAMPLE)
    profile = database.get_data()
    assert profile["name"] == "Ayesha Khan"
    assert profile["email"] == "ayesha@email.com"
    assert profile["phone"] == "+92-300-1234567"


def test_save_data_stores_optional_urls():
    """save_data() stores GitHub and LinkedIn URLs when provided (BR-06)."""
    database.save_data(SAMPLE)
    profile = database.get_data()
    assert profile["github_url"] == "https://github.com/ayeshakhan"
    assert profile["linkedin_url"] == "https://linkedin.com/in/ayeshakhan"


def test_save_data_normalizes_empty_string_to_null():
    """save_data() converts empty string project2_url to NULL (BR-05)."""
    database.save_data(SAMPLE)
    profile = database.get_data()
    assert profile["project2_url"] is None   # "" → NULL


def test_save_data_stores_null_for_missing_optional_fields():
    """save_data() stores NULL for project3 and cert2/cert3 when not provided."""
    database.save_data(SAMPLE)
    profile = database.get_data()
    assert profile["project3_title"] is None
    assert profile["cert2_name"] is None
    assert profile["cert3_name"] is None


# ---------------------------------------------------------------------------
# Tests: update_data
# ---------------------------------------------------------------------------

def test_update_data_overwrites_existing_record():
    """update_data() replaces all fields for the existing row (BR-04)."""
    database.save_data(SAMPLE)

    updated = SAMPLE.copy()
    updated["name"] = "Sara Ahmed"
    updated["email"] = "sara@email.com"
    database.update_data(updated)

    profile = database.get_data()
    assert profile["name"] == "Sara Ahmed"
    assert profile["email"] == "sara@email.com"


def test_update_data_clears_previously_set_optional_field():
    """update_data() sets a previously filled optional field to NULL when cleared."""
    database.save_data(SAMPLE)

    updated = SAMPLE.copy()
    updated["github_url"] = ""   # user cleared the field
    database.update_data(updated)

    profile = database.get_data()
    assert profile["github_url"] is None


def test_single_row_constraint():
    """Only one profile row (id=1) should ever exist (BR-07)."""
    database.save_data(SAMPLE)
    conn = database.get_connection()
    cursor = conn.execute("SELECT COUNT(*) as cnt FROM profile")
    assert cursor.fetchone()["cnt"] == 1
