from cart.serializer import CartSerializer, CartItemSerializer,cartStatusSerializer,paymentStatusSerializer
from cart.models import cart, cart_item, cart_status, payment_status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.viewsets import ModelViewSet

# Create your views here.

class cartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return cart.objects.all()
        return cart.objects.filter(user_id=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
    
class cartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return cart_item.objects.all()
        return cart_item.objects.filter(cart_id__user_id=self.request.user)

class cartStatusViewSet(ModelViewSet):
    serializer_class = cartStatusSerializer
    permission_classes = [IsAdminUser]
    queryset = cart_status.objects.all()
class paymentStatusViewSet(ModelViewSet):
    serializer_class = paymentStatusSerializer
    permission_classes = [IsAdminUser]
    queryset = payment_status.objects.all()
    
    