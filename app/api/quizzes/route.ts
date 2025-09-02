import { type NextRequest, NextResponse } from "next/server"
import { requirePaidAccess } from "@/lib/auth"
import { getQuizzesByLesson } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    await requirePaidAccess()

    const { searchParams } = new URL(request.url)
    const lessonId = searchParams.get("lesson_id")

    if (!lessonId) {
      return NextResponse.json({ error: "Lesson ID is required" }, { status: 400 })
    }

    const quizzes = getQuizzesByLesson(Number.parseInt(lessonId))

    return NextResponse.json({ quizzes })
  } catch (error) {
    console.error("Failed to fetch quizzes:", error)
    return NextResponse.json({ error: "Failed to fetch quizzes" }, { status: 500 })
  }
}
