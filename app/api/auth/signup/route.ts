import { type NextRequest, NextResponse } from "next/server"
import { createUser, getUserByEmail } from "@/lib/database"
import { createSession } from "@/lib/auth"

export async function POST(request: NextRequest) {
  try {
    const { email, password, first_name, last_name, role, language_preference } = await request.json()

    if (!email || !password || !first_name || !last_name || !role) {
      return NextResponse.json({ error: "All fields are required" }, { status: 400 })
    }

    if (!["student", "teacher"].includes(role)) {
      return NextResponse.json({ error: "Invalid role" }, { status: 400 })
    }

    // Check if user already exists
    const existingUser = getUserByEmail(email)
    if (existingUser) {
      return NextResponse.json({ error: "User already exists" }, { status: 409 })
    }

    const user = await createUser({
      email,
      password,
      role,
      first_name,
      last_name,
      language_preference: language_preference || "en",
    })

    await createSession(user)

    return NextResponse.json({
      user: {
        id: user.id,
        email: user.email,
        role: user.role,
        first_name: user.first_name,
        last_name: user.last_name,
        has_paid: user.has_paid,
      },
    })
  } catch (error) {
    console.error("Signup error:", error)
    return NextResponse.json({ error: "Internal server error" }, { status: 500 })
  }
}
