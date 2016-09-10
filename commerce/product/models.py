from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db import models


class ProductQuerySet(models.query.QuerySet):

	def active(self):
		return self.filter(active=True)

'''
Customizing Product.objects
'''
class ProductManager(models.Manager):

	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	'''
	overwriting get_quryset setting active=True
	customizing Product.objects.all()
	insted of Product.objects.filter(active=False)
	'''
	def all(self, *args, **kwargs):
		return self.get_queryset().active()

	'''
	Getting related products, writing special queryset method
	Customizing model manager to get related products from all
	and products as default one, exclude current shown displayed product
	'''
	def get_related(self, instance):
		products_group_one = self.get_queryset().filter(categories__in=instance.categories.all())
		products_group_two = self.get_queryset().filter(default=instance.default)
		qs = (products_group_one | products_group_two).exclude(id=instance.id).distinct()
		return qs


 

class Product(models.Model):
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	categories = models.ManyToManyField('Category', blank=True)
	default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)

	objects = ProductManager()


	def __str__(self):
		return self.title

	'''
	Creating urls to Product detail 
	'''
	def get_absolute_url(self):
		return reverse("product:product_detail", kwargs={"pk":self.pk})

	'''
	Getting imgs product and for related products
	'''
	def get_image_url(self):
		img =self.productimage_set.first()
		if img:
			return img.image.url
		return img


class Variations(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_absolute_url(self):
		return self.product.get_absolute_url()
	'''
	Creating a link to add item/Variation to cart
	'''
	def add_to_cart(self):
		return "{}?item={}&qty=1".format(reverse("carts:cart"), self.id)
	'''
	Creating a link to remove item/Variation to cart
	'''
	# def remove_to_cart(self):
	# 	return "{}?item={}&qty=1".format(reverse("carts:cart"), self.id)

'''
Checking if Product has variations if not will set default
Basket takes variations
'''
def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
	
	product = instance
	variations = product.variations_set.all()
	if variations.count() == 0:
		new_variation = Variations()
		new_variation.product = product
		new_variation.title = "Default"
		new_variation.price = product.price
		new_variation.save()



post_save.connect(product_post_saved_receiver, sender=Product)

# '''
# Changing file img name to one according product
# '''
# def image_upload_to(instance, filename):
# 	title = instance.product.title
# 	slug = slugify(title)
# 	basename, file_extension = filename.split(".")
# 	new_filename = "%s-%s-%s" %(slug, instance.id, file_extension)
# 	return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='product/static/product/pics')

	def __str__(self):
		return self.product.title



class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True, null=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('categories:category_detail', kwargs={"slug":self.slug})

'''
Changing file img name to one according ProductFeatured
upload_to=image_upload_to_featured
'''
def image_upload_to_featured(instance, filename):
	title = instance.prduct.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s-%s" %(slug, instance.id, file_extension)
	return "products/%s/%s" %(slug, new_filename)

class ProductFeatured(models.Model):
	prduct = models.ForeignKey(Product)
	image = models.ImageField(upload_to=image_upload_to_featured, blank=True)
	title = models.CharField(max_length=120, blank=True, null=True)
	text = models.TextField(max_length=120, blank=True, null=True)
	text_on_right_side = models.BooleanField(default=False)
	show_price = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.prduct.title






























