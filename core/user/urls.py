from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.user import views
#using DRF router to automatically generate URL patterns for the viewsets
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router=DefaultRouter()
router.register(r'myaccount',views.MyAccountViewSet,basename='myaccount')
router.register(r'admin/accounts',views.AdminAccountViewSet,basename='admin-accounts')
router.register(r'addresses',views.AddressesViewSet,basename='addresses')


urlpatterns =router.urls + [
    # Define your URL patterns here
    path('login/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('verify/',views.VerifyAccountAPIView.as_view(),name='verify_account'),
    path('send_verify_link/',views.SendVerifyLinkAPIView.as_view(),name='send_link'),
    path('send_reset_password/',views.SendRestPasswordAPIView.as_view(),name='send_link'),
    path('reset_password/',views.ChangeRestPasswordAPIView.as_view(),name='reset_password'),
    
]