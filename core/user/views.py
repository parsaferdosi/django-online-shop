#ApiView based on DRF and django
from user.serializer import AccountSerializer,AddressSerializer
from user.models import Account,Addresses
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
#swagger manual schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwt
from django.conf import settings
from utils.verify_token_generator import generate_and_send_verify_jwt
from .models import Account


class MyAccountViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    """AccountViewSet is a viewset for managing user accounts.
    It provides create, retrieve, update, and destroy operations for user accounts.

    Args:
        CreateModelMixin (POST): create a new user account.
        RetrieveModelMixin (GET): retrieve user account details.
        UpdateModelMixin (PATCH): update user account details.
        DestroyModelMixin (DELETE): delete a user account.
        ViewSet (_type_): Base class for viewsets that provides default implementations for common actions.
    """
    serializer_class = AccountSerializer
    def get_permissions(self):
        """allow non-authenticated user to create(), but everything else must be authenticated"""
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def get_object(self):
        """get the user account object based on the authenticated user"""
        return self.request.user
    
    def perform_create(self, serializer):

        user = serializer.save()
        generate_and_send_verify_jwt(user)
        return Response({"message":"لطفا برای تایید حساب کاربریتان ایمیل را چک کنید"},status=status.HTTP_200_OK)
     
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class AdminAccountViewSet(ModelViewSet):
    """AdminAccountViewSet is a viewset for managing user accounts by admin users.
    It provides create, retrieve, update, and destroy operations for user accounts.

    Args:
        ModelViewSet: A viewset that provides default implementations for create, retrieve, update, partial_update, destroy, and list actions.
    """
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [IsAdminUser]
class AddressesViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=AddressSerializer
    def get_queryset(self):
        return Addresses.objects.filter(user_id=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class SendVerifyLinkAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self , request):
        user = request.user
        generate_and_send_verify_jwt(user)
        return Response({"message":"لینک ارسال شد"},status=status.HTTP_200_OK)


class VerifyAccountAPIView(APIView):

    def get(self , request):
        token = request.GET.get("token")
        try :
            payload = jwt.decode(token , settings.SECRET_KEY , algorithms=["HS256"])
            if payload.get("purpose") != "verify_account" :
                return Response({"message":"توکن نامعتبر است "}, status=status.HTTP_400_BAD_REQUEST)
            
            user = Account.objects.get(id = payload.get("user_id"))
            user.is_verified = True
            user.save()
            return Response({"message":"حساب کاربری شما با موفقیت تایید شد"}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"message":"کاربر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
        except jwt.ExpiredSignatureError:
            return Response({"error": "لینک منقضی شده"}, status=400)
        except jwt.InvalidTokenError:
            return Response({"error": "توکن نامعتبر است"}, status=400)
