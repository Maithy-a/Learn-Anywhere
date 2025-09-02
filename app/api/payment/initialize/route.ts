import { type NextRequest, NextResponse } from "next/server"
import { requireAuth } from "@/lib/auth"
import { getUserById } from "@/lib/database"

export async function POST(request: NextRequest) {
  try {
    const session = await requireAuth()
    const user = getUserById(session.userId)

    if (!user) {
      return NextResponse.json({ error: "User not found" }, { status: 404 })
    }

    if (user.has_paid) {
      return NextResponse.json({ error: "Payment already completed" }, { status: 400 })
    }

    const paystackSecretKey = process.env.PAYSTACK_SECRET_KEY
    if (!paystackSecretKey) {
      return NextResponse.json({ error: "Payment system not configured" }, { status: 500 })
    }

    // Initialize Paystack transaction
    const response = await fetch("https://api.paystack.co/transaction/initialize", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${paystackSecretKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: user.email,
        amount: 100000, // 1000 KES in cents
        currency: "KES",
        reference: `learn_anywhere_${user.id}_${Date.now()}`,
        callback_url: `${process.env.NEXT_PUBLIC_APP_URL}/api/payment/verify`,
        metadata: {
          user_id: user.id,
          user_email: user.email,
          product: "Learn-Anywhere Access",
        },
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Payment initialization failed")
    }

    return NextResponse.json({
      authorization_url: data.data.authorization_url,
      reference: data.data.reference,
    })
  } catch (error) {
    console.error("Payment initialization error:", error)
    return NextResponse.json({ error: "Payment initialization failed" }, { status: 500 })
  }
}
