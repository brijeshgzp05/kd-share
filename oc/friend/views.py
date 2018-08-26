from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView, DeleteView, View, DetailView, ListView
from accounts.models import Profile
from .forms import AddForm
from .models import RequestCall, Friend

class AddView(FormView):
	form_class = AddForm
	template_name  = 'friend/addfriend.html'
	success_url = '/form-success/'

	def form_invalid(self, form):

		response = super(AddView, self).form_invalid(form)
		
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):

		response = super(AddView, self).form_valid(form)
		if self.request.is_ajax():

			uname = form.cleaned_data.get("uname")
			uname2 = self.request.user.username

			if uname==uname2:
				return JsonResponse({'msg':"You can not send a request to yourself"}, status=400)
			elif len(User.objects.filter(username=uname))==0:
				return JsonResponse({'msg':"This is not a valid username"}, status=400)	
			elif len(Friend.objects.filter(username=uname,profile=self.request.user.profile.id)):
				return JsonResponse({'msg':"You are already a friend"}, status=400)
			elif len(RequestCall.objects.filter(coming_from=uname2,coming_for=uname)):
				return JsonResponse({'msg':"Already sent a request"}, status=400)
			elif len(RequestCall.objects.filter(coming_from=uname,coming_for=uname2)):
				return JsonResponse({'msg':"You have already got a request"}, status=400)
			else:
				z = User.objects.filter(username=uname)

				req = RequestCall(
					coming_from=uname2, 
					coming_for=uname,
					coming_from_profile_id=self.request.user.profile.id ,
					coming_for_profile_id=z[0].profile.id ,
					coming_from_name=self.request.user.first_name+" "+self.request.user.last_name,
					coming_for_name=z[0].first_name+" "+z[0].last_name,
					)
				req.save()
				
				data = {
					'message': "Request Sent"
				}

				return JsonResponse(data)

		else:
			return response

class ReqView(TemplateView):
	template_name = 'friend/requests.html'
	def get_context_data(self, **kwargs):
		context = super(ReqView, self).get_context_data(**kwargs)
		send_username = self.request.user.username
		context['send_req'] = RequestCall.objects.filter(coming_from=send_username)
		context['rec_req'] = RequestCall.objects.filter(coming_for=send_username)

		return context


class DelReqView(DeleteView):
	def get(self,request, *args, **kwargs):
		try:
			r = RequestCall.objects.get(pk=self.kwargs['pk'])
			r.delete()
		except:
			pass
		finally:
			return JsonResponse({"message":"Deletion Confirmed"})


class AccReqView(DeleteView):
	def get(self,request, *args, **kwargs):
		try:
			r = RequestCall.objects.get(pk=self.kwargs['pk'])
			Friend.objects.create(
					profile_id = self.request.user.profile.id,
					username = r.coming_from,
					name = r.coming_from_name,
					fid =int(r.coming_from_profile_id),
				)
			u = User.objects.get(username=r.coming_from)
			Friend.objects.create(
					profile_id = u.profile.id,
					username = r.coming_for,
					name = r.coming_for_name,
					fid = int(r.coming_for_profile_id),
				)
			r.delete()
		except:
			pass
		finally:
			return JsonResponse({'message':'Request accepted'})

class FriendsView(TemplateView):
	template_name = 'friend/friend-page.html'
	def get_context_data(self, **kwargs):
		context = super(FriendsView, self).get_context_data(**kwargs)
		context['friends'] = Friend.objects.filter(profile_id=self.request.user.profile.id)

		return context