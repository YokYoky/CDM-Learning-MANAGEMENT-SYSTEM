from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, JsonResponse
from .EmailBackend import EmailBackend
from django.contrib.auth import get_backends
from .models import UserProfile, Student, Course, Professor
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def profile_view(request):
    user = request.user
    if user.user_type == "2":  # Student
        student = Student.objects.get(user=user)
        courses = student.coursesEnrolled.all()
        context = {
            'user': user,
            'user_name': f"{user.first_name} {user.last_name}",
            'courses_enrolled': courses,
        }
    elif user.user_type == "1":  # Professor
        professor = Professor.objects.get(user=user)
        courses = professor.coursesTaught.all()
        context = {
            'user': user,
            'user_name': f"{user.first_name} {user.last_name}",
            'courses_taught': courses,
        }
    else:
        context = {
            'user': user,
            'user_name': f"{user.first_name} {user.last_name}",
        }

    return render(request, 'core/profile.html', context)

@login_required
def base_view(request):
    user_name = request.user.get_full_name() or request.user.username
    context = {'user_name': user_name}
    return render(request, 'base.html', context)

def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect(reverse("users:instructor_dashboard"))
        elif request.user.user_type == '2':
            return redirect(reverse("users:student_dashboard"))
        else:
            return redirect(reverse("users:student_dashboard"))
    return render(request, 'authentication/login.html')


def dologin(request, **kwargs):      
    if request.method != 'POST':
        return HttpResponse("<h4>Denied</h4>")
    else:
        user = EmailBackend.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            for backend in get_backends():
                if isinstance(backend, EmailBackend):
                    user.backend = backend.__module__ + '.' + backend.__class__.__name__
                    break
            login(request, user)
            if user.user_type == '1':
                return redirect(reverse("users:instructor_dashboard"))
            elif user.user_type == '2':
                return redirect(reverse("users:student_dashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("/")
        
def logout_view(request):
    logout(request)
    return redirect('users:login_page')

def student_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('users:login_page')

    # Get the currently logged-in student
    student = Student.objects.get(user=request.user)

    # Get the total number of courses enrolled by the student
    total_subject = student.coursesEnrolled.count()
    
    # Get the courses enrolled by the student
    courses_enrolled = student.coursesEnrolled.all()

    user_name = f"{request.user.first_name} {request.user.last_name}"
    context = {
        'total_subject': total_subject,
        'user_name': user_name, # Pass the user's full name to the template
        'courses_enrolled': courses_enrolled,
    }

    return render(request, 'core/student_dashboard.html', context)  # Pass the context to the template
    
def instructor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('users:login_page')

    # Get the currently logged-in instructor
    instructor = Professor.objects.get(user=request.user)

    # Get the courses taught by the instructor
    courses_taught = instructor.coursesTaught.count()

    courses_list = instructor.coursesTaught.all()


    user_name = f"{request.user.first_name} {request.user.last_name}"
    context = {
        'courses_taught': courses_taught,
        'user_name': user_name,  # Pass the user's full name to the template
        'courses_list': courses_list,
    }

    return render(request, 'core/instructor_dashboard.html', context)  # Pass the context to the template


def courses(request):
    if request.user.is_authenticated:
        if request.user.user_type == "2":  # Student
            student = Student.objects.get(user=request.user)
            courses = student.coursesEnrolled.all()
        elif request.user.user_type == "1":  # Professor
            professor = Professor.objects.get(user=request.user)
            courses = professor.coursesTaught.all()
        else:
            courses = Course.objects.all()
    else:
        return redirect('users:login_page')
    user_name = f"{request.user.first_name} {request.user.last_name}"
    context = {
        'courses': courses,
        'user_name': user_name,
    }
    return render(request, 'core/courses.html', context)

@login_required
def selected_course(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return HttpResponse("Course not found.")
    return render(request, 'courses/selected_course.html', {'course': course})

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