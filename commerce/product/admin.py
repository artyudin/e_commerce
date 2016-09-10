from django.contrib import admin

from .models import Product, Variations, ProductImage, Category, ProductFeatured

'''
Adding variations view to Product detail admin,
extra sets the number of extra Variations in Product detail admin
'''
class VariationsInline(admin.TabularInline):
	model = Variations
	extra = 1

'''
Adding and managing images in Product detail admin
'''
class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1


'''
Customizing admin for a Product, displayng product name and price, 
can add any other Product fields 
'''
class ProductAdmin(admin.ModelAdmin):
	inlines = [
		VariationsInline,
		ProductImageInline,

	]
	list_display = ['__str__', 'price']
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)

admin.site.register(Variations)

admin.site.register(ProductImage)

admin.site.register(Category)

admin.site.register(ProductFeatured)