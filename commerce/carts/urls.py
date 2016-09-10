from django.conf.urls import url
from carts import views 


urlpatterns = [
	url(r'^$', views.CartView.as_view(), name="cart"),
    url(r'^count/$', views.ItemCounView.as_view(), name="cart_item_count"),
    url(r'^checkout/$', views.CheckOutView.as_view(), name="checkout"),
    url(r'^final/$', views.CheckoutFinalView.as_view(), name="final_checkout"),
    url(r'^contact/$', views.contact, name="contact"),
]