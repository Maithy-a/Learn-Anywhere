-- Creating Learn-Anywhere database schema
-- Users table with role-based access
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('student', 'teacher')),
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  language_preference TEXT DEFAULT 'en' CHECK (language_preference IN ('en', 'sw')),
  has_paid BOOLEAN DEFAULT FALSE,
  payment_reference TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Subjects table
CREATE TABLE IF NOT EXISTS subjects (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  name_sw TEXT, -- Kiswahili translation
  description TEXT,
  description_sw TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Lessons table for teacher-uploaded content
CREATE TABLE IF NOT EXISTS lessons (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject_id INTEGER NOT NULL,
  teacher_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  title_sw TEXT,
  content TEXT NOT NULL, -- JSON content from CSV
  grade_level INTEGER NOT NULL CHECK (grade_level BETWEEN 4 AND 8),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (subject_id) REFERENCES subjects(id),
  FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- Flashcards table
CREATE TABLE IF NOT EXISTS flashcards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lesson_id INTEGER NOT NULL,
  question TEXT NOT NULL,
  question_sw TEXT,
  answer TEXT NOT NULL,
  answer_sw TEXT,
  difficulty_level INTEGER DEFAULT 1 CHECK (difficulty_level BETWEEN 1 AND 5),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

-- Quizzes table
CREATE TABLE IF NOT EXISTS quizzes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lesson_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  title_sw TEXT,
  questions TEXT NOT NULL, -- JSON array of questions
  total_questions INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (lesson_id) REFERENCES lessons(id)
);

-- Student progress tracking
CREATE TABLE IF NOT EXISTS student_progress (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  lesson_id INTEGER NOT NULL,
  flashcards_completed INTEGER DEFAULT 0,
  quiz_attempts INTEGER DEFAULT 0,
  best_quiz_score REAL DEFAULT 0,
  total_study_time INTEGER DEFAULT 0, -- in minutes
  last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
  completion_percentage REAL DEFAULT 0,
  FOREIGN KEY (student_id) REFERENCES users(id),
  FOREIGN KEY (lesson_id) REFERENCES lessons(id),
  UNIQUE(student_id, lesson_id)
);

-- Quiz attempts for detailed tracking
CREATE TABLE IF NOT EXISTS quiz_attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  quiz_id INTEGER NOT NULL,
  score REAL NOT NULL,
  total_questions INTEGER NOT NULL,
  correct_answers INTEGER NOT NULL,
  time_taken INTEGER, -- in seconds
  answers TEXT, -- JSON array of answers
  completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES users(id),
  FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
);

-- Payment transactions
CREATE TABLE IF NOT EXISTS payment_transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  reference TEXT UNIQUE NOT NULL,
  amount REAL NOT NULL,
  currency TEXT DEFAULT 'USD',
  status TEXT NOT NULL CHECK (status IN ('pending', 'success', 'failed')),
  paystack_reference TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  verified_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
