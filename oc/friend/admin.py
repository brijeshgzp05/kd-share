from django.contrib import admin


from .models import Friend, RequestCall

class AdminFriend(admin.ModelAdmin):
	list_display = ['name', 'timestamp', 'username']


class AdminRequestCall(admin.ModelAdmin):
	list_display = ['coming_from', 'coming_for']

admin.site.register(Friend, AdminFriend)
admin.site.register(RequestCall, AdminRequestCall)