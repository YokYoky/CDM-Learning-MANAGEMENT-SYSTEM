from django.contrib import admin
from .models import Assignment, Submission, Group

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Group)