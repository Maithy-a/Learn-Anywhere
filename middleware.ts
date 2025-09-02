import { type NextRequest, NextResponse } from "next/server"
import { getSession } from "./lib/auth"

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Public routes that don't require authentication
  const publicRoutes = ["/", "/login", "/signup", "/api/auth/login", "/api/auth/signup", "/api/payment/verify"]

  if (publicRoutes.includes(pathname)) {
    return NextResponse.next()
  }

  // Check for session
  const session = await getSession()

  if (!session) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  // Routes that require payment
  const paidRoutes = ["/dashboard", "/student", "/teacher", "/lessons", "/quiz"]
  const requiresPayment = paidRoutes.some((route) => pathname.startsWith(route))

  if (requiresPayment && !session.hasPaid) {
    return NextResponse.redirect(new URL("/payment", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
