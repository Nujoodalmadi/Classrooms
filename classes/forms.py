from django import forms
from .models import Classroom, Student
from django.contrib.auth.models import User


class ClassroomForm(forms.ModelForm):
	class Meta:
		model = Classroom
		exclude = ['teacher',]


class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email' ,'password']

		widgets={
		'password': forms.PasswordInput(),
		}


class SigninForm(forms.Form): #form
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())

	# forms.PasswordInput(): Widget for password field (e.g., displays **** as a user types text)


class StudentForm(forms.ModelForm):

	class Meta:
		model = Student
		widgets = {
		'date_of_birth': forms.DateInput(attrs={'type': 'date'}) ,
		}
		exclude = ['classroom',]
		
