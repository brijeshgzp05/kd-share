from django.db import models
from accounts.models import Profile

# Create your models here.
class Status(models.Model):
	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True)
	content = models.CharField(max_length=200, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
	created_by_name = models.CharField(max_length=50, null=True, blank=True)

	class Meta:
		ordering=['timestamp']