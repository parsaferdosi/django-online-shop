from rest_framework import serializers 
from .models import Product , Comment , Like , Category

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    average_stars = serializers.SerializerMethodField()
    seller = serializers.StringRelatedField()
    category =  CategorySerializer(many=True)

    class Meta :
        model = Product
        fields = '__all__'
        

    def get_comments(self , obj):
        result = obj.comments.filter(status = 'approved')
        return CommentSerializer(instance = result , many =True , context=self.context ).data
    
    def get_average_stars(self , obj):
        return obj.average_stars()

    

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_like_count(self , obj):
        return obj.like_count()
    
    def get_dislike_count(self , obj):
        return obj.dislike_count()
    
    def get_is_owner(self, obj):
        request = self.context.get("request")
        # اگه request وجود نداره یا کاربر لاگین نکرده، False بده
        if request and request.user.is_authenticated:
            return obj.user == request.user
        return False


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Like
        fields = '__all__'

    def create(self , validated_data):
        user = self.context['request'].user
        comment = validated_data['comment']
        return Like.objects.create(comment = comment , user = user ,is_like=validated_data.get('is_like', True))



    

  
        




        