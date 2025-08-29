#!/usr/bin/env python3
"""
LearnAnywhere-CBC - Offline Learning App for Kenyan CBC Curriculum (Grades 1-9)
Supports all CBC subjects from Grade 1 to Grade 9.
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
        self.root.title("LearnAnywhere-CBC 🇰🇪")
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
            text="🎓 LearnAnywhere-CBC",
            font=("Arial", 28, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        title_label.pack(pady=30)
        
        subtitle_label = tk.Label(
            self.main_frame,
            text="Kenya's CBC Curriculum | Offline Learning for All",
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
        
        # Grade selection (Grades 1–9)
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
            values=[
                "Grade 1", "Grade 2", "Grade 3", "Grade 4",
                "Grade 5", "Grade 6", "Grade 7", "Grade 8", "Grade 9"
            ],
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
    
    def get_subjects_for_grade(self, grade):
        """Return CBC subjects based on grade level"""
        subjects = {
            "Grade 1": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 2": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 3": [("🧮 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 4": [
                ("🧮 Mathematics", "mathematics"),
                ("📚 English", "english"),
                ("📖 Kiswahili", "kiswahili"),
                ("🔬 Science & Technology", "science_technology"),
                ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"),
                ("🎨 Creative Arts", "creative_arts"),
                ("✝️ CRE", "cre")
            ],
            "Grade 5": [
                ("🧮 Mathematics", "mathematics"),
                ("📚 English", "english"),
                ("📖 Kiswahili", "kiswahili"),
                ("🔬 Science & Technology", "science_technology"),
                ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"),
                ("🎨 Creative Arts", "creative_arts"),
                ("✝️ CRE", "cre"),
                ("☪️ IRE", "ire")
            ],
            "Grade 6": [
                ("🧮 Mathematics", "mathematics"),
                ("📚 English", "english"),
                ("📖 Kiswahili", "kiswahili"),
                ("🔬 Science & Technology", "science_technology"),
                ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"),
                ("🎨 Creative Arts", "creative_arts"),
                ("✝️ CRE", "cre"),
                ("☪️ IRE", "ire")
            ],
            "Grade 7": [
                ("🧮 Mathematics", "mathematics"),
                ("📚 English", "english"),
                ("📖 Kiswahili", "kiswahili"),
                ("🔬 Integrated Science", "integrated_science"),
                ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"),
                ("🎨 Creative Arts", "creative_arts"),
                ("✝️ CRE", "cre"),
                ("☪️ IRE", "ire")
            ],
            "Grade 8": [
                ("🧮 Mathematics", "mathematics"),
                ("📚 English", "english"),
                ("📖 Kiswahili", "kiswahili"),
                ("🔬 Integrated Science", "integrated_science"),
                ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"),
                ("🎨 Creative Arts", "creative_arts"),
                ("✝️ CRE", "cre"),
                ("☪️ IRE", "ire")
            ],
            "Grade 9": [
                ("🧮 Mathematics", "mathematics"),
                ("📚 English", "english"),
                ("📖 Kiswahili", "kiswahili"),
                ("🔬 Integrated Science", "integrated_science"),
                ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"),
                ("🎨 Creative Arts", "creative_arts"),
                ("✝️ CRE", "cre"),
                ("☪️ IRE", "ire")
            ],
        }
        return subjects.get(grade, [("Math", "math"), ("English", "english")])
    
    def show_subject_selection(self):
        """Display subject selection screen with 2-column layout and full scroll support"""
        self.clear_screen()

        # Create a canvas and scrollbar
        canvas = tk.Canvas(self.main_frame, bg="#f0f8ff")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Welcome message
        welcome_label = tk.Label(
            scrollable_frame,
            text=f"Welcome, {self.student_name}! 🎉",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        welcome_label.pack(pady=20)

        grade_label = tk.Label(
            scrollable_frame,
            text=f"Grade: {self.student_grade}",
            font=("Arial", 14),
            fg="#7f8c8d",
            bg="#f0f8ff"
        )
        grade_label.pack(pady=5)

        # Subject selection title
        subject_title = tk.Label(
            scrollable_frame,
            text="📖 Choose Your Subject:",
            font=("Arial", 18, "bold"),
            fg="#34495e",
            bg="#f0f8ff"
        )
        subject_title.pack(pady=20)

        # Subject buttons container (2-column grid)
        subjects_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=10)

        subjects = self.get_subjects_for_grade(self.student_grade)

        for i, (text, subject) in enumerate(subjects):
            row = i // 2
            col = i % 2

            btn = tk.Button(
                subjects_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg="#3498db",
                fg="white",
                width=20,
                height=2,
                command=lambda s=subject: self.start_quiz(s)
            )
            btn.grid(row=row, column=col, padx=25, pady=12)

        # Additional options
        options_frame = tk.Frame(scrollable_frame, bg="#f0f8ff")
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

    # ==================== QUIZ MODE ====================
    def load_quiz_questions(self, subject):
        """Load quiz questions from CSV file by grade and subject"""
        quiz_file = f"quizzes/{self.student_grade.lower().replace(' ', '_')}/{subject}.csv"
        
        if not os.path.exists(quiz_file):
            messagebox.showerror("Error", f"Quiz file not found: {quiz_file}")
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
        self.show_quiz_question()
    
    def show_quiz_question(self):
        """Display current quiz question"""
        self.clear_screen()
        
        # Quiz header
        header_frame = tk.Frame(self.main_frame, bg="#34495e")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        quiz_title = tk.Label(
            header_frame,
            text=f"📚 {self.current_subject.replace('_', ' ').title()} Quiz",
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

        # Back Button (disabled on first question)
        back_btn = tk.Button(
            nav_frame,
            text="🔙 Back",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            command=self.previous_question,
            state="normal" if self.current_question_index > 0 else "disabled",
            padx=15,
            pady=8
        )
        back_btn.grid(row=0, column=0, padx=10)

        # Next / Finish Button
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
        next_btn.grid(row=0, column=1, padx=10)

        # Quit Quiz Button
        quit_btn = tk.Button(
            nav_frame,
            text="🚪 Quit Quiz",
            font=("Arial", 12),
            bg="#e67e22",
            fg="white",
            command=self.confirm_quit_quiz,
            padx=15,
            pady=8
        )
        quit_btn.grid(row=0, column=2, padx=10)
    
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
    
    def previous_question(self):
        """Go to the previous question"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_quiz_question()
    
    def confirm_quit_quiz(self):
        """Ask user before quitting the quiz"""
        if messagebox.askyesno("Quit Quiz?", "Are you sure you want to quit this quiz? Your progress will be lost."):
            self.show_subject_selection()
    
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
    
    # ==================== STUDY MODE ====================
    def show_study_mode(self):
        self.clear_screen()
        title_label = tk.Label(
            self.main_frame,
            text="📘 Study Mode",
            font=("Arial", 24, "bold"),
            fg="#2c3e50",
            bg="#f0f8ff"
        )
        title_label.pack(pady=30)
        
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
        
        self.add_back_button(self.show_subject_selection)

    def show_flashcards_choice(self):
        self.clear_screen()
        tk.Label(
            self.main_frame,
            text="🃏 Flashcards",
            font=("Arial", 22, "bold"),
            fg="#e74c3c",
            bg="#f0f8ff"
        ).pack(pady=20)
        
        subjects = self.get_subjects_for_grade(self.student_grade)
        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)
        
        for _, subject in subjects:
            btn = tk.Button(
                subjects_frame,
                text=subject.replace("_", " ").title(),
                font=("Arial", 12),
                bg="#f8f9fa",
                fg="#2c3e50",
                command=lambda s=subject: self.display_flashcards(s)
            )
            btn.pack(pady=8)
        
        self.add_back_button(self.show_study_mode)

    def display_flashcards(self, subject):
        self.clear_screen()
        tk.Label(
            self.main_frame,
            text=f"🃏 Flashcards: {subject.replace('_', ' ').title()}",
            font=("Arial", 20, "bold"),
            fg="#e74c3c",
            bg="#f0f8ff"
        ).pack(pady=20)
        
        file_path = f"study_mode/flashcards/{self.student_grade.lower().replace(' ', '_')}/{subject}.csv"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                flashcards = list(reader)
        except FileNotFoundError:
            flashcards = []
        except Exception as e:
            messagebox.showerror("Error", f"Could not load flashcards: {str(e)}")
            flashcards = []

        if not flashcards:
            no_label = tk.Label(
                self.main_frame,
                text=f"No flashcards available for {subject.replace('_', ' ').title()}.",
                font=("Arial", 14),
                fg="#7f8c8d",
                bg="#f0f8ff"
            )
            no_label.pack(pady=50)
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
                
                tk.Label(
                    card_frame,
                    text=f"🔹 {card['term']}",
                    font=("Arial", 13, "bold"),
                    fg="#e74c3c",
                    bg="white",
                    anchor="w"
                ).pack(fill=tk.X, padx=15, pady=5)
                
                tk.Label(
                    card_frame,
                    text=card['definition'],
                    font=("Arial", 11),
                    fg="#34495e",
                    bg="white",
                    anchor="w",
                    wraplength=700,
                    justify=tk.LEFT
                ).pack(fill=tk.X, padx=15, pady=(5, 10))
            
            canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
            scrollbar.pack(side="right", fill="y")
        
        self.add_back_button(self.show_flashcards_choice)

    def show_notes_choice(self):
        self.clear_screen()
        tk.Label(
            self.main_frame,
            text="📓 Study Notes",
            font=("Arial", 22, "bold"),
            fg="#3498db",
            bg="#f0f8ff"
        ).pack(pady=20)
        
        subjects = self.get_subjects_for_grade(self.student_grade)
        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)
        
        for _, subject in subjects:
            btn = tk.Button(
                subjects_frame,
                text=subject.replace("_", " ").title(),
                font=("Arial", 12),
                bg="#f8f9fa",
                fg="#2c3e50",
                command=lambda s=subject: self.show_notes(s)
            )
            btn.pack(pady=8)
        
        self.add_back_button(self.show_study_mode)

    def show_notes(self, subject):
        self.clear_screen()
        tk.Label(
            self.main_frame,
            text=f"📓 Notes: {subject.replace('_', ' ').title()}",
            font=("Arial", 20, "bold"),
            fg="#3498db",
            bg="#f0f8ff"
        ).pack(pady=20)
        
        filename = f"study_mode/notes/{self.student_grade.lower().replace(' ', '_')}/{subject}_notes.txt"
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = f"Notes for {subject.replace('_', ' ').title()} not available yet."
        
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
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        self.add_back_button(self.show_notes_choice)

    def add_back_button(self, command):
        tk.Button(
            self.main_frame,
            text="🔙 Back",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            command=command,
            padx=15,
            pady=8
        ).pack(pady=15)
    
    def export_results(self):
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
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    # Ensure all folders exist
    os.makedirs("data", exist_ok=True)
    for i in range(1, 10):
        os.makedirs(f"quizzes/grade_{i}", exist_ok=True)
        os.makedirs(f"study_mode/notes/grade_{i}", exist_ok=True)
    os.makedirs("study_mode/flashcards", exist_ok=True)
    
    root = tk.Tk()
    app = LearnAnywhereApp(root)
    try:
        root.mainloop()
    finally:
        if hasattr(app, 'conn'):
            app.conn.close()

if __name__ == "__main__":
    main()