from random import randint
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import JsonResponse, Http404
from django.views.generic import FormView, View, DetailView, TemplateView

from django.contrib.auth import (

	authenticate,
	login,
	logout

	)

from friend.models import Friend
from message.models import Message
from .models import Profile, ForgotPassword, ProfilePicture
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, VerifyCodeForm, ChangePicForm

class RegisterFormView(FormView):

	form_class = RegisterForm
	template_name  = 'accounts/register.html'
	success_url = '/form-success/'


	def form_invalid(self, form):

		response = super(RegisterFormView, self).form_invalid(form)
		
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):

		response = super(RegisterFormView, self).form_valid(form)
		if self.request.is_ajax():

			first_name = form.cleaned_data.get("first_name")
			last_name = form.cleaned_data.get("last_name")
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			email = form.cleaned_data.get("email")
			mobile = form.cleaned_data.get("mobile")
			gender = form.cleaned_data.get("gender")
			dob = form.cleaned_data.get("dob")

			user, create = User.objects.get_or_create(
			
				first_name=first_name,
				last_name=last_name,
				username=username,
				email=email,

			)
		
			user.set_password(password)
			user.save()

			pro = Profile(mobile=mobile, dob=dob, gender=gender, user=user)
			pro.save()

			propic = ProfilePicture(profile_id=pro.id)
			propic.save()

			subject = 'KD SHARE team'
			message = 'Thank you for your registration.\n\nThis email will help you in case you forgot your password.'
			from_email = settings.EMAIL_HOST_USER
			to_list = [user.email]
			send_mail(subject,message,from_email,to_list,fail_silently=True)

			data = {
				'message': "Successfully submitted form data."
			}

			return JsonResponse(data)

		else:
			return response

class LoginFormView(FormView):

	form_class = LoginForm
	template_name  = 'accounts/login.html'
	success_url = '/form-success/'
	def form_invalid(self, form):

		response = super(LoginFormView, self).form_invalid(form)
		
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):

		response = super(LoginFormView, self).form_valid(form)
		if self.request.is_ajax():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			
			user = authenticate(username=username, password=password)

			login(self.request, user)
			
			data = {
				'message': "Successfully logged in"
			}

			return JsonResponse(data)

		else:
			return response


class LogoutFormView(View):
	def get(self, request):
		logout(self.request)
		return HttpResponseRedirect(reverse('accounts:login'))


class ProfileView(DetailView):
	model = Profile
	template_name = 'accounts/profile.html'

	def get_context_data(self, **kwargs):

		context = super(ProfileView,self).get_context_data(**kwargs)
		id1 = self.kwargs['pk']
		context['friends'] = Friend.objects.filter(profile=id1)

		pic = ProfilePicture.objects.filter(profile_id=id1)
		if len(pic):
			context['pic'] = pic[0]

		if self.request.user.profile.gender=="Male":
			context['male'] = True

		else:
			context['male'] = False


		return context

	
def PseudoPro(request, username=None):
	u = User.objects.filter(username=username)
	try:
		pic = ProfilePicture.objects.filter(profile_id=u[0].profile.id)
		friends = Friend.objects.filter(profile=request.user.profile.id)
		curr_fr = Friend.objects.filter(username=username)

		if len(curr_fr)==0 or curr_fr[0] not in friends:
			raise Http404

		context = {
			'u':u[0]
		}

		if len(pic):
			context['pic'] = pic[0]

		if u[0].profile.gender=="Male":
			context['male'] = True

		else:
			context['male'] = False

		return render(request, 'accounts/pseudoprofile.html', context)
		
	except:
		raise Http404

def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.filter(id__in=user_id_list)


class OnlinePeopleView(TemplateView):
	template_name = 'friend/online.html'
	def get_context_data(self, **kwargs):
		context = super(OnlinePeopleView, self).get_context_data(**kwargs)
		user_friends = Friend.objects.filter(profile_id=self.request.user.profile.id)
		context['friends'] = []
		if len(user_friends):
			online_users = get_current_users()
			for f in user_friends:
				context['friends'] += online_users.filter(username=f.username)

		return context

class ForgotPasswordView(FormView):
	
	form_class = ForgotPasswordForm
	template_name  = 'accounts/f_password.html'
	success_url = '/form-success/'

	def form_invalid(self, form):

		response = super(ForgotPasswordView, self).form_invalid(form)
		
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):

		response = super(ForgotPasswordView, self).form_valid(form)
		if self.request.is_ajax():
			email = form.cleaned_data.get('email')
			

			u = User.objects.filter(email=email)
			g_num = str(randint(10000, 99999)) + u[0].username


			pre_fp = ForgotPassword.objects.filter(email=email)
			pre_fp.delete()

			fp = ForgotPassword(email=email, g_num = g_num)
			fp.save()


			subject = 'Reset Password - KD SHARE team'
			message = 'Your verification code is : ' + g_num
			from_email = settings.EMAIL_HOST_USER
			to_list = [email]
			send_mail(subject,message,from_email,to_list,fail_silently=True)


			data = {
				'message': "Successfully continued."
			}

			return JsonResponse(data)

		else:
			return response

class VerifyCodeView(FormView):

	form_class = VerifyCodeForm
	template_name  = 'accounts/verify-code.html'
	success_url = '/form-success/'

	def form_invalid(self, form):

		response = super(VerifyCodeView, self).form_invalid(form)
		
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response

	def form_valid(self, form):

		response = super(VerifyCodeView, self).form_valid(form)
		if self.request.is_ajax():
			password = form.cleaned_data.get('password')
			code = form.cleaned_data.get('code')
			print(code, password)
			uname = code[5:]
			u = User.objects.get(username=uname)
			u.set_password(password)
			u.save()
			obj = ForgotPassword.objects.filter(g_num=code)
			obj.delete()
			data = {
				'message': "Successfull"
				
			}

			return JsonResponse(data)

		else:
			return response

class ChangePicView(FormView):

	form_class = ChangePicForm
	template_name  = 'accounts/change-pic.html'
	success_url = ""

	def form_invalid(self, form):
		print('error')
		return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk':self.request.user.profile.id}))

		

	def form_valid(self, form):

		p = ProfilePicture.objects.filter(profile_id=self.request.user.profile.id)
		p.delete()
		
		form.save()

		return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk':self.request.user.profile.id}))


def UnfriendView(request, id=None):
	id1 = request.user.profile.id
	try:
		
		f = Friend.objects.filter(
			(Q(profile_id=id1)&Q(fid=id))|
			(Q(profile_id=id)&Q(fid=id1))
		)
		f.delete()

		msg_list = Message.objects.filter(
			(Q(sender_profile_id=id1)&Q(reciever_profile_id=id))|
			(Q(sender_profile_id=id)&Q(reciever_profile_id=id1))
		)
		msg_list.delete()
		print(msg_list)
	except:
		print("error")
	finally:
		return HttpResponseRedirect(reverse('accounts:profile', kwargs={'pk':id1}))

