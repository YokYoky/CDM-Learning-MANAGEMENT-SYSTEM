from django import forms
from .models import Assignment, Submission
from users.models import Student

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('file',)

class GradeSubmissionForm(forms.Form):
    grade = forms.DecimalField(max_digits=3, decimal_places=2)

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class AssignmentForm(forms.ModelForm):
    all_students = forms.BooleanField(required=False, label='Assign to all students')
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=False, widget=forms.CheckboxSelectMultiple, label='Select Students')

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'all_students', 'students']
