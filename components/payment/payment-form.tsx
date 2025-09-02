"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, CreditCard } from "lucide-react"

export function PaymentForm() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const router = useRouter()

  const handlePayment = async () => {
    setIsLoading(true)
    setError("")

    try {
      // Initialize Paystack payment
      const response = await fetch("/api/payment/initialize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Payment initialization failed")
      }

      // Redirect to Paystack checkout
      window.location.href = data.authorization_url
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <div className="bg-muted/50 p-4 rounded-lg">
        <div className="flex justify-between items-center mb-2">
          <span className="font-medium">Learn-Anywhere Access</span>
          <span className="font-bold">$10.00</span>
        </div>
        <p className="text-sm text-muted-foreground">One-time payment • Lifetime access • No recurring fees</p>
      </div>

      <Button onClick={handlePayment} className="w-full" size="lg" disabled={isLoading}>
        {isLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <CreditCard className="mr-2 h-4 w-4" />}
        Pay with Paystack
      </Button>

      <p className="text-xs text-center text-muted-foreground">Secure payment processing. Your data is protected.</p>
    </div>
  )
}
