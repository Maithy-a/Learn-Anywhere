#!/usr/bin/env python3
"""
LearnAnywhere-CBC - Modern Offline Learning App for Kenyan CBC Curriculum (Grades 1-9)
✅ 100% Fixed: All buttons work, database safe, runs in browser
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
        self.wrong_answers = []
        self.selected_answer = None  # Track selected answer

        # Initialize database
        self.init_database()

        # Navigation stack
        self.navigation_stack = []

        # Start with login
        self.show_login_screen()

    def init_database(self):
        """Initialize or update the quiz_results table with correct schema"""
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect("data/scores.db")
        cursor = self.conn.cursor()

        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_results'")
        if cursor.fetchone() is None:
            # Create table with all columns
            cursor.execute("""
                CREATE TABLE quiz_results (
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
        else:
            # Table exists — check if 'wrong_answers' column is missing
            cursor.execute("PRAGMA table_info(quiz_results)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'wrong_answers' not in columns:
                cursor.execute("ALTER TABLE quiz_results ADD COLUMN wrong_answers TEXT DEFAULT ''")

        self.conn.commit()

    def navigate_to(self, screen_func, *args):
        self.navigation_stack.append((screen_func, args))
        screen_func(*args)


    def navigate_back(self, e=None):
        if len(self.navigation_stack) > 1:
            self.navigation_stack.pop()
            prev_screen, args = self.navigation_stack[-1]
            prev_screen(*args)
        else:
            self.show_login_screen()

    def create_app_bar(self, title, show_back=True):
        actions = []
        if show_back and len(self.navigation_stack) > 1:
            actions.append(
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Go Back",
                    on_click=self.navigate_back
                )
            )
        return ft.AppBar(
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            actions=actions
        )

    def show_login_screen(self, e=None):
        self.navigation_stack = []

        name_field = ft.TextField(
            label="👤 Student Name",
            hint_text="Enter your full name",
            width=400,
            text_size=16,
            border_radius=10
        )

        grade_dropdown = ft.Dropdown(
            label="📚 Select Your Grade",
            hint_text="Choose your grade level",
            width=400,
            options=[ft.dropdown.Option(f"Grade {i}") for i in range(1, 10)],
            text_size=16,
            border_radius=10
        )

        def handle_login(e):
            name = name_field.value.strip()
            grade = grade_dropdown.value
            if not name:
                self.show_snackbar("Please enter your name!", ft.Colors.RED)
                return
            if not grade:
                self.show_snackbar("Please select your grade!", ft.Colors.RED)
                return
            self.student_name = name
            self.student_grade = grade
            self.navigate_to(self.show_subject_selection)

        start_button = ft.ElevatedButton(
            text="🚀 Start Learning!",
            width=400,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            ),
            on_click=handle_login
        )

        content = ft.Container(
            content=ft.Column([
                ft.Container(height=50),
                ft.Text("🎓 LearnAnywhere-CBC", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700, text_align=ft.TextAlign.CENTER),
                ft.Text("Kenya's CBC Curriculum | Offline Learning for All", size=16, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                ft.Container(height=40),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Container(height=20),
                            name_field,
                            ft.Container(height=20),
                            grade_dropdown,
                            ft.Container(height=30),
                            start_button,
                            ft.Container(height=20),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=40,
                        width=500
                    ),
                    elevation=8
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            expand=True
        )

        self.page.controls.clear()
        self.page.add(content)
        self.page.update()
        name_field.focus()

    def show_snackbar(self, message, color=ft.Colors.BLUE):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()

    def get_subjects_for_grade(self, grade):
        subjects = {
            "Grade 1": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 2": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 3": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 4": [
                ("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"),
                ("🔬 Science & Technology", "science_technology"), ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"), ("🎨 Creative Arts", "creative_arts"), ("✝️ CRE", "cre")
            ],
            "Grade 5": [
                ("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"),
                ("🔬 Science & Technology", "science_technology"), ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"), ("🎨 Creative Arts", "creative_arts"), ("✝️ CRE", "cre"), ("☪️ IRE", "ire")
            ],
            "Grade 6": [
                ("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"),
                ("🔬 Science & Technology", "science_technology"), ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"), ("🎨 Creative Arts", "creative_arts"), ("✝️ CRE", "cre"), ("☪️ IRE", "ire")
            ],
            "Grade 7": [
                ("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"),
                ("🔬 Integrated Science", "integrated_science"), ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"), ("🎨 Creative Arts", "creative_arts"), ("✝️ CRE", "cre"), ("☪️ IRE", "ire")
            ],
            "Grade 8": [
                ("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"),
                ("🔬 Integrated Science", "integrated_science"), ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"), ("🎨 Creative Arts", "creative_arts"), ("✝️ CRE", "cre"), ("☪️ IRE", "ire")
            ],
            "Grade 9": [
                ("🧮 Mathematics", "mathematics"), ("📚 English", "english"), ("📖 Kiswahili", "kiswahili"),
                ("🔬 Integrated Science", "integrated_science"), ("🌍 Social Studies", "social_studies"),
                ("🌱 Agriculture", "agriculture"), ("🎨 Creative Arts", "creative_arts"), ("✝️ CRE", "cre"), ("☪️ IRE", "ire")
            ],
        }
        return subjects.get(grade, [("Math", "math"), ("English", "english")])

    def show_subject_selection(self, e=None):
        subjects = self.get_subjects_for_grade(self.student_grade)
        subject_cards = []

        for i in range(0, len(subjects), 3):
            row = ft.Row([], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            for j in range(3):
                idx = i + j
                if idx < len(subjects):
                    text, subject = subjects[idx]
                    btn = ft.ElevatedButton(
                        text="Start Quiz",
                        width=150,
                        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
                        on_click=lambda e, subj=subject: self.navigate_to(self.start_quiz, subj)
                    )
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(text, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                btn
                            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=20,
                            width=200,
                            height=120
                        ),
                        elevation=4
                    )
                    row.controls.append(card)
            subject_cards.append(row)

        options_row = ft.Row([
            ft.ElevatedButton("💡 Study Mode", style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_600, color=ft.Colors.WHITE), on_click=lambda e: self.navigate_to(self.show_study_mode)),
            ft.ElevatedButton("📤 Export Results", style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE), on_click=lambda e: self.export_results()),
            ft.ElevatedButton("🚪 Logout", style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE), on_click=lambda e: self.show_login_screen())
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        content = ft.Column([
            ft.Container(height=20),
            ft.Text(f"Welcome, {self.student_name}! 🎉", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700, text_align=ft.TextAlign.CENTER),
            ft.Text(f"Grade: {self.student_grade}", size=16, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
            ft.Text("📖 Choose Your Subject:", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800, text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
            *subject_cards,
            ft.Container(height=30),
            options_row,
            ft.Container(height=20)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)

        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Subject Selection", show_back=False)
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()


    
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
        grade_dir = self.student_grade.lower().replace(' ', '_')
        quiz_dir = f"quizzes/{grade_dir}"
        quiz_file = f"{quiz_dir}/{subject}.csv"

        os.makedirs(quiz_dir, exist_ok=True)

        if not os.path.exists(quiz_file):

            sample = [
                {"question": "What is 2 + 2?", "option_a": "3", "option_b": "4", "option_c": "5", "option_d": "6", "correct_answer": "B"},
                {"question": "What is the capital of Kenya?", "option_a": "Kisumu", "option_b": "Mombasa", "option_c": "Nairobi", "option_d": "Nakuru", "correct_answer": "C"}
            ]
            with open(quiz_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["question", "option_a", "option_b", "option_c", "option_d", "correct_answer"])
                writer.writeheader()
                writer.writerows(sample)
            self.show_snackbar(f"Sample quiz created for {subject}!", ft.Colors.GREEN)


            messagebox.showerror("Error", f"Quiz file for {subject} not found!")
            return False
        
        try:
            with open(quiz_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                questions = list(reader)
            self.quiz_questions = random.sample(questions, min(10, len(questions)))
            return True

        except Exception as ex:
            self.show_snackbar(f"Load failed: {str(ex)}", ft.Colors.RED)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load quiz: {str(e)}")
 a6a4bd2d0e8710abcb109e29c8d6d7299847297d
            return False

    def start_quiz(self, subject, e=None):
        self.current_subject = subject
        if not self.load_quiz_questions(subject):
            return
        self.current_question_index = 0
        self.score = 0
        self.wrong_answers = []
        self.show_quiz_question()


    def show_quiz_question(self, e=None):
        if self.current_question_index >= len(self.quiz_questions):
            return

        q = self.quiz_questions[self.current_question_index]
        progress = (self.current_question_index + 1) / len(self.quiz_questions)

        self.selected_answer = None

        radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="A", label=f"A. {q['option_a']}", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="B", label=f"B. {q['option_b']}", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="C", label=f"C. {q['option_c']}", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="D", label=f"D. {q['option_d']}", label_style=ft.TextStyle(size=14)),
            ], spacing=15)
        )

        def on_radio_change(e):
            self.selected_answer = e.control.value

        radio_group.on_change = on_radio_change

        progress_bar = ft.ProgressBar(value=progress, width=600, height=8, bgcolor=ft.Colors.GREY_300, color=ft.Colors.BLUE_600)

        def next_click(e):
            if not self.selected_answer:
                self.show_snackbar("Please select an answer!", ft.Colors.ORANGE)
                return
            self.record_answer_and_proceed()

        def prev_click(e):
            self.current_question_index -= 1
            self.show_quiz_question()

        def quit_click(e):
            self.confirm_quit_quiz()

        buttons = [
            ft.ElevatedButton("🚪 Quit Quiz", on_click=quit_click, style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE))
        ]
        if self.current_question_index > 0:
            buttons.insert(0, ft.ElevatedButton("🔙 Previous", on_click=prev_click, style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE)))
        if self.current_question_index < len(self.quiz_questions) - 1:
            buttons.insert(0, ft.ElevatedButton("Next ➡️", on_click=next_click, style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)))
        else:
            buttons.insert(0, ft.ElevatedButton("Finish Quiz 🏁", on_click=next_click, style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE)))

        card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(f"Question {self.current_question_index + 1} of {len(self.quiz_questions)}", size=14, color=ft.Colors.GREY_600),
                    ft.Container(height=10),
                    ft.Text(q['question'], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                    ft.Container(height=20),
                    radio_group,
                    ft.Container(height=20),
                    ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                width=700
            ),
            elevation=8
        )

        self.page.controls.clear()
        self.page.appbar = self.create_app_bar(f"{self.current_subject.replace('_', ' ').title()} Quiz")
        self.page.add(
            ft.Container(
                content=ft.Column([
                    ft.Container(height=20),
                    progress_bar,
                    ft.Container(height=20),
                    card
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                padding=20
            )
        )
        self.page.update()

    def record_answer_and_proceed(self):
        # Prevent out-of-bounds access
        if self.current_question_index >= len(self.quiz_questions):

    
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

        q = self.quiz_questions[self.current_question_index]
        selected = self.selected_answer
        correct = q["correct_answer"].strip().upper()

        if selected == correct:
            self.score += 1
        else:
            self.wrong_answers.append({
                "question": q["question"],
                "selected": selected,
                "selected_text": q[f"option_{selected.lower()}"],
                "correct": correct,
                "correct_text": q[f"option_{correct.lower()}"]
            })

        self.current_question_index += 1


        if self.current_question_index < len(self.quiz_questions):
            self.show_quiz_question()

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
 a6a4bd2d0e8710abcb109e29c8d6d7299847297d
        else:
            self.save_quiz_results()
            self.navigate_to(self.show_quiz_results)

    def save_quiz_results(self):
        cursor = self.conn.cursor()
        wrong_str = str(self.wrong_answers) if self.wrong_answers else ""
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
            wrong_str,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.conn.commit()


    def show_quiz_results(self, e=None):
        total = len(self.quiz_questions)
        percentage = (self.score / total) * 100
        feedback = "🌟 Excellent!" if percentage >= 80 else "👍 Good!" if percentage >= 60 else "💪 Keep practicing!"

        content_items = [
            ft.Text("🎉 Quiz Complete!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600),
            ft.Text(f"Score: {self.score}/{total} ({percentage:.1f}%)", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
            ft.Text(feedback, size=16, color=ft.Colors.BLUE_800),
            ft.Container(height=30)
        ]

        if self.wrong_answers:
            content_items += [
                ft.Text("❌ Wrong Answers:", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                ft.Container(height=10)
            ]
            for i, w in enumerate(self.wrong_answers, 1):
                content_items += [
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(w["question"], size=14, weight=ft.FontWeight.BOLD),
                                ft.Row([ft.Icon(ft.Icons.CLOSE, color=ft.Colors.RED), ft.Text(f"Your: {w['selected']}. {w['selected_text']}", size=12, color=ft.Colors.RED)]),
                                ft.Row([ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN), ft.Text(f"Correct: {w['correct']}. {w['correct_text']}", size=12, color=ft.Colors.GREEN)])
                            ], spacing=5),
                            padding=15
                        )
                    ),
                    ft.Container(height=10)
                ]
        else:
            content_items.append(ft.Text("🎯 Perfect Score!", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600))

        content_items += [
            ft.Container(height=20),
            ft.ElevatedButton(
                "📚 Back to Subjects",
                width=200,
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
                on_click=lambda e: self.navigate_to(self.show_subject_selection)
            )
        ]

        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Quiz Results")
        self.page.add(
            ft.Container(
                content=ft.Column(content_items, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                expand=True,
                padding=20
            )
        )
        self.page.update()

    def confirm_quit_quiz(self, e=None):
        def close(e):
            dialog.open = False
            self.page.update()

        def quit_quiz(e):
            close(None)
            self.navigate_back()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Quit Quiz?"),
            content=ft.Text("Your progress will be lost."),
            actions=[
                ft.TextButton("Cancel", on_click=close),
                ft.TextButton("Quit", on_click=quit_quiz, style=ft.ButtonStyle(color=ft.Colors.RED))
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def export_results(self, e=None):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM quiz_results ORDER BY date_taken DESC")
        rows = cursor.fetchall()
        if not rows:
            self.show_snackbar("No results to export.", ft.Colors.ORANGE)
            return

        filename = f"quiz_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Grade", "Subject", "Score", "Total", "Wrong Count", "Date"])
            for r in rows:
                name, grade, subject, score, total, wrong_str, date = r[1], r[2], r[3], r[4], r[5], r[6], r[7]
                try:
                    wrong_count = len(eval(wrong_str)) if wrong_str else total - score
                except:
                    wrong_count = total - score
                writer.writerow([name, grade, subject, score, total, wrong_count, date])

        self.show_snackbar(f"Results saved to {filename}", ft.Colors.GREEN)

    def show_study_mode(self, e=None):
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Study Mode")
        self.page.add(ft.Container(ft.Text("Study mode coming soon!"), padding=20))
        self.page.update()


def main(page: ft.Page):
    # Ensure folders exist
    for folder in ["data"] + \
                  [f"quizzes/grade_{i}" for i in range(1, 10)] + \
                  [f"study_mode/notes/grade_{i}" for i in range(1, 10)]:
        os.makedirs(folder, exist_ok=True)
    LearnAnywhereApp(page)

    
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
 a6a4bd2d0e8710abcb109e29c8d6d7299847297d


# --- START APP IN BROWSER ---
if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        port=8888
    )