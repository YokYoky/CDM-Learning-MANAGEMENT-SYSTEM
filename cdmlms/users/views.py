from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from .EmailBackend import EmailBackend
from django.contrib.auth import login as auth_login
from .models import UserProfile


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("users:student_dashboard"))
        elif request.user.user_type == '2':
            return redirect(reverse("student_dashboard"))
        else:
            return redirect(reverse("student_home"))
    return render(request, 'authentication/login.html')


def login(request, **kwargs):      
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailBackend.authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            if user.user_type == '1':
                return redirect(reverse("users:student_dashboard"))
            elif user.user_type == '2':
                return redirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/login/")
    else:
        return render(request, 'authentication/login.html')


def student_dashboard(request):
    return render(request, 'core/student_dashboard.html')
    
def user_list(request):
    # Retrieve all UserProfile instances
    users = UserProfile.objects.all()

    # Create a string to accumulate user information
    user_info = "User Information:\n"
    for user in users:
        user_info += (
            f"Username: {user.username}\n"
            f"Email: {user.email}\n"
            f"User Type: {user.get_user_type_display()}\n"
            f"Gender: {user.get_gender_display()}\n"
            f"Address: {user.address}\n"
            f"Phone Number: {user.phoneNumber}\n\n"
        )

    return HttpResponse(user_info)