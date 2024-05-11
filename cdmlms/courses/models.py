from django.db import models


class Course(models.Model):
    courseName = models.CharField(max_length=200)
    courseCode = models.CharField(max_length=10)
    courseDescription = models.TextField()
    units = models.IntegerField()

    def __str__(self):
        return self.courseName

class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title