from rest_framework.serializers import ModelSerializer
from cart.models import cart, cart_item

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