from django.conf.urls import url
from product import views 


urlpatterns = [
	url(r'^$', views.ProductListView.as_view(), name="product_list"),
    url(r'^(?P<pk>\d+)/$', views.ProductDetailView.as_view(), name="product_detail"),
    url(r'^(?P<pk>\d+)/inventory/$', views.VariationsListView.as_view(), name="product_inventory"),
    url(r'^front/$', views.FrontPageView.as_view(), name="front_page"),
]