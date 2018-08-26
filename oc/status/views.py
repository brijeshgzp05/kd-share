from django.shortcuts import render
from django.views.generic import FormView
from .forms import PostForm
from django.http import JsonResponse
from .models import Status
from accounts.models import Profile

# Create your views here.

class StatusView(FormView):
	form_class = PostForm
	template_name  = 'home/home.html'
	success_url = 'form-success'
	def form_invalid(self, form):

		response = super(StatusView, self).form_invalid(form)
		
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):

		response = super(StatusView, self).form_valid(form)
		if self.request.is_ajax():
			status_pre = Status.objects.filter(profile_id=self.request.user.profile.id)
			status_pre.delete()

			content = form.cleaned_data.get('content')
			created_by_name = self.request.user.first_name + " " + self.request.user.last_name
			
			status = Status(profile_id=self.request.user.profile.id, content=content, created_by_name=created_by_name)
			status.save()
			
			data = {
				'message': "Posted",
				'content':status.content,
				'timestamp':status.timestamp,
				'created_by_name':status.created_by_name
			}

			return JsonResponse(data)

		else:
			return response

