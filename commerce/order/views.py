from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib import messages
from django.http import Http404
from .models import UserAddress, UserCheckout, Order
from .mixins import CartOrderMixin, LoginRequiredMixin
from .forms import AddressForm, UserAddressForm

'''
View that lets any user see order, regardless of authentication
'''
class OrderDetalView(DetailView):
	model = Order

	'''
	Method to get session user to see order_detail
	'''
	def dispatch(self, request, *args, **kwargs):
		try:
			user_check_id = self.request.session.get("user_checkout_id")
			user_checkout = UserCheckout.objects.get(id=user_check_id)
		except UserCheckout.DoesNotExist:
			user_checkout = UserCheckout.objects.get(user=request.user)
		except:
			user_checkout = None
		
		obj = self.get_object()
		if obj.user == user_checkout and user_checkout is not None:
			return super(OrderDetalView, self).dispatch(request, *args, **kwargs)	
		else:
			raise Http404


'''
View for listing orders
'''
class OrderListView(LoginRequiredMixin, ListView):
	queryset = Order.objects.all()
	print(queryset)


	'''
	Overwriting queryset method, now it is based on user,
	order associated with user checkout
	'''
	def get_queryset(self):
		user_check_id = self.request.user.id
		user_checkout = UserCheckout.objects.get(id=user_check_id)
		print(user_checkout)
		return super(OrderListView, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
	form_class = UserAddressForm
	template_name = "order/forms.html"
	success_url ="/order/address/"

	def get_checkout_user(self):
		user_check_id = self.request.session.get("user_checkout_id")
		user_checkout = UserCheckout.objects.get(id=user_check_id)
		return user_checkout

	def form_valid(self, form, *args, **kwargs):
		form.instance.user = self.get_checkout_user()
		return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)




class AddressSelectedFormView(CartOrderMixin, FormView):
	form_class = AddressForm
	template_name = "order/address_select.html"
	success_url ="/cart/checkout/"

	def dispatch(self, *args, **kwargs):
		b_address, s_address = self.get_addresses()
		if b_address.count() == 0:
			messages.success(self.request, "Please add a billing address")
			return redirect("order:create_address")
		elif s_address.count() == 0:
			messages.success(self.request, "Please add a shipping address")
			return redirect("order:create_address")

		else:
			return super(AddressSelectedFormView, self).dispatch(*args, **kwargs)

	'''
	Getting user's address
	'''
	def get_addresses(self, *args, **kwargs):
		user_check_id = self.request.session.get("user_checkout_id")
		user_checkout = UserCheckout.objects.get(id=user_check_id)
		
		b_address = UserAddress.objects.filter(
				user = user_checkout,
				type = 'billing',
			)
		
		s_address = UserAddress.objects.filter(
				user = user_checkout,
				type = 'shipping',
			)
		return b_address, s_address

	'''
	Chenging queryset for form,
	based on user's email from UserCheckout
	'''
	def get_form(self, *args, **kwargs):
		form = super(AddressSelectedFormView, self).get_form(*args, **kwargs)
		b_address, s_address = self.get_addresses()

		form.fields["billing_address"].queryset = b_address
		form.fields["shipping_address"].queryset = s_address
		return form

	'''
	Validating form
	'''
	def form_valid(self, form, *args, **kwargs):
		billing_address = form.cleaned_data["billing_address"]
		shipping_address = form.cleaned_data["shipping_address"]
		order = self.get_order()
		order.billing_address = billing_address
		order.shipping_address = shipping_address
		order.save()
		
		return super(AddressSelectedFormView, self).form_valid(form, *args, **kwargs)

	










