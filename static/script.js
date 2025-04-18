function showLoginOptions() {
    const loginOptions = document.getElementById('login-options');
    loginOptions.classList.toggle('hidden');
  }
fetch('/api/jobs')
  .then(response => response.json())
  .then(data => {
    const jobContainer = document.getElementById('jobs');
    data.forEach(job => {
      const jobCard = document.createElement('div');
      jobCard.className = 'job-card';
      jobCard.innerHTML = `
        <h3>${job.role} - ${job.company}</h3>
        <p><strong>Package:</strong> ${job.package}</p>
        <p><strong>Experience:</strong> ${job.experience}</p>
        <p><strong>Location:</strong> ${job.location}</p>
        <p><strong>Description:</strong> ${job.description}</p>
        <p><strong>Responsibilities:</strong> ${job.responsibilities}</p>
        <p><strong>Skills:</strong> ${job.skills}</p>
        <p><strong>Education:</strong> ${job.education}</p>
        <button onclick="applyJob('${job.id}')">Apply Now</button>
      `;
      jobContainer.appendChild(jobCard);
    });
  });