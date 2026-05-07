"""
database.py — Resume + Portfolio Builder
----------------------------------------
Handles all SQLite database operations:
  - Creating the database and tables on first run
  - User management (registration, login, authentication)
  - Login activity tracking
  - Saving user profile data (insert on first use)
  - Retrieving stored profile data
  - Updating existing profile data (overwrite on re-submit)

Uses Python's built-in sqlite3 module — no extra installation needed.
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Path to the SQLite database file (created automatically if it doesn't exist)
# On Vercel (serverless), the app directory is read-only — use /tmp instead.
# Locally, fall back to the app directory.
_app_dir = os.path.dirname(__file__)
_tmp_dir = "/tmp"
DB_PATH = os.path.join(
    _tmp_dir if os.path.isdir(_tmp_dir) and not os.access(_app_dir, os.W_OK) else _app_dir,
    "resume_portfolio.db"
)


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
# Schema: CREATE TABLES
# ---------------------------------------------------------------------------

# Users table for authentication
CREATE_USERS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email           TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    full_name       TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login      TIMESTAMP,
    is_active       INTEGER DEFAULT 1
);
"""

# Login activities table for tracking
CREATE_LOGIN_ACTIVITIES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS login_activities (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    email           TEXT    NOT NULL,
    login_time      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address      TEXT,
    user_agent      TEXT,
    status          TEXT    NOT NULL,  -- 'success', 'failed', 'logout'
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# Profile table (linked to users)
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS profile (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL UNIQUE,  -- Link to users table

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
    cert3_year      TEXT,

    -- Template Choice
    template_choice TEXT DEFAULT 'template1',  -- template1, template2, or template3
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""


def init_db():
    """
    Initialize the database by creating all tables if they do not
    already exist. Call this once when the Flask app starts up.

    The IF NOT EXISTS clause makes this safe to call on every startup —
    it will not overwrite existing data.
    """
    conn = get_connection()
    try:
        conn.execute(CREATE_USERS_TABLE_SQL)
        conn.execute(CREATE_LOGIN_ACTIVITIES_TABLE_SQL)
        conn.execute(CREATE_TABLE_SQL)
        conn.commit()
        print(f"[database] Database ready at: {DB_PATH}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# User Management Functions
# ---------------------------------------------------------------------------

def email_exists(email: str) -> bool:
    """
    Check if an email already exists in the users table.
    
    Args:
        email (str): Email address to check
        
    Returns:
        bool: True if email exists, False otherwise
    """
    SELECT_SQL = "SELECT id FROM users WHERE email = ? COLLATE NOCASE;"
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, (email,))
        row = cursor.fetchone()
        return row is not None
    finally:
        conn.close()


def create_user(email: str, password: str, full_name: str = None) -> dict | None:
    """
    Create a new user account with hashed password.
    
    Args:
        email (str): User's email address (must be unique)
        password (str): Plain text password (will be hashed)
        full_name (str): User's full name (optional)
        
    Returns:
        dict: User data if successful, None if email already exists
    """
    # Check if email already exists
    if email_exists(email):
        return None
    
    INSERT_SQL = """
        INSERT INTO users (email, password_hash, full_name)
        VALUES (?, ?, ?);
    """
    
    password_hash = generate_password_hash(password)
    
    conn = get_connection()
    try:
        cursor = conn.execute(INSERT_SQL, (email, password_hash, full_name))
        user_id = cursor.lastrowid
        conn.commit()
        print(f"[database] User created: {email}")
        
        # Return user data
        return {
            'id': user_id,
            'email': email,
            'full_name': full_name
        }
    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> dict | None:
    """
    Authenticate a user with email and password.
    
    Args:
        email (str): User's email address
        password (str): Plain text password to verify
        
    Returns:
        dict: User data if authentication successful, None otherwise
    """
    SELECT_SQL = """
        SELECT id, email, password_hash, full_name, is_active
        FROM users
        WHERE email = ? COLLATE NOCASE;
    """
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, (email,))
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        user = dict(row)
        
        # Check if account is active
        if not user['is_active']:
            return None
        
        # Verify password
        if check_password_hash(user['password_hash'], password):
            # Update last login time
            update_last_login(user['id'])
            
            # Remove password hash from returned data
            del user['password_hash']
            return user
        
        return None
    finally:
        conn.close()


def update_last_login(user_id: int) -> None:
    """
    Update the last login timestamp for a user.
    
    Args:
        user_id (int): User's ID
    """
    UPDATE_SQL = """
        UPDATE users
        SET last_login = CURRENT_TIMESTAMP
        WHERE id = ?;
    """
    
    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, (user_id,))
        conn.commit()
    finally:
        conn.close()


