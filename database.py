"""
database.py — Resume + Portfolio Builder
----------------------------------------
Handles all SQLite database operations:
  - Creating the database and table on first run
  - Saving user profile data (insert on first use)
  - Retrieving stored profile data
  - Updating existing profile data (overwrite on re-submit)

This app is single-user, so the table always holds at most ONE row (id = 1).
Uses Python's built-in sqlite3 module — no extra installation needed.
"""

import sqlite3
import os

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Path to the SQLite database file (created automatically if it doesn't exist)
DB_PATH = os.path.join(os.path.dirname(__file__), "resume_portfolio.db")


# ---------------------------------------------------------------------------
# Helper: get a database connection
# ---------------------------------------------------------------------------

def get_connection():
    """
    Open and return a connection to the SQLite database.

    Using check_same_thread=False is safe here because Flask's development
    server is single-threaded for local use.

    Returns:
        sqlite3.Connection: An active database connection with row_factory
                            set so rows are accessible like dictionaries.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # row_factory lets us access columns by name (e.g. row["name"])
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Schema: CREATE TABLE
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS profile (
    id              INTEGER PRIMARY KEY,   -- Always 1 (single-user app)

    -- Personal Information
    name            TEXT    NOT NULL,
    email           TEXT    NOT NULL,
    phone           TEXT    NOT NULL,
    github_url      TEXT,                  -- Optional GitHub profile link
    linkedin_url    TEXT,                  -- Optional LinkedIn profile link

    -- Education (free-text: institution, degree, year)
    education       TEXT,

    -- Skills (comma-separated or newline-separated list)
    skills          TEXT,

    -- Project 1
    project1_title  TEXT,
    project1_desc   TEXT,
    project1_url    TEXT,                  -- Optional project link

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
"""


def init_db():
    """
    Initialize the database by creating the 'profile' table if it does not
    already exist.  Call this once when the Flask app starts up.

    The IF NOT EXISTS clause makes this safe to call on every startup —
    it will not overwrite existing data.
    """
    conn = get_connection()
    try:
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()
        print(f"[database] Database ready at: {DB_PATH}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# CRUD Functions
# ---------------------------------------------------------------------------

def save_data(data: dict) -> None:
    """
    Insert a new profile row into the database (first-time use).

    The row is always inserted with id = 1.  If a row already exists,
    use update_data() instead.  In practice, app.py calls get_data() first
    to decide whether to call save_data() or update_data().

    Args:
        data (dict): A dictionary containing all profile fields.
                     Keys must match the column names in the profile table.
                     Optional fields (github_url, linkedin_url, project URLs,
                     cert fields) may be absent or None.

    Example:
        save_data({
            "name": "Ayesha Khan",
            "email": "ayesha@email.com",
            "phone": "+92-300-1234567",
            "github_url": "https://github.com/ayeshakhan",
            "linkedin_url": "https://linkedin.com/in/ayeshakhan",
            "education": "BS Computer Science, FAST-NUCES, 2024",
            "skills": "Python, HTML, CSS, JavaScript, SQL, Git",
            "project1_title": "Student Portal",
            "project1_desc": "A web app for managing student records",
            "project1_url": "",
            ...
        })
    """
    INSERT_SQL = """
        INSERT INTO profile (
            id,
            name, email, phone, github_url, linkedin_url,
            education, skills,
            project1_title, project1_desc, project1_url,
            project2_title, project2_desc, project2_url,
            project3_title, project3_desc, project3_url,
            cert1_name, cert1_org, cert1_year,
            cert2_name, cert2_org, cert2_year,
            cert3_name, cert3_org, cert3_year
        ) VALUES (
            1,
            :name, :email, :phone, :github_url, :linkedin_url,
            :education, :skills,
            :project1_title, :project1_desc, :project1_url,
            :project2_title, :project2_desc, :project2_url,
            :project3_title, :project3_desc, :project3_url,
            :cert1_name, :cert1_org, :cert1_year,
            :cert2_name, :cert2_org, :cert2_year,
            :cert3_name, :cert3_org, :cert3_year
        );
    """
    # Fill in any missing optional keys with None so SQLite stores NULL
    row = _fill_defaults(data)

    conn = get_connection()
    try:
        conn.execute(INSERT_SQL, row)
        conn.commit()
        print("[database] Profile saved (new record).")
    finally:
        conn.close()


def get_data() -> dict | None:
    """
    Retrieve the stored profile from the database.

    Returns:
        dict: A dictionary of all profile fields if a record exists.
        None: If no profile has been saved yet (first-time user).

    Example usage in app.py:
        profile = get_data()
        if profile:
            return render_template("view.html", profile=profile)
        else:
            return redirect("/")   # No data yet — send back to form
    """
    SELECT_SQL = "SELECT * FROM profile WHERE id = 1;"

    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL)
        row = cursor.fetchone()
        if row is None:
            return None
        # Convert sqlite3.Row to a plain dict for easy use in templates
        return dict(row)
    finally:
        conn.close()


def update_data(data: dict) -> None:
    """
    Overwrite the existing profile row with new data (re-submit / edit flow).

    This replaces every column value for the single profile row (id = 1).
    It is safe to call even if the user only changed one field — all fields
    are re-written from the submitted form data.

    Args:
        data (dict): Same structure as save_data(). All fields are updated.

    Example usage in app.py:
        existing = get_data()
        if existing:
            update_data(form_data)
        else:
            save_data(form_data)
    """
    UPDATE_SQL = """
        UPDATE profile SET
            name            = :name,
            email           = :email,
            phone           = :phone,
            github_url      = :github_url,
            linkedin_url    = :linkedin_url,
            education       = :education,
            skills          = :skills,
            project1_title  = :project1_title,
            project1_desc   = :project1_desc,
            project1_url    = :project1_url,
            project2_title  = :project2_title,
            project2_desc   = :project2_desc,
            project2_url    = :project2_url,
            project3_title  = :project3_title,
            project3_desc   = :project3_desc,
            project3_url    = :project3_url,
            cert1_name      = :cert1_name,
            cert1_org       = :cert1_org,
            cert1_year      = :cert1_year,
            cert2_name      = :cert2_name,
            cert2_org       = :cert2_org,
            cert2_year      = :cert2_year,
            cert3_name      = :cert3_name,
            cert3_org       = :cert3_org,
            cert3_year      = :cert3_year
        WHERE id = 1;
    """
    row = _fill_defaults(data)

    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, row)
        conn.commit()
        print("[database] Profile updated (existing record overwritten).")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _fill_defaults(data: dict) -> dict:
    """
    Ensure all expected keys exist in the data dictionary.

    Optional fields that are missing or empty strings are stored as None
    (NULL in SQLite) so templates can check `if profile['github_url']`
    cleanly.

    Args:
        data (dict): Raw form data dictionary.

    Returns:
        dict: A new dictionary with all required keys present.
    """
    # All columns except 'id' (which is always 1)
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

    filled = {}
    for key in expected_keys:
        value = data.get(key, None)
        # Treat empty strings as NULL for optional URL/text fields
        filled[key] = value if value != "" else None

    return filled
