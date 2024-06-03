from django.db import models
from django.contrib.auth.hashers import make_password
from courses.models import Course
from django.contrib.auth.models import AbstractUser, UserManager
from courses.models import Program, Assignment

# Create your models here.
BACHELOR_DEGREE = "Bachelor"


LEVEL = (
    # (LEVEL_COURSE, "Level course"),
    (BACHELOR_DEGREE, "Bachelor Degree"),
)

class CustomUserManager(UserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class UserProfile(AbstractUser):
    USER_TYPE = (("1", "Instructor"), ("2", "Student"))
    GENDER = [("M", "Male"), ("F", "Female")]
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    user_type = models.CharField(default="1", choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=1, choices=GENDER, default="")
    address = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=255)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.username
    
class Student(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    studentId = models.IntegerField()
    section = models.CharField(max_length=10)
    coursesEnrolled = models.ManyToManyField(Course, related_name='enrolled_students')
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, default=None)
    #submitted_assignments = models.ManyToManyField(Assignment, related_name='submitted_by')

    def __str__(self):
        return self.user.username

class Professor(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    professorId = models.IntegerField()
    coursesTaught = models.ManyToManyField(Course, related_name='professors')

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.user.username
        