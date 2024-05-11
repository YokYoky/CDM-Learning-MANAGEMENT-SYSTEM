from django.db import models
from courses.models import Course
from users.models import Student

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Student, related_name='assignments')
    dueDate = models.DateField()


    def __str__(self):
        return self.name

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submissionDate = models.DateField()
    file = models.FileField(upload_to='submissions/')
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.assignment.name} - {self.student.user.username}'

class Group(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Student)

    def __str__(self):
        return self.name
