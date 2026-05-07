// Multi-Step Form Wizard
(function() {
    let currentStep = 1;
    const totalSteps = 5;
    const formData = {};

    // Initialize wizard on page load
    document.addEventListener('DOMContentLoaded', function() {
        initWizard();
        loadFromLocalStorage();
        showStep(currentStep);
    });

    function initWizard() {
        const nextBtn = document.getElementById('nextBtn');
        const prevBtn = document.getElementById('prevBtn');
        const form = document.getElementById('profile-form');

        console.log('Initializing wizard...', { nextBtn, prevBtn, form });

        if (nextBtn) {
            nextBtn.addEventListener('click', function(e) {
                console.log('Next button clicked!');
                nextStep();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', function(e) {
                console.log('Previous button clicked!');
                prevStep();
            });
        }

        if (form) {
            form.addEventListener('submit', handleSubmit);
            // Save to localStorage on input change
            form.addEventListener('input', saveToLocalStorage);
        }
    }

    function showStep(step) {
        const steps = document.querySelectorAll('.form-step');
        const progressSteps = document.querySelectorAll('.progress-step');
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        const submitBtn = document.getElementById('submitBtn');
        const progressFill = document.getElementById('progressFill');

        // Hide all steps
        steps.forEach(s => s.classList.remove('active'));
        
        // Show current step
        const currentStepEl = document.querySelector(`.form-step[data-step="${step}"]`);
        if (currentStepEl) {
            currentStepEl.classList.add('active');
        }

        // Update progress indicator
        progressSteps.forEach((s, index) => {
            if (index < step) {
                s.classList.add('active');
                s.classList.add('completed');
            } else if (index === step - 1) {
                s.classList.add('active');
                s.classList.remove('completed');
            } else {
                s.classList.remove('active');
                s.classList.remove('completed');
            }
        });

        // Update progress bar
        const progress = ((step - 1) / (totalSteps - 1)) * 100;
        if (progressFill) {
            progressFill.style.width = progress + '%';
        }

        // Update button visibility
        if (prevBtn) {
            prevBtn.style.display = step === 1 ? 'none' : 'inline-block';
        }
        
        if (nextBtn && submitBtn) {
            if (step === totalSteps) {
                nextBtn.style.display = 'none';
                submitBtn.style.display = 'inline-block';
            } else {
                nextBtn.style.display = 'inline-block';
                submitBtn.style.display = 'none';
            }
        }

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function nextStep() {
        console.log('nextStep called, current step:', currentStep);
        if (validateStep(currentStep)) {
            console.log('Validation passed, moving to next step');
            saveFormState();
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        } else {
            console.log('Validation failed');
        }
    }

    function prevStep() {
        saveFormState();
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    }

    function validateStep(step) {
        clearErrors();
        let isValid = true;

        switch(step) {
            case 1: // Personal Information
                isValid = validatePersonalInfo();
                break;
            case 2: // Education
                isValid = validateEducation();
                break;
            case 3: // Skills
                isValid = validateSkills();
                break;
            case 4: // Projects
                isValid = validateProjects();
                break;
            case 5: // Certifications (optional)
                isValid = true;
                break;
        }

        return isValid;
    }

    function validatePersonalInfo() {
        let isValid = true;

        // Name validation
        const name = document.getElementById('name').value.trim();
        if (!name) {
            showError('name-error', 'Name is required');
            isValid = false;
        }

        // Email validation
        const email = document.getElementById('email').value.trim();
        if (!email) {
            showError('email-error', 'Email is required');
            isValid = false;
        } else if (!isValidEmail(email)) {
            showError('email-error', 'Please enter a valid email address');
            isValid = false;
        }

        // Phone validation
        const phone = document.getElementById('phone').value.trim();
        if (!phone) {
            showError('phone-error', 'Phone number is required');
            isValid = false;
        }

        // GitHub URL validation (optional but must be valid if provided)
        const github = document.getElementById('github_url').value.trim();
        if (github && !isValidURL(github)) {
            showError('github-error', 'Please enter a valid URL (must start with http:// or https://)');
            isValid = false;
        }

        // LinkedIn URL validation (optional but must be valid if provided)
        const linkedin = document.getElementById('linkedin_url').value.trim();
        if (linkedin && !isValidURL(linkedin)) {
            showError('linkedin-error', 'Please enter a valid URL (must start with http:// or https://)');
            isValid = false;
        }

        return isValid;
    }

    function validateEducation() {
        const education = document.getElementById('education').value.trim();
        if (!education) {
            showError('education-error', 'Education details are required');
            return false;
        }
        return true;
    }

    function validateSkills() {
        const skills = document.getElementById('skills').value.trim();
        if (!skills) {
            showError('skills-error', 'Please enter at least one skill');
            return false;
        }
        return true;
    }

    function validateProjects() {
        let isValid = true;

        // Project 1 is required
        const project1Title = document.getElementById('project1_title').value.trim();
        const project1Desc = document.getElementById('project1_desc').value.trim();

        if (!project1Title) {
            showError('project1-title-error', 'Project 1 title is required');
            isValid = false;
        }

        if (!project1Desc) {
            showError('project1-desc-error', 'Project 1 description is required');
            isValid = false;
        }

        // Validate project URLs if provided
        const project1Url = document.getElementById('project1_url').value.trim();
        if (project1Url && !isValidURL(project1Url)) {
            showError('project1-url-error', 'Please enter a valid URL or leave empty');
            isValid = false;
        }

        const project2Url = document.getElementById('project2_url').value.trim();
        if (project2Url && !isValidURL(project2Url)) {
            showError('project2-url-error', 'Please enter a valid URL or leave empty');
            isValid = false;
        }

        const project3Url = document.getElementById('project3_url').value.trim();
        if (project3Url && !isValidURL(project3Url)) {
            showError('project3-url-error', 'Please enter a valid URL or leave empty');
            isValid = false;
        }

        // Validate project 2 and 3 if title is provided
        const project2Title = document.getElementById('project2_title').value.trim();
        const project2Desc = document.getElementById('project2_desc').value.trim();
        if (project2Title && !project2Desc) {
            showError('project2-desc-error', 'Description is required if title is provided');
            isValid = false;
        }

        const project3Title = document.getElementById('project3_title').value.trim();
        const project3Desc = document.getElementById('project3_desc').value.trim();
        if (project3Title && !project3Desc) {
            showError('project3-desc-error', 'Description is required if title is provided');
            isValid = false;
        }

        return isValid;
    }

    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function isValidURL(url) {
        // Accept URLs without protocol and auto-prepend https://
        if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
            return true; // Will be handled by backend
        }
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    function showError(errorId, message) {
        const errorEl = document.getElementById(errorId);
        if (errorEl) {
            errorEl.textContent = message;
            errorEl.style.display = 'block';
            
            // Add error class to input
            const inputId = errorId.replace('-error', '');
            const input = document.getElementById(inputId);
            if (input) {
                input.classList.add('error');
            }
        }
    }

    function clearErrors() {
        const errors = document.querySelectorAll('.error-msg');
        errors.forEach(error => {
            error.textContent = '';
            error.style.display = 'none';
        });

        const inputs = document.querySelectorAll('.error');
        inputs.forEach(input => {
            input.classList.remove('error');
        });
    }

    function saveFormState() {
        const form = document.getElementById('profile-form');
        if (form) {
            const formDataObj = new FormData(form);
            const data = {};
            formDataObj.forEach((value, key) => {
                data[key] = value;
            });
            // Store in the module-level formData object
            Object.assign(formData, data);
        }
    }

    function saveToLocalStorage() {
        const form = document.getElementById('profile-form');
        if (form) {
            const formDataObj = new FormData(form);
            const data = {};
            formDataObj.forEach((value, key) => {
                data[key] = value;
            });
            localStorage.setItem('cvFormData', JSON.stringify(data));
        }
    }

    function loadFromLocalStorage() {
        const savedData = localStorage.getItem('cvFormData');
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const input = document.getElementById(key) || document.querySelector(`[name="${key}"]`);
                    if (input && !input.value) {
                        input.value = data[key];
                    }
                });
            } catch (e) {
                console.error('Error loading saved data:', e);
            }
        }
    }

    function handleSubmit(e) {
        e.preventDefault();
        
        if (!validateStep(currentStep)) {
            return;
        }

        // Auto-prepend https:// to URLs without protocol
        const urlFields = ['github_url', 'linkedin_url', 'project1_url', 'project2_url', 'project3_url'];
        urlFields.forEach(fieldId => {
            const input = document.getElementById(fieldId);
            if (input && input.value && !input.value.startsWith('http://') && !input.value.startsWith('https://')) {
                input.value = 'https://' + input.value;
            }
        });

        // Show loading spinner
        const spinner = document.getElementById('loadingSpinner');
        const form = document.getElementById('profile-form');
        
        if (spinner) {
            spinner.style.display = 'flex';
        }
        
        if (form) {
            form.style.display = 'none';
        }

        // Submit form
        setTimeout(() => {
            e.target.submit();
            // Clear localStorage after successful submission
            localStorage.removeItem('cvFormData');
        }, 500);
    }
})();
