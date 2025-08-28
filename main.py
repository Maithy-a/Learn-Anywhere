#!/usr/bin/env python3
"""
LearnAnywhere - Offline Quiz Application for Quality Education (SDG 4)
A desktop application supporting students with limited or no internet access.

Features:
- Login with student name and grade selection
- Multiple subjects: Math, English, Science, Kiswahili
- 10-question multiple choice quizzes
- Auto-scoring with feedback
- Local data storage with SQLite
- Study mode with flashcards and subject notes
- Export results to CSV for teachers

Author: LearnAnywhere Team
License: MIT
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
import os
from datetime import datetime
import random

class LearnAnywhereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LearnAnywhere - Quality Education for All")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f8ff")
        
        # Application state
        self.student_name = ""
        self.student_grade = ""
        self.current_subject = ""
        self.quiz_questions = []
        self.current_question_index = 0
        self.score = 0
        self.selected_answer = tk.StringVar()
        
        # Initialize database
        self.init_database()
        
        # Create main container
        self.main_frame = tk.Frame(self.root, bg="#f0f8ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
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
                date_taken TEXT NOT NULL
            )
        """)
        self.conn.commit()
    
    def clear_screen(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
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
        start_btn = tk.Button(
            login_frame,
            text="🚀 Start Learning!",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.login,
            padx=20,
            pady=10
        )
        start_btn.pack(pady=20)
        
        # Focus on name entry
        self.name_entry.focus()
    
    def login(self):
        """Process login and move to subject selection"""
        name = self.name_entry.get().strip()
        grade = self.grade_var.get()
        
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
        """Load quiz questions from CSV file"""
        quiz_file = f"quizzes/{subject}.csv"
        
        if not os.path.exists(quiz_file):
            messagebox.showerror("Error", f"Quiz file for {subject} not found!")
            return False
        
        try:
            with open(quiz_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                questions = list(reader)
                
            # Randomly select 10 questions
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
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Display current quiz question"""
        self.clear_screen()
        
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
        
        next_btn.pack()
    
    def next_question(self):
        """Move to next question"""
        if not self.selected_answer.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        # Check if answer is correct
        current_q = self.quiz_questions[self.current_question_index]
        if self.selected_answer.get() == current_q['correct_answer'].upper():
            self.score += 1
        
        self.current_question_index += 1
        self.show_quiz_question()
    
    def finish_quiz(self):
        """Finish quiz and show results"""
        if not self.selected_answer.get():
            messagebox.showwarning("Warning", "Please select an answer!")
            return
        
        # Check final answer
        current_q = self.quiz_questions[self.current_question_index]
        if self.selected_answer.get() == current_q['correct_answer'].upper():
            self.score += 1
        
        # Save results to database
        self.save_quiz_results()
        
        # Show results
        self.show_quiz_results()
    
    def save_quiz_results(self):
        """Save quiz results to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO quiz_results 
            (student_name, grade, subject, score, total_questions, date_taken)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.student_name,
            self.student_grade,
            self.current_subject,
            self.score,
            len(self.quiz_questions),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()
    
    def show_quiz_results(self):
        """Display quiz results with feedback"""
        self.clear_screen()
        
        # Results container
        results_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
        
        # Results title
        title_label = tk.Label(
            results_frame,
            text="🎉 Quiz Complete!",
            font=("Arial", 24, "bold"),
            fg="#27ae60",
            bg="#ffffff"
        )
        title_label.pack(pady=20)
        
        # Score display
        score_text = f"You got {self.score}/{len(self.quiz_questions)}!"
        score_label = tk.Label(
            results_frame,
            text=score_text,
            font=("Arial", 20, "bold"),
            fg="#2c3e50",
            bg="#ffffff"
        )
        score_label.pack(pady=10)
        
        # Feedback message
        percentage = (self.score / len(self.quiz_questions)) * 100
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
        return_btn.pack(pady=30)
    
    # ==================== STUDY MODE: FULLY UPGRADED ====================
    
    def show_study_mode(self):
        """Display Study Mode with Flashcards or Notes choice"""
        self.clear_screen()

        title_label = tk.Label(
            self.main_frame,
            text="📘 Study Mode",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        title_label.pack(pady=30)

        subtitle_label = tk.Label(
            self.main_frame,
            text="Choose how you'd like to study",
            font=("Arial", 14),
            fg="#7f8c8d",
            bg="#f0f8ff"
        )
        subtitle_label.pack(pady=10)

        # Choice buttons
        choices_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        choices_frame.pack(pady=40)

        flashcards_btn = tk.Button(
            choices_frame,
            text="🃏 Flashcards",
            font=("Arial", 16, "bold"),
            bg="#e74c3c",
            fg="white",
            width=20,
            height=2,
            command=self.show_flashcards_choice
        )
        flashcards_btn.grid(row=0, column=0, padx=30, pady=20)

        notes_btn = tk.Button(
            choices_frame,
            text="📓 Notes",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.show_notes_choice
        )
        notes_btn.grid(row=0, column=1, padx=30, pady=20)

        # Back button
        back_btn = tk.Button(
            self.main_frame,
            text="🔙 Back to Subjects",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            command=self.show_subject_selection,
            padx=15,
            pady=8
        )
        back_btn.pack(pady=20)

    def show_flashcards_choice(self):
        """Let user pick subject for flashcards"""
        self.clear_screen()

        title_label = tk.Label(
            self.main_frame,
            text="🃏 Flashcards",
            font=("Arial", 22, "bold"),
            fg="#e74c3c",
            bg="#f0f8ff"
        )
        title_label.pack(pady=20)

        tk.Label(
            self.main_frame,
            text="Select a subject:",
            font=("Arial", 14),
            bg="#f0f8ff"
        ).pack(pady=10)

        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)

        for subject in ["math", "english", "science", "kiswahili"]:
            btn = tk.Button(
                subjects_frame,
                text=f"{subject.title()}",
                font=("Arial", 14),
                bg="#f8f9fa",
                fg="#2c3e50",
                width=15,
                command=lambda s=subject: self.display_flashcards(s)
            )
            btn.pack(pady=8)

        self.add_back_button(self.show_study_mode)

    def display_flashcards(self, subject):
        """Display all flashcards (currently all from CSV)"""
        self.clear_screen()

        title_label = tk.Label(
            self.main_frame,
            text=f"🃏 Flashcards: {subject.title()}",
            font=("Arial", 20, "bold"),
            fg="#e74c3c",
            bg="#f0f8ff"
        )
        title_label.pack(pady=20)

        flashcards = self.load_flashcards()
        if not flashcards:
            no_cards_label = tk.Label(
                self.main_frame,
                text="No flashcards available.",
                font=("Arial", 14),
                fg="#7f8c8d",
                bg="#f0f8ff"
            )
            no_cards_label.pack(pady=50)
        else:
            canvas = tk.Canvas(self.main_frame, bg="#f0f8ff")
            scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            for card in flashcards:
                card_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
                card_frame.pack(fill=tk.X, pady=8, padx=20)

                term_label = tk.Label(
                    card_frame,
                    text=f"🔹 {card['term']}",
                    font=("Arial", 13, "bold"),
                    fg="#e74c3c",
                    bg="white",
                    anchor="w"
                )
                term_label.pack(fill=tk.X, padx=15, pady=5)

                def_label = tk.Label(
                    card_frame,
                    text=card['definition'],
                    font=("Arial", 11),
                    fg="#34495e",
                    bg="white",
                    anchor="w",
                    wraplength=700,
                    justify=tk.LEFT
                )
                def_label.pack(fill=tk.X, padx=15, pady=(5, 10))

            canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
            scrollbar.pack(side="right", fill="y")

        self.add_back_button(self.show_flashcards_choice)

    def show_notes_choice(self):
        """Let user pick subject for notes"""
        self.clear_screen()

        title_label = tk.Label(
            self.main_frame,
            text="📓 Study Notes",
            font=("Arial", 22, "bold"),
            fg="#3498db",
            bg="#f0f8ff"
        )
        title_label.pack(pady=20)

        tk.Label(
            self.main_frame,
            text="Select a subject to read notes:",
            font=("Arial", 14),
            bg="#f0f8ff"
        ).pack(pady=10)

        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)

        for subject in ["math", "science", "english", "kiswahili"]:
            btn = tk.Button(
                subjects_frame,
                text=f"{subject.title()}",
                font=("Arial", 14),
                bg="#f8f9fa",
                fg="#2c3e50",
                width=15,
                command=lambda s=subject: self.show_notes(s)
            )
            btn.pack(pady=8)

        self.add_back_button(self.show_study_mode)

    def show_notes(self, subject):
        """Display notes for selected subject"""
        self.clear_screen()

        title_label = tk.Label(
            self.main_frame,
            text=f"📓 Notes: {subject.title()}",
            font=("Arial", 20, "bold"),
            fg="#3498db",
            bg="#f0f8ff"
        )
        title_label.pack(pady=20)

        filename = f"study_mode/notes/{subject.lower()}_notes.txt"
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = f"Notes for {subject.title()} not available yet."

        text_widget = tk.Text(
            self.main_frame,
            wrap=tk.WORD,
            font=("Arial", 12),
            bg="white",
            fg="#34495e",
            padx=20,
            pady=10,
            height=20
        )
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)  # Make read-only
        text_widget.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        self.add_back_button(self.show_notes_choice)

    def add_back_button(self, command):
        """Add a consistent back button"""
        back_btn = tk.Button(
            self.main_frame,
            text="🔙 Back",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            command=command,
            padx=15,
            pady=8
        )
        back_btn.pack(pady=15)
    
    # ==================== OTHER FEATURES ====================
    
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
                initialfile="quiz_results.csv"
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
    os.makedirs("study_mode/notes", exist_ok=True)  # Create notes folder
    
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
    main()