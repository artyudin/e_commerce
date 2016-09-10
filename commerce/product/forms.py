from django import forms
from django.forms.models import modelformset_factory

from.models import Variations



class VariationsInventoryForm(forms.ModelForm):
	class Meta:
		model = Variations
		fields = [
			"title",
			"price",
			"sale_price",
			"inventory",
			"active",
		]

VariationsInventoryFormSet = modelformset_factory(Variations, form=VariationsInventoryForm, extra=1)