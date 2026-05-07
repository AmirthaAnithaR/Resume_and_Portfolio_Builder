# Build Instructions
# Resume + Portfolio Builder

---

## Prerequisites

| Requirement | Version | Check Command |
|---|---|---|
| Python | 3.8 or higher | `python --version` |
| pip | Latest | `pip --version` |
| Web Browser | Chrome, Edge, or Firefox | — |

No build tool (Maven, npm, webpack) is needed — Flask serves files directly.

---

## Step 1: Navigate to the Project Folder

```bash
cd resume-portfolio-builder
```

All commands below are run from inside this folder.

---

## Step 2: Create a Virtual Environment (Recommended)

A virtual environment keeps Flask isolated from your system Python.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed flask-3.0.3 ...
```

Only one package is installed: **Flask 3.0.3**. All other modules (`sqlite3`, `os`) are Python standard library.

---

## Step 4: Verify the Installation

```bash
python -c "import flask; print('Flask', flask.__version__)"
```

**Expected output:**
```
Flask 3.0.3
```

---

## Step 5: Run the Application

```bash
python app.py
```

**Expected output:**
```
Starting Resume + Portfolio Builder...
Open your browser and go to: http://localhost:5000
[database] Database ready at: .../resume_portfolio.db
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

The SQLite database file `resume_portfolio.db` is created automatically on first run.

---

## Step 6: Open in Browser

Go to: **http://localhost:5000**

You should see the input form with sections for Personal Information, Education, Skills, Projects, and Certifications.

---

## Build Artifacts

| Artifact | Location | Created By |
|---|---|---|
| `resume_portfolio.db` | `resume-portfolio-builder/` | `init_db()` on first `python app.py` |

No compiled files, no build output directory — Flask runs directly from source.

---

## Stopping the Application

Press `Ctrl + C` in the terminal.

---

## Troubleshooting

| Problem | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Flask not installed | Run `pip install -r requirements.txt` |
| `Address already in use` on port 5000 | Another process using port 5000 | Change to `app.run(debug=True, port=5001)` in `app.py` |
| `TemplateNotFound: index.html` | Running from wrong directory | Make sure you are inside `resume-portfolio-builder/` |
| `OperationalError: no such table: profile` | DB not initialized | This shouldn't happen — `init_db()` runs on startup; delete `resume_portfolio.db` and restart |
| Virtual environment not activating (Windows) | Execution policy | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in PowerShell |