def log_login_activity(user_id: int, email: str, status: str, 
                       ip_address: str = None, user_agent: str = None) -> None:
    """
    Log a login activity (success, failed, or logout).
    
    Args:
        user_id (int): User's ID (0 for failed login attempts)
        email (str): Email address used for login attempt
        status (str): 'success', 'failed', or 'logout'
        ip_address (str): IP address of the request (optional)
        user_agent (str): User agent string (optional)
    """
    INSERT_SQL = """
        INSERT INTO login_activities (user_id, email, status, ip_address, user_agent)
        VALUES (?, ?, ?, ?, ?);
    """
    
    conn = get_connection()
    try:
        conn.execute(INSERT_SQL, (user_id, email, status, ip_address, user_agent))
        conn.commit()
        print(f"[database] Login activity logged: {email} - {status}")
    finally:
        conn.close()


def get_login_activities(user_id: int = None, limit: int = 50) -> list:
    """
    Get login activities, optionally filtered by user.
    
    Args:
        user_id (int): Filter by user ID (None for all users)
        limit (int): Maximum number of records to return
        
    Returns:
        list: List of login activity dictionaries
    """
    if user_id:
        SELECT_SQL = """
            SELECT * FROM login_activities
            WHERE user_id = ?
            ORDER BY login_time DESC
            LIMIT ?;
        """
        params = (user_id, limit)
    else:
        SELECT_SQL = """
            SELECT * FROM login_activities
            ORDER BY login_time DESC
            LIMIT ?;
        """
        params = (limit,)
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> dict | None:
    """
    Get user data by user ID.
    
    Args:
        user_id (int): User's ID
        
    Returns:
        dict: User data if found, None otherwise
    """
    SELECT_SQL = """
        SELECT id, email, full_name, created_at, last_login, is_active
        FROM users
        WHERE id = ?;
    """
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Profile CRUD Functions (now linked to users)
# ---------------------------------------------------------------------------

def save_data(data: dict, user_id: int) -> None:
    """
    Insert a new profile row into the database for a specific user.

    Args:
        data (dict): A dictionary containing all profile fields.
        user_id (int): The user ID to link this profile to.
    """
    INSERT_SQL = """
        INSERT INTO profile (
            user_id,
            name, email, phone, github_url, linkedin_url,
            education, skills,
            project1_title, project1_desc, project1_url,
            project2_title, project2_desc, project2_url,
            project3_title, project3_desc, project3_url,
            cert1_name, cert1_org, cert1_year,
            cert2_name, cert2_org, cert2_year,
            cert3_name, cert3_org, cert3_year,
            template_choice
        ) VALUES (
            :user_id,
            :name, :email, :phone, :github_url, :linkedin_url,
            :education, :skills,
            :project1_title, :project1_desc, :project1_url,
            :project2_title, :project2_desc, :project2_url,
            :project3_title, :project3_desc, :project3_url,
            :cert1_name, :cert1_org, :cert1_year,
            :cert2_name, :cert2_org, :cert2_year,
            :cert3_name, :cert3_org, :cert3_year,
            :template_choice
        );
    """
    row = _fill_defaults(data)
    row['user_id'] = user_id

    conn = get_connection()
    try:
        conn.execute(INSERT_SQL, row)
        conn.commit()
        print(f"[database] Profile saved for user {user_id}.")
    finally:
        conn.close()


