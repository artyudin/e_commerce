from django import forms
from django.contrib.auth import get_user_model
from .models import UserCheckout, UserAddress

User = get_user_model()


class GuestCheckoutForm(forms.Form):
	email = forms.EmailField()
	email2 = forms.EmailField(label='Confirm Email')

	'''
	Verifying email
	'''
	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get('email2')

		if email == email2:
			user_exists = User.objects.filter(email=email).count()
			# email_in_db = UserCheckout.objects.filter(email=email).count()
			if user_exists != 0:
				raise forms.ValidationError("This User already exists. Please login instead.")
			# elif email_in_db != 0:
			# 	raise forms.ValidationError("This Email already exists.")
			return email2
		else:
			raise forms.ValidationError("Please confirm emails are the same")


class AddressForm(forms.Form):
	billing_address = forms.ModelChoiceField(
		queryset=UserAddress.objects.filter(type="billing"),
		widget = forms.RadioSelect,
		empty_label = None,
		)

	shipping_address = forms.ModelChoiceField(
		queryset=UserAddress.objects.filter(type="shipping"),
		widget = forms.RadioSelect,
		empty_label = None,
		)

class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
				'street_one', 
				'street_two', 
				'city',
				'state', 
				'zip_code',
				'zip_ext', 
				'type', 


		]




















