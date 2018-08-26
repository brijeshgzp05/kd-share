from __future__ import unicode_literals
from django.db import models
from accounts.models import Profile

class Friend(models.Model):

	profile = models.ForeignKey(Profile, on_delete = models.CASCADE, null=True)
	fid = models.IntegerField(null=True)
	name  = models.CharField(max_length=20, null=True)
	username = models.CharField(max_length=30, null=True)
	timestamp = models.DateField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.name

class RequestCall(models.Model):
	coming_from = models.CharField(max_length=30)
	coming_from_profile_id = models.CharField(max_length=10, null=True)
	coming_for = models.CharField(max_length=30)
	coming_for_profile_id = models.CharField(max_length=10, null=True)
	coming_from_name = models.CharField(max_length=50, null=True)
	coming_for_name = models.CharField(max_length=50, null=True)
