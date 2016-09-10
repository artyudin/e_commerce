from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from product.models import Variations
from django.db.models.signals import  pre_save, post_save, post_delete
from decimal import Decimal



'''
Incase the buyer wants to by several variations of the same product
Need to use two ForeignKey if using through=CartItem,
"Cart" has to be in quotes because class Cart defined after CartItem
'''
class CartItem(models.Model):
	cart = models.ForeignKey("Cart")
	item = models.ForeignKey(Variations)
	quantity = models.PositiveIntegerField(default=1)
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2,null=True,)


	def __str__(self):
		return self.item.title

	'''
	Romove method for the cart to remove items,
	creates a link to remove an item
	'''
	def remove(self):
		return "{}?item={}&delete=True".format(reverse("carts:cart"), self.item.id)

	'''
	Getting title from model to display in the Cart
	'''
	def get_title(self):
		return "{}   {}".format(self.item.product.title, self.item.title)

'''
Setting the line_item_total through pre save signal
'''
def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty =instance.quantity
	if int(qty) >= 1:
		price = instance.item.get_price()
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)

'''
Happaning after the item has been saved into db
'''
def cart_itemm_post_save_receiver(sender, instance, *args, **kwargs):
	instance.cart.update_subtotal()

post_save.connect(cart_itemm_post_save_receiver, sender = CartItem)

post_delete.connect(cart_itemm_post_save_receiver, sender = CartItem)



'''
Cart is based on Variations, all products/items in the cart = Variations
Althogh the queryset is Variations it would use CartItem as an intermediary
'''
class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	items = models.ManyToManyField(Variations, through=CartItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=20, decimal_places=2,default=1)
	tax_percentage = models.DecimalField(max_digits=20, decimal_places=5, default=0.085)
	tax_total = models.DecimalField(max_digits=20, decimal_places=2,null=True,default=1)
	total = models.DecimalField(max_digits=20, decimal_places=2,null=True,default=1)

	def __str__(self):
		return str(self.id)

	'''
	Updating sub_total
	'''
	def update_subtotal(self):
		subtotal = 0
		items = self.cartitem_set.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal = "{:10.2f}".format(subtotal)
		self.save()


'''
Saving taxes and total
'''
def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
	subtotal = Decimal(instance.subtotal)
	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) #8.5%
	total = round(subtotal + Decimal(tax_total), 2)
	instance.tax_total = "{:10.2f}".format(tax_total)
	instance.total = "{:10.2f}".format(total)

pre_save.connect(do_tax_and_total_receiver, sender=Cart)




























