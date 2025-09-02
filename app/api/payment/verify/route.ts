import { type NextRequest, NextResponse } from "next/server"
import { getUserById, updateUserPaymentStatus } from "@/lib/database"

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const reference = searchParams.get("reference")

    if (!reference) {
      return NextResponse.redirect(new URL("/payment?error=missing_reference", request.url))
    }

    const paystackSecretKey = process.env.PAYSTACK_SECRET_KEY
    if (!paystackSecretKey) {
      return NextResponse.redirect(new URL("/payment?error=config_error", request.url))
    }

    // Verify transaction with Paystack
    const response = await fetch(`https://api.paystack.co/transaction/verify/${reference}`, {
      headers: {
        Authorization: `Bearer ${paystackSecretKey}`,
      },
    })

    const data = await response.json()

    if (!response.ok || data.data.status !== "success") {
      return NextResponse.redirect(new URL("/payment?error=verification_failed", request.url))
    }

    // Update user payment status
    const userId = data.data.metadata.user_id
    updateUserPaymentStatus(userId, reference)

    // Redirect to dashboard with a success message
    return NextResponse.redirect(new URL("/dashboard?payment=success", request.url))

  } catch (error) {
    console.error("Payment verification error:", error)
    return NextResponse.redirect(new URL("/payment?error=server_error", request.url))
  }
}
