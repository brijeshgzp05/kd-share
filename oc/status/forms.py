from django import forms

class PostForm(forms.Form):
	content=forms.CharField(label="", widget=forms.TextInput(attrs={'autofocus':'on','autocomplete':'off','required':'required','class':'form-control','placeholder':"What's on your mind"}))
