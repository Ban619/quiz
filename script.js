// Initialize EmailJS
(function(){
    emailjs.init("YOUR_USER_ID"); // Replace with your EmailJS user ID
})();

// App State
let currentUser = null;
let soundEnabled = true;
let currentQuestionIndex = 0;
let selectedAnswers = [];
let score = 0;
let currentQuestionType = 'multiple-choice';
let selectedTrueFalseAnswer = null;

// Default quiz data with mixed question types
let quizData = [
    {
        question: "What is the capital of France?",
        type: "multiple-choice",
        answers: ["London", "Berlin", "Paris", "Madrid"],
        correct: 2
    },
    {
        question: "The Earth is flat.",
        type: "true-false",
        correct: false
    },
    {
        question: "JavaScript is a programming language.",
        type: "true-false",
        correct: true
    },
    {
        question: "What is the largest planet in our solar system?",
        type: "identification",
        correct: "Jupiter"
    },
    {
        question: "Which programming language is known as the 'language of the web'?",
        type: "multiple-choice",
        answers: ["Python", "Java", "JavaScript", "C++"],
        correct: 2
    },
    {
        question: "HTML stands for HyperText Markup Language.",
        type: "true-false",
        correct: true
    },
    {
        question: "What does CSS stand for?",
        type: "identification",
        correct: "Cascading Style Sheets"
    },
    {
        question: "Which ocean is the largest?",
        type: "multiple-choice",
        answers: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        correct: 3
    }
];

// Load custom questions from localStorage
function loadCustomQuestions() {
    const saved = localStorage.getItem('customQuestions');
    if (saved) {
        const customQuestions = JSON.parse(saved);
        quizData = [...quizData, ...customQuestions];
    }
}

// Save custom questions to localStorage
function saveCustomQuestions() {
    const customQuestions = quizData.filter(q => q.custom);
    localStorage.setItem('customQuestions', JSON.stringify(customQuestions));
}

// Sound effects
function playClickSound() {
    if (soundEnabled) {
        // Create a simple beep sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800;
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    }
}

// Login/Signup functionality
function switchTab(tab) {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const tabButtons = document.querySelectorAll('.tab-btn');
    
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    if (tab === 'login') {
        loginForm.classList.remove('hidden');
        signupForm.classList.add('hidden');
        document.querySelector('.tab-btn').classList.add('active');
    } else {
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
    }
}

// Handle login
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    // Simple validation (in real app, this would be server-side)
    const savedUser = localStorage.getItem('user_' + email);
    if (savedUser) {
        const userData = JSON.parse(savedUser);
        if (userData.password === password) {
            currentUser = userData;
            document.getElementById('user-name').textContent = userData.name;
            showMainMenu();
            playClickSound();
        } else {
            alert('Invalid password!');
        }
    } else {
        alert('User not found! Please sign up first.');
    }
});

// Handle signup
document.getElementById('signup-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    
    // Save user data
    const userData = { name, email, password };
    localStorage.setItem('user_' + email, JSON.stringify(userData));
    currentUser = userData;
    
    // Send welcome email
    sendWelcomeEmail(name, email);
    
    document.getElementById('user-name').textContent = name;
    showMainMenu();
    playClickSound();
});

// Send welcome email using EmailJS
function sendWelcomeEmail(name, email) {
    const templateParams = {
        to_name: name,
        to_email: email,
        message: `Welcome to Quiz Master! We're excited to have you join our community of quiz enthusiasts. Start creating and taking quizzes today!`
    };

    // Note: You'll need to replace these with your actual EmailJS service details
    emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', templateParams)
        .then(function(response) {
            console.log('Welcome email sent successfully!', response.status, response.text);
            alert('Welcome! A confirmation email has been sent to your inbox.');
        }, function(error) {
            console.log('Failed to send email:', error);
            alert('Account created successfully! (Email service not configured)');
        });
}

// Navigation functions
function showMainMenu() {
    hideAllScreens();
    document.getElementById('main-menu-screen').classList.remove('hidden');
}

function showQuizStart() {
    hideAllScreens();
    document.getElementById('quiz-start-screen').classList.remove('hidden');
    document.getElementById('total-questions-display').textContent = quizData.length;
    playClickSound();
}

function showEditQuestions() {
    hideAllScreens();
    document.getElementById('edit-screen').classList.remove('hidden');
    displayQuestionList();
    playClickSound();
}

function showSettings() {
    hideAllScreens();
    document.getElementById('settings-screen').classList.remove('hidden');
    playClickSound();
}

function hideAllScreens() {
    const screens = ['login-screen', 'main-menu-screen', 'quiz-start-screen', 'edit-screen', 'settings-screen', 'quiz-screen', 'results-screen'];
    screens.forEach(screen => {
        document.getElementById(screen).classList.add('hidden');
    });
}

function logout() {
    currentUser = null;
    hideAllScreens();
    document.getElementById('login-screen').classList.remove('hidden');
    playClickSound();
}

