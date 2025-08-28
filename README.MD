# 🎓 LearnAnywhere - Offline Quiz Application

**Quality Education for All (SDG 4)**

LearnAnywhere is an offline desktop quiz application designed to support students with limited or no internet access. Built with Python and Tkinter, it provides a complete learning environment that works entirely offline.

## 🌟 Features

### Core Functionality
- **Student Login**: Name entry and grade level selection (Grade 4-8)
- **Multi-Subject Quizzes**: Math, English, Science, and Kiswahili
- **Interactive Quiz Interface**: 10 multiple-choice questions per subject
- **Auto-Scoring**: Immediate feedback with encouraging messages
- **Local Data Storage**: SQLite database for storing results

### Advanced Features
- **Study Mode**: Flashcards with key educational concepts
- **Results Export**: CSV export for teachers and administrators
- **Progress Tracking**: Historical performance data
- **Offline Operation**: No internet connection required

## 📁 Project Structure

```
LearnAnywhere/
├── main.py                 # Main application file
├── quizzes/               # Quiz question files
│   ├── math.csv
│   ├── english.csv
│   ├── science.csv
│   └── kiswahili.csv
├── study_mode/
│   └── flashcards.csv     # Study materials
├── data/
│   └── scores.db          # SQLite database (auto-created)
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually included with Python)
- No additional dependencies required!

### Installation & Running
1. Ensure you have Python installed on your system
2. Run the application:
   ```bash
   python main.py
   ```

## 💡 How to Use

### For Students
1. **Login**: Enter your name and select your grade level
2. **Choose Subject**: Click on Math, English, Science, or Kiswahili
3. **Take Quiz**: Answer 10 multiple-choice questions
4. **View Results**: See your score and encouraging feedback
5. **Study Mode**: Review flashcards for additional learning

### For Teachers
1. **Monitor Progress**: Use "Export Results" to download student scores
2. **Add Questions**: Edit CSV files in the `quizzes/` folder to add new questions
3. **Customize Content**: Modify flashcards in `study_mode/flashcards.csv`

## 📝 Quiz Format

Each quiz CSV file contains questions with this format:
```csv
question,option_a,option_b,option_c,option_d,correct_answer
"What is 2+2?",3,4,5,6,B
```

## 🎯 Educational Impact (SDG 4)

LearnAnywhere directly supports UN Sustainable Development Goal 4: Quality Education by:

- **Ensuring Inclusive Education**: Works without internet, reaching underserved communities
- **Supporting Literacy & Numeracy**: Covers core subjects (Math, English, Science)
- **Cultural Relevance**: Includes local language (Kiswahili) support
- **Teacher Support**: Provides tools for monitoring student progress
- **Self-Paced Learning**: Students can learn at their own speed

## 🛠️ Technical Details

- **GUI Framework**: Tkinter (native Python GUI)
- **Database**: SQLite for local data storage
- **Data Format**: CSV files for easy content management
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Size**: Lightweight application (~50KB + content)

## 📊 Sample Quiz Coverage

### Math (20 questions available)
- Basic arithmetic (addition, subtraction, multiplication, division)
- Fractions and percentages
- Geometry (area, perimeter, angles)
- Word problems

### English (20 questions available)
- Grammar (nouns, verbs, adjectives)
- Spelling and vocabulary
- Reading comprehension
- Sentence structure

### Science (20 questions available)
- Life science (plants, animals, human body)
- Physical science (states of matter, forces)
- Earth science (planets, weather)
- Health and nutrition

### Kiswahili (20 questions available)
- Basic vocabulary and greetings
- Grammar and sentence structure
- Cultural expressions
- Reading comprehension

## 🔧 Customization

### Adding New Questions
1. Open the appropriate CSV file in `quizzes/`
2. Add new rows following the existing format
3. Ensure correct answers are marked with A, B, C, or D

### Adding Study Materials
1. Edit `study_mode/flashcards.csv`
2. Add new terms and definitions
3. Keep definitions concise and clear

## 🤝 Contributing

This project is designed for educational use in underserved communities. Contributions are welcome:

- Additional quiz questions in local languages
- Improved user interface elements
- Translation support for more languages
- Enhanced study materials

## 📈 Future Enhancements

- **Multi-language Interface**: Full UI translation
- **Audio Support**: Question narration for better accessibility
- **Adaptive Learning**: Questions adjust based on performance
- **Offline Synchronization**: When internet becomes available
- **Mobile Version**: Using Kivy for smartphone compatibility

## 📄 License

This project is released under the MIT License, making it freely available for educational use worldwide.

## 🌍 Impact Statement

LearnAnywhere embodies the principle that quality education should be accessible to every child, regardless of their internet connectivity or economic circumstances. By providing a robust, offline learning platform, we're helping bridge the digital divide and ensuring that no student is left behind in their educational journey.

**"Education is the most powerful weapon which you can use to change the world." - Nelson Mandela**

---

*Built with ❤️ for students everywhere*