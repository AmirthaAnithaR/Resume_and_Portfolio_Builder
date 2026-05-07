# Build and Test Summary
# Resume + Portfolio Builder

---

## Build Status

| Item | Detail |
|---|---|
| **Build Tool** | None required — Flask runs directly from source |
| **Runtime** | Python 3.8+ |
| **Dependencies** | Flask==3.0.3 (single external package) |
| **Install Command** | `pip install -r requirements.txt` |
| **Run Command** | `python app.py` |
| **Build Artifacts** | `resume_portfolio.db` (auto-created on first run) |
| **Build Status** | Ready — no compilation step needed |

---

## Test Summary

### Unit Tests

| Category | Tests | Coverage |
|---|---|---|
| `_fill_defaults()` normalization | 4 tests | BR-05, all 25 keys |
| `database.py` CRUD | 7 tests | save, get, update, NULL storage, single-row constraint |
| `GET /` route | 3 tests | 200 response, form present, pre-population |
| `POST /save` route | 3 tests | redirect, persistence, update-not-duplicate |
| `GET /view` route | 5 tests | redirect guard, 200, name display, GitHub conditional, portfolio |
| **Total** | **22 tests** | All business rules covered |

**Run command**: `pytest test_app.py -v`

### Integration Tests

| Scenario | Tests | Status |
|---|---|---|
| First-time user flow (form → submit → view) | 1 test | Covered |
| Edit and re-submit flow | 1 test | Covered |
| Optional fields absent then added | 1 test | Covered |
| View guard with no data | 1 test | Covered |
| **Total** | **4 tests** | All key workflows covered |

**Run command**: `pytest test_integration.py -v`

### Performance Tests

| Test | Status | Notes |
|---|---|---|
| Load testing | N/A | Single-user local app; not applicable |
| Manual page load verification | Recommended | DevTools Network tab; expect < 200ms |
| NFR-04 compliance | Met by design | Local SQLite, no network latency |

### Additional Tests

| Test Type | Status | Notes |
|---|---|---|
| Contract tests | N/A | No microservices or external APIs |
| Security tests | N/A | Security extension disabled (user opted out) |
| E2E browser tests | Manual checklist provided | See unit-test-instructions.md |

---

## Business Rules Verification

| Rule | Verified By |
|---|---|
| BR-01: Required field validation | Unit test + manual checklist |
| BR-02: Email format validation | Manual checklist (client-side JS) |
| BR-03: Optional URL validation | Manual checklist (client-side JS) |
| BR-04: Save vs. update decision | Unit test `test_save_calls_update_on_resubmit` |
| BR-05: Empty string → NULL | Unit test `test_empty_string_becomes_none` |
| BR-06: Conditional display | Unit tests `test_view_shows/hides_github_link` |
| BR-07: Single profile constraint | Unit test `test_single_profile_constraint` |
| BR-08: Form pre-population | Unit test `test_index_prepopulates_when_data_exists` |
| BR-09: Redirect after POST | Unit test `test_save_redirects_to_view` |
| BR-10: View page guard | Unit test `test_view_redirects_when_no_data` |
| BR-11: PDF scope | Manual checklist (print CSS) |

---

## Overall Status

| Area | Status |
|---|---|
| Build | ✅ Ready |
| Unit Tests | ✅ 22 tests defined, all business rules covered |
| Integration Tests | ✅ 4 scenarios covering all key user flows |
| Performance Tests | ✅ N/A (single-user local app) |
| Manual Checklist | ✅ Provided in unit-test-instructions.md |
| **Ready to Run** | ✅ **Yes** |

---

## Quick Start (3 Commands)

```bash
cd resume-portfolio-builder
pip install -r requirements.txt
python app.py
```

Then open **http://localhost:5000** in your browser.
