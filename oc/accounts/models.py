from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	mobile = models.CharField(max_length=13)
	dob = models.DateField(auto_now=False, auto_now_add=False)
	gender = models.CharField(max_length=6)
	date_created = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
	

	def __str__(self):
		return self.mobile

	def __unicode__(self):
		return self.mobile

class ProfilePicture(models.Model):
	profile_id = models.IntegerField(null=True)
	dp = models.ImageField(upload_to="profile",null=True, blank=True)

class ForgotPassword(models.Model):
	email = models.EmailField(null=True, blank=True)
	g_num = models.CharField(max_length=40, null=True, blank=True)

	def __str__(self):
		return self.email 

	def __unicode__(self):
		return self.email



