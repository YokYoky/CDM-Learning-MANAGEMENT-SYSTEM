from django.db import models
from courses.models import Course
from django.contrib.auth.models import AbstractUser
from courses.models import Program

# Create your models here.
BACHLOAR_DEGREE = "Bachloar"


LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BACHLOAR_DEGREE, "Bachloar Degree"),
)

class UserProfile(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    studentId = models.IntegerField()
    section = models.CharField(max_length=10)
    coursesEnrolled = models.ManyToManyField(Course)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    program = models.OneToOneField(Program, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.user.username

class Professor(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    professorId = models.IntegerField()
    coursesTaught = models.ManyToManyField(Course, related_name='professors')

    def __str__(self):
        return self.user.username
        