def get_data(user_id: int = None) -> dict | None:
    """
    Retrieve the stored profile from the database for a specific user.

    Args:
        user_id (int): The user ID to retrieve profile for.

    Returns:
        dict: A dictionary of all profile fields if a record exists.
        None: If no profile has been saved yet for this user.
    """
    SELECT_SQL = "SELECT * FROM profile WHERE user_id = ?;"

    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        # Convert sqlite3.Row to a plain dict for easy use in templates
        return dict(row)
    finally:
        conn.close()


def update_data(data: dict, user_id: int) -> None:
    """
    Overwrite the existing profile row with new data for a specific user.

    Args:
        data (dict): Same structure as save_data(). All fields are updated.
        user_id (int): The user ID whose profile to update.
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
            cert3_year      = :cert3_year,
            template_choice = :template_choice
        WHERE user_id = :user_id;
    """
    row = _fill_defaults(data)
    row['user_id'] = user_id

    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, row)
        conn.commit()
        print(f"[database] Profile updated for user {user_id}.")
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
    expected_keys = [
        "name", "email", "phone", "github_url", "linkedin_url",
        "education", "skills",
        "project1_title", "project1_desc", "project1_url",
        "project2_title", "project2_desc", "project2_url",
        "project3_title", "project3_desc", "project3_url",
        "cert1_name", "cert1_org", "cert1_year",
        "cert2_name", "cert2_org", "cert2_year",
        "cert3_name", "cert3_org", "cert3_year",
        "template_choice",
    ]

    filled = {}
    for key in expected_keys:
        value = data.get(key, None)
        # Treat empty strings as NULL for optional URL/text fields
        filled[key] = value if value != "" else None

    return filled


# ---------------------------------------------------------------------------
# Resume Versions Table Schema
# ---------------------------------------------------------------------------

CREATE_RESUME_VERSIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS resume_versions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    
    -- Version metadata
    version_name    TEXT    NOT NULL,
    description     TEXT,
    target_job      TEXT,
    is_default      INTEGER DEFAULT 0,
    is_archived     INTEGER DEFAULT 0,
    is_deleted      INTEGER DEFAULT 0,
    deleted_at      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Profile data (same as profile table)
    name            TEXT    NOT NULL,
    email           TEXT    NOT NULL,
    phone           TEXT    NOT NULL,
    github_url      TEXT,
    linkedin_url    TEXT,
    education       TEXT,
    skills          TEXT,
    project1_title  TEXT,
    project1_desc   TEXT,
    project1_url    TEXT,
    project2_title  TEXT,
    project2_desc   TEXT,
    project2_url    TEXT,
    project3_title  TEXT,
    project3_desc   TEXT,
    project3_url    TEXT,
    cert1_name      TEXT,
    cert1_org       TEXT,
    cert1_year      TEXT,
    cert2_name      TEXT,
    cert2_org       TEXT,
    cert2_year      TEXT,
    cert3_name      TEXT,
    cert3_org       TEXT,
    cert3_year      TEXT,
    template_choice TEXT DEFAULT 'template1',
    
    -- Customization settings (JSON blob)
    customization_settings TEXT,
    
    -- File paths
    profile_photo_path TEXT,
    logo_path          TEXT,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

CREATE_RESUME_VERSIONS_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_resume_versions_user_id ON resume_versions(user_id);",
    "CREATE INDEX IF NOT EXISTS idx_resume_versions_is_default ON resume_versions(is_default);",
    "CREATE INDEX IF NOT EXISTS idx_resume_versions_is_archived ON resume_versions(is_archived);",
    "CREATE INDEX IF NOT EXISTS idx_resume_versions_is_deleted ON resume_versions(is_deleted);",
]


# ---------------------------------------------------------------------------
# Resume Versions CRUD Functions
# ---------------------------------------------------------------------------

