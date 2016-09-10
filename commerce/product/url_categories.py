from django.conf.urls import url
from product import views 


urlpatterns = [
	url(r'^$', views.CategoryListView.as_view(), name="categories_list"),
    url(r'^(?P<slug>[\w-]+)/$', views.CategoryDetailView.as_view(), name="category_detail"),
    # url(r'^(?P<pk>\d+)/inventory/$', views.VariationsListView.as_view(), name="product_inventory"),
]