import Database from "better-sqlite3"
import { hash, compare } from "bcryptjs"

// Database connection
let db: Database.Database | null = null

export function getDatabase() {
  if (!db) {
    db = new Database("learn-anywhere.db")
    db.pragma("journal_mode = WAL")
    db.pragma("foreign_keys = ON")
  }
  return db
}

// User types
export interface User {
  password_hash(password: any, password_hash: any): unknown
  id: number
  email: string
  role: "student" | "teacher"
  first_name: string
  last_name: string
  language_preference: "en" | "sw"
  has_paid: boolean
  payment_reference?: string
  created_at: string
}

export interface Subject {
  id: number
  name: string
  name_sw?: string
  description?: string
  description_sw?: string
}

export interface Lesson {
  id: number
  subject_id: number
  teacher_id: number
  title: string
  title_sw?: string
  content: string
  grade_level: number
  created_at: string
  updated_at: string
}

export interface StudentProgress {
  id: number
  student_id: number
  lesson_id: number
  flashcards_completed: number
  quiz_attempts: number
  best_quiz_score: number
  total_study_time: number
  completion_percentage: number
  last_accessed: string
}

export interface Flashcard {
  id: number
  lesson_id: number
  question: string
  question_sw?: string
  answer: string
  answer_sw?: string
  difficulty_level: number
}

export interface Quiz {
  id: number
  lesson_id: number
  title: string
  title_sw?: string
  questions: string // JSON array
  total_questions: number
}

export interface QuizAttempt {
  id: number
  student_id: number
  quiz_id: number
  score: number
  total_questions: number
  correct_answers: number
  time_taken?: number
  answers: string // JSON array
  completed_at: string
}

// Authentication utilities
export async function hashPassword(password: string): Promise<string> {
  return hash(password, 12)
}

export async function verifyPassword(password: string, hashedPassword: string): Promise<boolean> {
  return compare(password, hashedPassword)
}

// User operations
export async function createUser(userData: {
  email: string
  password: string
  role: "student" | "teacher"
  first_name: string
  last_name: string
  language_preference?: "en" | "sw"
}): Promise<User> {
  const database = getDatabase()

  const stmt = database.prepare(`
    INSERT INTO users (email, password_hash, role, first_name, last_name, language_preference)
    VALUES (?, ?, ?, ?, ?, ?)
  `)

  const hashedPassword = await hashPassword(userData.password)

  const result = stmt.run(
    userData.email,
    hashedPassword,
    userData.role,
    userData.first_name,
    userData.last_name,
    userData.language_preference || "en",
  )

  return getUserById(result.lastInsertRowid as number)!
}

export function getUserById(id: number): User | null {
  const database = getDatabase()
  const stmt = database.prepare("SELECT * FROM users WHERE id = ?")
  return stmt.get(id) as User | null
}

export function getUserByEmail(email: string): User | null {
  const database = getDatabase()
  const stmt = database.prepare("SELECT * FROM users WHERE email = ?")
  return stmt.get(email) as User | null
}

export function updateUserPaymentStatus(userId: number, paymentReference: string): void {
  const database = getDatabase()
  const stmt = database.prepare(`
    UPDATE users 
    SET has_paid = TRUE, payment_reference = ?, updated_at = CURRENT_TIMESTAMP 
    WHERE id = ?
  `)
  stmt.run(paymentReference, userId)
}

// Subject operations
export function getAllSubjects(): Subject[] {
  const database = getDatabase()
  const stmt = database.prepare("SELECT * FROM subjects ORDER BY name")
  return stmt.all() as Subject[]
}

// Lesson operations
export function getLessonsBySubject(subjectId: number, gradeLevel?: number): Lesson[] {
  const database = getDatabase()
  let query = "SELECT * FROM lessons WHERE subject_id = ?"
  const params: any[] = [subjectId]

  if (gradeLevel) {
    query += " AND grade_level = ?"
    params.push(gradeLevel)
  }

  query += " ORDER BY created_at DESC"

  const stmt = database.prepare(query)
  return stmt.all(...params) as Lesson[]
}

export function getLessonById(id: number): Lesson | null {
  const database = getDatabase()
  const stmt = database.prepare("SELECT * FROM lessons WHERE id = ?")
  return stmt.get(id) as Lesson | null
}

// Flashcard operations
export function getFlashcardsByLesson(lessonId: number): Flashcard[] {
  const database = getDatabase()
  const stmt = database.prepare("SELECT * FROM flashcards WHERE lesson_id = ? ORDER BY difficulty_level, id")
  return stmt.all(lessonId) as Flashcard[]
}

// Quiz operations
export function getQuizzesByLesson(lessonId: number): Quiz[] {
  const database = getDatabase()
  const stmt = database.prepare("SELECT * FROM quizzes WHERE lesson_id = ?")
  return stmt.all(lessonId) as Quiz[]
}

// Progress operations
export function getStudentProgress(studentId: number, lessonId?: number): StudentProgress[] {
  const database = getDatabase()
  let query = "SELECT * FROM student_progress WHERE student_id = ?"
  const params: any[] = [studentId]

  if (lessonId) {
    query += " AND lesson_id = ?"
    params.push(lessonId)
  }

  const stmt = database.prepare(query)
  return stmt.all(...params) as StudentProgress[]
}

export function updateStudentProgress(studentId: number, lessonId: number, updates: Partial<StudentProgress>): void {
  const database = getDatabase()

  // First, try to get existing progress
  const existing = database
    .prepare("SELECT * FROM student_progress WHERE student_id = ? AND lesson_id = ?")
    .get(studentId, lessonId)

  if (existing) {
    // Update existing record
    const fields = Object.keys(updates)
      .map((key) => `${key} = ?`)
      .join(", ")
    const values = Object.values(updates)
    const stmt = database.prepare(
      `UPDATE student_progress SET ${fields}, last_accessed = CURRENT_TIMESTAMP WHERE student_id = ? AND lesson_id = ?`,
    )
    stmt.run(...values, studentId, lessonId)
  } else {
    // Create new record
    const stmt = database.prepare(`
      INSERT INTO student_progress (student_id, lesson_id, flashcards_completed, quiz_attempts, best_quiz_score, total_study_time, completion_percentage)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `)
    stmt.run(
      studentId,
      lessonId,
      updates.flashcards_completed || 0,
      updates.quiz_attempts || 0,
      updates.best_quiz_score || 0,
      updates.total_study_time || 0,
      updates.completion_percentage || 0,
    )
  }
}

export function recordQuizAttempt(attempt: Omit<QuizAttempt, "id" | "completed_at">): number {
  const database = getDatabase()
  const stmt = database.prepare(`
    INSERT INTO quiz_attempts (student_id, quiz_id, score, total_questions, correct_answers, time_taken, answers)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `)

  const result = stmt.run(
    attempt.student_id,
    attempt.quiz_id,
    attempt.score,
    attempt.total_questions,
    attempt.correct_answers,
    attempt.time_taken,
    attempt.answers,
  )

  return result.lastInsertRowid as number
}

// Initialize database with tables
export function initializeDatabase() {
  const database = getDatabase()

  // Read and execute SQL files would be done here
  // For now, we'll create tables directly
  console.log("Database initialized")
}
