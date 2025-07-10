# 🎯 Quiz Master - Advanced Interactive Quiz Application

A modern, fully-featured quiz application with user authentication, multiple question types, and email functionality.

## ✨ Features

### 🔐 User Authentication
- **Login/Signup System**: Complete user registration and authentication
- **Email Notifications**: Automated welcome emails via EmailJS
- **Session Management**: Persistent login sessions

### 🎮 Interactive Quiz System
- **Multiple Question Types**:
  - Multiple Choice (4 options)
  - True/False questions
  - Identification (text input)
- **Progress Tracking**: Visual progress bar and question counter
- **Score Calculation**: Real-time scoring with performance feedback
- **Navigation**: Previous/Next question functionality

### ✏️ Question Creation & Management
- **Dynamic Question Creator**: Add custom questions in all supported formats
- **Question Management**: View, edit, and delete custom questions
- **Data Persistence**: Questions saved to browser localStorage
- **Export Functionality**: Download questions as JSON file

### 🎵 Sound & Settings
- **Sound Effects**: Interactive button clicks and audio feedback
- **Sound Controls**: Toggle sound on/off
- **Customizable Settings**: 
  - Time limits per question
  - Show/hide correct answers
  - Audio preferences
- **Theme Customization**: Modern gradient design with smooth animations

### 📱 Responsive Design
- **Mobile-Friendly**: Works on all screen sizes
- **Modern UI**: Beautiful gradients, animations, and smooth transitions
- **Accessibility**: Keyboard navigation and screen reader friendly

## � File Structure

The application is organized into three separate files for better maintainability:

- **`index.html`** - Main HTML structure with all screens and forms
- **`style.css`** - Complete styling and responsive design
- **`script.js`** - All JavaScript functionality and logic

## �🚀 Getting Started

### 1. Download & Setup
1. Save all three files (`index.html`, `style.css`, `script.js`) to the same directory
2. Open `index.html` in any modern web browser (Chrome, Firefox, Safari, Edge)

### 2. Email Configuration (Optional but Recommended)

To enable email notifications for new user signups, you'll need to set up EmailJS:

#### Step 1: Create EmailJS Account
1. Go to [EmailJS.com](https://www.emailjs.com/)
2. Sign up for a free account
3. Create a new email service (Gmail, Outlook, etc.)

#### Step 2: Get Your Credentials
1. **User ID**: Found in your EmailJS dashboard under "Account"
2. **Service ID**: Created when you set up your email service
3. **Template ID**: Create a new email template

#### Step 3: Update the Code
In the `script.js` file, find these lines and replace with your actual values:

```javascript
emailjs.init("YOUR_USER_ID"); // Replace with your EmailJS user ID

emailjs.send('YOUR_SERVICE_ID', 'YOUR_TEMPLATE_ID', templateParams)
```

#### Step 4: Create Email Template
In EmailJS, create an email template with these variables:
- `{{to_name}}` - Recipient's name
- `{{to_email}}` - Recipient's email
- `{{message}}` - Welcome message

Example template:
```
Subject: Welcome to Quiz Master!

Hello {{to_name}},

{{message}}

Best regards,
Quiz Master Team
```

## 📋 How to Use

### 1. First Time Setup
1. Open the app in your browser
2. Click "Sign Up" to create a new account
3. Fill in your details (name, email, password)
4. You'll receive a welcome email (if EmailJS is configured)

### 2. Taking Quizzes
1. Log in to access the main menu
2. Click "🚀 Start Quiz" 
3. Answer questions using:
   - Click for Multiple Choice and True/False
   - Type answers for Identification questions
4. Navigate with Previous/Next buttons
5. View your results at the end

### 3. Creating Questions
1. From main menu, click "✏️ Edit Questions"
2. Select question type (Multiple Choice, True/False, Identification)
3. Enter your question and answers
4. Click "Add Question" to save
5. View all questions in the list below

### 4. Settings & Customization
1. Click "⚙️ Settings" from main menu
2. Toggle sound effects and background music
3. Set time limits per question
4. Configure answer display preferences
5. Export or reset your custom questions

## 🎯 Question Types Guide

### Multiple Choice
- Create 4 answer options
- Select which option is correct
- Students click their chosen answer

### True/False
- Simple true or false statements
- Students click True or False
- Great for facts and concepts

### Identification
- Open-ended text questions
- Students type their answers
- Automatic case-insensitive matching
- Perfect for definitions and short answers

## 💾 Data Storage

- **User Accounts**: Stored in browser localStorage
- **Custom Questions**: Saved locally with export option
- **Settings**: Preferences saved between sessions
- **No Server Required**: Everything runs in your browser

## 🔧 Customization

### Adding More Default Questions
Edit the `quizData` array in `script.js`:

```javascript
{
    question: "Your question here",
    type: "multiple-choice", // or "true-false" or "identification"
    answers: ["Option 1", "Option 2", "Option 3", "Option 4"], // only for multiple-choice
    correct: 2 // index for multiple-choice, true/false for boolean, string for identification
}
```

### Styling Customization
Modify `style.css` to change:
- Colors and gradients
- Fonts and sizes
- Animation speeds
- Layout and spacing

### Structure Customization
Modify `index.html` to:
- Add new screens or sections
- Change form layouts
- Update content and text

## 🛠️ Technical Details

- **Frontend**: Pure HTML, CSS, JavaScript
- **No Dependencies**: Works offline after initial load
- **EmailJS**: For email notifications (optional)
- **LocalStorage**: For data persistence
- **Web Audio API**: For sound effects
- **Responsive Design**: CSS Grid and Flexbox

## 🌟 Advanced Features

### Sound System
- Interactive click sounds using Web Audio API
- Volume controls and mute functionality
- Audio feedback for user actions

### Performance Tracking
- Percentage-based scoring
- Performance categories (Excellent, Good, Needs Improvement)
- Detailed results with encouragement messages

### Export/Import
- Export custom questions as JSON
- Easy backup and sharing of question sets
- Future-proof data format

## 🔒 Privacy & Security

- All data stored locally in your browser
- No external servers (except EmailJS for emails)
- Passwords stored in plain text (for demo purposes)
- **Note**: For production use, implement proper password hashing

## 🐛 Troubleshooting

### Email Not Sending
1. Check EmailJS configuration
2. Verify User ID, Service ID, and Template ID
3. Ensure email service is properly connected
4. Check browser console for error messages

### Questions Not Saving
1. Ensure browser allows localStorage
2. Check if you're in private/incognito mode
3. Try refreshing the page
4. Clear browser cache and try again

### Sound Not Working
1. Click the 🔊 button to unmute
2. Some browsers require user interaction before playing audio
3. Check browser audio permissions
4. Try clicking around first, then test sound

## 📱 Browser Compatibility

- **Chrome**: Fully supported
- **Firefox**: Fully supported  
- **Safari**: Fully supported
- **Edge**: Fully supported
- **Mobile Browsers**: Responsive design works on all devices

## 🎨 Screenshots & Demo

The app features:
- 🎯 Modern login screen with tabs
- 🏠 Intuitive main menu with colorful buttons
- 📝 Comprehensive question editor
- 🎮 Interactive quiz interface
- 📊 Detailed results screen
- ⚙️ Complete settings panel

## 📞 Support

This is a demo application. For questions or issues:
1. Check the troubleshooting section above
2. Review the browser console for error messages
3. Ensure all setup steps were completed correctly

## 🎉 Enjoy Your Quiz Experience!

Quiz Master provides a complete, professional quiz experience with modern features and beautiful design. Perfect for education, training, or just fun quizzes with friends!