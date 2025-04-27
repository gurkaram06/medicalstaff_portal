from django import forms
from django.contrib.auth.models import User
from .models import Notice

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description']
