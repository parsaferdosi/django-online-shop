from rest_framework.response import Response
from rest_framework import viewsets , status
from .serializers import ProductSerializer , LikeSerializer
from .models import Product , Like
from django.db.models import Avg
# Create your views here.

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving products.

    Features:
    - List all products
    - Retrieve product details by slug
    - Filter products by category (query parameter `?category=<slug>`)
    - Sort products by average stars in descending order


    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get("category")
        if slug :
            queryset = queryset.filter(category__slug = slug)

        queryset = queryset.annotate(avg_stars = Avg("comments__stars"))
        queryset = queryset.order_by("-avg_stars")

        return queryset
    

class LikeViewSet(viewsets.ViewSet):
    
    def create(self , request):
        srz_data = LikeSerializer(data = request.data , context = {"request":request})
        srz_data.is_valid(raise_exception=True)
        comment = srz_data.validated_data['comment']
        is_exists = Like.objects.filter(user = request.user , comment = comment).first()

        if is_exists :
            is_exists.delete()
            return Response({"message":"Like removed"},status.HTTP_200_OK)
        
        like = srz_data.save()
        action = "liked" if like.is_like else "disLiked"
        return Response({"message":action} , status= status.HTTP_201_CREATED)
        
         
    

        
        


    
