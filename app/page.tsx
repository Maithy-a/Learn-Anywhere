import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { BookOpen, Users, Wifi, Globe, Star, CheckCircle } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BookOpen className="h-8 w-8 text-primary" />
            <span className="text-xl font-bold text-foreground">Learn-Anywhere</span>
          </div>
          <div className="flex items-center gap-2">
            <Link href="/login">
              <Button variant="outline">Login</Button>
            </Link>
            <Link href="/signup">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl text-center">
          <Badge className="mb-6 bg-primary/10 text-primary border-primary/20">SDG 4: Quality Education</Badge>
          <h1 className="text-4xl md:text-6xl font-bold text-balance mb-6 text-foreground">
            Learn Anywhere, <span className="text-primary">Anytime</span>
          </h1>
          <p className="text-xl text-muted-foreground text-balance mb-8 max-w-3xl mx-auto">
            Offline-first educational platform designed for underserved communities. Master Math, English, Science, and
            Kiswahili with AI-powered tools that work without internet.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <Link href="/signup">
              <Button size="lg" className="text-lg px-8 py-6">
                Start Learning - $10
              </Button>
            </Link>
            <p className="text-sm text-muted-foreground">One-time payment • Lifetime access • Works offline</p>
          </div>

          {/* Feature Grid */}
          <div className="grid md:grid-cols-3 gap-6 mt-16">
            <Card className="border-border/50 hover:border-primary/50 transition-colors">
              <CardHeader className="text-center">
                <Wifi className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Offline-First</CardTitle>
                <CardDescription>Learn without internet. All content syncs when connected.</CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-border/50 hover:border-primary/50 transition-colors">
              <CardHeader className="text-center">
                <Globe className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>Bilingual Support</CardTitle>
                <CardDescription>Full support for English and Kiswahili languages.</CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-border/50 hover:border-primary/50 transition-colors">
              <CardHeader className="text-center">
                <Star className="h-12 w-12 text-primary mx-auto mb-4" />
                <CardTitle>AI-Powered</CardTitle>
                <CardDescription>Smart quizzes and personalized learning paths.</CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6 text-foreground">Built for Real-World Learning</h2>
              <div className="space-y-4">
                {[
                  "Offline flashcards and study materials",
                  "AI-generated quizzes that work without internet",
                  "Progress tracking and analytics",
                  "Teacher dashboard for content management",
                  "Multi-device sync when online",
                  "Secure payment with Paystack",
                ].map((feature) => (
                  <div key={feature} className="flex items-center gap-3">
                    <CheckCircle className="h-5 w-5 text-primary flex-shrink-0" />
                    <span className="text-muted-foreground">{feature}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="relative">
              <Card className="p-8 bg-gradient-to-br from-primary/5 to-secondary/5 border-primary/20">
                <div className="text-center">
                  <Users className="h-16 w-16 text-primary mx-auto mb-6" />
                  <h3 className="text-2xl font-bold mb-4 text-foreground">For Students & Teachers</h3>
                  <p className="text-muted-foreground mb-6">
                    Students get personalized learning experiences while teachers can upload content, monitor progress,
                    and support their students effectively.
                  </p>
                  <div className="flex justify-center gap-4">
                    <Badge variant="secondary">Student Dashboard</Badge>
                    <Badge variant="secondary">Teacher Tools</Badge>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Subjects Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">Comprehensive Curriculum</h2>
            <p className="text-xl text-muted-foreground text-balance">
              Covering essential subjects for grades 4-8 with culturally relevant content
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: "Mathematics", nameKw: "Hisabati", icon: "📊" },
              { name: "English", nameKw: "Kiingereza", icon: "📚" },
              { name: "Science", nameKw: "Sayansi", icon: "🔬" },
              { name: "Kiswahili", nameKw: "Kiswahili", icon: "🗣️" },
            ].map((subject) => (
              <Card key={subject.name} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="text-4xl mb-4">{subject.icon}</div>
                  <CardTitle className="text-lg">{subject.name}</CardTitle>
                  <CardDescription className="text-primary font-medium">{subject.nameKw}</CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    Interactive lessons, flashcards, and AI-generated quizzes
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-primary/5">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6 text-foreground">Start Your Learning Journey Today</h2>
          <p className="text-xl text-muted-foreground mb-8 text-balance">
            Join thousands of students already learning with Learn-Anywhere. One payment, lifetime access to quality
            education.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/signup">
              <Button size="lg" className="text-lg px-8 py-6">
                Get Started for $10
              </Button>
            </Link>
            <Link href="/login">
              <Button variant="outline" size="lg" className="text-lg px-8 py-6 bg-transparent">
                Already have an account?
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-card/50 py-12 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <BookOpen className="h-6 w-6 text-primary" />
                <span className="font-bold text-foreground">Learn-Anywhere</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Empowering education in underserved communities through offline-first technology.
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4 text-foreground">Platform</h4>
              <div className="space-y-2 text-sm text-muted-foreground">
                <div>Student Dashboard</div>
                <div>Teacher Tools</div>
                <div>Offline Learning</div>
                <div>Progress Tracking</div>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-4 text-foreground">Support</h4>
              <div className="space-y-2 text-sm text-muted-foreground">
                <div>Help Center</div>
                <div>Contact Us</div>
                <div>Privacy Policy</div>
                <div>Terms of Service</div>
              </div>
            </div>
          </div>

          <div className="border-t border-border mt-8 pt-8 text-center text-sm text-muted-foreground">
            © 2024 Learn-Anywhere. Supporting SDG 4: Quality Education for All.
          </div>
        </div>
      </footer>
    </div>
  )
}
