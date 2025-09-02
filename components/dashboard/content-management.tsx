"use client"

import type React from "react"

import { useState, useEffect } from "react"
import type { User, Subject, Lesson } from "@/lib/database"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Upload, FileText, Edit, Trash2, Download, Plus } from "lucide-react"

interface ContentManagementProps {
  user: User
  subjects: Subject[]
}

export function ContentManagement({ user, subjects }: ContentManagementProps) {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [loading, setLoading] = useState(true)
  const [uploadMode, setUploadMode] = useState(false)
  const [editingLesson, setEditingLesson] = useState<Lesson | null>(null)

  useEffect(() => {
    fetchLessons()
  }, [])

  const fetchLessons = async () => {
    try {
      const response = await fetch("/api/teacher/lessons")
      const data = await response.json()
      setLessons(data.lessons || [])
    } catch (error) {
      console.error("Failed to fetch lessons:", error)
    } finally {
      setLoading(false)
    }
  }

  if (uploadMode) {
    return <CSVUploader user={user} subjects={subjects} onBack={() => setUploadMode(false)} onSuccess={fetchLessons} />
  }

  if (editingLesson) {
    return (
      <LessonEditor
        lesson={editingLesson}
        user={user}
        subjects={subjects}
        onBack={() => setEditingLesson(null)}
        onSuccess={fetchLessons}
      />
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">
            {user.language_preference === "sw" ? "Usimamizi wa Maudhui" : "Content Management"}
          </h2>
          <p className="text-muted-foreground">
            {user.language_preference === "sw" ? "Ongeza na usimamie masomo yako" : "Create and manage your lessons"}
          </p>
        </div>
        <Button onClick={() => setUploadMode(true)}>
          <Upload className="h-4 w-4 mr-2" />
          {user.language_preference === "sw" ? "Pakia CSV" : "Upload CSV"}
        </Button>
      </div>

      {/* Upload Instructions */}
      <Card className="bg-primary/5 border-primary/20">
        <CardHeader>
          <CardTitle className="text-primary">
            {user.language_preference === "sw" ? "Jinsi ya Kupakia Maudhui" : "How to Upload Content"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="text-sm">
            {user.language_preference === "sw"
              ? "1. Tengeneza faili ya CSV na safu za: 'question', 'answer', 'difficulty'"
              : "1. Create a CSV file with columns: 'question', 'answer', 'difficulty'"}
          </p>
          <p className="text-sm">
            {user.language_preference === "sw"
              ? "2. Ongeza safu za 'question_sw', 'answer_sw' kwa tafsiri za Kiswahili"
              : "2. Add 'question_sw', 'answer_sw' columns for Kiswahili translations"}
          </p>
          <p className="text-sm">
            {user.language_preference === "sw"
              ? "3. Chagua somo na darasa kabla ya kupakia"
              : "3. Select subject and grade level before uploading"}
          </p>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            {user.language_preference === "sw" ? "Pakua Mfano" : "Download Template"}
          </Button>
        </CardContent>
      </Card>

      {/* Lessons List */}
      <Card>
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Masomo Yako" : "Your Lessons"}</CardTitle>
          <CardDescription>
            {lessons.length} {user.language_preference === "sw" ? "masomo yaliyotengenezwa" : "lessons created"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Loading lessons...</p>
            </div>
          ) : lessons.length === 0 ? (
            <div className="text-center py-8">
              <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">
                {user.language_preference === "sw" ? "Hakuna Masomo" : "No Lessons Yet"}
              </h3>
              <p className="text-muted-foreground mb-4">
                {user.language_preference === "sw"
                  ? "Anza kwa kupakia faili ya CSV ya kwanza"
                  : "Get started by uploading your first CSV file"}
              </p>
              <Button onClick={() => setUploadMode(true)}>
                <Plus className="h-4 w-4 mr-2" />
                {user.language_preference === "sw" ? "Ongeza Somo" : "Create Lesson"}
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {lessons.map((lesson) => (
                <div
                  key={lesson.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <Badge variant="outline">
                        {subjects.find((s) => s.id === lesson.subject_id)?.name || "Unknown"}
                      </Badge>
                      <Badge variant="secondary">
                        {user.language_preference === "sw" ? "Darasa" : "Grade"} {lesson.grade_level}
                      </Badge>
                    </div>
                    <h3 className="font-medium">
                      {user.language_preference === "sw" && lesson.title_sw ? lesson.title_sw : lesson.title}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      {user.language_preference === "sw" ? "Imetengenezwa" : "Created"}:{" "}
                      {new Date(lesson.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" onClick={() => setEditingLesson(lesson)}>
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

interface CSVUploaderProps {
  user: User
  subjects: Subject[]
  onBack: () => void
  onSuccess: () => void
}

function CSVUploader({ user, subjects, onBack, onSuccess }: CSVUploaderProps) {
  const [formData, setFormData] = useState({
    title: "",
    title_sw: "",
    subject_id: "",
    grade_level: "",
    file: null as File | null,
  })
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState("")

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file && file.type === "text/csv") {
      setFormData({ ...formData, file })
      setError("")
    } else {
      setError("Please select a valid CSV file")
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!formData.file || !formData.title || !formData.subject_id || !formData.grade_level) {
      setError("Please fill in all required fields")
      return
    }

    setUploading(true)
    setError("")

    try {
      const uploadFormData = new FormData()
      uploadFormData.append("file", formData.file)
      uploadFormData.append("title", formData.title)
      uploadFormData.append("title_sw", formData.title_sw)
      uploadFormData.append("subject_id", formData.subject_id)
      uploadFormData.append("grade_level", formData.grade_level)

      const response = await fetch("/api/teacher/upload-csv", {
        method: "POST",
        body: uploadFormData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Upload failed")
      }

      onSuccess()
      onBack()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed")
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={onBack}>
          ← {user.language_preference === "sw" ? "Rudi" : "Back"}
        </Button>
        <h2 className="text-2xl font-bold">
          {user.language_preference === "sw" ? "Pakia Faili ya CSV" : "Upload CSV File"}
        </h2>
      </div>

      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Maelezo ya Somo" : "Lesson Details"}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="title">
                  {user.language_preference === "sw" ? "Jina la Somo (Kiingereza)" : "Lesson Title (English)"}
                </Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="title_sw">
                  {user.language_preference === "sw" ? "Jina la Somo (Kiswahili)" : "Lesson Title (Kiswahili)"}
                </Label>
                <Input
                  id="title_sw"
                  value={formData.title_sw}
                  onChange={(e) => setFormData({ ...formData, title_sw: e.target.value })}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="subject">{user.language_preference === "sw" ? "Somo" : "Subject"}</Label>
                <Select
                  value={formData.subject_id}
                  onValueChange={(value) => setFormData({ ...formData, subject_id: value })}
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
                  value={formData.grade_level}
                  onValueChange={(value) => setFormData({ ...formData, grade_level: value })}
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

            <div className="space-y-2">
              <Label htmlFor="file">{user.language_preference === "sw" ? "Faili ya CSV" : "CSV File"}</Label>
              <Input id="file" type="file" accept=".csv" onChange={handleFileChange} required />
            </div>

            <Button type="submit" disabled={uploading} className="w-full">
              {uploading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  {user.language_preference === "sw" ? "Inapakia..." : "Uploading..."}
                </>
              ) : (
                <>
                  <Upload className="h-4 w-4 mr-2" />
                  {user.language_preference === "sw" ? "Pakia Somo" : "Upload Lesson"}
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}

interface LessonEditorProps {
  lesson: Lesson
  user: User
  subjects: Subject[]
  onBack: () => void
  onSuccess: () => void
}

function LessonEditor({ lesson, user, subjects, onBack, onSuccess }: LessonEditorProps) {
  const [formData, setFormData] = useState({
    title: lesson.title,
    title_sw: lesson.title_sw || "",
    subject_id: lesson.subject_id.toString(),
    grade_level: lesson.grade_level.toString(),
  })
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)
    setError("")

    try {
      const response = await fetch(`/api/teacher/lessons/${lesson.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || "Update failed")
      }

      onSuccess()
      onBack()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Update failed")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={onBack}>
          ← {user.language_preference === "sw" ? "Rudi" : "Back"}
        </Button>
        <h2 className="text-2xl font-bold">{user.language_preference === "sw" ? "Hariri Somo" : "Edit Lesson"}</h2>
      </div>

      <Card className="max-w-2xl">
        <CardHeader>
          <CardTitle>{user.language_preference === "sw" ? "Maelezo ya Somo" : "Lesson Details"}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="title">
                  {user.language_preference === "sw" ? "Jina la Somo (Kiingereza)" : "Lesson Title (English)"}
                </Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="title_sw">
                  {user.language_preference === "sw" ? "Jina la Somo (Kiswahili)" : "Lesson Title (Kiswahili)"}
                </Label>
                <Input
                  id="title_sw"
                  value={formData.title_sw}
                  onChange={(e) => setFormData({ ...formData, title_sw: e.target.value })}
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="subject">{user.language_preference === "sw" ? "Somo" : "Subject"}</Label>
                <Select
                  value={formData.subject_id}
                  onValueChange={(value) => setFormData({ ...formData, subject_id: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
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
                  value={formData.grade_level}
                  onValueChange={(value) => setFormData({ ...formData, grade_level: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
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

            <Button type="submit" disabled={saving} className="w-full">
              {saving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  {user.language_preference === "sw" ? "Inahifadhi..." : "Saving..."}
                </>
              ) : user.language_preference === "sw" ? (
                "Hifadhi Mabadiliko"
              ) : (
                "Save Changes"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
