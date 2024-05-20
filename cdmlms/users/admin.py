from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Student, Professor

# Register your models here.
class UserProfileAdmin(UserAdmin):
    list_display = ['username', 'user_type', 'email', 'gender', 'address', 'phoneNumber']
    search_fields = ['username', 'user_type', 'email', 'gender', 'address', 'phoneNumber']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'studentId', 'program', 'section', 'display_courses_enrolled', 'level']
    list_filter = ['section', 'level']
    search_fields = ['user__username', 'studentId']

    def display_courses_enrolled(self, obj):
        return ", ".join([course.courseName for course in obj.coursesEnrolled.all()])
    display_courses_enrolled.short_description = 'Courses Enrolled'


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['user', 'professorId', 'display_courses_taught']
    list_filter = ['coursesTaught']
    search_fields = ['user__username', 'professorId']

    def display_courses_taught(self, obj):
        return ", ".join([course.courseName for course in obj.coursesTaught.all()])
    display_courses_taught.short_description = 'Courses Taught'

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfessorAdmin)