"use client"

import type { User } from "@/lib/database"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts"

interface ProgressOverviewProps {
  user: User
}

export function ProgressOverview({ user }: ProgressOverviewProps) {
  // Mock data - in real app, this would come from the database
  const subjectProgress = [
    { subject: "Mathematics", progress: 75, lessons: 12, quizzes: 8 },
    { subject: "English", progress: 60, lessons: 10, quizzes: 6 },
    { subject: "Science", progress: 85, lessons: 8, quizzes: 7 },
    { subject: "Kiswahili", progress: 45, lessons: 6, quizzes: 3 },
  ]

  const weeklyProgress = [
    { day: "Mon", minutes: 45 },
    { day: "Tue", minutes: 60 },
    { day: "Wed", minutes: 30 },
    { day: "Thu", minutes: 75 },
    { day: "Fri", minutes: 90 },
    { day: "Sat", minutes: 120 },
    { day: "Sun", minutes: 80 },
  ]

  const quizScores = [
    { week: "Week 1", score: 65 },
    { week: "Week 2", score: 72 },
    { week: "Week 3", score: 78 },
    { week: "Week 4", score: 85 },
  ]

  return (
    <div className="space-y-6">
      {/* Subject Progress */}
      <Card>
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Maendeleo ya Masomo" : "Subject Progress"}</CardTitle>
          <CardDescription>
            {user.language_preference === "sw"
              ? "Maendeleo yako katika kila somo"
              : "Your progress across all subjects"}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {subjectProgress.map((subject) => (
            <div key={subject.subject} className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-medium">{subject.subject}</span>
                <span className="text-sm text-muted-foreground">{subject.progress}%</span>
              </div>
              <Progress value={subject.progress} className="h-2" />
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>
                  {subject.lessons} {user.language_preference === "sw" ? "masomo" : "lessons"}
                </span>
                <span>
                  {subject.quizzes} {user.language_preference === "sw" ? "majaribio" : "quizzes"}
                </span>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Weekly Study Time */}
      <Card>
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Muda wa Kusoma wa Wiki" : "Weekly Study Time"}</CardTitle>
          <CardDescription>
            {user.language_preference === "sw" ? "Dakika za kusoma kwa siku" : "Minutes studied per day"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={weeklyProgress}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="minutes" fill="hsl(var(--primary))" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Quiz Performance */}
      <Card>
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Utendaji wa Majaribio" : "Quiz Performance"}</CardTitle>
          <CardDescription>
            {user.language_preference === "sw" ? "Wastani wa alama za majaribio" : "Average quiz scores over time"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={quizScores}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="week" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="hsl(var(--primary))" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
