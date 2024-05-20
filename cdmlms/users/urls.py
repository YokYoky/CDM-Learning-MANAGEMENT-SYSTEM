from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('dologin/', views.dologin, name='dologin'),
    path('logout/', views.logout_view, name='logout'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('user-list/', views.user_list, name='user_list'),
]