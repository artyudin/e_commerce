from django.conf.urls import url
from order import views 


urlpatterns = [
	url(r'^address/$', views.AddressSelectedFormView.as_view(), name="checkout_address"),
    url(r'^address/add/$', views.UserAddressCreateView.as_view(), name="create_address"),
    url(r'^list/$', views.OrderListView.as_view(), name="order_list"),
    url(r'^(?P<pk>\d+)/$', views.OrderDetalView.as_view(), name="order_detail"),
]
