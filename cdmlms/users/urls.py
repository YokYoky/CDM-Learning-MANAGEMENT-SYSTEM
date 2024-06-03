from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from courses.views import course_assignments, create_assignment, update_assignment, delete_assignment, download_file, submit_assignment, view_submission_file, download_submission_file

app_name = 'users'

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('dologin/', views.dologin, name='dologin'),
    path('logout/', views.logout_view, name='logout'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor_dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('courses/', views.courses, name='courses'),
    path('profile/', views.profile_view, name='profile'),

    path('user-list/', views.user_list, name='user_list'),
    path('courses/<int:course_id>/', views.selected_course, name='selected_course'),

    path('course/<int:course_id>/', views.selected_course, name='selected_course'),
    path('course/<int:course_id>/assignments/', course_assignments, name='course_assignments'),
    path('course/<int:course_id>/create_assignment/', create_assignment, name='create_assignment'),
    path('course/<int:course_id>/delete_assignment/<int:assignment_id>/', delete_assignment, name='delete_assignment'),

    path('<int:assignment_id>/download/', download_file, name='download_file'),
    path('course/<int:assignment_id>/submit/', submit_assignment, name='submit_assignment'),
    path('view_submission_file/<int:assignment_id>/', view_submission_file, name='view_submission_file'),
    path('download_submission_file/<int:submission_id>/', download_submission_file, name='download_submission_file'),
    path('assignment/update/<int:assignment_id>/', update_assignment, name='update_assignment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)