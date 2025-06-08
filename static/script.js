let questions = [];
let currentQuestion = 0;
let score = 0;
let username = '';

const usernameSection = document.getElementById('username-section');
const quizSection = document.getElementById('quiz-section');
const resultSection = document.getElementById('result-section');

const questionEl = document.getElementById('question');
const optionsEl = document.getElementById('options');
const scoreEl = document.getElementById('score');
const leaderboardEl = document.getElementById('leaderboard');

const startBtn = document.getElementById('start-btn');
const nextBtn = document.getElementById('next-btn');
const restartBtn = document.getElementById('restart-btn');

startBtn.onclick = async () => {
  username = document.getElementById('username').value.trim();
  if (!username) {
    alert('Please enter a username');
    return;
  }
  const res = await fetch('/questions');
  questions = await res.json();
  currentQuestion = 0;
  score = 0;
  usernameSection.style.display = 'none';
  quizSection.style.display = 'block';
  showQuestion();
};

nextBtn.onclick = () => {
  const selected = document.querySelector('input[name="option"]:checked');
  if (!selected) {
    alert('Please select an option');
    return;
  }
  const answer = parseInt(selected.value);
  if (answer === questions[currentQuestion].answer) {
    score++;
  }
  currentQuestion++;
  if (currentQuestion < questions.length) {
    showQuestion();
  } else {
    endQuiz();
  }
};

restartBtn.onclick = () => {
  resultSection.style.display = 'none';
  usernameSection.style.display = 'block';
};

function showQuestion() {
  const q = questions[currentQuestion];
  questionEl.textContent = q.question;
  optionsEl.innerHTML = '';
  q.options.forEach((opt, idx) => {
    const label = document.createElement('label');
    const input = document.createElement('input');
    input.type = 'radio';
    input.name = 'option';
    input.value = idx;
    label.appendChild(input);
    label.appendChild(document.createTextNode(opt));
    const div = document.createElement('div');
    div.appendChild(label);
    optionsEl.appendChild(div);
  });
}

async function endQuiz() {
  quizSection.style.display = 'none';
  scoreEl.textContent = `You scored ${score} out of ${questions.length}`;
  const res = await fetch('/submit', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, score})
  });
  const leaderboard = await res.json();
  leaderboardEl.innerHTML = '';
  leaderboard.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.username}: ${item.score}`;
    leaderboardEl.appendChild(li);
  });
  resultSection.style.display = 'block';
}
