"use client"

import type React from "react"

import { useState } from "react"
import type { User, Subject } from "@/lib/database"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ArrowLeft, Plus, Trash2, Save } from "lucide-react"

interface LessonCreatorProps {
  user: User
  subjects: Subject[]
  onBack: () => void
}

interface FlashcardData {
  id: string
  question: string
  question_sw: string
  answer: string
  answer_sw: string
  difficulty: number
}

export function LessonCreator({ user, subjects, onBack }: LessonCreatorProps) {
  const [lessonData, setLessonData] = useState({
    title: "",
    title_sw: "",
    subject_id: "",
    grade_level: "",
  })
  const [flashcards, setFlashcards] = useState<FlashcardData[]>([
    {
      id: "1",
      question: "",
      question_sw: "",
      answer: "",
      answer_sw: "",
      difficulty: 1,
    },
  ])
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")

  const addFlashcard = () => {
    const newCard: FlashcardData = {
      id: Date.now().toString(),
      question: "",
      question_sw: "",
      answer: "",
      answer_sw: "",
      difficulty: 1,
    }
    setFlashcards([...flashcards, newCard])
  }

  const removeFlashcard = (id: string) => {
    if (flashcards.length > 1) {
      setFlashcards(flashcards.filter((card) => card.id !== id))
    }
  }

  const updateFlashcard = (id: string, field: keyof FlashcardData, value: string | number) => {
    setFlashcards(flashcards.map((card) => (card.id === id ? { ...card, [field]: value } : card)))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!lessonData.title || !lessonData.subject_id || !lessonData.grade_level) {
      setError("Please fill in all lesson details")
      return
    }

    const validFlashcards = flashcards.filter((card) => card.question && card.answer)
    if (validFlashcards.length === 0) {
      setError("Please add at least one complete flashcard")
      return
    }

    setSaving(true)
    setError("")

    try {
      const response = await fetch("/api/teacher/create-lesson", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...lessonData,
          flashcards: validFlashcards,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Failed to create lesson")
      }

      onBack()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create lesson")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={onBack}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              {user.language_preference === "sw" ? "Rudi" : "Back"}
            </Button>
            <h1 className="text-xl font-bold">
              {user.language_preference === "sw" ? "Tengeneza Somo" : "Create Lesson"}
            </h1>
          </div>
          <Button onClick={handleSubmit} disabled={saving}>
            <Save className="h-4 w-4 mr-2" />
            {saving
              ? user.language_preference === "sw"
                ? "Inahifadhi..."
                : "Saving..."
              : user.language_preference === "sw"
                ? "Hifadhi Somo"
                : "Save Lesson"}
          </Button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Lesson Details */}
          <Card>
            <CardHeader>
              <CardTitle>{user.language_preference === "sw" ? "Maelezo ya Somo" : "Lesson Details"}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="title">
                    {user.language_preference === "sw" ? "Jina la Somo (Kiingereza)" : "Lesson Title (English)"}
                  </Label>
                  <Input
                    id="title"
                    value={lessonData.title}
                    onChange={(e) => setLessonData({ ...lessonData, title: e.target.value })}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="title_sw">
                    {user.language_preference === "sw" ? "Jina la Somo (Kiswahili)" : "Lesson Title (Kiswahili)"}
                  </Label>
                  <Input
                    id="title_sw"
                    value={lessonData.title_sw}
                    onChange={(e) => setLessonData({ ...lessonData, title_sw: e.target.value })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="subject">{user.language_preference === "sw" ? "Somo" : "Subject"}</Label>
                  <Select
                    value={lessonData.subject_id}
                    onValueChange={(value) => setLessonData({ ...lessonData, subject_id: value })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder={user.language_preference === "sw" ? "Chagua somo" : "Select subject"} />
                    </SelectTrigger>
                    <SelectContent>
                      {subjects.map((subject) => (
                        <SelectItem key={subject.id} value={subject.id.toString()}>
                          {user.language_preference === "sw" && subject.name_sw ? subject.name_sw : subject.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="grade">{user.language_preference === "sw" ? "Darasa" : "Grade Level"}</Label>
                  <Select
                    value={lessonData.grade_level}
                    onValueChange={(value) => setLessonData({ ...lessonData, grade_level: value })}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder={user.language_preference === "sw" ? "Chagua darasa" : "Select grade"} />
                    </SelectTrigger>
                    <SelectContent>
                      {[4, 5, 6, 7, 8].map((grade) => (
                        <SelectItem key={grade} value={grade.toString()}>
                          {user.language_preference === "sw" ? "Darasa" : "Grade"} {grade}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Flashcards */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardTitle>{user.language_preference === "sw" ? "Kadi za Kujifunzia" : "Flashcards"}</CardTitle>
                <CardDescription>
                  {user.language_preference === "sw"
                    ? "Ongeza maswali na majibu ya kujifunzia"
                    : "Add questions and answers for studying"}
                </CardDescription>
              </div>
              <Button type="button" onClick={addFlashcard}>
                <Plus className="h-4 w-4 mr-2" />
                {user.language_preference === "sw" ? "Ongeza Kadi" : "Add Card"}
              </Button>
            </CardHeader>
            <CardContent className="space-y-6">
              {flashcards.map((card, index) => (
                <div key={card.id} className="border rounded-lg p-4 space-y-4">
                  <div className="flex items-center justify-between">
                    <h4 className="font-medium">
                      {user.language_preference === "sw" ? "Kadi" : "Card"} {index + 1}
                    </h4>
                    {flashcards.length > 1 && (
                      <Button type="button" variant="ghost" size="sm" onClick={() => removeFlashcard(card.id)}>
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    )}
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>{user.language_preference === "sw" ? "Swali (Kiingereza)" : "Question (English)"}</Label>
                      <Textarea
                        value={card.question}
                        onChange={(e) => updateFlashcard(card.id, "question", e.target.value)}
                        rows={3}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>{user.language_preference === "sw" ? "Swali (Kiswahili)" : "Question (Kiswahili)"}</Label>
                      <Textarea
                        value={card.question_sw}
                        onChange={(e) => updateFlashcard(card.id, "question_sw", e.target.value)}
                        rows={3}
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>{user.language_preference === "sw" ? "Jibu (Kiingereza)" : "Answer (English)"}</Label>
                      <Textarea
                        value={card.answer}
                        onChange={(e) => updateFlashcard(card.id, "answer", e.target.value)}
                        rows={3}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label>{user.language_preference === "sw" ? "Jibu (Kiswahili)" : "Answer (Kiswahili)"}</Label>
                      <Textarea
                        value={card.answer_sw}
                        onChange={(e) => updateFlashcard(card.id, "answer_sw", e.target.value)}
                        rows={3}
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>{user.language_preference === "sw" ? "Kiwango cha Ugumu" : "Difficulty Level"}</Label>
                    <Select
                      value={card.difficulty.toString()}
                      onValueChange={(value) => updateFlashcard(card.id, "difficulty", Number.parseInt(value))}
                    >
                      <SelectTrigger className="w-48">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="1">1 - {user.language_preference === "sw" ? "Rahisi" : "Easy"}</SelectItem>
                        <SelectItem value="2">
                          2 - {user.language_preference === "sw" ? "Wastani" : "Medium"}
                        </SelectItem>
                        <SelectItem value="3">3 - {user.language_preference === "sw" ? "Ngumu" : "Hard"}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </form>
      </div>
    </div>
  )
}
