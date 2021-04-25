from django.urls import path, include
from .views import *
from .views_staff import *

urlpatterns =[
    path('', index, name='home'),
    path('product', product, name='product'),
    path('product-detail/<pk>', viewProductDetail),
    path('order-product/<pk>', orderProduct),
    path('success', success),
    path('accounts/signup', signup),
] 
