#!/usr/bin/env python3
"""
LearnAnywhere-CBC - Offline Learning App for Kenyan CBC Curriculum (Grades 1-9)
Supports all CBC subjects from PP1 to Grade 9.
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
            "Grade 3": [("🧮 Mathematical Activities", "mathematical_activities"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 4": [("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("🌍 Science & Technology", "science_technology"), ("🌍 Social Studies", "social_studies"), ("📖 Kiswahili", "kiswahili")],
            "Grade 5": [("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("🌍 Science & Technology", "science_technology"), ("🌍 Social Studies", "social_studies"), ("📖 Kiswahili", "kiswahili")],
            "Grade 6": [("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("🌍 Science & Technology", "science_technology"), ("🌍 Social Studies", "social_studies"), ("📖 Kiswahili", "kiswahili")],
            "Grade 7": [("🧮 Mathematics", "mathematics"), ("🔬 Integrated Science", "integrated_science"), ("🌍 Social Studies", "social_studies"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"), ("💻 Computer Studies", "computer_studies")],
            "Grade 8": [("🧮 Mathematics", "mathematics"), ("🔬 Integrated Science", "integrated_science"), ("🌍 Social Studies", "social_studies"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"), ("💻 Computer Studies", "computer_studies")],
            "Grade 9": [("🧮 Mathematics", "mathematics"), ("🔬 Integrated Science", "integrated_science"), ("🌍 Social Studies", "social_studies"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"), ("💻 Computer Studies", "computer_studies")]
        }
        return subjects.get(grade, [("Math", "math"), ("English", "english")])
    
    def show_subject_selection(self):
        """Display subject selection screen based on grade"""
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
        # (Same as before — no changes needed)
        # ... [Keep your existing show_quiz_question, next_question, finish_quiz, etc.]
        pass  # For brevity — keep your existing quiz logic

    # === STUDY MODE: GRADE + SUBJECT AWARE ===
    
    def show_study_mode(self):
        self.clear_screen()
        title_label = tk.Label(self.main_frame, text="📘 Study Mode", font=("Arial", 24, "bold"), fg="#2c3e50", bg="#f0f8ff")
        title_label.pack(pady=30)
        
        choices_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        choices_frame.pack(pady=40)
        
        flashcards_btn = tk.Button(choices_frame, text="🃏 Flashcards", font=("Arial", 16, "bold"), bg="#e74c3c", fg="white", width=20, height=2, command=self.show_flashcards_choice)
        flashcards_btn.grid(row=0, column=0, padx=30, pady=20)
        
        notes_btn = tk.Button(choices_frame, text="📓 Notes", font=("Arial", 16, "bold"), bg="#3498db", fg="white", width=20, height=2, command=self.show_notes_choice)
        notes_btn.grid(row=0, column=1, padx=30, pady=20)
        
        self.add_back_button(self.show_subject_selection)

    def show_flashcards_choice(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="🃏 Flashcards", font=("Arial", 22, "bold"), fg="#e74c3c", bg="#f0f8ff").pack(pady=20)
        subjects = self.get_subjects_for_grade(self.student_grade)
        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)
        
        for _, subject in subjects:
            btn = tk.Button(subjects_frame, text=subject.replace("_", " ").title(), font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50", command=lambda s=subject: self.display_flashcards(s))
            btn.pack(pady=8)
        self.add_back_button(self.show_study_mode)

    def display_flashcards(self, subject):
        # Load from: study_mode/flashcards/grade_1_flashcards.csv
        file_path = f"study_mode/flashcards/{self.student_grade.lower().replace(' ', '_')}_flashcards.csv"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                flashcards = [row for row in reader if row.get('subject', '').lower() == subject or not row.get('subject')]
        except:
            flashcards = []

        # Display logic same as before...
        # (Add scrollable canvas and labels)
    
    def show_notes_choice(self):
        self.clear_screen()
        tk.Label(self.main_frame, text="📓 Study Notes", font=("Arial", 22, "bold"), fg="#3498db", bg="#f0f8ff").pack(pady=20)
        subjects = self.get_subjects_for_grade(self.student_grade)
        subjects_frame = tk.Frame(self.main_frame, bg="#f0f8ff")
        subjects_frame.pack(pady=20)
        
        for _, subject in subjects:
            btn = tk.Button(subjects_frame, text=subject.replace("_", " ").title(), font=("Arial", 12), bg="#f8f9fa", fg="#2c3e50", command=lambda s=subject: self.show_notes(s))
            btn.pack(pady=8)
        self.add_back_button(self.show_study_mode)

    def show_notes(self, subject):
        filename = f"study_mode/notes/{self.student_grade.lower().replace(' ', '_')}/{subject}_notes.txt"
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            content = f"Notes for {subject.replace('_', ' ').title()} not available yet."

        # Display in Text widget...
        # (Same as before)

    def add_back_button(self, command):
        tk.Button(self.main_frame, text="🔙 Back", font=("Arial", 12), bg="#95a5a6", fg="white", command=command, padx=15, pady=8).pack(pady=15)

    # Keep your existing quiz, export, and cleanup methods...
    # (show_quiz_question, finish_quiz, export_results, etc.)

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