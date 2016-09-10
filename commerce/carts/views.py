from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.base import View
from product.models import Variations
from carts.models import Cart, CartItem
from django.contrib.auth.forms import AuthenticationForm
from order.mixins import CartOrderMixin
from order.models import UserCheckout, Order, UserAddress
from order.forms import GuestCheckoutForm
from .forms import ContactForm

def contact(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		email = form.cleaned_data.get("email")
		message = form.cleaned_data.get("message")
		full_name = form.cleaned_data.get("full_name")
		subject = "HUY"
		from_email = settings.EMAIL_HOST_USER
		to_email = ["artyudin@outlook.com"]
		contact_message = "Full name: {},Emal: {},Message: {}".format(full_name,email,message)
		send_mail(
    		subject,
    		contact_message,
    		from_email,
    		to_email,
    		fail_silently=False,
		)

	context = {
			"form":form,

	}
	return render(request, "carts/contact.html", context)






'''
Importing braintree
'''
import braintree 

if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
		merchant_id=settings.BRAINTREE_MERCHAND_ID,
		public_key=settings.BRAINTREE_PUBLIC,
		private_key=settings.BRAINTREE_PRIVATE)


'''
View to get cart count number by cart-count-badge
'''
class ItemCounView(View):

	def get(self, request, *args, **kwargs):

		if request.is_ajax():
			cart_id = self.request.session.get("cart_id")
			if cart_id == None:
				count = 0
			else:
				cart = Cart.objects.get(id=cart_id)
				count = cart.items.count()
			request.session["cart_item_count"] = count
			return JsonResponse({"count":count})
		else:
			raise HttpResponseRedirect


'''
Cart is binded to session, if cart does not exist, we create 
new cart and bind it the session, session would expire in
set_expiry(300) = 5 min or if (0) when browser closed,
if user is_authenticated then cart would be bined to user  
'''
class CartView(SingleObjectMixin, View):
	model = Cart
	template_name = "carts/cart.html"

	'''
	Checking if cart exists, if not creating a Cart
	'''
	def get_object(self, *args, **kwargs):
		self.request.session.set_expiry(0)
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			# self.request.user.get_tax_percentage()
			# cart.tax_percentage = 0.075
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(id=cart_id)
		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart

	'''
	Adding item to a cart
	'''
	def get(self, request, *args, **kwargs):
		cart =self.get_object()
		item_id = request.GET.get("item")
		delete_item = request.GET.get("delete", False)
		item_added = False
		if item_id:
			item_instance = get_object_or_404(Variations, id=item_id)
			qty = request.GET.get("qty", 1)
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404
			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			if created:
				item_added = True
			if delete_item:
				cart_item.delete()
			else:
				cart_item.quantity = qty
				cart_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("carts:cart"))

		if request.is_ajax():
			try:
				total = cart_item.line_item_total
			except:
				total = None
			try:
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None
			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None
			try:
				tax_total = cart_item.cart.tax_total
			except:
				tax_total = None
			try:
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
					"deleted":delete_item, 
					"item_added": item_added,
					"line_total": total,
					"subtotal": subtotal,
					"cart_total": cart_total,
					"tax_total": tax_total,
					"total_items":total_items,
					}

			return JsonResponse(data)
		context = {
			"object":self.get_object()
		}
		template = self.template_name

		return render(request, template, context)





'''
Checking out process
'''
class CheckOutView(CartOrderMixin, FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		cart = self.get_cart()
		if cart == None:
			return None
		return cart

	'''
	Allowing checking out for non registered users
	'''
	def get_context_data(self, *args, **kwargs):
		context = super(CheckOutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_check_id = self.request.session.get("user_checkout_id")

		if self.request.user.is_authenticated():
			user_can_continue = True
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token() 
			self.request.session["user_checkout_id"] = user_checkout.id
		elif not self.request.user.is_authenticated() and user_check_id == None:
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()
		else:
			pass

		if user_check_id != None:
			user_can_continue = True
			if not self.request.user.is_authenticated(): #guest user
				user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
				context["client_token"] = user_checkout_2.get_client_token()

		context["order"] = self.get_order()
		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		return context 

	'''
	Getting email from unregistered users
	'''
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			email = form.cleaned_data.get("email")
			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	'''
	If we get email successfuly we redirect to the same checkout
	'''
	def get_success_url(self):
		return reverse("order:checkout_address")

	'''
	Creating new order,
	by obtaining session id
	'''
	def get(self, request, *args, **kwargs):
		get_data = super(CheckOutView, self).get(request, *args, **kwargs)
		cart = self.get_object()
		if cart == None:
			return redirect("carts:cart")
		new_order = self.get_order()
		user_checkout_id = request.session.get("user_checkout_id")
		if user_checkout_id != None:
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
			if new_order.billing_address_id == None or new_order.shipping_address_id == None:
				return redirect("order:checkout_address")

			new_order.user = user_checkout
			new_order.save()
		return get_data


'''
Finalizing checkout,
obtaining payment_method_nonce from checkout.html,
for braintree
'''
class CheckoutFinalView(CartOrderMixin, View):

	def post(self, request, *args, **kwargs):
		order = self.get_order()
		order_total = order.order_total
		nonce = request.POST.get("payment_method_nonce")
		if nonce:
			result = braintree.Transaction.sale({
				"amount": order_total,
				"payment_method_nonce": nonce,
				"billing": {
					"postal_code": "{}".format(order.billing_address.zip_code),
			  	},
				"options": {
					"submit_for_settlement": True
				}
			})
			if result.is_success:
				order.mark_completed(order_id = result.transaction.id)
				messages.success(request, "Thank you for your order.")
				del request.session["cart_id"]
				del request.session["order_id"]
			else:
				messages.success(request, "{}".format(result.message))
				return redirect("carts:checkout")

		return redirect("order:order_detail", pk=order.pk)

	def get(self, request, *args, **kwargs):
		return redirect("carts:checkout")





















