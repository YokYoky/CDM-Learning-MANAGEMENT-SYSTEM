from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=255, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(label='Password', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
