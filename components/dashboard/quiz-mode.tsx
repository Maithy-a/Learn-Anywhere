"use client"

import { useState, useEffect } from "react"
import type { User, Lesson, Quiz } from "@/lib/database"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Label } from "@/components/ui/label"
import { ArrowLeft, Clock, CheckCircle, XCircle } from "lucide-react"

interface QuizModeProps {
  lesson: Lesson
  user: User
  onBack: () => void
}

interface QuizQuestion {
  id: string
  question: string
  options: string[]
  correct_answer: number
}

export function QuizMode({ lesson, user, onBack }: QuizModeProps) {
  const [quizzes, setQuizzes] = useState<Quiz[]>([])
  const [currentQuiz, setCurrentQuiz] = useState<Quiz | null>(null)
  const [questions, setQuestions] = useState<QuizQuestion[]>([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<string>("")
  const [answers, setAnswers] = useState<number[]>([])
  const [showResults, setShowResults] = useState(false)
  const [timeLeft, setTimeLeft] = useState(300) // 5 minutes
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const response = await fetch(`/api/quizzes?lesson_id=${lesson.id}`)
        const data = await response.json()
        setQuizzes(data.quizzes || [])

        if (data.quizzes && data.quizzes.length > 0) {
          const quiz = data.quizzes[0]
          setCurrentQuiz(quiz)
          setQuestions(JSON.parse(quiz.questions))
        }
      } catch (error) {
        console.error("Failed to fetch quizzes:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchQuizzes()
  }, [lesson.id])

  useEffect(() => {
    if (currentQuiz && !showResults && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleSubmitQuiz()
            return 0
          }
          return prev - 1
        })
      }, 1000)

      return () => clearInterval(timer)
    }
  }, [currentQuiz, showResults, timeLeft])

  const handleAnswerSelect = (value: string) => {
    setSelectedAnswer(value)
  }

  const handleNextQuestion = () => {
    const answerIndex = Number.parseInt(selectedAnswer)
    const newAnswers = [...answers]
    newAnswers[currentQuestionIndex] = answerIndex
    setAnswers(newAnswers)

    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      setSelectedAnswer("")
    } else {
      handleSubmitQuiz(newAnswers)
    }
  }

  const handleSubmitQuiz = (finalAnswers = answers) => {
    setShowResults(true)
    // Here you would typically save the quiz attempt to the database
  }

  const calculateScore = () => {
    let correct = 0
    questions.forEach((question, index) => {
      if (answers[index] === question.correct_answer) {
        correct++
      }
    })
    return Math.round((correct / questions.length) * 100)
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, "0")}`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading quiz...</p>
        </div>
      </div>
    )
  }

  if (!currentQuiz || questions.length === 0) {
    return (
      <div className="min-h-screen bg-background">
        <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4 flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={onBack}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              {user.language_preference === "sw" ? "Rudi" : "Back"}
            </Button>
            <h1 className="text-xl font-bold">{user.language_preference === "sw" ? "Hali ya Jaribio" : "Quiz Mode"}</h1>
          </div>
        </header>

        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-2xl mx-auto">
            <CardContent className="text-center py-12">
              <h3 className="text-lg font-medium mb-2">
                {user.language_preference === "sw" ? "Hakuna Majaribio" : "No Quizzes Available"}
              </h3>
              <p className="text-muted-foreground">
                {user.language_preference === "sw"
                  ? "Majaribio ya somo hili hayajaongezwa bado."
                  : "Quizzes for this lesson haven't been created yet."}
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (showResults) {
    const score = calculateScore()
    const correctAnswers = answers.filter((answer, index) => answer === questions[index].correct_answer).length

    return (
      <div className="min-h-screen bg-background">
        <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
          <div className="container mx-auto px-4 py-4 flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={onBack}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              {user.language_preference === "sw" ? "Rudi" : "Back"}
            </Button>
            <h1 className="text-xl font-bold">
              {user.language_preference === "sw" ? "Matokeo ya Jaribio" : "Quiz Results"}
            </h1>
          </div>
        </header>

        <div className="container mx-auto px-4 py-8">
          <div className="max-w-2xl mx-auto space-y-6">
            <Card className="text-center">
              <CardHeader>
                <CardTitle className="text-3xl font-bold text-primary">{score}%</CardTitle>
                <p className="text-muted-foreground">
                  {correctAnswers} / {questions.length} {user.language_preference === "sw" ? "sahihi" : "correct"}
                </p>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <Progress value={score} className="h-4" />
                  <p className="text-lg">
                    {score >= 80
                      ? user.language_preference === "sw"
                        ? "Vizuri sana!"
                        : "Excellent work!"
                      : score >= 60
                        ? user.language_preference === "sw"
                          ? "Vizuri!"
                          : "Good job!"
                        : user.language_preference === "sw"
                          ? "Jaribu tena!"
                          : "Keep practicing!"}
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Answer Review */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">
                {user.language_preference === "sw" ? "Mapitio ya Majibu" : "Answer Review"}
              </h3>
              {questions.map((question, index) => (
                <Card
                  key={index}
                  className={
                    answers[index] === question.correct_answer
                      ? "border-green-200 bg-green-50"
                      : "border-red-200 bg-red-50"
                  }
                >
                  <CardContent className="pt-6">
                    <div className="flex items-start gap-3">
                      {answers[index] === question.correct_answer ? (
                        <CheckCircle className="h-5 w-5 text-green-600 mt-1" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600 mt-1" />
                      )}
                      <div className="flex-1">
                        <p className="font-medium mb-2">{question.question}</p>
                        <p className="text-sm text-muted-foreground">
                          {user.language_preference === "sw" ? "Jibu sahihi" : "Correct answer"}:{" "}
                          {question.options[question.correct_answer]}
                        </p>
                        {answers[index] !== question.correct_answer && (
                          <p className="text-sm text-red-600">
                            {user.language_preference === "sw" ? "Jibu lako" : "Your answer"}:{" "}
                            {question.options[answers[index]] || "No answer"}
                          </p>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  const currentQuestion = questions[currentQuestionIndex]
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100

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
                {user.language_preference === "sw" ? "Hali ya Jaribio" : "Quiz Mode"}
              </h1>
              <p className="text-sm text-muted-foreground">
                {user.language_preference === "sw" && currentQuiz.title_sw ? currentQuiz.title_sw : currentQuiz.title}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-sm">
            <Clock className="h-4 w-4" />
            <span className={timeLeft < 60 ? "text-red-600 font-bold" : ""}>{formatTime(timeLeft)}</span>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        <div className="max-w-2xl mx-auto space-y-6">
          {/* Progress */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>{user.language_preference === "sw" ? "Maendeleo" : "Progress"}</span>
              <span>
                {currentQuestionIndex + 1} / {questions.length}
              </span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>

          {/* Question */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">
                {user.language_preference === "sw" ? "Swali" : "Question"} {currentQuestionIndex + 1}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <p className="text-lg">{currentQuestion.question}</p>

              <RadioGroup value={selectedAnswer} onValueChange={handleAnswerSelect}>
                {currentQuestion.options.map((option, index) => (
                  <div key={index} className="flex items-center space-x-2 p-3 rounded-lg border hover:bg-muted/50">
                    <RadioGroupItem value={index.toString()} id={`option-${index}`} />
                    <Label htmlFor={`option-${index}`} className="flex-1 cursor-pointer">
                      {option}
                    </Label>
                  </div>
                ))}
              </RadioGroup>
            </CardContent>
          </Card>

          {/* Navigation */}
          <div className="flex justify-end">
            <Button onClick={handleNextQuestion} disabled={!selectedAnswer}>
              {currentQuestionIndex === questions.length - 1
                ? user.language_preference === "sw"
                  ? "Maliza"
                  : "Finish"
                : user.language_preference === "sw"
                  ? "Ifuatayo"
                  : "Next"}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
