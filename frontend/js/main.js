// Main JS for Learning Helper

// Smooth scroll helper
function scrollToSection(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
}

// Modal handling
const signinModal = document.getElementById('signinModal');
const registerModal = document.getElementById('registerModal');

function openModal(modal) {
  modal.style.display = 'block';
}

function closeModal(modal) {
  modal.style.display = 'none';
}

window.addEventListener('click', (event) => {
  if (event.target === signinModal) closeModal(signinModal);
  if (event.target === registerModal) closeModal(registerModal);
});

// Hook up nav links for modals
document.addEventListener('DOMContentLoaded', () => {
  const signInLink = document.querySelector('a[href="#signin"]');
  const registerLink = document.querySelector('a[href="#register"]');
  const modalCloses = document.querySelectorAll('.modal .close');

  if (signInLink) signInLink.addEventListener('click', (e) => { e.preventDefault(); openModal(signinModal); });
  if (registerLink) registerLink.addEventListener('click', (e) => { e.preventDefault(); openModal(registerModal); });

  modalCloses.forEach((btn) => btn.addEventListener('click', () => {
    closeModal(signinModal);
    closeModal(registerModal);
  }));

  // Register form submit handler (frontend validation; backend integration later)
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);
      const payload = Object.fromEntries(formData.entries());

      // Basic validation
      if (!payload.userType || !payload.email || !payload.password || !payload.childName) {
        alert('Please fill all required fields.');
        return;
      }

      try {
        // TODO: Replace with real API call once backend is ready
        console.log('Submitting registration', payload);
        alert('Registration successful! You are now logged in.');
        closeModal(registerModal);
        scrollToSection('test');
      } catch (err) {
        alert('Registration failed. Please try again.');
      }
    });
  }
});

// Test logic (interactive 50-question wizard)
const QUESTIONS = Array.from({ length: 50 }, (_, i) => ({
  id: i + 1,
  text: `Sample question ${i + 1}: Does your child experience scenario ${i + 1}?`,
  // For now, categories rotate; can be replaced by real questions from DB
  category: ['dyslexia', 'dyscalculia', 'dysgraphia'][i % 3]
}));

let currentIndex = 0;
let answers = Array(50).fill(null); // values: 0,1,2

function renderTest() {
  const container = document.querySelector('.test-section .container');
  if (!container) return;

  container.innerHTML = `
    <h2>Ready for the Screening Test? 🎯</h2>
    <div class="test-container" id="testContainer">
      <div class="progress-bar"><div class="progress-fill" style="width: ${(currentIndex / 49) * 100}%"></div></div>
      <div class="question-card">
        <div class="question-number">Question ${currentIndex + 1} of 50</div>
        <div class="question-text">${QUESTIONS[currentIndex].text}</div>
        <div class="answer-options">
          ${renderOption(0, 'No (it doesn\'t happen)', '😄')}
          ${renderOption(1, 'Sometimes (sometimes it happens)', '😐')}
          ${renderOption(2, 'Yes (it happens)', '🙁')}
        </div>
      </div>
      <div class="navigation-buttons">
        <button class="nav-button prev-button" ${currentIndex === 0 ? 'disabled' : ''} onclick="prevQuestion()">Previous</button>
        ${currentIndex < 49
          ? `<button class="nav-button next-button" onclick="nextQuestion()">Next</button>`
          : `<button class="nav-button submit-button" onclick="submitTest()">Submit Test</button>`}
      </div>
    </div>
  `;

  // Add click handlers for options
  document.querySelectorAll('.answer-option').forEach((el) => {
    el.addEventListener('click', () => {
      const value = parseInt(el.getAttribute('data-value'));
      selectAnswer(value);
    });
  });

  // Highlight selected
  const selected = answers[currentIndex];
  if (selected !== null) {
    document.querySelector(`.answer-option[data-value="${selected}"]`)?.classList.add('selected');
  }
}

function renderOption(value, label, emoji) {
  return `<div class="answer-option" data-value="${value}"><span class="option-emoji">${emoji}</span> ${label}</div>`;
}

function selectAnswer(value) {
  answers[currentIndex] = value;
  renderTest();
}

function nextQuestion() {
  if (answers[currentIndex] === null) {
    alert('Please select an option before continuing.');
    return;
  }
  currentIndex = Math.min(49, currentIndex + 1);
  renderTest();
}

function prevQuestion() {
  currentIndex = Math.max(0, currentIndex - 1);
  renderTest();
}

function startTest() {
  currentIndex = 0;
  answers = Array(50).fill(null);
  renderTest();
}

function submitTest() {
  if (answers.some((a) => a === null)) {
    alert('Please answer all questions before submitting.');
    return;
  }
  const totalScore = answers.reduce((a, b) => a + b, 0);

  // Simple placeholder thresholds (to be replaced by ML inference later)
  const hasLD = totalScore >= 35; // arbitrary threshold

  // Category scores
  const catScores = { dyslexia: 0, dyscalculia: 0, dysgraphia: 0 };
  QUESTIONS.forEach((q, i) => { catScores[q.category] += answers[i]; });

  const types = Object.entries(catScores).sort((a, b) => b[1] - a[1]);
  const likelyType = types[0][0];

  // Placeholder mental health indicator based on variance/pattern (very naive)
  const highStreak = answers.join('').includes('2222');
  const mentalDisorder = hasLD && highStreak; // placeholder only

  alert(
    `Results:\n` +
    `- Learning Difference: ${hasLD ? 'Likely' : 'Unlikely'}\n` +
    `- Most indicative type: ${likelyType}\n` +
    `- Mental disorder indicator: ${mentalDisorder ? 'Flagged' : 'Not flagged'}\n` +
    `Note: This is a screening tool, not a diagnosis. Please consult professionals for evaluation.`
  );

  // TODO: Send results to backend for storage and real ML inference
  // fetch('/api/results', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answers }) })
}
