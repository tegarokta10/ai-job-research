const form = document.querySelector('#analysis-form');
const button = document.querySelector('#analyze-button');
const errorMessage = document.querySelector('#error-message');
const resultPanel = document.querySelector('#result');

function renderSkills(listId, skills) {
  const list = document.querySelector(`#${listId}`);
  list.replaceChildren();
  if (!skills.length) {
    const item = document.createElement('li');
    item.className = 'empty';
    item.textContent = 'Tidak ada';
    list.append(item);
    return;
  }
  for (const skill of skills) {
    const item = document.createElement('li');
    item.textContent = skill;
    list.append(item);
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorMessage.hidden = true;
  resultPanel.hidden = true;
  button.disabled = true;
  button.querySelector('span:first-child').textContent = 'Analyze...';

  const payload = {
    job_description: form.elements.job_description.value,
    candidate_profile: form.elements.candidate_profile.value,
  };

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      const validationErrors = Array.isArray(data.errors)
        ? data.errors.map((error) => `${error.field}: ${error.message}`).join(' ')
        : '';
      throw new Error(validationErrors || data.detail || 'Analisis gagal. Silakan coba lagi.');
    }

    document.querySelector('#job-title').textContent = data.job_title;
    document.querySelector('#match-score').textContent = `${data.match_score}%`;
    document.querySelector('#recommendation').textContent = data.recommendation;
    renderSkills('required-skills', data.required_skills);
    renderSkills('matching-skills', data.matching_skills);
    renderSkills('missing-skills', data.missing_skills);
    resultPanel.hidden = false;
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (error) {
    errorMessage.textContent = error.message || 'Tidak dapat terhubung ke server. Coba lagi nanti.';
    errorMessage.hidden = false;
  } finally {
    button.disabled = false;
    button.querySelector('span:first-child').textContent = 'Analyze Job';
  }
});