// Question creation functionality
function selectQuestionType(type) {
    currentQuestionType = type;
    
    // Update type buttons
    document.querySelectorAll('.type-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Show/hide relevant options
    document.getElementById('multiple-choice-options').classList.toggle('hidden', type !== 'multiple-choice');
    document.getElementById('true-false-options').classList.toggle('hidden', type !== 'true-false');
    document.getElementById('identification-options').classList.toggle('hidden', type !== 'identification');
    
    playClickSound();
}

function selectTrueFalse(answer) {
    selectedTrueFalseAnswer = answer;
    document.querySelectorAll('.tf-option').forEach(option => option.classList.remove('selected'));
    event.target.classList.add('selected');
    playClickSound();
}

function addQuestion() {
    const questionText = document.getElementById('question-input').value.trim();
    
    if (!questionText) {
        alert('Please enter a question!');
        return;
    }
    
    let newQuestion = {
        question: questionText,
        type: currentQuestionType,
        custom: true
    };
    
    switch (currentQuestionType) {
        case 'multiple-choice':
            const options = [
                document.getElementById('option-1').value.trim(),
                document.getElementById('option-2').value.trim(),
                document.getElementById('option-3').value.trim(),
                document.getElementById('option-4').value.trim()
            ];
            
            if (options.some(opt => !opt)) {
                alert('Please fill in all options!');
                return;
            }
            
            newQuestion.answers = options;
            newQuestion.correct = parseInt(document.getElementById('correct-answer').value);
            break;
            
        case 'true-false':
            if (selectedTrueFalseAnswer === null) {
                alert('Please select the correct answer (True or False)!');
                return;
            }
            newQuestion.correct = selectedTrueFalseAnswer;
            break;
            
        case 'identification':
            const answer = document.getElementById('identification-answer').value.trim();
            if (!answer) {
                alert('Please enter the correct answer!');
                return;
            }
            newQuestion.correct = answer;
            break;
    }
    
    quizData.push(newQuestion);
    saveCustomQuestions();
    displayQuestionList();
    clearForm();
    playClickSound();
    alert('Question added successfully!');
}

function clearForm() {
    document.getElementById('question-input').value = '';
    document.getElementById('option-1').value = '';
    document.getElementById('option-2').value = '';
    document.getElementById('option-3').value = '';
    document.getElementById('option-4').value = '';
    document.getElementById('identification-answer').value = '';
    selectedTrueFalseAnswer = null;
    document.querySelectorAll('.tf-option').forEach(option => option.classList.remove('selected'));
}

function displayQuestionList() {
    const container = document.getElementById('question-list');
    container.innerHTML = '';
    
    if (quizData.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #666;">No questions added yet.</p>';
        return;
    }
    
    quizData.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-item';
        
        let typeClass = question.type.replace('-', '-');
        let answerDisplay = '';
        
        switch (question.type) {
            case 'multiple-choice':
                answerDisplay = `Correct: ${question.answers[question.correct]}`;
                break;
            case 'true-false':
                answerDisplay = `Correct: ${question.correct ? 'True' : 'False'}`;
                break;
            case 'identification':
                answerDisplay = `Correct: ${question.correct}`;
                break;
        }
        
        questionDiv.innerHTML = `
            <span class="type-badge ${typeClass}">${question.type.replace('-', ' ').toUpperCase()}</span>
            <h4>${question.question}</h4>
            <p style="color: #666; margin-bottom: 10px;">${answerDisplay}</p>
            ${question.custom ? `<button class="delete-btn" onclick="deleteQuestion(${index})">Delete</button>` : ''}
        `;
        
        container.appendChild(questionDiv);
    });
}

function deleteQuestion(index) {
    if (confirm('Are you sure you want to delete this question?')) {
        quizData.splice(index, 1);
        saveCustomQuestions();
        displayQuestionList();
        playClickSound();
    }
}

// Settings functionality
function toggleSound() {
    soundEnabled = !soundEnabled;
    document.getElementById('sound-toggle').textContent = soundEnabled ? '🔊' : '🔇';
    localStorage.setItem('soundEnabled', soundEnabled);
}

function toggleSoundEffects() {
    const toggle = document.getElementById('sound-effects-toggle');
    toggle.classList.toggle('active');
    playClickSound();
}

function toggleBackgroundMusic() {
    const toggle = document.getElementById('bg-music-toggle');
    toggle.classList.toggle('active');
    playClickSound();
}

function toggleShowAnswers() {
    const toggle = document.getElementById('show-answers-toggle');
    toggle.classList.toggle('active');
    playClickSound();
}

function resetAllQuestions() {
    if (confirm('This will delete all custom questions. Are you sure?')) {
        localStorage.removeItem('customQuestions');
        location.reload();
        playClickSound();
    }
}

