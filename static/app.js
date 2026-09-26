const sessionLength = 180;
let state = { active: false, secondsLeft: sessionLength, correct: 0, wrong: 0, attempted: 0, problem: null, timerId: null };

const elements = {
  timer: document.querySelector('#timer'), correct: document.querySelector('#correct-count'), accuracy: document.querySelector('#accuracy'), speed: document.querySelector('#speed'),
  question: document.querySelector('#question'), answer: document.querySelector('#answer'), submit: document.querySelector('#submit'), start: document.querySelector('#start'),
  feedback: document.querySelector('#feedback'), progress: document.querySelector('#progress-label'), number: document.querySelector('#problem-number'), results: document.querySelector('#results'),
  finalCorrect: document.querySelector('#final-correct'), finalWrong: document.querySelector('#final-wrong'), finalSpeed: document.querySelector('#final-speed'), restart: document.querySelector('#restart')
};

function formatTime(seconds) { return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`; }
function updateStats() {
  elements.timer.textContent = formatTime(state.secondsLeft);
  elements.correct.textContent = state.correct;
  elements.accuracy.textContent = state.attempted ? `${Math.round((state.correct / state.attempted) * 100)}%` : '--%';
  const elapsed = sessionLength - state.secondsLeft;
  elements.speed.innerHTML = `${elapsed ? Math.round((state.attempted / elapsed) * 60) : '--'} <small>cpm</small>`;
}

async function nextProblem() {
  const response = await fetch('/api/problem');
  state.problem = await response.json();
  elements.question.textContent = state.problem.question;
  elements.number.textContent = `#${String(state.attempted + 1).padStart(2, '0')}`;
  elements.answer.value = '';
  elements.answer.focus();
}

async function submitAnswer() {
  if (!state.active || elements.answer.value.trim() === '') return;
  const response = await fetch('/api/check', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answer: elements.answer.value, expected: state.problem.answer }) });
  const result = await response.json();
  state.attempted += 1;
  result.correct ? state.correct += 1 : state.wrong += 1;
  elements.feedback.textContent = result.correct ? 'Certo. Continue nesse ritmo.' : `A resposta era ${state.problem.answer}. Próximo.`;
  elements.feedback.className = `feedback ${result.correct ? 'correct' : 'wrong'}`;
  updateStats();
  await nextProblem();
}

function finish() {
  state.active = false;
  clearInterval(state.timerId);
  elements.answer.disabled = true; elements.submit.disabled = true; elements.start.hidden = true;
  elements.progress.textContent = 'FIM DA SESSÃO';
  elements.finalCorrect.textContent = state.correct; elements.finalWrong.textContent = state.wrong;
  elements.finalSpeed.textContent = Math.round((state.attempted / sessionLength) * 60);
  elements.results.hidden = false;
}

async function startSession() {
  state = { active: true, secondsLeft: sessionLength, correct: 0, wrong: 0, attempted: 0, problem: null, timerId: null };
  elements.results.hidden = true; elements.start.hidden = true; elements.answer.disabled = false; elements.submit.disabled = false;
  elements.progress.textContent = 'EM ANDAMENTO'; elements.feedback.textContent = 'Resolva e envie sua resposta.'; elements.feedback.className = 'feedback';
  updateStats(); await nextProblem();
  state.timerId = setInterval(() => { state.secondsLeft -= 1; updateStats(); if (state.secondsLeft <= 0) finish(); }, 1000);
}

elements.start.addEventListener('click', startSession);
elements.restart.addEventListener('click', startSession);
elements.submit.addEventListener('click', submitAnswer);
elements.answer.addEventListener('keydown', (event) => { if (event.key === 'Enter') submitAnswer(); });
updateStats();
