from django.contrib.auth import authenticate
from django import forms
from .models import Profile, ForgotPassword, ProfilePicture
from django.contrib.auth.models import User

GENDER_CHOICES = [('Male','Male'), ('Female','Female'), ('Others','Others')]

class RegisterForm(forms.Form):
	first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'autofocus':'on', 'autocomplete':'off', 'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Surname'}))
	gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES, attrs={'class':'custom-control-inline'}))
	dob = forms.DateField(label="Date of birth", widget=forms.DateInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'YYYY-MM-DD'}))
	email = forms.CharField(label="", widget=forms.EmailInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Email address'}))
	mobile = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Mobile Number'}))
	username = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Username'}))
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Your Password'}))
	cpassword = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Confirm Password'}))
	

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if len(User.objects.filter(email=email)):
			raise forms.ValidationError("Email Already Registered")

		return email

	def clean_mobile(self):
		mobile = self.cleaned_data.get("mobile")
		try:
			a = int(mobile)
		except:
			raise forms.ValidationError("Incorrect mobile number")
		if len(mobile)!=10:
			raise forms.ValidationError("Incorrect mobile number")
		elif len(Profile.objects.filter(mobile=mobile)):
			raise forms.ValidationError("Mobile Already Registered")

		return mobile

	def clean_username(self):
		username = self.cleaned_data.get("username")
		if len(User.objects.filter(username=username)):
			raise forms.ValidationError("Username already has been taken")

		return username

	def clean_password(self):
		password = self.cleaned_data.get("password")
		if len(password)<6:
			raise forms.ValidationError("Password must be at least 6 characters")

		return password
	def clean_cpassword(self):
		password = self.cleaned_data.get("password")
		cpassword = self.cleaned_data.get("cpassword")
		if password!=cpassword:
			raise forms.ValidationError("Passwords must match")

		return password

class LoginForm(forms.Form):
	username = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off','autofocus':'on','class':'form-control', 'placeholder':'Username'}))
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Password'}))

	def clean_username(self):
		username = self.cleaned_data.get("username")
		if len(User.objects.filter(username=username))==0:
			raise forms.ValidationError("Username does not exist")

		return username

	def clean_password(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		if user is None:
			raise forms.ValidationError("Wrong Username or Password")
		return password

class ForgotPasswordForm(forms.Form):
	email = forms.CharField(label="", widget=forms.EmailInput(attrs={'autocomplete':'off',"required":"required",'autofocus':'on','class':'form-control', 'placeholder':'Enter your email'}))

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if len(User.objects.filter(email=email))==0:
			raise forms.ValidationError("Your entered email does not match")

		return email



class VerifyCodeForm(forms.Form):
	code = forms.CharField(label="", widget=forms.TextInput(attrs={'autocomplete':'off',"required":"required",'autofocus':'on','class':'form-control', 'placeholder':'Code'}))
	password = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'New password'}))
	cpassword = forms.CharField(label="", widget=forms.PasswordInput(attrs={'autocomplete':'off','class':'form-control', 'placeholder':'Confirm new password'}))

	def clean_code(self):
		code=self.cleaned_data.get('code')
		obj = ForgotPassword.objects.filter(g_num=code)
		if len(obj)==0 or obj[0].g_num!=code:
			raise forms.ValidationError("Enter correct code")
		return code

	def clean_password(self):
		password = self.cleaned_data.get("password")
		if len(password)<6:
			raise forms.ValidationError("Password must be at least 6 characters")

		return password
	def clean_cpassword(self):
		password = self.cleaned_data.get("password")
		cpassword = self.cleaned_data.get("cpassword")
		if password!=cpassword:
			raise forms.ValidationError("Passwords must match")

		return password

class ChangePicForm(forms.ModelForm):
	class Meta:
		model = ProfilePicture
		fields = ['profile_id','dp']
	