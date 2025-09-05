from rest_framework.serializers import ModelSerializer
from cart.models import cart, cart_item , cart_status,payment_status

class CartSerializer(ModelSerializer):
    class Meta:
        model = cart
        fields = '__all__'
        read_only_fields = ['user_id', 'created_at', 'payment_date']
class CartItemSerializer(ModelSerializer):
    class Meta:
        model = cart_item
        fields = '__all__'
        read_only_fields = ['total_price']
class cartStatusSerializer(ModelSerializer):
    class Meta:
        model = cart_status
        fields = '__all__'
class paymentStatusSerializer(ModelSerializer):
    class Meta:
        model = payment_status
        fields = '__all__'