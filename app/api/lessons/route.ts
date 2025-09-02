import { type NextRequest, NextResponse } from "next/server"
import { requirePaidAccess } from "@/lib/auth"
import { getLessonsBySubject } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    await requirePaidAccess()

    const { searchParams } = new URL(request.url)
    const subjectId = searchParams.get("subject_id")
    const gradeLevel = searchParams.get("grade_level")

    if (!subjectId) {
      return NextResponse.json({ error: "Subject ID is required" }, { status: 400 })
    }

    const lessons = getLessonsBySubject(
      Number.parseInt(subjectId),
      gradeLevel ? Number.parseInt(gradeLevel) : undefined,
    )

    return NextResponse.json({ lessons })
  } catch (error) {
    console.error("Failed to fetch lessons:", error)
    return NextResponse.json({ error: "Failed to fetch lessons" }, { status: 500 })
  }
}
