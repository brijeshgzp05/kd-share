from __future__ import unicode_literals
from django.db import models
from accounts.models import Profile

class Message(models.Model):
	msg = models.CharField(max_length=70, default="")	
	sender_profile_id = models.IntegerField(null=True)
	sender_name = models.CharField(max_length=60)
	reciever_profile_id = models.IntegerField(null= True)
	seen_status = models.BooleanField(default=False)
	send_time = models.DateTimeField(auto_now=True, auto_now_add=False)



	def __str__(self):
		return self.sender_name

	def __unicode__(self):
		return self.sender_name

	class Meta:
		ordering = ['-send_time']

