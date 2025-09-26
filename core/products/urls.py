from django.urls import path , include
from rest_framework_nested import routers
from core.products.views import ProductViewSet , LikeViewSet , CommentViewset , ProductManagerViewSet

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product_manager', ProductManagerViewSet, basename='product_manager')
product_router =  routers.NestedDefaultRouter(router , r'product' , lookup  = 'product')
product_router.register(r'comment', CommentViewset, basename='comment_manager')
router.register(r'comment_like', LikeViewSet, basename='like_dislike')



urlpatterns = [
    path('', include(router.urls)),
    path('',include(product_router.urls))
    
]