function exportQuestions() {
    const customQuestions = quizData.filter(q => q.custom);
    const dataStr = JSON.stringify(customQuestions, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'quiz_questions.json';
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    playClickSound();
}

// Quiz functionality
function startQuiz() {
    hideAllScreens();
    document.getElementById('quiz-screen').classList.remove('hidden');
    
    selectedAnswers = new Array(quizData.length).fill(null);
    currentQuestionIndex = 0;
    score = 0;
    
    document.getElementById('total-questions').textContent = quizData.length;
    displayQuestion();
    playClickSound();
}

function displayQuestion() {
    const question = quizData[currentQuestionIndex];
    
    document.getElementById('question-text').textContent = question.question;
    document.getElementById('current-question').textContent = currentQuestionIndex + 1;
    
    // Update progress bar
    const progress = ((currentQuestionIndex) / quizData.length) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';
    
    // Clear previous answers
    const answersContainer = document.getElementById('answers-container');
    answersContainer.innerHTML = '';
    
    // Create answer options based on question type
    switch (question.type) {
        case 'multiple-choice':
            question.answers.forEach((answer, index) => {
                const answerDiv = document.createElement('div');
                answerDiv.className = 'answer';
                answerDiv.textContent = answer;
                answerDiv.onclick = () => selectAnswer(index);
                
                if (selectedAnswers[currentQuestionIndex] === index) {
                    answerDiv.classList.add('selected');
                }
                
                answersContainer.appendChild(answerDiv);
            });
            break;
            
        case 'true-false':
            ['True', 'False'].forEach((answer, index) => {
                const answerDiv = document.createElement('div');
                answerDiv.className = 'answer';
                answerDiv.textContent = answer;
                answerDiv.onclick = () => selectAnswer(index === 0);
                
                if (selectedAnswers[currentQuestionIndex] === (index === 0)) {
                    answerDiv.classList.add('selected');
                }
                
                answersContainer.appendChild(answerDiv);
            });
            break;
            
        case 'identification':
            const inputDiv = document.createElement('div');
            inputDiv.innerHTML = `
                <input type="text" class="identification-input" 
                       placeholder="Type your answer here..." 
                       value="${selectedAnswers[currentQuestionIndex] || ''}"
                       oninput="handleIdentificationInput(this.value)">
            `;
            answersContainer.appendChild(inputDiv);
            break;
    }
    
    // Update button states
    document.getElementById('prev-btn').disabled = currentQuestionIndex === 0;
    document.getElementById('next-btn').disabled = selectedAnswers[currentQuestionIndex] === null;
    document.getElementById('next-btn').textContent = currentQuestionIndex === quizData.length - 1 ? 'Finish Quiz' : 'Next';
}

function selectAnswer(answerValue) {
    document.querySelectorAll('.answer').forEach(answer => {
        answer.classList.remove('selected');
    });
    
    event.target.classList.add('selected');
    selectedAnswers[currentQuestionIndex] = answerValue;
    document.getElementById('next-btn').disabled = false;
    playClickSound();
}

function handleIdentificationInput(value) {
    selectedAnswers[currentQuestionIndex] = value.trim();
    document.getElementById('next-btn').disabled = !value.trim();
}

function nextQuestion() {
    if (currentQuestionIndex < quizData.length - 1) {
        currentQuestionIndex++;
        displayQuestion();
    } else {
        showResults();
    }
    playClickSound();
}

function previousQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
    playClickSound();
}

function showResults() {
    score = 0;
    selectedAnswers.forEach((answer, index) => {
        const question = quizData[index];
        
        switch (question.type) {
            case 'multiple-choice':
                if (answer === question.correct) score++;
                break;
            case 'true-false':
                if (answer === question.correct) score++;
                break;
            case 'identification':
                if (answer && answer.toLowerCase() === question.correct.toLowerCase()) score++;
                break;
        }
    });
    
    hideAllScreens();
    document.getElementById('results-screen').classList.remove('hidden');
    
    document.getElementById('final-score').textContent = `${score}/${quizData.length}`;
    const percentage = Math.round((score / quizData.length) * 100);
    document.getElementById('score-percentage').textContent = `${percentage}%`;
    
    const performanceMessage = document.getElementById('performance-message');
    if (percentage >= 80) {
        performanceMessage.textContent = "Excellent! You're a quiz master! 🏆";
        performanceMessage.className = "performance-message excellent";
    } else if (percentage >= 60) {
        performanceMessage.textContent = "Good job! Keep learning! 👍";
        performanceMessage.className = "performance-message good";
    } else {
        performanceMessage.textContent = "Keep practicing! You'll do better next time! 💪";
        performanceMessage.className = "performance-message needs-improvement";
    }
    
    document.getElementById('progress-fill').style.width = '100%';
    playClickSound();
}

function restartQuiz() {
    showQuizStart();
    document.getElementById('progress-fill').style.width = '0%';
    playClickSound();
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadCustomQuestions();
    
    // Load sound preference
    const savedSound = localStorage.getItem('soundEnabled');
    if (savedSound !== null) {
        soundEnabled = savedSound === 'true';
        document.getElementById('sound-toggle').textContent = soundEnabled ? '🔊' : '🔇';
    }
    
    // Check if user is already logged in
    const lastUser = localStorage.getItem('lastUser');
    if (lastUser) {
        currentUser = JSON.parse(lastUser);
        document.getElementById('user-name').textContent = currentUser.name;
        showMainMenu();
    }
    
    displayQuestionList();
});