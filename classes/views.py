from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm
from django.http import HttpResponse



def no_access(request):
	return HttpResponse(" <h1>You have no access!</h1>")



def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classroom": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):

	classroom = Classroom.objects.get(id=classroom_id)
	students = classroom.students.all()
	context = {
		"classroom": classroom,
		"students": students,
	}
	return render(request, 'classroom_detail.html', context)




def classroom_create(request):

	if request.user.is_anonymous:
		return redirect("signin")

	form = ClassroomForm()

	if request.method == "POST":
		form = ClassroomForm(request.POST)
		if form.is_valid():
			classroom = form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()
			return redirect('classroom-list')
			form.save()

			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def student_create(request, classroom_id):

	classroom = Classroom.objects.get(id=classroom_id)

	if not(request.user == classroom.teacher):
		messages.success(request, "you can't add")
		return redirect("classroom_list")

	form = StudentForm()
	
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			student = form.save(commit=False)
			student.classroom = classroom 
			student.save()
			messages.success(request, "Successfully created")

			return redirect('classroom-detail', classroom_id)
		print(form.errors)

	context = {
		"form":form,
		"classroom": classroom,
	}
	return render(request, 'student_create.html', context)

#--------------------------------------------

def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)

	if not(request.user == classroom.teacher):
		messages.success(request, "you can't add")
		return redirect("classroom-list")

	form = ClassroomForm(instance=classroom)


	if request.method == "POST":
		form = ClassroomForm(request.POST, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)

	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def student_update(request, student_id):

	if request.user.is_anonymous:
		return redirect('signin')

	student = Student.objects.get(id=student_id)
	if not (request.user == student.classroom.teacher):
		messages.warning(request, "cannot")
		return redirect('classroom-list')

	form = StudentForm(instance=student)

	if request.method == "POST":
		form = StudentForm(request.POST, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			
			return redirect('classroom-detail', classroom_id=student.classroom.id)
		print (form.errors)
	context = {
	"form": form,
	"student": student,
	}
	return render(request, 'update_student.html', context)

#---------------------------------------------------

def classroom_delete(request, classroom_id):

	classroom = Classroom.objects.get(id=classroom_id)
	if not(request.user == classroom.teacher):
		messages.success(request, "you can't delete")
		return redirect("classroom_list")

	classroom.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def student_delete(request, classroom_id, student_id):
	student = Student.objects.get(id=student_id)

	if not (request.user == student.classroom.teacher):
		HttpResponse(" <h1>no</h1>")
		return redirect("classroom_list")
	
	class_id = student.classroom.id

	student.delete()
	messages.success(request, "Successfully Deleted!")

	return redirect('classroom-detail', classroom_id = class_id)

#----------------------------------------------------------

def signup(request):

	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)

		if form.is_valid():
			user = form.save(commit=False)

			user.set_password(user.password)
			user.save()

			login(request, user)
			messages.success(request, "signed in!")
			return redirect("classroom-list")
		
	context = {
		"form":form,
	}

	return render(request, 'signup.html', context)


def signin(request):

	form = SigninForm() 
	if request.method == 'POST':
		form = SigninForm(request.POST)

		if form.is_valid(): 

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			auth_user = authenticate(username=username, password=password)
		   
			if auth_user is not None:
				login(request, auth_user)

				messages.success(request, "Successfully signed in!")
				return redirect('classroom-list')

			messages.warning(request, "incorrect!") 
		

	context = {
		"form":form
	}
	return render(request, 'signin.html', context) 

def signout(request):
	logout(request)
	return redirect("signin")


