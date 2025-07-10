// Initialize EmailJS
(function(){
    emailjs.init("YOUR_USER_ID"); // Replace with your actual EmailJS User ID from your dashboard
})();

// EmailJS Configuration
const EMAIL_CONFIG = {
    serviceId: "service_ngbt5ss", // Your EmailJS Service ID
    templateId: "YOUR_TEMPLATE_ID", // Replace with your actual Template ID
    userId: "YOUR_USER_ID" // Replace with your actual User ID
};

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

// Enhanced form validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    return password.length >= 6; // Minimum 6 characters
}

function showFormError(message) {
    // Create or update error message
    let errorDiv = document.querySelector('.form-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.style.cssText = `
            background: #ff416c;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            text-align: center;
            font-weight: 600;
        `;
        document.querySelector('.login-body').insertBefore(errorDiv, document.querySelector('.form-tabs').nextSibling);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    // Hide error after 5 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}

function showFormSuccess(message) {
    // Create or update success message
    let successDiv = document.querySelector('.form-success');
    if (!successDiv) {
        successDiv = document.createElement('div');
        successDiv.className = 'form-success';
        successDiv.style.cssText = `
            background: #56ab2f;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            text-align: center;
            font-weight: 600;
        `;
        document.querySelector('.login-body').insertBefore(successDiv, document.querySelector('.form-tabs').nextSibling);
    }
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    
    // Hide success after 3 seconds
    setTimeout(() => {
        successDiv.style.display = 'none';
    }, 3000);
}

// Handle login
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    
    // Client-side validation
    if (!email) {
        showFormError('Please enter your email address.');
        return;
    }
    
    if (!validateEmail(email)) {
        showFormError('Please enter a valid email address.');
        return;
    }
    
    if (!password) {
        showFormError('Please enter your password.');
        return;
    }
    
    // Check if user exists in localStorage
    const savedUser = localStorage.getItem('user_' + email.toLowerCase());
    if (savedUser) {
        const userData = JSON.parse(savedUser);
        if (userData.password === password) {
            currentUser = userData;
            localStorage.setItem('lastUser', JSON.stringify(userData)); // Remember user
            document.getElementById('user-name').textContent = userData.name;
            showFormSuccess('Login successful! Welcome back!');
            playClickSound();
            
            // Delay navigation for better UX
            setTimeout(() => {
                showMainMenu();
            }, 1500);
        } else {
            showFormError('Invalid password. Please try again.');
        }
    } else {
        showFormError('Account not found. Please sign up first.');
    }
});

// Handle signup
document.getElementById('signup-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('signup-name').value.trim();
    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    
    // Client-side validation
    if (!name) {
        showFormError('Please enter your full name.');
        return;
    }
    
    if (name.length < 2) {
        showFormError('Name must be at least 2 characters long.');
        return;
    }
    
    if (!email) {
        showFormError('Please enter your email address.');
        return;
    }
    
    if (!validateEmail(email)) {
        showFormError('Please enter a valid email address.');
        return;
    }
    
    if (!password) {
        showFormError('Please enter a password.');
        return;
    }
    
    if (!validatePassword(password)) {
        showFormError('Password must be at least 6 characters long.');
        return;
    }
    
    // Check if user already exists
    const existingUser = localStorage.getItem('user_' + email.toLowerCase());
    if (existingUser) {
        showFormError('An account with this email already exists. Please login instead.');
        return;
    }
    
    // Save user data
    const userData = { 
        name, 
        email: email.toLowerCase(), 
        password,
        dateCreated: new Date().toISOString(),
        quizzesTaken: 0,
        bestScore: 0
    };
    
    localStorage.setItem('user_' + email.toLowerCase(), JSON.stringify(userData));
    localStorage.setItem('lastUser', JSON.stringify(userData)); // Remember user
    currentUser = userData;
    
    // Show success message
    showFormSuccess('Account created successfully! Welcome to Quiz Master!');
    playClickSound();
    
    // Send welcome email
    sendWelcomeEmail(name, email);
    
    document.getElementById('user-name').textContent = name;
    
    // Delay navigation for better UX
    setTimeout(() => {
        showMainMenu();
    }, 2000);
});

// Send welcome email using EmailJS
function sendWelcomeEmail(name, email) {
    // Prepare email template parameters
    const templateParams = {
        to_name: name,
        to_email: email,
        user_name: name,
        user_email: email,
        app_name: "Quiz Master",
        message: `Welcome to Quiz Master! We're excited to have you join our community of quiz enthusiasts. 

Here's what you can do:
• Take interactive quizzes with multiple question types
• Create your own custom questions
• Track your progress and scores
• Export and share your questions

Start your quiz journey today and test your knowledge!

Best regards,
The Quiz Master Team`,
        subject: "Welcome to Quiz Master - Let's Start Learning!"
    };

    // Check if EmailJS is properly configured
    if (EMAIL_CONFIG.templateId === 'YOUR_TEMPLATE_ID' || EMAIL_CONFIG.userId === 'YOUR_USER_ID') {
        console.log('EmailJS not fully configured. Email not sent.');
        console.log('Template params that would be sent:', templateParams);
        showNotification('Account created! Email service needs configuration.', 'info');
        return;
    }

    // Send email using EmailJS
    emailjs.send(EMAIL_CONFIG.serviceId, EMAIL_CONFIG.templateId, templateParams)
        .then(function(response) {
            console.log('Welcome email sent successfully!', response.status, response.text);
            showNotification('Welcome email sent! Check your inbox.', 'success');
        })
        .catch(function(error) {
            console.log('Failed to send email:', error);
            showNotification('Account created! (Email delivery failed)', 'warning');
        });
}

// Enhanced notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification';
    
    // Set styles based on type
    let backgroundColor, borderColor;
    switch(type) {
        case 'success':
            backgroundColor = '#56ab2f';
            borderColor = '#4a9626';
            break;
        case 'error':
            backgroundColor = '#ff416c';
            borderColor = '#e03456';
            break;
        case 'warning':
            backgroundColor = '#ff9500';
            borderColor = '#e6850d';
            break;
        default: // info
            backgroundColor = '#4facfe';
            borderColor = '#3d8bfe';
    }
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${backgroundColor};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        border-left: 4px solid ${borderColor};
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        font-weight: 600;
        max-width: 350px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

// Add CSS for notification animations
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(notificationStyles);

// Navigation functions
function showMainMenu() {
    hideAllScreens();
    document.getElementById('main-menu-screen').classList.remove('hidden');
    
    // Update user statistics display
    if (currentUser) {
        const userNameElement = document.getElementById('user-name');
        const statsHtml = `
            ${currentUser.name}
            <br>
            <small style="color: #999; font-size: 0.8em;">
                Quizzes taken: ${currentUser.quizzesTaken || 0} | 
                Best Score: ${currentUser.bestScore || 0}%
            </small>
        `;
        userNameElement.innerHTML = statsHtml;
    }
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
    if (currentUser) {
        showNotification(`Goodbye, ${currentUser.name}! Thanks for using Quiz Master.`, 'info');
    }
    
    // Clear current user data
    currentUser = null;
    localStorage.removeItem('lastUser');
    
    // Reset form fields
    document.getElementById('login-email').value = '';
    document.getElementById('login-password').value = '';
    document.getElementById('signup-name').value = '';
    document.getElementById('signup-email').value = '';
    document.getElementById('signup-password').value = '';
    
    // Hide any error/success messages
    const errorDiv = document.querySelector('.form-error');
    const successDiv = document.querySelector('.form-success');
    if (errorDiv) errorDiv.style.display = 'none';
    if (successDiv) successDiv.style.display = 'none';
    
    // Switch to login tab
    switchTab('login');
    
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
    
    // Update user statistics if logged in
    if (currentUser) {
        const percentage = Math.round((score / quizData.length) * 100);
        currentUser.quizzesTaken = (currentUser.quizzesTaken || 0) + 1;
        
        if (percentage > (currentUser.bestScore || 0)) {
            currentUser.bestScore = percentage;
            showNotification(`New personal best: ${percentage}%! 🎉`, 'success');
        }
        
        // Save updated user data
        localStorage.setItem('user_' + currentUser.email.toLowerCase(), JSON.stringify(currentUser));
        localStorage.setItem('lastUser', JSON.stringify(currentUser));
    }
    
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