def create_resume_version(user_id: int, version_name: str, data: dict, 
                         description: str = None, target_job: str = None,
                         is_default: int = 0) -> int:
    """
    Create a new resume version for a user.
    
    Args:
        user_id (int): User's ID
        version_name (str): Name of the version
        data (dict): Profile data dictionary
        description (str): Optional description
        target_job (str): Optional target job/company
        is_default (int): 1 if this should be the default version, 0 otherwise
        
    Returns:
        int: ID of the newly created version
    """
    INSERT_SQL = """
        INSERT INTO resume_versions (
            user_id, version_name, description, target_job, is_default,
            name, email, phone, github_url, linkedin_url,
            education, skills,
            project1_title, project1_desc, project1_url,
            project2_title, project2_desc, project2_url,
            project3_title, project3_desc, project3_url,
            cert1_name, cert1_org, cert1_year,
            cert2_name, cert2_org, cert2_year,
            cert3_name, cert3_org, cert3_year,
            template_choice, customization_settings,
            profile_photo_path, logo_path
        ) VALUES (
            :user_id, :version_name, :description, :target_job, :is_default,
            :name, :email, :phone, :github_url, :linkedin_url,
            :education, :skills,
            :project1_title, :project1_desc, :project1_url,
            :project2_title, :project2_desc, :project2_url,
            :project3_title, :project3_desc, :project3_url,
            :cert1_name, :cert1_org, :cert1_year,
            :cert2_name, :cert2_org, :cert2_year,
            :cert3_name, :cert3_org, :cert3_year,
            :template_choice, :customization_settings,
            :profile_photo_path, :logo_path
        );
    """
    
    row = _fill_defaults(data)
    row['user_id'] = user_id
    row['version_name'] = version_name
    row['description'] = description
    row['target_job'] = target_job
    row['is_default'] = is_default
    row['customization_settings'] = data.get('customization_settings', None)
    row['profile_photo_path'] = data.get('profile_photo_path', None)
    row['logo_path'] = data.get('logo_path', None)
    
    conn = get_connection()
    try:
        # If this is set as default, unset all other defaults for this user
        if is_default == 1:
            conn.execute("UPDATE resume_versions SET is_default = 0 WHERE user_id = ?;", (user_id,))
        
        cursor = conn.execute(INSERT_SQL, row)
        version_id = cursor.lastrowid
        conn.commit()
        print(f"[database] Resume version '{version_name}' created for user {user_id}.")
        return version_id
    finally:
        conn.close()


def get_resume_version(version_id: int) -> dict | None:
    """
    Get a specific resume version by ID.
    
    Args:
        version_id (int): Version ID
        
    Returns:
        dict: Version data if found, None otherwise
    """
    SELECT_SQL = "SELECT * FROM resume_versions WHERE id = ? AND is_deleted = 0;"
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, (version_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()


def get_user_resume_versions(user_id: int, include_archived: bool = False, 
                             include_deleted: bool = False) -> list:
    """
    Get all resume versions for a user.
    
    Args:
        user_id (int): User's ID
        include_archived (bool): Include archived versions
        include_deleted (bool): Include deleted versions
        
    Returns:
        list: List of version dictionaries
    """
    conditions = ["user_id = ?"]
    params = [user_id]
    
    if not include_archived:
        conditions.append("is_archived = 0")
    if not include_deleted:
        conditions.append("is_deleted = 0")
    
    where_clause = " AND ".join(conditions)
    SELECT_SQL = f"SELECT * FROM resume_versions WHERE {where_clause} ORDER BY last_modified DESC;"
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_default_resume_version(user_id: int) -> dict | None:
    """
    Get the default resume version for a user.
    
    Args:
        user_id (int): User's ID
        
    Returns:
        dict: Default version data, or None if no default set
    """
    SELECT_SQL = """
        SELECT * FROM resume_versions 
        WHERE user_id = ? AND is_default = 1 AND is_deleted = 0
        LIMIT 1;
    """
    
    conn = get_connection()
    try:
        cursor = conn.execute(SELECT_SQL, (user_id,))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)
    finally:
        conn.close()


