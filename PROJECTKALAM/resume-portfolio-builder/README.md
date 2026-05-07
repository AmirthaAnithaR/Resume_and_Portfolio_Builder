# Resume + Portfolio Builder

A beginner-friendly web application where you enter your personal and academic details and the system automatically generates a formatted resume and a personal portfolio webpage — all in one place.

Built with **Python / Flask**, **HTML/CSS/JavaScript**, and **SQLite**.

---

## Features

- **Input Form** — Enter your name, email, phone, GitHub, LinkedIn, education, skills, up to 3 projects, and up to 3 certifications
- **Resume View** — Clean, professional resume layout generated from your data
- **Portfolio View** — Personal portfolio page with About Me, Skills badges, Project cards, and Contact section — on the same page as your resume
- **Download as PDF** — One-click PDF export using your browser's built-in print dialog (no extra software needed)
- **Edit Anytime** — Go back to the form, update any field, and re-submit to overwrite your data
- **Local & Private** — Everything runs on your machine; no data is sent anywhere

---

## Prerequisites

- Python **3.8** or higher
- pip (comes with Python)

Check your Python version:
```bash
python --version
```

---

## Setup & Run

### Step 1 — Get the project

If you have the folder already, open a terminal inside `resume-portfolio-builder/`.

### Step 2 — Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

This installs only one package: **Flask 3.0.3**. Everything else (SQLite, os) is part of Python's standard library.

### Step 4 — Run the application

```bash
python app.py
```

You should see:
```
Starting Resume + Portfolio Builder...
Open your browser and go to: http://localhost:5000
[database] Database ready at: .../resume_portfolio.db
 * Running on http://127.0.0.1:5000
```

### Step 5 — Open in browser

Go to: **http://localhost:5000**

---

## How to Use

1. **Fill in the form** on the home page with your details
2. Click **Generate Resume & Portfolio**
3. Your resume and portfolio appear on the same page
4. Click **Download as PDF** — your browser's print dialog opens; choose "Save as PDF"
5. To edit, click **Edit Details** or navigate back to Home — your data is pre-filled
6. Update any fields and re-submit to overwrite

---

## Sample Test Data

Use this data to try the app quickly:

```
Name:          Ayesha Khan
Email:         ayesha.khan@email.com
Phone:         +92-300-1234567
GitHub URL:    https://github.com/ayeshakhan
LinkedIn URL:  https://linkedin.com/in/ayeshakhan

Education:
  BS Computer Science, FAST-NUCES, 2024

Skills:
  Python, HTML, CSS, JavaScript, SQL, Git

Project 1:
  Title:       Student Portal
  Description: A web app for managing student records built with Django and SQLite
  Link:        https://github.com/ayeshakhan/student-portal

Project 2:
  Title:       Weather App
  Description: Fetches live weather data using the OpenWeatherMap API (Python, Flask)
  Link:        https://github.com/ayeshakhan/weather-app

Project 3:
  Title:       Portfolio Website
  Description: Static personal portfolio built with HTML and CSS
  Link:        (leave blank)

Certification 1:
  Name:  Python for Everybody
  Org:   Coursera
  Year:  2023

Certification 2:
  Name:  Web Development Bootcamp
  Org:   Udemy
  Year:  2023

Certification 3:
  Name:  SQL Basics
  Org:   Khan Academy
  Year:  2022
```

---

## Folder Structure

```
resume-portfolio-builder/
|
+-- app.py                    # Flask routes (GET /, POST /save, GET /view)
+-- database.py               # SQLite setup and CRUD functions
+-- requirements.txt          # Python dependencies (Flask only)
+-- README.md                 # This file
|
+-- templates/
|   +-- index.html            # Input form page
|   +-- view.html             # Resume + Portfolio view page
|
+-- static/
|   +-- css/
|   |   +-- style.css         # Main screen stylesheet
|   |   +-- print.css         # Print / PDF stylesheet
|   +-- js/
|       +-- form.js           # Client-side form validation
|
+-- resume_portfolio.db       # SQLite database (auto-created on first run)
```

---

## How It Works (Technical Overview)

```
Browser  →  GET /        →  Flask index()   →  get_data()  →  render index.html
Browser  →  POST /save   →  Flask save()    →  save_data() or update_data()  →  redirect /view
Browser  →  GET /view    →  Flask view()    →  get_data()  →  render view.html
```

- **database.py** handles all SQLite operations. The database stores one row (your profile).
- **app.py** contains the three Flask routes. It calls database functions and renders templates.
- **index.html** is the form. Jinja2 pre-populates fields from stored data on edit visits.
- **view.html** shows the resume and portfolio. Optional fields (GitHub, LinkedIn, project links) only appear if you filled them in.
- **print.css** hides the portfolio section, navbar, and buttons when printing — so your PDF contains only the resume.

---

## Stopping the App

Press `Ctrl + C` in the terminal to stop the Flask server.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| Port 5000 already in use | Change `app.run(debug=True)` to `app.run(debug=True, port=5001)` in app.py |
| Form submits but nothing shows | Check the terminal for error messages |
| PDF looks wrong | Use Chrome or Edge for best print-to-PDF results |
| Want to reset your data | Delete `resume_portfolio.db` and restart the app |
