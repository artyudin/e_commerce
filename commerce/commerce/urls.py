"""commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf import settings
from django.conf.urls import url, include
# from django.conf.urls.static import static
from django.contrib import admin
from product import urls as product
from product import url_categories as categories
from carts import urls as carts
from order import urls as order
from website import urls as website

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^product/', include('product.urls', app_name="product", namespace="product")),
    url(r'^categories/', include('product.url_categories', app_name="categories", namespace="categories")),
    url(r'^cart/', include('carts.urls', app_name="carts", namespace="carts")),
    url(r'^order/', include('order.urls', app_name="order", namespace="order")),
    url(r'^web/', include('website.urls', app_name="website", namespace="website")),
]
