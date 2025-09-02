import { type NextRequest, NextResponse } from "next/server"
import { requireAuth } from "@/lib/auth"
import { getDatabase } from "@/lib/database"

export async function POST(request: NextRequest) {
  try {
    const session = await requireAuth()

    if (session.role !== "teacher") {
      return NextResponse.json({ error: "Access denied" }, { status: 403 })
    }

    const formData = await request.formData()
    const file = formData.get("file") as File
    const title = formData.get("title") as string
    const title_sw = formData.get("title_sw") as string
    const subject_id = formData.get("subject_id") as string
    const grade_level = formData.get("grade_level") as string

    if (!file || !title || !subject_id || !grade_level) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 })
    }

    // Parse CSV content
    const csvText = await file.text()
    const lines = csvText.split("\n").filter((line) => line.trim())

    if (lines.length < 2) {
      return NextResponse.json({ error: "CSV file must have at least a header and one data row" }, { status: 400 })
    }

    const headers = lines[0].split(",").map((h) => h.trim().replace(/"/g, ""))
    const flashcards = []

    for (let i = 1; i < lines.length; i++) {
      const values = lines[i].split(",").map((v) => v.trim().replace(/"/g, ""))
      const row: any = {}

      headers.forEach((header, index) => {
        row[header] = values[index] || ""
      })

      if (row.question && row.answer) {
        flashcards.push({
          question: row.question,
          question_sw: row.question_sw || "",
          answer: row.answer,
          answer_sw: row.answer_sw || "",
          difficulty: Number.parseInt(row.difficulty) || 1,
        })
      }
    }

    if (flashcards.length === 0) {
      return NextResponse.json({ error: "No valid flashcards found in CSV" }, { status: 400 })
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
      JSON.stringify({ flashcards, source: "csv_upload" }),
      Number.parseInt(grade_level),
    )

    const lessonId = lessonResult.lastInsertRowid as number

    // Create flashcards
    const flashcardStmt = database.prepare(`
      INSERT INTO flashcards (lesson_id, question, question_sw, answer, answer_sw, difficulty_level)
      VALUES (?, ?, ?, ?, ?, ?)
    `)

    for (const card of flashcards) {
      flashcardStmt.run(
        lessonId,
        card.question,
        card.question_sw || null,
        card.answer,
        card.answer_sw || null,
        card.difficulty,
      )
    }

    return NextResponse.json({
      success: true,
      lesson_id: lessonId,
      flashcards_created: flashcards.length,
      message: "CSV uploaded and lesson created successfully",
    })
  } catch (error) {
    console.error("Failed to upload CSV:", error)
    return NextResponse.json({ error: "Failed to upload CSV" }, { status: 500 })
  }
}
