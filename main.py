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
    
    def navigate_back(self):
        """Go back to previous screen"""
        if len(self.navigation_stack) > 1:
            self.navigation_stack.pop()  # Remove current screen
            prev_screen, args = self.navigation_stack[-1]
            prev_screen(*args)
        else:
            self.show_login_screen()
    
    def create_app_bar(self, title, show_back=True):
        """Create consistent app bar for all screens"""
        actions = []
        
        if show_back and len(self.navigation_stack) > 1:
            actions.append(
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Go Back",
                    on_click=lambda _: self.navigate_back()
                )
            )
        
        return ft.AppBar(
            title=ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            actions=actions
        )
    
    def show_login_screen(self):
        """Display the modern login screen"""
        self.navigation_stack = []
        
        # Name input field
        self.name_field = ft.TextField(
            label="👤 Student Name",
            hint_text="Enter your full name",
            width=400,
            text_size=16,
            border_radius=10
        )
        
        # Grade dropdown
        self.grade_dropdown = ft.Dropdown(
            label="📚 Select Your Grade",
            hint_text="Choose your grade level",
            width=400,
            options=[
                ft.dropdown.Option(f"Grade {i}") for i in range(1, 10)
            ],
            text_size=16,
            border_radius=10
        )
        
        # Start button
        start_button = ft.ElevatedButton(
            text="🚀 Start Learning!",
            width=400,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
                text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD)
            ),
            on_click=self.handle_login
        )
        
        # Main content
        content = ft.Container(
            content=ft.Column([
                ft.Container(height=50),
                ft.Text(
                    "🎓 LearnAnywhere-CBC",
                    size=36,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Kenya's CBC Curriculum | Offline Learning for All",
                    size=16,
                    color=ft.Colors.GREY_700,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=40),
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Container(height=20),
                            self.name_field,
                            ft.Container(height=20),
                            self.grade_dropdown,
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
        
        # Focus on name field
        self.name_field.focus()
    
    def handle_login(self, e):
        """Process login and move to subject selection"""
        name = self.name_field.value.strip()
        grade = self.grade_dropdown.value
        
        if not name:
            self.show_snackbar("Please enter your name!", ft.Colors.RED)
            return
        
        if not grade:
            self.show_snackbar("Please select your grade!", ft.Colors.RED)
            return
        
        self.student_name = name
        self.student_grade = grade
        self.navigate_to(self.show_subject_selection)
    
    def show_snackbar(self, message, color=ft.Colors.BLUE):
        """Show snackbar notification"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def get_subjects_for_grade(self, grade):
        """Return CBC subjects based on grade level"""
        subjects = {
            "Grade 1": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 2": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
            "Grade 3": [("🔢 Number Work", "number_work"), ("📚 Language Activities", "language_activities"), ("🌍 Environmental Activities", "environmental_activities")],
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
        """Display subject selection screen with modern card layout"""
        subjects = self.get_subjects_for_grade(self.student_grade)
        
        # Create subject cards in a responsive grid
        subject_cards = []
        for i in range(0, len(subjects), 3):  # 3 cards per row
            row = ft.Row([], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            for j in range(3):
                if i + j < len(subjects):
                    text, subject = subjects[i + j]
                    card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(text, size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                                ft.ElevatedButton(
                                    text="Start Quiz",
                                    width=150,
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
                                    on_click=lambda _, s=subject: self.navigate_to(self.start_quiz, s)
                                )
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                            padding=20,
                            width=200,
                            height=120
                        ),
                        elevation=4
                    )
                    row.controls.append(card)
            subject_cards.append(row)
        
        # Additional options
        options_row = ft.Row([
            ft.ElevatedButton(
                text="💡 Study Mode",
                style=ft.ButtonStyle(bgcolor=ft.Colors.TEAL_600, color=ft.Colors.WHITE),
                on_click=lambda _: self.navigate_to(self.show_study_mode)
            ),
            ft.ElevatedButton(
                text="📤 Export Results",
                style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_600, color=ft.Colors.WHITE),
                on_click=lambda _: self.export_results()
            ),
            ft.ElevatedButton(
                text="🚪 Logout",
                style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE),
                on_click=lambda _: self.show_login_screen()
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        content = ft.Column([
            ft.Container(height=20),
            ft.Text(
                f"Welcome, {self.student_name}! 🎉",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Text(
                f"Grade: {self.student_grade}",
                size=16,
                color=ft.Colors.GREY_600,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=20),
            ft.Text(
                "📖 Choose Your Subject:",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_800,
                text_align=ft.TextAlign.CENTER
            ),
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
    
    def load_quiz_questions(self, subject):
        """Load quiz questions from CSV file by grade and subject"""
        quiz_file = f"quizzes/{self.student_grade.lower().replace(' ', '_')}/{subject}.csv"
        
        if not os.path.exists(quiz_file):
            self.show_snackbar(f"Quiz file not found: {quiz_file}", ft.Colors.RED)
            return False
        
        try:
            with open(quiz_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                questions = list(reader)
            self.quiz_questions = random.sample(questions, min(10, len(questions)))
            return True
        except Exception as e:
            self.show_snackbar(f"Failed to load quiz: {str(e)}", ft.Colors.RED)
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
        
        # Progress indicator
        progress = (self.current_question_index + 1) / len(self.quiz_questions)
        progress_bar = ft.ProgressBar(
            value=progress,
            width=600,
            height=8,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.BLUE_600
        )
        
        # Question card
        question_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        f"Question {self.current_question_index + 1} of {len(self.quiz_questions)}",
                        size=14,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        current_q['question'],
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_800,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    self.create_answer_options(current_q),
                    ft.Container(height=20),
                    self.create_navigation_buttons()
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=30,
                width=700
            ),
            elevation=8
        )
        
        content = ft.Column([
            ft.Container(height=20),
            progress_bar,
            ft.Container(height=20),
            question_card
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar(f"{self.current_subject.replace('_', ' ').title()} Quiz")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def create_answer_options(self, question):
        """Create radio button options for answers"""
        self.answer_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(
                    value="A",
                    label=f"A. {question['option_a']}",
                    label_style=ft.TextStyle(size=14)
                ),
                ft.Radio(
                    value="B",
                    label=f"B. {question['option_b']}",
                    label_style=ft.TextStyle(size=14)
                ),
                ft.Radio(
                    value="C",
                    label=f"C. {question['option_c']}",
                    label_style=ft.TextStyle(size=14)
                ),
                ft.Radio(
                    value="D",
                    label=f"D. {question['option_d']}",
                    label_style=ft.TextStyle(size=14)
                )
            ], spacing=15)
        )
        return self.answer_group
    
    def create_navigation_buttons(self):
        """Create navigation buttons for quiz"""
        buttons = []
        
        # Back button (disabled on first question)
        if self.current_question_index > 0:
            buttons.append(
                ft.ElevatedButton(
                    text="🔙 Previous",
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_600, color=ft.Colors.WHITE),
                    on_click=self.previous_question
                )
            )
        
        # Next/Finish button
        if self.current_question_index < len(self.quiz_questions) - 1:
            buttons.append(
                ft.ElevatedButton(
                    text="Next ➡️",
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE),
                    on_click=self.next_question
                )
            )
        else:
            buttons.append(
                ft.ElevatedButton(
                    text="Finish Quiz 🏁",
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE),
                    on_click=self.finish_quiz
                )
            )
        
        # Quit button
        buttons.append(
            ft.ElevatedButton(
                text="🚪 Quit Quiz",
                style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_600, color=ft.Colors.WHITE),
                on_click=self.confirm_quit_quiz
            )
        )
        
        return ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    
    def next_question(self, e):
        """Move to next question"""
        if not self.answer_group.value:
            self.show_snackbar("Please select an answer!", ft.Colors.ORANGE)
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
    
    def previous_question(self, e):
        """Go to the previous question"""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_quiz_question()
    
    def confirm_quit_quiz(self, e):
        """Ask user before quitting the quiz"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        def quit_quiz(e):
            dialog.open = False
            self.page.update()
            self.navigate_back()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Quit Quiz?"),
            content=ft.Text("Are you sure you want to quit this quiz? Your progress will be lost."),
            actions=[
                ft.TextButton("Cancel", on_click=close_dialog),
                ft.TextButton("Quit", on_click=quit_quiz, style=ft.ButtonStyle(color=ft.Colors.RED))
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def finish_quiz(self, e):
        """Finish quiz and show results"""
        if not self.answer_group.value:
            self.show_snackbar("Please select an answer!", ft.Colors.ORANGE)
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
            color = ft.Colors.GREEN_600
        elif percentage >= 60:
            feedback = "👍 Good job! Keep practicing!"
            color = ft.Colors.ORANGE_600
        else:
            feedback = "💪 Keep studying! You'll do better next time!"
            color = ft.Colors.RED_600
        
        # Score summary card
        score_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("🎉 Quiz Complete!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_600),
                    ft.Text(f"Score: {self.score}/{len(self.quiz_questions)} ({percentage:.1f}%)", 
                            size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Text(feedback, size=16, color=color, text_align=ft.TextAlign.CENTER)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=30,
                width=600
            ),
            elevation=8
        )
        
        content_items = [score_card, ft.Container(height=20)]
        
        # Show wrong answers if any
        if self.wrong_answers:
            wrong_answers_title = ft.Text(
                "❌ Questions You Got Wrong:",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED_700
            )
            content_items.append(wrong_answers_title)
            content_items.append(ft.Container(height=10))
            
            for i, wrong in enumerate(self.wrong_answers, 1):
                wrong_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Question {i}:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_600),
                            ft.Text(wrong['question'], size=14, color=ft.Colors.BLACK),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.CLOSE, color=ft.Colors.RED, size=16),
                                ft.Text(f"Your answer: {wrong['selected']}. {wrong['selected_text']}", 
                                        size=12, color=ft.Colors.RED_700)
                            ]),
                            ft.Row([
                                ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN, size=16),
                                ft.Text(f"Correct answer: {wrong['correct']}. {wrong['correct_text']}", 
                                        size=12, color=ft.Colors.GREEN_700)
                            ])
                        ], spacing=5),
                        padding=15,
                        width=650
                    ),
                    elevation=4
                )
                content_items.append(wrong_card)
                content_items.append(ft.Container(height=10))
        else:
            perfect_card = ft.Card(
                content=ft.Container(
                    content=ft.Text(
                        "🎯 Perfect Score! You got all questions correct!",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_600,
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=20,
                    width=600
                ),
                elevation=4
            )
            content_items.append(perfect_card)
        
        # Return button
        content_items.extend([
            ft.Container(height=20),
            ft.ElevatedButton(
                text="📚 Back to Subjects",
                width=200,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE,
                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                ),
                on_click=lambda _: self.navigate_to(self.show_subject_selection)
            )
        ])
        
        content = ft.Column(
            content_items,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Quiz Results")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def show_study_mode(self):
        """Display study mode options"""
        study_cards = ft.Row([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.QUIZ, size=48, color=ft.Colors.RED_600),
                        ft.Text("🃏 Flashcards", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Review key concepts", size=12, color=ft.Colors.GREY_600),
                        ft.ElevatedButton(
                            text="Start",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_600, color=ft.Colors.WHITE),
                            on_click=lambda _: self.navigate_to(self.show_flashcards_choice)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=30,
                    width=250,
                    height=200
                ),
                elevation=6
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.NOTES, size=48, color=ft.Colors.BLUE_600),
                        ft.Text("📓 Study Notes", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("Read detailed notes", size=12, color=ft.Colors.GREY_600),
                        ft.ElevatedButton(
                            text="Start",
                            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
                            on_click=lambda _: self.navigate_to(self.show_notes_choice)
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=30,
                    width=250,
                    height=200
                ),
                elevation=6
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=30)
        
        content = ft.Column([
            ft.Container(height=50),
            ft.Text(
                "📘 Study Mode",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=40),
            study_cards
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Study Mode")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def show_flashcards_choice(self):
        """Show subject selection for flashcards"""
        subjects = self.get_subjects_for_grade(self.student_grade)
        
        subject_buttons = []
        for text, subject in subjects:
            button = ft.ElevatedButton(
                text=text,
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_50,
                    color=ft.Colors.BLUE_800,
                    text_style=ft.TextStyle(size=14)
                ),
                on_click=lambda _, s=subject: self.navigate_to(self.display_flashcards, s)
            )
            subject_buttons.append(button)
            subject_buttons.append(ft.Container(height=10))
        
        content = ft.Column([
            ft.Container(height=20),
            ft.Text(
                "🃏 Choose Subject for Flashcards",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED_600,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=30),
            *subject_buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Flashcards")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def display_flashcards(self, subject):
        """Display flashcards for selected subject"""
        file_path = f"study_mode/flashcards/{self.student_grade.lower().replace(' ', '_')}/{subject}.csv"
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                flashcards = list(reader)
        except FileNotFoundError:
            flashcards = []
        except Exception as e:
            self.show_snackbar(f"Could not load flashcards: {str(e)}", ft.Colors.RED)
            flashcards = []
        
        content_items = [
            ft.Text(
                f"🃏 Flashcards: {subject.replace('_', ' ').title()}",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED_600,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=20)
        ]
        
        if not flashcards:
            content_items.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Text(
                            f"No flashcards available for {subject.replace('_', ' ').title()}.",
                            size=16,
                            color=ft.Colors.GREY_600,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=40
                    ),
                    elevation=4
                )
            )
        else:
            for card in flashcards:
                flashcard = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"🔹 {card['term']}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED_600
                            ),
                            ft.Container(height=5),
                            ft.Text(
                                card['definition'],
                                size=14,
                                color=ft.Colors.BLUE_800
                            )
                        ], spacing=5),
                        padding=20,
                        width=650
                    ),
                    elevation=4
                )
                content_items.append(flashcard)
                content_items.append(ft.Container(height=10))
        
        content = ft.Column(
            content_items,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar(f"Flashcards: {subject.replace('_', ' ').title()}")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def show_notes_choice(self):
        """Show subject selection for study notes"""
        subjects = self.get_subjects_for_grade(self.student_grade)
        
        subject_buttons = []
        for text, subject in subjects:
            button = ft.ElevatedButton(
                text=text,
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.BLUE_50,
                    color=ft.Colors.BLUE_800,
                    text_style=ft.TextStyle(size=14)
                ),
                on_click=lambda _, s=subject: self.navigate_to(self.show_notes, s)
            )
            subject_buttons.append(button)
            subject_buttons.append(ft.Container(height=10))
        
        content = ft.Column([
            ft.Container(height=20),
            ft.Text(
                "📓 Choose Subject for Study Notes",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_600,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=30),
            *subject_buttons
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar("Study Notes")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def show_notes(self, subject):
        """Display study notes for selected subject"""
        filename = f"study_mode/notes/{self.student_grade.lower().replace(' ', '_')}/{subject}_notes.txt"
        
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content_text = file.read()
        except FileNotFoundError:
            content_text = f"Study notes for {subject.replace('_', ' ').title()} are not available yet.\n\nThis section will be updated with comprehensive study materials soon."
        
        notes_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        content_text,
                        size=14,
                        color=ft.Colors.BLUE_800,
                        selectable=True
                    )
                ]),
                padding=30,
                width=700
            ),
            elevation=6
        )
        
        content = ft.Column([
            ft.Container(height=20),
            ft.Text(
                f"📓 Notes: {subject.replace('_', ' ').title()}",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_600,
                text_align=ft.TextAlign.CENTER
            ),
            ft.Container(height=20),
            notes_card
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.controls.clear()
        self.page.appbar = self.create_app_bar(f"Notes: {subject.replace('_', ' ').title()}")
        self.page.add(ft.Container(content=content, expand=True, padding=20))
        self.page.update()
    
    def export_results(self):
        """Export all quiz results from SQLite to a CSV file"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM quiz_results")
            rows = cursor.fetchall()

            if not rows:
                self.show_snackbar("No results to export!", ft.Colors.ORANGE)
                return

            # Create filename with timestamp
            filename = f"data/results_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            # Ensure data folder exists
            os.makedirs("data", exist_ok=True)

            # Write CSV file
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([desc[0] for desc in cursor.description])  # headers
                writer.writerows(rows)

            self.show_snackbar(f"Results exported → {filename}", ft.Colors.GREEN)

        except Exception as e:
            self.show_snackbar(f"Export failed: {str(e)}", ft.Colors.RED)
def main(page: ft.Page):
    # Ensure all folders exist
    os.makedirs("data", exist_ok=True)
    for i in range(1, 10):
        os.makedirs(f"quizzes/grade_{i}", exist_ok=True)
        os.makedirs(f"study_mode/notes/grade_{i}", exist_ok=True)
        os.makedirs(f"study_mode/flashcards/grade_{i}", exist_ok=True)
    
    app = LearnAnywhereApp(page)

if __name__ == "__main__":
    ft.app(target=main)