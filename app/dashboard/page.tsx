import { redirect } from "next/navigation"
import { requirePaidAccess } from "@/lib/auth"
import { getUserById, getAllSubjects } from "@/lib/database"
import { StudentDashboard } from "@/components/dashboard/student-dashboard"
import { TeacherDashboard } from "@/components/dashboard/teacher-dashboard"

export default async function DashboardPage() {
  try {
    const session = await requirePaidAccess()
    const user = getUserById(session.userId)

    if (!user) {
      redirect("/login")
    }

    const subjects = getAllSubjects()

    return user.role === "student" ? (
      <StudentDashboard user={user} subjects={subjects} />
    ) : (
      <TeacherDashboard user={user} subjects={subjects} />
    )
  } catch (error) {
    redirect("/login")
  }
}
