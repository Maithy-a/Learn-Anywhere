import { SignJWT, jwtVerify } from "jose"
import { cookies } from "next/headers"
import type { User } from "./database"

const secretKey = process.env.JWT_SECRET || "learn-anywhere-secret-key"
const key = new TextEncoder().encode(secretKey)

export async function encrypt(payload: any) {
  return await new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("24h")
    .sign(key)
}

export async function decrypt(input: string): Promise<any> {
  const { payload } = await jwtVerify(input, key, {
    algorithms: ["HS256"],
  })
  return payload
}

export async function createSession(user: User) {
  const expires = new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
  const session = await encrypt({
    userId: user.id,
    email: user.email,
    role: user.role,
    hasPaid: user.has_paid,
  })

  const cookieStore = await cookies()
  cookieStore.set("session", session, {
    expires,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
  })
}

export async function getSession() {
  const cookieStore = await cookies()
  const session = cookieStore.get("session")?.value

  if (!session) return null

  try {
    return await decrypt(session)
  } catch (error) {
    return null
  }
}

export async function deleteSession() {
  const cookieStore = await cookies()
  cookieStore.delete("session")
}

export async function requireAuth() {
  const session = await getSession()
  if (!session) {
    throw new Error("Authentication required")
  }
  return session
}

export async function requirePaidAccess() {
  const session = await requireAuth()
  if (!session.hasPaid) {
    throw new Error("Payment required")
  }
  return session
}
