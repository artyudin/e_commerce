from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Variations, Category, ProductFeatured
from .forms import VariationsInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone

'''
Updating inventory for Product Variations through variations_list.html
using VariationsInventoryFormSet plus two additional empty forms 
'''
class VariationsListView(StaffRequiredMixin, ListView):
	model = Variations
	queryset = Variations.objects.all()

	'''
	Rendering Form
	'''
	def get_context_data(self, *args, **kwargs):
		context = super(VariationsListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationsInventoryFormSet(queryset=self.get_queryset())
		return context 

	'''
	Obtaining variations for a particular product based on a pruduct pk
	out of all Variations
	'''
	def get_queryset(self, *args, **kwargs):

		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variations.objects.filter(product=product)
		return queryset

	'''
	This POST method can handle FILES
	Messages alert user when something has been done in the system
	'''
	def post(self, request, *args, **kwargs):
		formset = VariationsInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				if new_item.title:
					product_pk = self.kwargs.get("pk")
					product = get_object_or_404(Product, pk=product_pk)
					new_item.product = product
					new_item.save()
			messages.success(request, "Your inventory updated")
			return redirect("product:product_list")
		
		raise Http404







'''
Returns specific list of products
'''
class ProductListView(ListView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		# overwriting original context to maipulate context
		# getting default content by super
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		# customize context by adding attributes to context
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q")
		return context 

	'''
	Overwriting query search to make site searchable
	pay attention on _ _icontains
	for more precise search create qs2
	distinct() makes sure that we recieve anly one object 
	'''
	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs



'''
Returns specific product details
can be customized
template_name = 'product/product_detail.html'
'''
class ProductDetailView(DetailView):
	model = Product

	'''
	Method to get related products out of Model manager
	get_related(), can be ordered and show only number of related products, 
	can be ordered and show only number of related products
	order is managed by lambda function
	'''
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		context["related"] = sorted(Product.objects.get_related(instance)[:5], key=lambda x: x.title)
		return context




'''
List view for categories
'''
class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = 'product/product_list.html'

'''
Category detail view
'''
class CategoryDetailView(DetailView):
	model= Category

	'''
	Setting how query would come 
	'''
	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj =self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products).distinct()
		context["products"] = products
		return context 

class FrontPageView(View):
	template_name = "product/base.html"
	# model = ClientIncome
	# form_class = ClientIncomeForm
	context = None

	def get(self, request):
		featured_product = ProductFeatured.objects.first()
		# if self.model.objects.filter(user=request.user).exists():
		# 	return render(request, 'dashboard.html')
		# else:
		self.context = {"featured_product":featured_product}

		return render(request, self.template_name, self.context)
















