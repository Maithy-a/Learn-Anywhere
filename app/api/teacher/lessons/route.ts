import { type NextRequest, NextResponse } from "next/server"
import { requireAuth } from "@/lib/auth"
import { getDatabase } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    const session = await requireAuth()

    if (session.role !== "teacher") {
      return NextResponse.json({ error: "Access denied" }, { status: 403 })
    }

    const database = getDatabase()
    const stmt = database.prepare(`
      SELECT l.*, s.name as subject_name, s.name_sw as subject_name_sw
      FROM lessons l
      JOIN subjects s ON l.subject_id = s.id
      WHERE l.teacher_id = ?
      ORDER BY l.created_at DESC
    `)

    const lessons = stmt.all(session.userId)

    return NextResponse.json({ lessons })
  } catch (error) {
    console.error("Failed to fetch teacher lessons:", error)
    return NextResponse.json({ error: "Failed to fetch lessons" }, { status: 500 })
  }
}
