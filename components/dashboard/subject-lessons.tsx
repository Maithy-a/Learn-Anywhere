"use client"

import { useState, useEffect } from "react"
import type { User, Subject, Lesson } from "@/lib/database"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, BookOpen, Brain, Star } from "lucide-react"

interface SubjectLessonsProps {
  subject: Subject
  user: User
  onBack: () => void
  onStartStudy: (lesson: Lesson) => void
  onStartQuiz: (lesson: Lesson) => void
}

export function SubjectLessons({ subject, user, onBack, onStartStudy, onStartQuiz }: SubjectLessonsProps) {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const response = await fetch(`/api/lessons?subject_id=${subject.id}`)
        const data = await response.json()
        setLessons(data.lessons || [])
      } catch (error) {
        console.error("Failed to fetch lessons:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchLessons()
  }, [subject.id])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading lessons...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="sm" onClick={onBack}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          {user.language_preference === "sw" ? "Rudi" : "Back"}
        </Button>
        <div>
          <h1 className="text-2xl font-bold">
            {user.language_preference === "sw" && subject.name_sw ? subject.name_sw : subject.name}
          </h1>
          <p className="text-muted-foreground">
            {user.language_preference === "sw" && subject.description_sw ? subject.description_sw : subject.description}
          </p>
        </div>
      </div>

      {/* Subject Overview */}
      <div className="grid md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Jumla ya Masomo" : "Total Lessons"}
            </CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{lessons.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Masomo Yaliyokamilika" : "Completed"}
            </CardTitle>
            <Star className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">3</div>
            <p className="text-xs text-muted-foreground">
              {Math.round((3 / Math.max(lessons.length, 1)) * 100)}% complete
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Wastani wa Alama" : "Average Score"}
            </CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">82%</div>
          </CardContent>
        </Card>
      </div>

      {/* Lessons List */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">
          {user.language_preference === "sw" ? "Masomo Yaliyopatikana" : "Available Lessons"}
        </h2>

        {lessons.length === 0 ? (
          <Card>
            <CardContent className="text-center py-12">
              <BookOpen className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">
                {user.language_preference === "sw" ? "Hakuna Masomo" : "No Lessons Available"}
              </h3>
              <p className="text-muted-foreground">
                {user.language_preference === "sw"
                  ? "Masomo ya somo hili hayajaongezwa bado."
                  : "Lessons for this subject haven't been added yet."}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4">
            {lessons.map((lesson, index) => (
              <Card key={lesson.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="outline">
                          {user.language_preference === "sw" ? "Darasa" : "Grade"} {lesson.grade_level}
                        </Badge>
                        <Badge variant="secondary">
                          {user.language_preference === "sw" ? `Somo ${index + 1}` : `Lesson ${index + 1}`}
                        </Badge>
                      </div>
                      <CardTitle className="text-lg">
                        {user.language_preference === "sw" && lesson.title_sw ? lesson.title_sw : lesson.title}
                      </CardTitle>
                      <CardDescription className="mt-2">
                        {user.language_preference === "sw"
                          ? "Jifunze kupitia kadi za kujifunzia na majaribio ya akili."
                          : "Learn through interactive flashcards and AI-powered quizzes."}
                      </CardDescription>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-muted-foreground mb-2">
                        {user.language_preference === "sw" ? "Maendeleo" : "Progress"}
                      </div>
                      <Progress value={Math.random() * 100} className="w-20 h-2" />
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    <Button variant="outline" size="sm" onClick={() => onStartStudy(lesson)}>
                      <BookOpen className="h-4 w-4 mr-2" />
                      {user.language_preference === "sw" ? "Soma" : "Study"}
                    </Button>
                    <Button size="sm" onClick={() => onStartQuiz(lesson)}>
                      <Brain className="h-4 w-4 mr-2" />
                      {user.language_preference === "sw" ? "Jaribio" : "Quiz"}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
