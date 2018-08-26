from django.shortcuts import render
from status.forms import PostForm
from status.models import Status
from friend.models import Friend
from django.views.generic import TemplateView

class HomeView(TemplateView):
	template_name = 'home/home.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		id1=self.request.user.profile.id
		form = PostForm()
		context['form']=form
		friends = Friend.objects.filter(profile=id1)
		posts = []
		status = Status.objects.all()
		
		for f in friends:
			s = status.filter(profile=f.fid)
			
			if len(s):
				posts+=s
		user_post = status.filter(profile=id1)
		
		if len(user_post):
			posts+=user_post

		context['posts']=posts
		return context

