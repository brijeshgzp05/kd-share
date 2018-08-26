from django import forms
from django.contrib.auth.models import User
from .models import Friend, RequestCall

class AddForm(forms.Form):
	uname = forms.CharField(label="",widget=forms.TextInput(attrs={'autofocus':'on','autocomplete':'off','class':'form-control','placeholder':'Username of your friend'}))
	