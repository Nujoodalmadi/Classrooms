from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Classroom(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()
	teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	

	

	def get_absolute_url(self): # get a url that defines object instances
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})

		

class Student(models.Model):
	GENDER = (
		('m', 'Male'),
		('f', 'Female'),
	   )

	name = models.CharField(max_length=120)
	date_of_birth = models.DateField()
	gender= models.CharField(max_length=1, choices=GENDER)
	exam_grade= models.FloatField()
	classroom= models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name= 'students')

	
	class Meta:
		ordering = ['name', '-exam_grade'] # define behavior for a  model as a whole. leading “-” for decending order

		

