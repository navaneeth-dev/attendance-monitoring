from django import forms
from .models import Student

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Student
        fields = ['registerNo', 'studName', 'password']

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data['password'])
        if commit:
            student.save()
        return student

class LoginForm(forms.Form):
    registerNo = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
