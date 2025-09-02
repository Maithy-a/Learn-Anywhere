"use client"

import { useState, useEffect } from "react"
import type { User, Lesson, Flashcard } from "@/lib/database"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { ArrowLeft, RotateCcw, ChevronLeft, ChevronRight, Eye, EyeOff } from "lucide-react"

interface StudyModeProps {
  lesson: Lesson
  user: User
  onBack: () => void
}

export function StudyMode({ lesson, user, onBack }: StudyModeProps) {
  const [flashcards, setFlashcards] = useState<Flashcard[]>([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [showAnswer, setShowAnswer] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchFlashcards = async () => {
      try {
        const response = await fetch(`/api/flashcards?lesson_id=${lesson.id}`)
        const data = await response.json()
        setFlashcards(data.flashcards || [])
      } catch (error) {
        console.error("Failed to fetch flashcards:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchFlashcards()
  }, [lesson.id])

  const currentCard = flashcards[currentIndex]
  const progress = flashcards.length > 0 ? ((currentIndex + 1) / flashcards.length) * 100 : 0

  const nextCard = () => {
    if (currentIndex < flashcards.length - 1) {
      setCurrentIndex(currentIndex + 1)
      setShowAnswer(false)
    }
  }

  const prevCard = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1)
      setShowAnswer(false)
    }
  }

  const resetCards = () => {
    setCurrentIndex(0)
    setShowAnswer(false)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading flashcards...</p>
        </div>
      </div>
    )
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
            <div>
              <h1 className="text-xl font-bold">
                {user.language_preference === "sw" ? "Hali ya Kusoma" : "Study Mode"}
              </h1>
              <p className="text-sm text-muted-foreground">
                {user.language_preference === "sw" && lesson.title_sw ? lesson.title_sw : lesson.title}
              </p>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={resetCards}>
            <RotateCcw className="h-4 w-4 mr-2" />
            {user.language_preference === "sw" ? "Anza Upya" : "Reset"}
          </Button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {flashcards.length === 0 ? (
          <Card className="max-w-2xl mx-auto">
            <CardContent className="text-center py-12">
              <h3 className="text-lg font-medium mb-2">
                {user.language_preference === "sw" ? "Hakuna Kadi za Kujifunzia" : "No Flashcards Available"}
              </h3>
              <p className="text-muted-foreground">
                {user.language_preference === "sw"
                  ? "Kadi za kujifunzia za somo hili hazijaongezwa bado."
                  : "Flashcards for this lesson haven't been created yet."}
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Progress */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>{user.language_preference === "sw" ? "Maendeleo" : "Progress"}</span>
                <span>
                  {currentIndex + 1} / {flashcards.length}
                </span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>

            {/* Flashcard */}
            <Card className="min-h-[400px] cursor-pointer" onClick={() => setShowAnswer(!showAnswer)}>
              <CardHeader className="text-center">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  {showAnswer
                    ? user.language_preference === "sw"
                      ? "Jibu"
                      : "Answer"
                    : user.language_preference === "sw"
                      ? "Swali"
                      : "Question"}
                </CardTitle>
              </CardHeader>
              <CardContent className="flex items-center justify-center min-h-[300px]">
                <div className="text-center space-y-4">
                  <p className="text-2xl font-medium text-balance">
                    {showAnswer
                      ? user.language_preference === "sw" && currentCard?.answer_sw
                        ? currentCard.answer_sw
                        : currentCard?.answer
                      : user.language_preference === "sw" && currentCard?.question_sw
                        ? currentCard.question_sw
                        : currentCard?.question}
                  </p>
                  <Button variant="ghost" size="sm">
                    {showAnswer ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                    {showAnswer
                      ? user.language_preference === "sw"
                        ? "Ficha Jibu"
                        : "Hide Answer"
                      : user.language_preference === "sw"
                        ? "Onyesha Jibu"
                        : "Show Answer"}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex justify-between items-center">
              <Button variant="outline" onClick={prevCard} disabled={currentIndex === 0}>
                <ChevronLeft className="h-4 w-4 mr-2" />
                {user.language_preference === "sw" ? "Iliyotangulia" : "Previous"}
              </Button>

              <div className="text-center">
                <p className="text-sm text-muted-foreground">
                  {user.language_preference === "sw" ? "Bofya kadi kuonyesha jibu" : "Click card to reveal answer"}
                </p>
              </div>

              <Button variant="outline" onClick={nextCard} disabled={currentIndex === flashcards.length - 1}>
                {user.language_preference === "sw" ? "Ifuatayo" : "Next"}
                <ChevronRight className="h-4 w-4 ml-2" />
              </Button>
            </div>

            {/* Completion */}
            {currentIndex === flashcards.length - 1 && showAnswer && (
              <Card className="bg-primary/5 border-primary/20">
                <CardContent className="text-center py-6">
                  <h3 className="text-lg font-medium mb-2">
                    {user.language_preference === "sw" ? "Hongera!" : "Congratulations!"}
                  </h3>
                  <p className="text-muted-foreground mb-4">
                    {user.language_preference === "sw"
                      ? "Umekamilisha kadi zote za kujifunzia za somo hili."
                      : "You've completed all flashcards for this lesson."}
                  </p>
                  <Button onClick={resetCards}>
                    <RotateCcw className="h-4 w-4 mr-2" />
                    {user.language_preference === "sw" ? "Rudia" : "Review Again"}
                  </Button>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
