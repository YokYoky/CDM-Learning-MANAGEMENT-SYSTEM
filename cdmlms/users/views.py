from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from .EmailBackend import EmailBackend
from .models import UserProfile


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("users:student_dashboard"))
        elif request.user.user_type == '2':
            return redirect(reverse("student_dashboard"))
        else:
            return redirect(reverse("users:student_dashboard"))
    return render(request, 'authentication/login.html')


def dologin(request, **kwargs):      
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("users:student_dashboard"))
            elif user.user_type == '2':
                return redirect(reverse("users:student_dashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")
        
def logout_view(request):
    logout(request)
    return redirect('users:login_page')

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