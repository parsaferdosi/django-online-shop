from django.urls import path , include
from rest_framework import routers
from .views import ProductViewSet , LikeViewSet

router = routers.DefaultRouter()
router.register(r'display', ProductViewSet, basename='product')
router.register(r'like', LikeViewSet, basename='like_dislike')

urlpatterns = [
    path('product/', include(router.urls)),
]