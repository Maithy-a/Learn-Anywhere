#!/usr/bin/env python3
"""
LearnAnywhere-CBC - Modern Offline Learning App for Kenyan CBC Curriculum (Grades 1-9)
Built with Flet for responsive, modern UI design.
"""

import flet as ft
import sqlite3
import csv
import os
from datetime import datetime
import random

class LearnAnywhereApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "LearnAnywhere-CBC 🇰🇪"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        self.page.padding = 0
        
        # Application state
        self.student_name = ""
        self.student_grade = ""
        self.current_subject = ""
        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0
        self.wrong_answers = []  # Track wrong answers for detailed results
        self.selected_answer = ""
        
        # Initialize database
        self.init_database()
        
        # Navigation state
        self.navigation_stack = []
        
        # Start with login screen
        self.show_login_screen()
    
    def init_database(self):
        """Initialize SQLite database for storing quiz results"""
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect("data/scores.db")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT NOT NULL,
                grade TEXT NOT NULL,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total_questions INTEGER NOT NULL,
                wrong_answers TEXT,
                date_taken TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    def navigate_to(self, screen_func, *args):
        """Add current screen to navigation stack and go to new screen"""
        self.navigation_stack.append((screen_func, args))
        screen_func(*args)
    
    def show_login_screen(self):
        """Display the login screen for student registration"""
        self.clear_screen()
        
        # Title
        title_label = tk.Label(
            self.main_frame,
            text="🎓 LearnAnywhere",
            font=("Arial", 28, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(
            self.main_frame,
            text="Quality Education for All - Offline Learning Made Easy",
            font=("Arial", 14),
            fg="#34495e",
            bg="#f0f8ff"
        )
        subtitle_label.pack(pady=10)
        
        # Login form container
        login_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        login_frame.pack(pady=40, padx=100, fill=tk.X)
        
        # Student name input
        tk.Label(
            login_frame,
            text="👤 Student Name:",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=10)
        
        self.name_entry = tk.Entry(
            login_frame,
            font=("Arial", 12),
            width=30,
            justify="center"
        )
        self.name_entry.pack(pady=5)
        
        # Grade selection
        tk.Label(
            login_frame,
            text="📚 Select Your Grade:",
            font=("Arial", 12, "bold"),
            bg="#ffffff"
        ).pack(pady=10)
        
        self.grade_var = tk.StringVar()
        grade_dropdown = ttk.Combobox(
            login_frame,
            textvariable=self.grade_var,
            values=["Grade 4", "Grade 5", "Grade 6", "Grade 7", "Grade 8"],
            state="readonly",
            font=("Arial", 12),
            width=20
        )
        grade_dropdown.pack(pady=5)
        
        # Start button
        start_button = ft.ElevatedButton(
            text="🚀 Start Learning!",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.login,
            padx=20,
            pady=10
        )
        start_btn.pack(pady=20)
        
        # Focus on name field
        self.name_field.focus()
    
    def handle_login(self, e):
        """Process login and move to subject selection"""
        name = self.name_field.value.strip()
        grade = self.grade_dropdown.value
        
        if not name:
            messagebox.showerror("Error", "Please enter your name!")
            return
        
        if not grade:
            messagebox.showerror("Error", "Please select your grade!")
            return
        
        self.student_name = name
        self.student_grade = grade
        self.show_subject_selection()
    
    def show_subject_selection(self):
        """Display subject selection screen"""
        self.clear_screen()
        
        # Welcome message
        welcome_label = tk.Label(
            self.main_frame,
            text=f"Welcome, {self.student_name}! 🎉",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        welcome_label.pack(pady=20)
        
        grade_label = tk.Label(
            self.main_frame,
            text=f"Grade: {self.student_grade}",
            font=("Arial", 14),
            fg="#7f8c8d",
            bg="#f0f8ff"
        )
        grade_label.pack(pady=5)
        
        # Subject selection title
        subject_title = tk.Label(
            self.main_frame,
            text="📖 Choose Your Subject:",
            font=("Arial", 18, "bold"),
            fg="#34495e",
            bg="#f0f8ff"
        )
        subject_title.pack(pady=30)
        
        # Subject buttons container
        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)
        
        # Subject buttons
        subjects = [
            ("📊 Math", "#e74c3c", "math"),
            ("📝 English", "#3498db", "english"),
            ("🔬 Science", "#9b59b6", "science"),
            ("🗣️ Kiswahili", "#f39c12", "kiswahili")
        ]
        
        for i, (text, color, subject) in enumerate(subjects):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                subjects_frame,
                text=text,
                font=("Arial", 16, "bold"),
                bg=color,
                fg="white",
                width=15,
                height=3,
                command=lambda s=subject: self.start_quiz(s)
            )
            btn.grid(row=row, column=col, padx=20, pady=15)
        
        # Additional options
        options_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        options_frame.pack(pady=30)
        
        study_btn = tk.Button(
            options_frame,
            text="💡 Study Mode",
            font=("Arial", 12, "bold"),
            bg="#16a085",
            fg="white",
            command=self.show_study_mode,
            padx=15,
            pady=5
        )
        study_btn.pack(side=tk.LEFT, padx=10)
        
        export_btn = tk.Button(
            options_frame,
            text="📤 Export Results",
            font=("Arial", 12, "bold"),
            bg="#8e44ad",
            fg="white",
            command=self.export_results,
            padx=15,
            pady=5
        )
        export_btn.pack(side=tk.LEFT, padx=10)
        
        logout_btn = tk.Button(
            options_frame,
            text="🚪 Logout",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            command=self.show_login_screen,
            padx=15,
            pady=5
        )
        logout_btn.pack(side=tk.LEFT, padx=10)
    
    def load_quiz_questions(self, subject):
        """Load quiz questions from CSV file by grade and subject"""
        quiz_file = f"quizzes/{self.student_grade.lower().replace(' ', '_')}/{subject}.csv"
        
        if not os.path.exists(quiz_file):
            messagebox.showerror("Error", f"Quiz file for {subject} not found!")
            return False
        
        try:
            with open(quiz_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                questions = list(reader)
            self.quiz_questions = random.sample(questions, min(10, len(questions)))
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load quiz: {str(e)}")
            return False
    
    def start_quiz(self, subject):
        """Start quiz for selected subject"""
        self.current_subject = subject
        if not self.load_quiz_questions(subject):
            return
        self.current_question_index = 0
        self.score = 0
        self.wrong_answers = []
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Display current quiz question with modern UI"""
        current_q = self.quiz_questions[self.current_question_index]
        
        # Quiz header
        header_frame = tk.Frame(self.main_frame, bg="#34495e")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        quiz_title = tk.Label(
            header_frame,
            text=f"📚 {self.current_subject.title()} Quiz",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#34495e"
        )
        quiz_title.pack(pady=10)
        
        progress_text = f"Question {self.current_question_index + 1} of {len(self.quiz_questions)}"
        progress_label = tk.Label(
            header_frame,
            text=progress_text,
            font=("Arial", 12),
            fg="#ecf0f1",
            bg="#34495e"
        )
        progress_label.pack(pady=5)
        
        # Question container
        question_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        question_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Current question
        current_q = self.quiz_questions[self.current_question_index]
        
        question_label = tk.Label(
            question_frame,
            text=current_q['question'],
            font=("Arial", 14, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
            wraplength=700,
            justify=tk.LEFT
        )
        question_label.pack(pady=20, padx=20)
        
        # Answer options
        self.selected_answer.set("")
        options = ['A', 'B', 'C', 'D']
        
        for option in options:
            option_text = f"{option}. {current_q[f'option_{option.lower()}']}"
            
            radio_btn = tk.Radiobutton(
                question_frame,
                text=option_text,
                variable=self.selected_answer,
                value=option,
                font=("Arial", 12),
                fg="#34495e",
                bg="#ffffff",
                anchor="w",
                wraplength=650
            )
            radio_btn.pack(fill=tk.X, padx=40, pady=8)
        
        # Navigation buttons
        nav_frame = tk.Frame(question_frame, bg="#ffffff")
        nav_frame.pack(pady=20)
        
        if self.current_question_index < len(self.quiz_questions) - 1:
            next_btn = tk.Button(
                nav_frame,
                text="Next ➡️",
                font=("Arial", 12, "bold"),
                bg="#27ae60",
                fg="white",
                command=self.next_question,
                padx=20,
                pady=10
            )
        else:
            next_btn = tk.Button(
                nav_frame,
                text="Finish Quiz 🏁",
                font=("Arial", 12, "bold"),
                bg="#e74c3c",
                fg="white",
                command=self.finish_quiz,
                padx=20,
                pady=10
            )
        )
        
        return ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    
    def next_question(self, e):
        """Move to next question"""
        if not self.selected_answer.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        # Check if answer is correct and track wrong answers
        current_q = self.quiz_questions[self.current_question_index]
        selected = self.answer_group.value
        correct = current_q['correct_answer'].upper()
        
        if selected == correct:
            self.score += 1
        else:
            # Store wrong answer details
            wrong_answer = {
                'question': current_q['question'],
                'selected': selected,
                'selected_text': current_q[f'option_{selected.lower()}'],
                'correct': correct,
                'correct_text': current_q[f'option_{correct.lower()}']
            }
            self.wrong_answers.append(wrong_answer)
        
        self.current_question_index += 1
        self.show_quiz_question()
    
    def finish_quiz(self):
        """Finish quiz and show results"""
        if not self.selected_answer.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        # Check final answer
        current_q = self.quiz_questions[self.current_question_index]
        selected = self.answer_group.value
        correct = current_q['correct_answer'].upper()
        
        if selected == correct:
            self.score += 1
        else:
            wrong_answer = {
                'question': current_q['question'],
                'selected': selected,
                'selected_text': current_q[f'option_{selected.lower()}'],
                'correct': correct,
                'correct_text': current_q[f'option_{correct.lower()}']
            }
            self.wrong_answers.append(wrong_answer)
        
        # Save results to database
        self.save_quiz_results()
        
        # Show detailed results
        self.navigate_to(self.show_quiz_results)
    
    def save_quiz_results(self):
        """Save quiz results to database including wrong answers"""
        cursor = self.conn.cursor()
        
        # Convert wrong answers to string for storage
        wrong_answers_str = str(self.wrong_answers) if self.wrong_answers else ""
        
        cursor.execute("""
            INSERT INTO quiz_results 
            (student_name, grade, subject, score, total_questions, wrong_answers, date_taken)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.student_name,
            self.student_grade,
            self.current_subject,
            self.score,
            len(self.quiz_questions),
            wrong_answers_str,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()
    
    def show_quiz_results(self):
        """Display detailed quiz results with wrong answers and solutions"""
        percentage = (self.score / len(self.quiz_questions)) * 100
        
        # Feedback based on score
        if percentage >= 80:
            feedback = "🌟 Excellent work! You're doing great!"
            color = "#27ae60"
        elif percentage >= 60:
            feedback = "👍 Good job! Keep practicing!"
            color = "#f39c12"
        else:
            feedback = "💪 Keep studying! You'll do better next time!"
            color = "#e74c3c"
        
        feedback_label = tk.Label(
            results_frame,
            text=feedback,
            font=("Arial", 16),
            fg=color,
            bg="#ffffff"
        )
        feedback_label.pack(pady=20)
        
        # Return button
        return_btn = tk.Button(
            results_frame,
            text="📚 Back to Subjects",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            command=self.show_subject_selection,
            padx=20,
            pady=10
        )
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Quiz Results")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def show_study_mode(self):
        """Display study mode with flashcards"""
        self.clear_screen()
        
        # Study mode title
        title_label = tk.Label(
            self.main_frame,
            text="💡 Study Mode - Flashcards",
            font=("Arial", 22, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        title_label.pack(pady=20)
        
        # Load flashcards
        flashcards = self.load_flashcards()
        
        if not flashcards:
            no_cards_label = tk.Label(
                self.main_frame,
                text="📝 No flashcards available yet!",
                font=("Arial", 16),
                fg="#7f8c8d",
                bg="#f0f8ff"
            )
            no_cards_label.pack(pady=50)
        else:
            # Flashcards container
            cards_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
            cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Display flashcards
            for i, card in enumerate(flashcards):
                card_frame = tk.Frame(cards_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
                card_frame.pack(fill=tk.X, pady=10)
                
                term_label = tk.Label(
                    card_frame,
                    text=f"📌 {card['term']}:",
                    font=("Arial", 14, "bold"),
                    fg="#e74c3c",
                    bg="#ffffff",
                    anchor="w"
                )
                term_label.pack(fill=tk.X, padx=15, pady=(10, 5))
                
                definition_label = tk.Label(
                    card_frame,
                    text=card['definition'],
                    font=("Arial", 12),
                    fg="#34495e",
                    bg="#ffffff",
                    anchor="w",
                    wraplength=700,
                    justify=tk.LEFT
                )
                definition_label.pack(fill=tk.X, padx=15, pady=(5, 10))
        
        # Back button
        back_btn = tk.Button(
            self.main_frame,
            text="🔙 Back to Subjects",
            font=("Arial", 12, "bold"),
            bg="#95a5a6",
            fg="white",
            command=self.show_subject_selection,
            padx=15,
            pady=8
        )
        back_btn.pack(pady=20)
    
    def load_flashcards(self):
        """Load flashcards from CSV file"""
        flashcards_file = "study_mode/flashcards.csv"
        
        if not os.path.exists(flashcards_file):
            return []
        
        try:
            with open(flashcards_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception:
            return []
    
    def export_results(self):
        """Export all quiz results to CSV file"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT student_name, grade, subject, score, total_questions, date_taken
                FROM quiz_results
                ORDER BY date_taken DESC
            """)
            results = cursor.fetchall()
            
            if not results:
                messagebox.showinfo("Info", "No quiz results to export!")
                return
            
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialvalue="quiz_results.csv"
            )
            
            if file_path:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Student Name", "Grade", "Subject", "Score", "Total Questions", "Percentage", "Date"])
                    
                    for result in results:
                        name, grade, subject, score, total, date = result
                        percentage = f"{(score/total)*100:.1f}%"
                        writer.writerow([name, grade, subject, score, total, percentage, date])
                
                messagebox.showinfo("Success", f"Results exported to {file_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export results: {str(e)}")
    
    def __del__(self):
        """Close database connection when app is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    """Main function to run the application"""
    # Ensure required directories exist
    os.makedirs("quizzes", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("study_mode", exist_ok=True)
    
    # Create and run the application
    root = tk.Tk()
    app = LearnAnywhereApp(root)
    
    try:
        root.mainloop()
    finally:
        # Ensure database connection is closed
        if hasattr(app, 'conn'):
            app.conn.close()

if __name__ == "__main__":
    ft.app(target=main)