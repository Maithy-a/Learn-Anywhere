"use client"

import { useState } from "react"
import type { User, Subject } from "@/lib/database"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { BookOpen, Brain, Trophy, Clock, LogOut, Globe } from "lucide-react"
import { SubjectLessons } from "./subject-lessons"
import { StudyMode } from "./study-mode"
import { QuizMode } from "./quiz-mode"
import { ProgressOverview } from "./progress-overview"

interface StudentDashboardProps {
  user: User
  subjects: Subject[]
}

export function StudentDashboard({ user, subjects }: StudentDashboardProps) {
  const [activeTab, setActiveTab] = useState("overview")
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null)
  const [currentMode, setCurrentMode] = useState<"lessons" | "study" | "quiz">("lessons")
  const [selectedLesson, setSelectedLesson] = useState<any>(null)

  const handleLogout = async () => {
    await fetch("/api/auth/logout", { method: "POST" })
    window.location.href = "/"
  }

  const getGreeting = () => {
    const hour = new Date().getHours()
    const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening"
    return user.language_preference === "sw"
      ? hour < 12
        ? "Habari za asubuhi"
        : hour < 18
          ? "Habari za mchana"
          : "Habari za jioni"
      : greeting
  }

  if (currentMode === "study" && selectedLesson) {
    return <StudyMode lesson={selectedLesson} user={user} onBack={() => setCurrentMode("lessons")} />
  }

  if (currentMode === "quiz" && selectedLesson) {
    return <QuizMode lesson={selectedLesson} user={user} onBack={() => setCurrentMode("lessons")} />
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <BookOpen className="h-8 w-8 text-primary" />
            <div>
              <h1 className="text-xl font-bold text-foreground">Learn-Anywhere</h1>
              <p className="text-sm text-muted-foreground">
                {getGreeting()}, {user.first_name}!
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm">
              <Globe className="h-4 w-4 mr-2" />
              {user.language_preference === "sw" ? "Kiswahili" : "English"}
            </Button>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <Button variant="ghost" size="sm">
                  <LogOut className="h-4 w-4 mr-2" />
                  {user.language_preference === "sw" ? "Ondoka" : "Logout"}
                </Button>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>
                    {user.language_preference === "sw" ? "Una uhakika?" : "Are you sure?"}
                  </AlertDialogTitle>
                  <AlertDialogDescription>
                    {user.language_preference === "sw"
                      ? "Hii itakuondoa kwenye akaunti yako."
                      : "This will log you out of your account."}
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>
                    {user.language_preference === "sw" ? "Ghairi" : "Cancel"}
                  </AlertDialogCancel>
                  <AlertDialogAction onClick={handleLogout}>
                    {user.language_preference === "sw" ? "Ondoka" : "Logout"}
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {selectedSubject ? (
          <SubjectLessons
            subject={selectedSubject}
            user={user}
            onBack={() => setSelectedSubject(null)}
            onStartStudy={(lesson) => {
              setSelectedLesson(lesson)
              setCurrentMode("study")
            }}
            onStartQuiz={(lesson) => {
              setSelectedLesson(lesson)
              setCurrentMode("quiz")
            }}
          />
        ) : (
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="overview">{user.language_preference === "sw" ? "Muhtasari" : "Overview"}</TabsTrigger>
              <TabsTrigger value="subjects">{user.language_preference === "sw" ? "Masomo" : "Subjects"}</TabsTrigger>
              <TabsTrigger value="progress">{user.language_preference === "sw" ? "Maendeleo" : "Progress"}</TabsTrigger>
              <TabsTrigger value="achievements">
                {user.language_preference === "sw" ? "Mafanikio" : "Achievements"}
              </TabsTrigger>
            </TabsList>

            <TabsContent value="overview" className="space-y-6">
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      {user.language_preference === "sw" ? "Masomo Yaliyokamilika" : "Lessons Completed"}
                    </CardTitle>
                    <BookOpen className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">12</div>
                    <p className="text-xs text-muted-foreground">
                      {user.language_preference === "sw" ? "+2 wiki hii" : "+2 this week"}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      {user.language_preference === "sw" ? "Alama za Jaribio" : "Quiz Score"}
                    </CardTitle>
                    <Brain className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">85%</div>
                    <p className="text-xs text-muted-foreground">
                      {user.language_preference === "sw" ? "Wastani wa wiki hii" : "Average this week"}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      {user.language_preference === "sw" ? "Muda wa Kusoma" : "Study Time"}
                    </CardTitle>
                    <Clock className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">4.2h</div>
                    <p className="text-xs text-muted-foreground">
                      {user.language_preference === "sw" ? "Wiki hii" : "This week"}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">
                      {user.language_preference === "sw" ? "Tuzo" : "Achievements"}
                    </CardTitle>
                    <Trophy className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold">3</div>
                    <p className="text-xs text-muted-foreground">
                      {user.language_preference === "sw" ? "Tuzo mpya" : "New badges"}
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Recent Activity */}
              <Card>
                <CardHeader>
                  <CardTitle>
                    {user.language_preference === "sw" ? "Shughuli za Hivi Karibuni" : "Recent Activity"}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { subject: "Mathematics", lesson: "Fractions and Decimals", score: 92, time: "2 hours ago" },
                    { subject: "Science", lesson: "Plant Biology", score: 78, time: "1 day ago" },
                    { subject: "English", lesson: "Reading Comprehension", score: 88, time: "2 days ago" },
                  ].map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <div>
                        <p className="font-medium">{activity.lesson}</p>
                        <p className="text-sm text-muted-foreground">{activity.subject}</p>
                      </div>
                      <div className="text-right">
                        <Badge variant={activity.score >= 80 ? "default" : "secondary"}>{activity.score}%</Badge>
                        <p className="text-xs text-muted-foreground mt-1">{activity.time}</p>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="subjects" className="space-y-6">
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {subjects.map((subject) => (
                  <Card
                    key={subject.id}
                    className="cursor-pointer hover:shadow-lg transition-shadow"
                    onClick={() => setSelectedSubject(subject)}
                  >
                    <CardHeader className="text-center">
                      <div className="text-4xl mb-4">
                        {subject.name === "Mathematics"
                          ? "📊"
                          : subject.name === "English"
                            ? "📚"
                            : subject.name === "Science"
                              ? "🔬"
                              : "🗣️"}
                      </div>
                      <CardTitle className="text-lg">
                        {user.language_preference === "sw" && subject.name_sw ? subject.name_sw : subject.name}
                      </CardTitle>
                      <CardDescription>
                        {user.language_preference === "sw" && subject.description_sw
                          ? subject.description_sw
                          : subject.description}
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>{user.language_preference === "sw" ? "Maendeleo" : "Progress"}</span>
                          <span>65%</span>
                        </div>
                        <Progress value={65} className="h-2" />
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="progress">
              <ProgressOverview user={user} />
            </TabsContent>

            <TabsContent value="achievements" className="space-y-6">
              <div className="grid md:grid-cols-3 gap-6">
                {[
                  { name: "First Quiz", description: "Complete your first quiz", earned: true },
                  { name: "Study Streak", description: "7 days of continuous learning", earned: true },
                  { name: "Math Master", description: "Score 90% in 5 math quizzes", earned: false },
                  { name: "Science Explorer", description: "Complete all science lessons", earned: false },
                  { name: "Language Expert", description: "Master both English and Kiswahili", earned: false },
                  { name: "Perfect Score", description: "Get 100% on any quiz", earned: true },
                ].map((achievement, index) => (
                  <Card key={index} className={achievement.earned ? "border-primary/50 bg-primary/5" : "opacity-60"}>
                    <CardHeader className="text-center">
                      <div className="text-4xl mb-2">{achievement.earned ? "🏆" : "🔒"}</div>
                      <CardTitle className="text-lg">{achievement.name}</CardTitle>
                      <CardDescription>{achievement.description}</CardDescription>
                    </CardHeader>
                  </Card>
                ))}
              </div>
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  )
}
