from django import forms

class ContactForm(forms.Form):
	full_name = forms.CharField(max_length=120, )
	email = forms.EmailField(max_length=120, )
	message = forms.CharField(max_length=120, )