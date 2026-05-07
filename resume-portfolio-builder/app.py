import os
from flask import Flask, render_template, request, redirect, url_for, session
from database import init_db_v2, get_data, save_data, update_data, email_exists, create_user, authenticate_user, log_login_activity

# Use the directory of this file as the root for templates and static assets.
# This ensures Flask finds them correctly whether run directly or imported
# from a parent directory (e.g. Vercel's api/index.py entry point).
_base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(_base_dir, 'templates'),
    static_folder=os.path.join(_base_dir, 'static'),
)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Initialize DB at import time so it runs on Vercel's serverless environment
# (the __main__ block never executes in a WSGI/serverless context)
init_db_v2()

@app.route("/", methods=["GET"])
def index():
    user_id = session.get('user_id')
    profile = get_data(user_id) if user_id else None
    profile_exists = profile is not None
    return render_template("landing.html", current_page='landing', profile_exists=profile_exists)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        full_name = request.form.get("full_name", "").strip()
        
        if not email or not password:
            return render_template("register.html", error="Email and password are required", 
                                 current_page='register', profile_exists=False)
        
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match", 
                                 current_page='register', profile_exists=False)
        
        if len(password) < 6:
            return render_template("register.html", error="Password must be at least 6 characters", 
                                 current_page='register', profile_exists=False)
        
        if email_exists(email):
            return render_template("register.html", 
                                 error=f"Email '{email}' is already registered. Please login or use a different email.", 
                                 current_page='register', profile_exists=False)
        
        user = create_user(email, password, full_name)
        if user:
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            log_login_activity(user['id'], email, 'registered', ip_address, user_agent)
            
            return render_template("register.html", 
                                 success=f"Account created successfully! Please login with your email: {email}", 
                                 current_page='register', profile_exists=False)
        else:
            return render_template("register.html", error="Registration failed. Please try again.", 
                                 current_page='register', profile_exists=False)
    
    return render_template("register.html", current_page='register', profile_exists=False)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        if not email or not password:
            return render_template("login.html", error="Please enter email and password", 
                                 current_page='login', profile_exists=False)
        
        user = authenticate_user(email, password)
        
        if user:
            log_login_activity(user['id'], email, 'success', ip_address, user_agent)
            
            session['logged_in'] = True
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['full_name'] = user.get('full_name', '')
            session['form_completed'] = False
            session['template_selected'] = False
            
            return redirect(url_for("form"))
        else:
            log_login_activity(0, email, 'failed', ip_address, user_agent)
            
            return render_template("login.html", 
                                 error="Invalid email or password. Please try again.", 
                                 current_page='login', profile_exists=False)
    
    return render_template("login.html", current_page='login', profile_exists=False)

@app.route("/form", methods=["GET"])
def form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    profile = get_data(user_id)
    profile_exists = profile is not None
    return render_template("form.html", profile=profile, current_page='form', profile_exists=profile_exists)

@app.route("/save-simple", methods=["POST"])
def save_simple():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    
    data = {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "github_url": request.form.get("github_url", "").strip(),
        "linkedin_url": request.form.get("linkedin_url", "").strip(),
        "education": request.form.get("education", "").strip(),
        "skills": request.form.get("skills", "").strip(),
        "project1_title": request.form.get("project1_title", "").strip(),
        "project1_desc": request.form.get("project1_desc", "").strip(),
        "project1_url": request.form.get("project1_url", "").strip(),
        "project2_title": request.form.get("project2_title", "").strip(),
        "project2_desc": request.form.get("project2_desc", "").strip(),
        "project2_url": request.form.get("project2_url", "").strip(),
        "project3_title": request.form.get("project3_title", "").strip(),
        "project3_desc": request.form.get("project3_desc", "").strip(),
        "project3_url": request.form.get("project3_url", "").strip(),
        "cert1_name": request.form.get("cert1_name", "").strip(),
        "cert1_org": request.form.get("cert1_org", "").strip(),
        "cert1_year": request.form.get("cert1_year", "").strip(),
        "cert2_name": request.form.get("cert2_name", "").strip(),
        "cert2_org": request.form.get("cert2_org", "").strip(),
        "cert2_year": request.form.get("cert2_year", "").strip(),
        "cert3_name": request.form.get("cert3_name", "").strip(),
        "cert3_org": request.form.get("cert3_org", "").strip(),
        "cert3_year": request.form.get("cert3_year", "").strip(),
    }

    existing = get_data(user_id)
    if existing:
        update_data(data, user_id)
    else:
        save_data(data, user_id)

    session['form_completed'] = True
    return redirect(url_for("choose_format"))

@app.route("/choose-format", methods=["GET"])
def choose_format():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if not session.get('form_completed'):
        return redirect(url_for('form'))
    
    user_id = session.get('user_id')
    profile = get_data(user_id)
    
    if profile is None:
        return redirect(url_for("form"))
    
    profile_exists = True
    return render_template("choose-format.html", profile=profile, current_page='choose', profile_exists=profile_exists)

@app.route("/choose-resume", methods=["POST"])
def choose_resume():
    if not session.get('logged_in') or not session.get('form_completed'):
        return redirect(url_for('login'))
    
    session['format_choice'] = 'resume'
    return redirect(url_for("select_template"))

@app.route("/choose-portfolio", methods=["POST"])
def choose_portfolio():
    if not session.get('logged_in') or not session.get('form_completed'):
        return redirect(url_for('login'))
    
    session['format_choice'] = 'portfolio'
    session['template_selected'] = True
    return redirect(url_for("portfolio"))

@app.route("/select-template", methods=["GET"])
def select_template():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if not session.get('form_completed'):
        return redirect(url_for('form'))
    
    user_id = session.get('user_id')
    profile = get_data(user_id)
    
    if profile is None:
        return redirect(url_for("form"))
    
    profile_exists = True
    return render_template("template-selection.html", profile=profile, current_page='template', profile_exists=profile_exists)

@app.route("/save-template", methods=["POST"])
def save_template():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    template_choice = request.form.get("template_choice", "template1")
    
    profile = get_data(user_id)
    if profile:
        profile["template_choice"] = template_choice
        update_data(profile, user_id)
    
    session['template_selected'] = True
    return redirect(url_for("view_resume"))

@app.route("/view-resume", methods=["GET"])
def view_resume():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if not session.get('form_completed'):
        return redirect(url_for('form'))
    
    if not session.get('template_selected'):
        return redirect(url_for('select_template'))
    
    user_id = session.get('user_id')
    profile = get_data(user_id)

    if profile is None:
        return redirect(url_for("form"))

    template_choice = profile.get("template_choice", "template1")
    profile_exists = True
    
    return render_template("view.html", profile=profile, template_choice=template_choice, 
                         current_page='view', profile_exists=profile_exists)

@app.route("/portfolio", methods=["GET"])
def portfolio():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    user_id = session.get('user_id')
    profile = get_data(user_id)
    
    if profile is None:
        return redirect(url_for("form"))
    
    profile_exists = True
    return render_template("portfolio.html", profile=profile, current_page='portfolio', profile_exists=profile_exists)

@app.route("/logout", methods=["GET"])
def logout():
    if session.get('logged_in'):
        user_id = session.get('user_id')
        email = session.get('email')
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        log_login_activity(user_id, email, 'logout', ip_address, user_agent)
    
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db_v2()
    print("Starting Resume + Portfolio Builder...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True)