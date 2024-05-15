from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login/', views.login, name='login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('user-list/', views.user_list, name='user_list'),

]