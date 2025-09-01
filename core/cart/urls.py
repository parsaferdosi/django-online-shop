from django.urls import path
from rest_framework import routers
from cart.views import cartViewSet, cartItemViewSet,cartStatusViewSet,paymentStatusViewSet

routers=routers.DefaultRouter()
routers.register(r'cart/cart',cartViewSet,basename='cart')
routers.register(r'cart/cart-items',cartItemViewSet,basename='cart-items')
routers.register(r'admin/cartStatus',cartStatusViewSet,basename='admin-cartStatus')
routers.register(r'admin/paymentStatus',paymentStatusViewSet,basename='admin-paymentStatus')


urlpatterns=routers.urls
