from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from localflavor.us.us_states import STATE_CHOICES
from carts.models import Cart
from django.db.models.signals import pre_save, post_save


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
Unregisterd users can checkout
'''
class UserCheckout(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
	email = models.EmailField(unique=True)
	braintree_id = models.CharField(max_length=120, null=True, blank=True)

	def __str__(self):
		return self.email

	'''
	Creating instance method for user checkout
	'''
	@property
	def get_braintree_id(self):
		instance = self
		if not instance.braintree_id:
			result = braintree.Customer.create({
				"email": instance.email,
			})
			if result.is_success:
				instance.braintree_id = result.customer.id
				instance.save()
		return instance.braintree_id

	'''
	Creating client token
	'''
	def get_client_token(self):
		customer_id = self.get_braintree_id
		if customer_id:
			client_token = braintree.ClientToken.generate({
				"customer_id": customer_id
			})
			return client_token
		return None


'''
Post save signal for braintree
'''
def update_braintree_id(sender, instance, *args, **kwargs):
	if not instance.braintree_id:
		instance.get_braintree_id




post_save.connect(update_braintree_id, sender=UserCheckout)




ADDRESS_TYPE = (
	('billing','Billing'),
	('shipping','Shipping'),
	)

class UserAddress(models.Model):
	user = models.ForeignKey(UserCheckout)
	type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
	street_one = models.CharField(blank=True, max_length=25)
	street_two = models.CharField(blank=True, max_length=25)
	city = models.CharField(blank=True, max_length=25)
	state = models.CharField(max_length=2, choices=STATE_CHOICES, null=True, blank=True)
	zip_code = models.IntegerField(blank=True, max_length=5, default=0)
	zip_ext = models.IntegerField(blank=True, max_length=4, default=0)

	def __str__(self):
		return self.street_one

	def get_address(self):
		return "{},{},{},{},{},{}".format(self.street_one, self.street_two, self.city, self.state, self.zip_code, self.zip_ext)
	
ORDER_STATUS_CHOICES = (
	('created','Created'),
	('paid','Paid'),
	('shipped','Shipped'),
	('refunded','Refunded'),
	)

class Order(models.Model):
	status = models.CharField(max_length=120, choices = ORDER_STATUS_CHOICES, default='created')
	cart = models.ForeignKey(Cart)
	user = models.ForeignKey(UserCheckout, null=True)
	billing_address = models.ForeignKey(UserAddress, related_name='billing_address', null=True)
	shipping_address = models.ForeignKey(UserAddress, related_name='shipping_address', null=True)
	shipping_total_price = models.DecimalField(max_digits=20, decimal_places=2, default=5.99)
	order_total = models.DecimalField(max_digits=20, decimal_places=2)
	order_id = models.CharField(max_length=20, null=True, blank=True)


	def __str__(self):
		return str(self.cart.id)

	class Meta:
		ordering = ['-id']

	'''
	Setting url for order_detail
	'''
	def get_absolute_url(self):
		return reverse("order:order_detail", kwargs={"pk": self.pk})

	'''
	Method to complete order
	'''
	def mark_completed(self, order_id=None):
		self.status = "paid"
		if order_id and not self.order_id:
			self.order_id = order_id
		self.save()


def order_pre_save(sender, instance, *args, **kwargs):
	shipping_total_price = instance.shipping_total_price
	cart_total = instance.cart.total
	order_total = Decimal(shipping_total_price) + Decimal(cart_total)
	instance.order_total = order_total

pre_save.connect(order_pre_save, sender=Order)



















