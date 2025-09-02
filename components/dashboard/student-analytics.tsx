"use client"

import { useState, useEffect } from "react"
import type { User } from "@/lib/database"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Search, TrendingUp, TrendingDown, Users, Clock } from "lucide-react"

interface StudentAnalyticsProps {
  user: User
}

interface StudentData {
  id: number
  name: string
  email: string
  lessons_completed: number
  quiz_average: number
  study_time: number
  last_active: string
  progress: number
}

export function StudentAnalytics({ user }: StudentAnalyticsProps) {
  const [students, setStudents] = useState<StudentData[]>([])
  const [filteredStudents, setFilteredStudents] = useState<StudentData[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [sortBy, setSortBy] = useState("name")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Mock data - in real app, this would come from API
    const mockStudents: StudentData[] = [
      {
        id: 1,
        name: "John Doe",
        email: "john@example.com",
        lessons_completed: 12,
        quiz_average: 85,
        study_time: 240,
        last_active: "2024-01-15",
        progress: 75,
      },
      {
        id: 2,
        name: "Jane Smith",
        email: "jane@example.com",
        lessons_completed: 8,
        quiz_average: 92,
        study_time: 180,
        last_active: "2024-01-14",
        progress: 60,
      },
      {
        id: 3,
        name: "Mike Johnson",
        email: "mike@example.com",
        lessons_completed: 15,
        quiz_average: 78,
        study_time: 320,
        last_active: "2024-01-16",
        progress: 90,
      },
      {
        id: 4,
        name: "Sarah Wilson",
        email: "sarah@example.com",
        lessons_completed: 6,
        quiz_average: 88,
        study_time: 150,
        last_active: "2024-01-13",
        progress: 45,
      },
    ]

    setStudents(mockStudents)
    setFilteredStudents(mockStudents)
    setLoading(false)
  }, [])

  useEffect(() => {
    const filtered = students.filter(
      (student) =>
        student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        student.email.toLowerCase().includes(searchTerm.toLowerCase()),
    )

    // Sort students
    filtered.sort((a, b) => {
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name)
        case "progress":
          return b.progress - a.progress
        case "quiz_average":
          return b.quiz_average - a.quiz_average
        case "study_time":
          return b.study_time - a.study_time
        default:
          return 0
      }
    })

    setFilteredStudents(filtered)
  }, [students, searchTerm, sortBy])

  const getPerformanceTrend = (score: number) => {
    if (score >= 80) return { icon: TrendingUp, color: "text-green-600", label: "Excellent" }
    if (score >= 60) return { icon: TrendingUp, color: "text-blue-600", label: "Good" }
    return { icon: TrendingDown, color: "text-red-600", label: "Needs Help" }
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
        <p className="text-muted-foreground">Loading student data...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold">
          {user.language_preference === "sw" ? "Takwimu za Wanafunzi" : "Student Analytics"}
        </h2>
        <p className="text-muted-foreground">
          {user.language_preference === "sw"
            ? "Fuatilia maendeleo ya wanafunzi wako"
            : "Track your students' progress and performance"}
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Jumla ya Wanafunzi" : "Total Students"}
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{students.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Wastani wa Alama" : "Average Score"}
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(students.reduce((acc, s) => acc + s.quiz_average, 0) / students.length)}%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Wastani wa Muda" : "Average Study Time"}
            </CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Math.round(students.reduce((acc, s) => acc + s.study_time, 0) / students.length / 60)}h
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {user.language_preference === "sw" ? "Wanashiriki" : "Active Students"}
            </CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {students.filter((s) => new Date(s.last_active) > new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)).length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Orodha ya Wanafunzi" : "Student List"}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder={user.language_preference === "sw" ? "Tafuta mwanafunzi..." : "Search students..."}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="name">{user.language_preference === "sw" ? "Jina" : "Name"}</SelectItem>
                <SelectItem value="progress">{user.language_preference === "sw" ? "Maendeleo" : "Progress"}</SelectItem>
                <SelectItem value="quiz_average">
                  {user.language_preference === "sw" ? "Wastani wa Alama" : "Quiz Average"}
                </SelectItem>
                <SelectItem value="study_time">
                  {user.language_preference === "sw" ? "Muda wa Kusoma" : "Study Time"}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Students List */}
          <div className="space-y-4">
            {filteredStudents.map((student) => {
              const trend = getPerformanceTrend(student.quiz_average)
              const TrendIcon = trend.icon

              return (
                <div
                  key={student.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                      <span className="font-medium text-primary">
                        {student.name
                          .split(" ")
                          .map((n) => n[0])
                          .join("")}
                      </span>
                    </div>
                    <div>
                      <h3 className="font-medium">{student.name}</h3>
                      <p className="text-sm text-muted-foreground">{student.email}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-6">
                    <div className="text-center">
                      <p className="text-sm font-medium">{student.lessons_completed}</p>
                      <p className="text-xs text-muted-foreground">
                        {user.language_preference === "sw" ? "Masomo" : "Lessons"}
                      </p>
                    </div>

                    <div className="text-center">
                      <div className="flex items-center gap-1">
                        <TrendIcon className={`h-4 w-4 ${trend.color}`} />
                        <span className="text-sm font-medium">{student.quiz_average}%</span>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        {user.language_preference === "sw" ? "Wastani" : "Average"}
                      </p>
                    </div>

                    <div className="text-center">
                      <p className="text-sm font-medium">{Math.round(student.study_time / 60)}h</p>
                      <p className="text-xs text-muted-foreground">
                        {user.language_preference === "sw" ? "Muda" : "Time"}
                      </p>
                    </div>

                    <div className="w-24">
                      <div className="flex justify-between text-xs mb-1">
                        <span>{user.language_preference === "sw" ? "Maendeleo" : "Progress"}</span>
                        <span>{student.progress}%</span>
                      </div>
                      <Progress value={student.progress} className="h-2" />
                    </div>

                    <Badge
                      variant={
                        new Date(student.last_active) > new Date(Date.now() - 24 * 60 * 60 * 1000)
                          ? "default"
                          : "secondary"
                      }
                    >
                      {new Date(student.last_active) > new Date(Date.now() - 24 * 60 * 60 * 1000)
                        ? user.language_preference === "sw"
                          ? "Anashiriki"
                          : "Active"
                        : user.language_preference === "sw"
                          ? "Haashiriki"
                          : "Inactive"}
                    </Badge>
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
