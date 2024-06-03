from django.db import models
from django.utils import timezone

class Course(models.Model):
    courseName = models.CharField(max_length=200)
    courseCode = models.CharField(max_length=10)
    courseDescription = models.TextField()
    units = models.IntegerField()
    instructor = models.ForeignKey("users.Professor", on_delete=models.CASCADE, null=True, blank=True)
    #students = models.ManyToManyField("users.Student", blank=True)

    def __str__(self):
        return self.courseName

class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_students = models.ManyToManyField('users.Student', blank=True, related_name='assigned_assignments')

    def __str__(self):
        return self.title


    
def submission_upload_to(instance, filename):
    assignment_title = instance.assignment.title
    return f'submissions/{assignment_title}/{filename}'

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='assignment_submissions')
    file = models.FileField(upload_to=submission_upload_to)
    grade = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.assignment.title}'
    