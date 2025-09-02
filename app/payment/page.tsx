import { PaymentForm } from "@/components/payment/payment-form"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen, CheckCircle } from "lucide-react"
import Link from "next/link"

export default function PaymentPage() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 text-2xl font-bold text-foreground">
            <BookOpen className="h-8 w-8 text-primary" />
            Learn-Anywhere
          </Link>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Payment Form */}
          <Card>
            <CardHeader>
              <CardTitle>Complete Your Purchase</CardTitle>
              <CardDescription>Secure payment powered by Paystack</CardDescription>
            </CardHeader>
            <CardContent>
              <PaymentForm />
            </CardContent>
          </Card>

          {/* What You Get */}
          <Card className="bg-primary/5 border-primary/20">
            <CardHeader>
              <CardTitle className="text-primary">What You Get</CardTitle>
              <CardDescription>Lifetime access for just $10</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              {[
                "Complete offline learning platform",
                "Math, English, Science & Kiswahili",
                "AI-powered quiz generation",
                "Progress tracking & analytics",
                "Teacher dashboard (for teachers)",
                "Multi-device sync",
                "Lifetime updates",
              ].map((feature) => (
                <div key={feature} className="flex items-center gap-3">
                  <CheckCircle className="h-4 w-4 text-primary flex-shrink-0" />
                  <span className="text-sm text-muted-foreground">{feature}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
