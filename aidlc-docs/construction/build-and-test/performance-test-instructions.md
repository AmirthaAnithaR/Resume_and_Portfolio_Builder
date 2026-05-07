# Performance Test Instructions
# Resume + Portfolio Builder

---

## Applicability

**Status**: N/A for standard use

This is a single-user local application. Formal load/stress testing is not applicable because:
- Only one person uses it at a time
- It runs on localhost with no network latency
- SQLite handles single-user read/write with sub-millisecond response times

The NFR-04 requirement (respond within 2 seconds on a local machine) is met by design.

---

## Manual Performance Verification

These simple checks confirm the app meets NFR-04 without a load testing tool:

### Check 1: Page Load Time

1. Open Chrome/Edge DevTools (`F12`) → Network tab
2. Navigate to `http://localhost:5000`
3. Check the total load time in the bottom status bar

**Expected**: < 200ms (typically 10–50ms on localhost)

### Check 2: Form Submission Time

1. Fill in the form with sample data
2. Open DevTools → Network tab
3. Submit the form
4. Check the time for the `POST /save` request

**Expected**: < 500ms

### Check 3: View Page Load

1. Navigate to `http://localhost:5000/view`
2. Check load time in DevTools Network tab

**Expected**: < 200ms

---

## If You Want to Stress Test (Optional)

If you deploy this app to a server and want to test it under load, use [locust](https://locust.io/):

```bash
pip install locust==2.29.0
```

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class ResumePortfolioUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def view_form(self):
        self.client.get("/")

    @task(1)
    def submit_form(self):
        self.client.post("/save", data={
            "name": "Test User", "email": "test@test.com", "phone": "1234567890",
            "github_url": "", "linkedin_url": "", "education": "BS CS",
            "skills": "Python", "project1_title": "", "project1_desc": "",
            "project1_url": "", "project2_title": "", "project2_desc": "",
            "project2_url": "", "project3_title": "", "project3_desc": "",
            "project3_url": "", "cert1_name": "", "cert1_org": "", "cert1_year": "",
            "cert2_name": "", "cert2_org": "", "cert2_year": "",
            "cert3_name": "", "cert3_org": "", "cert3_year": "",
        })

    @task(2)
    def view_resume(self):
        self.client.get("/view")
```

```bash
locust --host=http://localhost:5000
```

Open `http://localhost:8089` to run the test from the Locust UI.
