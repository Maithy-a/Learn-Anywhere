import { type NextRequest, NextResponse } from "next/server"
import { requireAuth } from "@/lib/auth"
import { getDatabase } from "@/lib/database"

export async function POST(request: NextRequest) {
  try {
    const session = await requireAuth()

    if (session.role !== "teacher") {
      return NextResponse.json({ error: "Access denied" }, { status: 403 })
    }

    const { title, title_sw, subject_id, grade_level, flashcards } = await request.json()

    if (!title || !subject_id || !grade_level || !flashcards || flashcards.length === 0) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 })
    }

    const database = getDatabase()

    // Create lesson
    const lessonStmt = database.prepare(`
      INSERT INTO lessons (subject_id, teacher_id, title, title_sw, content, grade_level)
      VALUES (?, ?, ?, ?, ?, ?)
    `)

    const lessonResult = lessonStmt.run(
      Number.parseInt(subject_id),
      session.userId,
      title,
      title_sw || null,
      JSON.stringify({ flashcards }),
      Number.parseInt(grade_level),
    )

    const lessonId = lessonResult.lastInsertRowid as number

    // Create flashcards
    const flashcardStmt = database.prepare(`
      INSERT INTO flashcards (lesson_id, question, question_sw, answer, answer_sw, difficulty_level)
      VALUES (?, ?, ?, ?, ?, ?)
    `)

    for (const card of flashcards) {
      if (card.question && card.answer) {
        flashcardStmt.run(
          lessonId,
          card.question,
          card.question_sw || null,
          card.answer,
          card.answer_sw || null,
          card.difficulty || 1,
        )
      }
    }

    return NextResponse.json({
      success: true,
      lesson_id: lessonId,
      message: "Lesson created successfully",
    })
  } catch (error) {
    console.error("Failed to create lesson:", error)
    return NextResponse.json({ error: "Failed to create lesson" }, { status: 500 })
  }
}
