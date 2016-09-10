from django.conf.urls import url
from website import views 


urlpatterns = [
	url(r'^huy/$', views.IndexView.as_view(), name="index"),
    # url(r'^address/add/$', views.UserAddressCreateView.as_view(), name="create_address"),
    # url(r'^list/$', views.OrderListView.as_view(), name="order_list"),
    # url(r'^(?P<pk>\d+)/$', views.OrderDetalView.as_view(), name="order_detail"),
]