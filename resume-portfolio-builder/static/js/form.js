/**
 * form.js — Resume + Portfolio Builder
 * ----------------------------------------
 * Client-side form validation for the profile input form (index.html).
 *
 * Business rules enforced:
 *   BR-01: name, email, phone must be non-empty
 *   BR-02: email must match a valid email format
 *   BR-03: github_url, linkedin_url, project URLs must be valid http/https
 *          URLs — but only if the field is non-empty (they are optional)
 *
 * How it works:
 *   1. The form's submit event is intercepted by validateForm()
 *   2. All error messages are cleared first
 *   3. Each field is validated in order
 *   4. If any field fails, an error message is shown and submission is blocked
 *   5. If all fields pass, the form submits normally to POST /save
 */

// ---------------------------------------------------------------------------
// Regex patterns
// ---------------------------------------------------------------------------

/** Valid email: something@something.something */
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

/** Valid URL: must start with http:// or https:// */
const URL_REGEX = /^https?:\/\/.+/;

// ---------------------------------------------------------------------------
// Main validation handler
// ---------------------------------------------------------------------------

/**
 * Intercept the form submit event and run all validation checks.
 * Blocks submission if any check fails.
 *
 * @param {Event} event - The form submit event
 */
function validateForm(event) {
  // Clear all previous error messages before re-validating
  clearErrors();

  let isValid = true;

  // --- Required fields ---
  if (!validateRequired("name", "name-error", "Full name is required.")) {
    isValid = false;
  }

  if (!validateRequired("email", "email-error", "Email address is required.")) {
    isValid = false;
  } else if (!validateEmail(document.getElementById("email").value.trim())) {
    // Email is non-empty but format is wrong
    showError("email", "email-error", "Please enter a valid email address.");
    isValid = false;
  }

  if (!validateRequired("phone", "phone-error", "Phone number is required.")) {
    isValid = false;
  }

  // --- Optional URL fields (validate format only if non-empty) ---
  if (!validateOptionalUrl("github_url", "github-error",
      "GitHub URL must start with http:// or https://")) {
    isValid = false;
  }

  if (!validateOptionalUrl("linkedin_url", "linkedin-error",
      "LinkedIn URL must start with http:// or https://")) {
    isValid = false;
  }

  if (!validateOptionalUrl("project1_url", "project1-url-error",
      "Project 1 URL must start with http:// or https://")) {
    isValid = false;
  }

  if (!validateOptionalUrl("project2_url", "project2-url-error",
      "Project 2 URL must start with http:// or https://")) {
    isValid = false;
  }

  if (!validateOptionalUrl("project3_url", "project3-url-error",
      "Project 3 URL must start with http:// or https://")) {
    isValid = false;
  }

  // Block form submission if any validation failed
  if (!isValid) {
    event.preventDefault();

    // Scroll to the first visible error message so the user sees it
    const firstError = document.querySelector(".error-msg:not(:empty)");
    if (firstError) {
      firstError.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }
}

// ---------------------------------------------------------------------------
// Validation helpers
// ---------------------------------------------------------------------------

/**
 * Check that a required field is not empty after trimming whitespace.
 * Shows an error message and marks the input if the field is empty.
 *
 * @param {string} fieldId   - The id of the input element
 * @param {string} errorId   - The id of the error <span> element
 * @param {string} message   - The error message to display
 * @returns {boolean} true if the field has a value, false if empty
 */
function validateRequired(fieldId, errorId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return true;  // field not present — skip

  if (field.value.trim() === "") {
    showError(fieldId, errorId, message);
    return false;
  }
  return true;
}

/**
 * Validate an optional URL field.
 * If the field is empty, it passes (optional).
 * If the field has a value, it must match the URL regex.
 *
 * @param {string} fieldId   - The id of the input element
 * @param {string} errorId   - The id of the error <span> element
 * @param {string} message   - The error message to display if format is wrong
 * @returns {boolean} true if valid (empty or correct URL), false if bad format
 */
function validateOptionalUrl(fieldId, errorId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return true;  // field not present — skip

  const value = field.value.trim();
  if (value === "") return true;  // empty is fine for optional fields

  if (!validateUrl(value)) {
    showError(fieldId, errorId, message);
    return false;
  }
  return true;
}

/**
 * Test whether a string is a valid email address.
 *
 * @param {string} value - The email string to test
 * @returns {boolean} true if valid email format
 */
function validateEmail(value) {
  return EMAIL_REGEX.test(value);
}

/**
 * Test whether a string is a valid http/https URL.
 *
 * @param {string} value - The URL string to test
 * @returns {boolean} true if starts with http:// or https://
 */
function validateUrl(value) {
  return URL_REGEX.test(value);
}

// ---------------------------------------------------------------------------
// Error display helpers
// ---------------------------------------------------------------------------

/**
 * Show an error message for a field and mark the input with an error style.
 *
 * @param {string} fieldId  - The id of the input element
 * @param {string} errorId  - The id of the error <span> element
 * @param {string} message  - The error text to display
 */
function showError(fieldId, errorId, message) {
  const field = document.getElementById(fieldId);
  const errorSpan = document.getElementById(errorId);

  if (field) {
    field.classList.add("input-error");
  }
  if (errorSpan) {
    errorSpan.textContent = message;
  }
}

/**
 * Clear all error messages and remove error styling from all inputs.
 * Called at the start of each validation run.
 */
function clearErrors() {
  // Remove error text from all error spans
  document.querySelectorAll(".error-msg").forEach(function (span) {
    span.textContent = "";
  });

  // Remove error border styling from all inputs
  document.querySelectorAll(".input-error").forEach(function (input) {
    input.classList.remove("input-error");
  });
}

// ---------------------------------------------------------------------------
// Attach event listener when the DOM is ready
// ---------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("profile-form");
  if (form) {
    form.addEventListener("submit", validateForm);
  }
});
