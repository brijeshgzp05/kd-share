from django.contrib import admin

# Register your models here.
from .models import Profile

class AdminProfile(admin.ModelAdmin):
	list_display = ['mobile', 'dob', 'gender', 'date_created']

admin.site.register(Profile,AdminProfile)