"use client"

import { useState } from "react"
import type { User, Subject } from "@/lib/database"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
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
import { BookOpen, Users, Upload, BarChart3, LogOut, Globe, Plus } from "lucide-react"
import { ContentManagement } from "./content-management"
import { StudentAnalytics } from "./student-analytics"
import { LessonCreator } from "./lesson-creator"

interface TeacherDashboardProps {
  user: User
  subjects: Subject[]
}

export function TeacherDashboard({ user, subjects }: TeacherDashboardProps) {
  const [activeTab, setActiveTab] = useState("overview")
  const [showLessonCreator, setShowLessonCreator] = useState(false)

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

  if (showLessonCreator) {
    return <LessonCreator user={user} subjects={subjects} onBack={() => setShowLessonCreator(false)} />
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
                {getGreeting()}, {user.language_preference === "sw" ? "Mwalimu" : "Teacher"} {user.first_name}!
              </p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Button onClick={() => setShowLessonCreator(true)}>
              <Plus className="h-4 w-4 mr-2" />
              {user.language_preference === "sw" ? "Ongeza Somo" : "Create Lesson"}
            </Button>
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
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="overview">{user.language_preference === "sw" ? "Muhtasari" : "Overview"}</TabsTrigger>
            <TabsTrigger value="content">{user.language_preference === "sw" ? "Maudhui" : "Content"}</TabsTrigger>
            <TabsTrigger value="students">{user.language_preference === "sw" ? "Wanafunzi" : "Students"}</TabsTrigger>
            <TabsTrigger value="analytics">{user.language_preference === "sw" ? "Takwimu" : "Analytics"}</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {user.language_preference === "sw" ? "Masomo Yaliyotengenezwa" : "Lessons Created"}
                  </CardTitle>
                  <BookOpen className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">24</div>
                  <p className="text-xs text-muted-foreground">
                    {user.language_preference === "sw" ? "+3 wiki hii" : "+3 this week"}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {user.language_preference === "sw" ? "Wanafunzi Wanashiriki" : "Active Students"}
                  </CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">156</div>
                  <p className="text-xs text-muted-foreground">
                    {user.language_preference === "sw" ? "+12 mwezi huu" : "+12 this month"}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {user.language_preference === "sw" ? "Wastani wa Alama" : "Average Score"}
                  </CardTitle>
                  <BarChart3 className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">78%</div>
                  <p className="text-xs text-muted-foreground">
                    {user.language_preference === "sw" ? "+5% kutoka wiki iliyopita" : "+5% from last week"}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    {user.language_preference === "sw" ? "Maudhui Yaliyopakiwa" : "Content Uploads"}
                  </CardTitle>
                  <Upload className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">8</div>
                  <p className="text-xs text-muted-foreground">
                    {user.language_preference === "sw" ? "Wiki hii" : "This week"}
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
                  {
                    action: "Created lesson",
                    subject: "Mathematics",
                    title: "Advanced Fractions",
                    time: "2 hours ago",
                  },
                  { action: "Updated content", subject: "Science", title: "Plant Biology", time: "1 day ago" },
                  { action: "Reviewed quiz", subject: "English", title: "Reading Comprehension", time: "2 days ago" },
                ].map((activity, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                    <div>
                      <p className="font-medium">{activity.title}</p>
                      <p className="text-sm text-muted-foreground">
                        {activity.action} • {activity.subject}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-muted-foreground">{activity.time}</p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>

            {/* Subject Overview */}
            <Card>
              <CardHeader>
                <CardTitle>{user.language_preference === "sw" ? "Muhtasari wa Masomo" : "Subject Overview"}</CardTitle>
                <CardDescription>
                  {user.language_preference === "sw"
                    ? "Masomo yako katika kila somo"
                    : "Your lessons across all subjects"}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-2 gap-4">
                  {subjects.map((subject) => (
                    <div key={subject.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center gap-3">
                        <div className="text-2xl">
                          {subject.name === "Mathematics"
                            ? "📊"
                            : subject.name === "English"
                              ? "📚"
                              : subject.name === "Science"
                                ? "🔬"
                                : "🗣️"}
                        </div>
                        <div>
                          <p className="font-medium">
                            {user.language_preference === "sw" && subject.name_sw ? subject.name_sw : subject.name}
                          </p>
                          <p className="text-sm text-muted-foreground">
                            {Math.floor(Math.random() * 10) + 1}{" "}
                            {user.language_preference === "sw" ? "masomo" : "lessons"}
                          </p>
                        </div>
                      </div>
                      <Badge variant="secondary">
                        {Math.floor(Math.random() * 50) + 20}{" "}
                        {user.language_preference === "sw" ? "wanafunzi" : "students"}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="content">
            <ContentManagement user={user} subjects={subjects} />
          </TabsContent>

          <TabsContent value="students">
            <StudentAnalytics user={user} />
          </TabsContent>

          <TabsContent value="analytics">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>
                    {user.language_preference === "sw" ? "Takwimu za Utendaji" : "Performance Analytics"}
                  </CardTitle>
                  <CardDescription>
                    {user.language_preference === "sw"
                      ? "Takwimu za kina za utendaji wa wanafunzi"
                      : "Detailed insights into student performance"}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">
                    {user.language_preference === "sw"
                      ? "Takwimu za kina zitaongezwa hapa."
                      : "Detailed analytics will be implemented here."}
                  </p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}
