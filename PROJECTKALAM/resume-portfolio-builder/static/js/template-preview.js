// Template Preview and Selection
let currentPreviewTemplate = null;

function previewTemplate(templateId) {
    currentPreviewTemplate = templateId;
    const modal = document.getElementById('previewModal');
    const previewTitle = document.getElementById('previewTitle');
    const previewContent = document.getElementById('previewContent');
    const useBtn = document.getElementById('useTemplateBtn');

    // Set title
    const titles = {
        'template1': 'Corporate Professional Template',
        'template2': 'Modern Developer Template',
        'template3': 'Creative Portfolio Template'
    };
    previewTitle.textContent = titles[templateId] || 'Template Preview';

    // Generate preview HTML
    previewContent.innerHTML = generatePreviewHTML(templateId, window.profileData);

    // Set up use button
    useBtn.onclick = () => {
        closePreview();
        selectTemplate(templateId);
    };

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closePreview() {
    const modal = document.getElementById('previewModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    currentPreviewTemplate = null;
}

function selectTemplate(templateId) {
    const form = document.getElementById('templateForm');
    const input = document.getElementById('templateChoice');
    
    if (form && input) {
        input.value = templateId;
        form.submit();
    }
}

function generatePreviewHTML(templateId, profile) {
    // Parse skills
    const skills = parseSkills(profile.skills);
    
    // Get projects
    const projects = getProjects(profile);
    
    // Get certifications
    const certs = getCertifications(profile);

    switch(templateId) {
        case 'template1':
            return generateTemplate1Preview(profile, skills, projects, certs);
        case 'template2':
            return generateTemplate2Preview(profile, skills, projects, certs);
        case 'template3':
            return generateTemplate3Preview(profile, skills, projects, certs);
        default:
            return '<p>Template not found</p>';
    }
}

function parseSkills(skillsStr) {
    if (!skillsStr) return [];
    // Split by comma or newline
    return skillsStr.split(/[,\n]/).map(s => s.trim()).filter(s => s);
}

function getProjects(profile) {
    const projects = [];
    for (let i = 1; i <= 3; i++) {
        const title = profile[`project${i}_title`];
        const desc = profile[`project${i}_desc`];
        const url = profile[`project${i}_url`];
        if (title && desc) {
            projects.push({ title, desc, url });
        }
    }
    return projects;
}

function getCertifications(profile) {
    const certs = [];
    for (let i = 1; i <= 3; i++) {
        const name = profile[`cert${i}_name`];
        const org = profile[`cert${i}_org`];
        const year = profile[`cert${i}_year`];
        if (name) {
            certs.push({ name, org, year });
        }
    }
    return certs;
}

function generateTemplate1Preview(profile, skills, projects, certs) {
    return `
        <div class="resume-preview template1-preview">
            <div class="resume-header">
                <h1>${profile.name || 'Your Name'}</h1>
                <div class="contact-info">
                    ${profile.email ? `<span>${profile.email}</span>` : ''}
                    ${profile.phone ? `<span>${profile.phone}</span>` : ''}
                    ${profile.github_url ? `<span><a href="${profile.github_url}" target="_blank">GitHub</a></span>` : ''}
                    ${profile.linkedin_url ? `<span><a href="${profile.linkedin_url}" target="_blank">LinkedIn</a></span>` : ''}
                </div>
            </div>
            
            ${profile.education ? `
            <div class="resume-section">
                <h2>Education</h2>
                <p>${profile.education}</p>
            </div>
            ` : ''}
            
            ${skills.length > 0 ? `
            <div class="resume-section">
                <h2>Skills</h2>
                <p>${skills.join(', ')}</p>
            </div>
            ` : ''}
            
            ${projects.length > 0 ? `
            <div class="resume-section">
                <h2>Projects</h2>
                ${projects.map(p => `
                    <div class="project-item">
                        <h3>${p.title}</h3>
                        <p>${p.desc}</p>
                        ${p.url ? `<a href="${p.url}" target="_blank">View Project</a>` : ''}
                    </div>
                `).join('')}
            </div>
            ` : ''}
            
            ${certs.length > 0 ? `
            <div class="resume-section">
                <h2>Certifications</h2>
                ${certs.map(c => `
                    <div class="cert-item">
                        <strong>${c.name}</strong> - ${c.org || ''} ${c.year ? `(${c.year})` : ''}
                    </div>
                `).join('')}
            </div>
            ` : ''}
        </div>
    `;
}

function generateTemplate2Preview(profile, skills, projects, certs) {
    return `
        <div class="resume-preview template2-preview">
            <div class="resume-header modern">
                <h1>${profile.name || 'Your Name'}</h1>
                <div class="contact-info">
                    ${profile.email ? `<span>📧 ${profile.email}</span>` : ''}
                    ${profile.phone ? `<span>📱 ${profile.phone}</span>` : ''}
                    ${profile.github_url ? `<span>💻 <a href="${profile.github_url}" target="_blank">GitHub</a></span>` : ''}
                    ${profile.linkedin_url ? `<span>🔗 <a href="${profile.linkedin_url}" target="_blank">LinkedIn</a></span>` : ''}
                </div>
            </div>
            
            ${skills.length > 0 ? `
            <div class="resume-section">
                <h2>Skills</h2>
                <div class="skills-badges">
                    ${skills.map(skill => `<span class="skill-badge">${skill}</span>`).join('')}
                </div>
            </div>
            ` : ''}
            
            ${projects.length > 0 ? `
            <div class="resume-section">
                <h2>Projects</h2>
                <div class="projects-grid">
                    ${projects.map(p => `
                        <div class="project-card">
                            <h3>${p.title}</h3>
                            <p>${p.desc}</p>
                            ${p.url ? `<a href="${p.url}" target="_blank" class="project-link">View Project →</a>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            ${profile.education ? `
            <div class="resume-section">
                <h2>Education</h2>
                <p>${profile.education}</p>
            </div>
            ` : ''}
            
            ${certs.length > 0 ? `
            <div class="resume-section">
                <h2>Certifications</h2>
                <div class="certs-list">
                    ${certs.map(c => `
                        <div class="cert-badge">
                            <strong>${c.name}</strong><br>
                            <small>${c.org || ''} ${c.year ? `• ${c.year}` : ''}</small>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        </div>
    `;
}

function generateTemplate3Preview(profile, skills, projects, certs) {
    return `
        <div class="resume-preview template3-preview">
            <div class="resume-header creative">
                <h1>${profile.name || 'Your Name'}</h1>
                <div class="contact-info creative">
                    ${profile.email ? `<span>${profile.email}</span>` : ''}
                    ${profile.phone ? `<span>${profile.phone}</span>` : ''}
                    ${profile.github_url ? `<span><a href="${profile.github_url}" target="_blank">GitHub</a></span>` : ''}
                    ${profile.linkedin_url ? `<span><a href="${profile.linkedin_url}" target="_blank">LinkedIn</a></span>` : ''}
                </div>
            </div>
            
            ${skills.length > 0 ? `
            <div class="resume-section creative">
                <h2>Skills</h2>
                <div class="skills-visual">
                    ${skills.map(skill => `<div class="skill-item">${skill}</div>`).join('')}
                </div>
            </div>
            ` : ''}
            
            ${projects.length > 0 ? `
            <div class="resume-section creative">
                <h2>Projects</h2>
                <div class="projects-portfolio">
                    ${projects.map(p => `
                        <div class="portfolio-item">
                            <h3>${p.title}</h3>
                            <p>${p.desc}</p>
                            ${p.url ? `<a href="${p.url}" target="_blank">View →</a>` : ''}
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
            
            ${profile.education ? `
            <div class="resume-section creative">
                <h2>Education</h2>
                <p>${profile.education}</p>
            </div>
            ` : ''}
            
            ${certs.length > 0 ? `
            <div class="resume-section creative">
                <h2>Certifications</h2>
                <div class="certs-timeline">
                    ${certs.map(c => `
                        <div class="cert-timeline-item">
                            <div class="cert-year">${c.year || '—'}</div>
                            <div class="cert-details">
                                <strong>${c.name}</strong><br>
                                <small>${c.org || ''}</small>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        </div>
    `;
}

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closePreview();
    }
});
