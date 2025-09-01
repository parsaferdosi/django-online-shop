from django.urls import path
from rest_framework import routers
from cart.views import cartViewSet, cartItemViewSet

routers=routers.DefaultRouter()
routers.register(r'cart',cartViewSet,basename='cart')
routers.register(r'cart-items',cartItemViewSet,basename='cart-items')

urlpatterns=routers.urls
