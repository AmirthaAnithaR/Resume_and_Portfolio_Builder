# My CV Creator — Resume & Portfolio Builder

A full-stack web application that lets you create a professional resume and personal portfolio in minutes. Fill in your details once, choose a template, and get a polished, downloadable CV — no design skills needed.

Built with **Python / Flask**, **HTML / CSS / JavaScript**, and **SQLite**.

---

## Live Demo

🚀 [View Live on Vercel](https://resume-and-portfolio-builder.vercel.app)

---

## Features

| Feature | Description |
|---|---|
| 🔐 User Accounts | Register and log in — your data is saved to your account |
| 📝 Smart Form | Enter name, contact info, education, skills, up to 3 projects, and 3 certifications |
| 🎨 3 Resume Templates | Choose from three professionally designed layouts |
| 🌐 Portfolio Page | Auto-generated personal portfolio with skills badges and project cards |
| 📄 PDF Download | One-click export via browser print dialog — no extra software needed |
| ✏️ Always Editable | Update your details anytime and regenerate instantly |
| 📱 Responsive Design | Works on desktop, tablet, and mobile |

---

## Screenshots

> Landing page → Form → Template selection → Resume view → Portfolio view

---

## Tech Stack

- **Backend**: Python 3.x, Flask 3.0
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Database**: SQLite (local) via Python's built-in `sqlite3`
- **Auth**: Werkzeug password hashing
- **Deployment**: Vercel (serverless Python)

---

## Project Structure

```
Resume_and_Portfolio_Builder/
│
├── api/
│   └── index.py                  # Vercel serverless entry point
│
├── resume-portfolio-builder/
│   ├── app.py                    # Flask routes and application logic
│   ├── database.py               # SQLite CRUD, user auth, resume versions
│   ├── requirements.txt          # Python dependencies
│   ├── wsgi.py                   # WSGI entry point (local/production)
│   │
│   ├── templates/
│   │   ├── base.html             # Shared layout
│   │   ├── landing.html          # Home / marketing page
│   │   ├── register.html         # User registration
│   │   ├── login.html            # User login
│   │   ├── form.html             # Profile input form
│   │   ├── choose-format.html    # Resume vs Portfolio choice
│   │   ├── template-selection.html  # Pick a resume template
│   │   ├── view.html             # Resume viewer
│   │   ├── portfolio.html        # Portfolio viewer
│   │   ├── resume-template1.html # Template 1
│   │   ├── resume-template2.html # Template 2
│   │   ├── resume-template3.html # Template 3
│   │   └── my-resumes.html       # Saved resume versions
│   │
│   └── static/
│       ├── css/                  # Stylesheets
│       └── js/                   # Client-side scripts
│
├── vercel.json                   # Vercel deployment config
├── requirements.txt              # Root-level deps for Vercel
└── README.md                     # This file
```

---

## Local Setup

### Prerequisites

- Python **3.8+**
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/AmirthaAnithaR/Resume_and_Portfolio_Builder.git
cd Resume_and_Portfolio_Builder/resume-portfolio-builder

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open your browser at **http://localhost:5000**

---

## Deploying to Vercel

The repo is pre-configured for Vercel. To deploy your own instance:

1. Fork this repository
2. Go to [vercel.com](https://vercel.com) → New Project → Import your fork
3. Leave the root directory as `/` (do **not** set it to the subfolder)
4. Add environment variables in Vercel dashboard → Settings → Environment Variables:

   | Variable | Value |
   |---|---|
   | `SECRET_KEY` | A random 32-byte hex string (see below) |
   | `FLASK_ENV` | `production` |

   Generate a secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

5. Deploy — Vercel will auto-deploy on every push to `main`

> **Note on the database**: SQLite is ephemeral on Vercel — data resets on each cold start. For persistent storage, migrate to [Supabase](https://supabase.com) (free PostgreSQL) and update `database.py` to use `psycopg2`.

---

## How It Works

```
User registers / logs in
        ↓
Fills in profile form
        ↓
Chooses: Resume or Portfolio
        ↓
  Resume → picks template → views formatted resume → downloads PDF
  Portfolio → views personal portfolio page
```

All data is stored per-user in SQLite. Passwords are hashed with Werkzeug's `pbkdf2:sha256`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| Port 5000 in use | Change to `app.run(port=5001)` in `app.py` |
| PDF looks wrong | Use Chrome or Edge for best print-to-PDF output |
| Want to reset local data | Delete `resume_portfolio.db` and restart |

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## License

[MIT](https://choosealicense.com/licenses/mit/)

---

Made with ❤️ by [AmirthaAnithaR](https://github.com/AmirthaAnithaR)
