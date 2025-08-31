from django.urls import path , include
from rest_framework_nested import routers
from .views import ProductViewSet , LikeViewSet , CommentViewset

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
product_router =  routers.NestedDefaultRouter(router , r'product' , lookup  = 'product')
product_router.register(r'comment', CommentViewset, basename='comment_manager')
router.register(r'comment_like', LikeViewSet, basename='like_dislike')



urlpatterns = [
    path('', include(router.urls)),
    path('',include(product_router.urls))
    
]