def update_resume_version(version_id: int, data: dict) -> None:
    """
    Update an existing resume version.
    
    Args:
        version_id (int): Version ID to update
        data (dict): Updated profile data
    """
    UPDATE_SQL = """
        UPDATE resume_versions SET
            version_name    = :version_name,
            description     = :description,
            target_job      = :target_job,
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
            cert3_year      = :cert3_year,
            template_choice = :template_choice,
            customization_settings = :customization_settings,
            profile_photo_path = :profile_photo_path,
            logo_path       = :logo_path,
            last_modified   = CURRENT_TIMESTAMP
        WHERE id = :version_id;
    """
    
    row = _fill_defaults(data)
    row['version_id'] = version_id
    row['version_name'] = data.get('version_name', 'Untitled Resume')
    row['description'] = data.get('description', None)
    row['target_job'] = data.get('target_job', None)
    row['customization_settings'] = data.get('customization_settings', None)
    row['profile_photo_path'] = data.get('profile_photo_path', None)
    row['logo_path'] = data.get('logo_path', None)
    
    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, row)
        conn.commit()
        print(f"[database] Resume version {version_id} updated.")
    finally:
        conn.close()


def set_default_resume_version(user_id: int, version_id: int) -> None:
    """
    Set a resume version as the default for a user.
    
    Args:
        user_id (int): User's ID
        version_id (int): Version ID to set as default
    """
    conn = get_connection()
    try:
        # Unset all defaults for this user
        conn.execute("UPDATE resume_versions SET is_default = 0 WHERE user_id = ?;", (user_id,))
        # Set the specified version as default
        conn.execute("UPDATE resume_versions SET is_default = 1 WHERE id = ?;", (version_id,))
        conn.commit()
        print(f"[database] Resume version {version_id} set as default for user {user_id}.")
    finally:
        conn.close()


def archive_resume_version(version_id: int) -> None:
    """
    Archive a resume version.
    
    Args:
        version_id (int): Version ID to archive
    """
    UPDATE_SQL = "UPDATE resume_versions SET is_archived = 1 WHERE id = ?;"
    
    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, (version_id,))
        conn.commit()
        print(f"[database] Resume version {version_id} archived.")
    finally:
        conn.close()


def unarchive_resume_version(version_id: int) -> None:
    """
    Unarchive a resume version.
    
    Args:
        version_id (int): Version ID to unarchive
    """
    UPDATE_SQL = "UPDATE resume_versions SET is_archived = 0 WHERE id = ?;"
    
    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, (version_id,))
        conn.commit()
        print(f"[database] Resume version {version_id} unarchived.")
    finally:
        conn.close()


def delete_resume_version(version_id: int) -> None:
    """
    Soft delete a resume version (moves to trash).
    
    Args:
        version_id (int): Version ID to delete
    """
    UPDATE_SQL = """
        UPDATE resume_versions 
        SET is_deleted = 1, deleted_at = CURRENT_TIMESTAMP 
        WHERE id = ?;
    """
    
    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, (version_id,))
        conn.commit()
        print(f"[database] Resume version {version_id} moved to trash.")
    finally:
        conn.close()


def restore_resume_version(version_id: int) -> None:
    """
    Restore a deleted resume version from trash.
    
    Args:
        version_id (int): Version ID to restore
    """
    UPDATE_SQL = """
        UPDATE resume_versions 
        SET is_deleted = 0, deleted_at = NULL 
        WHERE id = ?;
    """
    
    conn = get_connection()
    try:
        conn.execute(UPDATE_SQL, (version_id,))
        conn.commit()
        print(f"[database] Resume version {version_id} restored from trash.")
    finally:
        conn.close()


def permanently_delete_resume_version(version_id: int) -> None:
    """
    Permanently delete a resume version from database.
    
    Args:
        version_id (int): Version ID to permanently delete
    """
    DELETE_SQL = "DELETE FROM resume_versions WHERE id = ?;"
    
    conn = get_connection()
    try:
        conn.execute(DELETE_SQL, (version_id,))
        conn.commit()
        print(f"[database] Resume version {version_id} permanently deleted.")
    finally:
        conn.close()


