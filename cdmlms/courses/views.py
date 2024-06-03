from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Course, Assignment, Submission
from users.models import Student, Professor
from .forms import AssignmentForm, SubmissionForm, GradeSubmissionForm, CommentForm
from django.http import FileResponse
from django.core.files import File
from django.conf import settings

@login_required
def course_assignments(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.user_type == "2":  # Student
        student = Student.objects.get(user=request.user)
        assignments = Assignment.objects.filter(course=course, assigned_students=student).order_by('-created_at')
        courses = student.coursesEnrolled.all()
    elif request.user.user_type == "1":  # Professor
        assignments = Assignment.objects.filter(course=course).order_by('-created_at')
        professor = Professor.objects.get(user=request.user)
        courses = professor.coursesTaught.all()
    else:
        assignments = Assignment.objects.filter(course=course).order_by('-created_at')
        courses = Course.objects.all()

    user_name = f"{request.user.first_name} {request.user.last_name}"
    context = {
        'course': course,
        'assignments': assignments,
        'user_name': user_name,
        'courses': courses,
    }

    return render(request, 'courses/course_assignments.html', context)


@login_required
def create_assignment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    professor = Professor.objects.get(user=request.user)
    courses = professor.coursesTaught.all()
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.save()

            if form.cleaned_data['all_students']:
                assignment.assigned_students.set(Student.objects.all())
            else:
                assignment.assigned_students.set(form.cleaned_data['students'])

            messages.success(request, 'Assignment created successfully.')
            return redirect(reverse('users:course_assignments', args=[course_id]))
    else:
        form = AssignmentForm()
    user_name = f"{request.user.first_name} {request.user.last_name}"
    return render(request, 'courses/create_assignments.html', {'form': form, 'course_id': course_id, 'user_name': user_name, 'courses': courses})


@login_required
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user.student
            submission.save()
            messages.success(request, 'Assignment submitted successfully.')
            return redirect(reverse('users:course_assignments', args=[assignment.course.id]))
    else:
        form = SubmissionForm()
    return render(request, 'courses/submit_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    course_id = assignment.course.id
    professor = Professor.objects.get(user=request.user)
    courses = professor.coursesTaught.all()
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course_id = course_id
            assignment.save()

            if form.cleaned_data['all_students']:
                assignment.assigned_students.set(Student.objects.all())
            else:
                assignment.assigned_students.set(form.cleaned_data['students'])

            messages.success(request, 'Assignment updated successfully.')
            return redirect(reverse('users:course_assignments', args=[course_id]))
    else:
        form = AssignmentForm(instance=assignment)
    user_name = f"{request.user.first_name} {request.user.last_name}"
    return render(request, 'courses/update_assignments.html', {'form': form, 'assignment_id': assignment_id, 'user_name': user_name, 'courses': courses})


@login_required
def delete_assignment(request, course_id, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully.')
        return redirect(reverse('users:course_assignments', args=[course_id]))
    return JsonResponse({'assignment_title': assignment.title})

def download_file(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    file_path = assignment.file.path
    file = File(open(file_path, 'rb'))
    response = FileResponse(file)
    response['Content-Type'] = 'application/msword'
    response['Content-Disposition'] = f'attachment; filename={assignment.file.name}'
    return response

def view_submission_file(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.user.user_type == "1":  # Professor
        submissions = Submission.objects.filter(assignment=assignment)
        professor = Professor.objects.get(user=request.user)
        courses = professor.coursesTaught.all()
    elif request.user.user_type == "2":  # Student
        submissions = Submission.objects.filter(assignment=assignment, student=request.user.student)
        student = Student.objects.get(user=request.user)
        courses = student.coursesEnrolled.all()
    user_name = f"{request.user.first_name} {request.user.last_name}"
    context = {
        'submissions': submissions,
        'courses': courses,
        'user_name': user_name,
    }

    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST)
        comment_form = CommentForm(request.POST)
        if form.is_valid() and comment_form.is_valid():
            submission_id = request.POST.get('submission_id')
            submission = Submission.objects.get(id=submission_id)
            submission.grade = form.cleaned_data['grade']
            submission.comment = comment_form.cleaned_data['comment']
            submission.save()
            messages.success(request, 'Grade and comment updated successfully.')
            return redirect(reverse('users:view_submission_file', args=[assignment_id]))
    else:
        form = GradeSubmissionForm()
        comment_form = CommentForm()

    context['form'] = form
    context['comment_form'] = comment_form
    return render(request, 'courses/view_submission_file.html', context)

def download_submission_file(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    file_path = submission.file.path
    file = File(open(file_path, 'rb'))
    response = FileResponse(file)
    response['Content-Type'] = 'application/msword'
    response['Content-Disposition'] = f'attachment; filename={submission.file.name}'
    return response

