import { type NextRequest, NextResponse } from "next/server"
import { requirePaidAccess } from "@/lib/auth"
import { getFlashcardsByLesson } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    await requirePaidAccess()

    const { searchParams } = new URL(request.url)
    const lessonId = searchParams.get("lesson_id")

    if (!lessonId) {
      return NextResponse.json({ error: "Lesson ID is required" }, { status: 400 })
    }

    const flashcards = getFlashcardsByLesson(Number.parseInt(lessonId))

    return NextResponse.json({ flashcards })
  } catch (error) {
    console.error("Failed to fetch flashcards:", error)
    return NextResponse.json({ error: "Failed to fetch flashcards" }, { status: 500 })
  }
}