def clone_resume_version(version_id: int, new_version_name: str) -> int:
    """
    Clone an existing resume version.
    
    Args:
        version_id (int): Version ID to clone
        new_version_name (str): Name for the cloned version
        
    Returns:
        int: ID of the newly cloned version
    """
    # Get the original version
    original = get_resume_version(version_id)
    if original is None:
        raise ValueError(f"Resume version {version_id} not found")
    
    # Create a copy with new name
    data = dict(original)
    data['version_name'] = new_version_name
    data['description'] = f"Cloned from {original['version_name']}"
    
    return create_resume_version(
        user_id=original['user_id'],
        version_name=new_version_name,
        data=data,
        description=data['description'],
        target_job=original.get('target_job'),
        is_default=0  # Clones are never default by default
    )


# ---------------------------------------------------------------------------
# Migration Functions
# ---------------------------------------------------------------------------

def migrate_profile_to_versions() -> None:
    """
    Migrate existing profile data to resume_versions table.
    Creates a default version for each user with existing profile data.
    """
    conn = get_connection()
    try:
        # Check if migration has already been done
        cursor = conn.execute("SELECT COUNT(*) as count FROM resume_versions;")
        count = cursor.fetchone()['count']
        if count > 0:
            print("[database] Migration already completed (resume_versions table has data).")
            return
        
        # Get all profiles
        cursor = conn.execute("SELECT * FROM profile;")
        profiles = cursor.fetchall()
        
        if len(profiles) == 0:
            print("[database] No profiles to migrate.")
            return
        
        print(f"[database] Migrating {len(profiles)} profiles to resume_versions...")
        
        for profile in profiles:
            profile_dict = dict(profile)
            user_id = profile_dict['user_id']
            
            # Create default version for this user
            create_resume_version(
                user_id=user_id,
                version_name="My First Resume",
                data=profile_dict,
                description="Migrated from original profile",
                is_default=1
            )
        
        print(f"[database] Successfully migrated {len(profiles)} profiles to resume_versions.")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# File Upload Helper Functions
# ---------------------------------------------------------------------------

def save_uploaded_file(file, user_id: int, file_type: str) -> str:
    """
    Save an uploaded file and return the file path.
    
    Args:
        file: Werkzeug FileStorage object
        user_id (int): User's ID
        file_type (str): 'photo' or 'logo'
        
    Returns:
        str: Relative file path for storage in database
    """
    import os
    from werkzeug.utils import secure_filename
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads', f'user_{user_id}', file_type + 's')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Secure the filename
    filename = secure_filename(file.filename)
    
    # Add timestamp to avoid conflicts
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{timestamp}{ext}"
    
    # Save the file
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # Return relative path for database storage
    relative_path = f"uploads/user_{user_id}/{file_type}s/{filename}"
    print(f"[database] File saved: {relative_path}")
    return relative_path


def delete_uploaded_file(file_path: str) -> None:
    """
    Delete an uploaded file from the filesystem.
    
    Args:
        file_path (str): Relative file path from database
    """
    import os
    
    if not file_path:
        return
    
    full_path = os.path.join(os.path.dirname(__file__), 'static', file_path)
    
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"[database] File deleted: {file_path}")
    except Exception as e:
        print(f"[database] Error deleting file {file_path}: {e}")


# ---------------------------------------------------------------------------
# Update init_db to include resume_versions table
# ---------------------------------------------------------------------------

def init_db_v2():
    """
    Initialize the database with all tables including resume_versions.
    Run migration if needed.
    """
    conn = get_connection()
    try:
        # Create all tables
        conn.execute(CREATE_USERS_TABLE_SQL)
        conn.execute(CREATE_LOGIN_ACTIVITIES_TABLE_SQL)
        conn.execute(CREATE_TABLE_SQL)
        conn.execute(CREATE_RESUME_VERSIONS_TABLE_SQL)
        
        # Create indexes
        for index_sql in CREATE_RESUME_VERSIONS_INDEXES_SQL:
            conn.execute(index_sql)
        
        conn.commit()
        print(f"[database] Database ready at: {DB_PATH}")
        
        # Run migration if needed
        migrate_profile_to_versions()
    finally:
        conn.close()
