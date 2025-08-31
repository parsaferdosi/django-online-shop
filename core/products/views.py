from rest_framework.response import Response
from rest_framework import viewsets , status , generics , mixins
from .serializers import ProductSerializer , LikeSerializer , CommentSerializer
from .models import Product , Like , Comment
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
    
    

class CommentViewset(viewsets.ModelViewSet):
    """
    Manage comments of authenticated users for a specific product.

    Features:
    - List, create, update, and delete user's comments.
    - Automatically set status to 'pending' if an approved comment is updated.

    URL should include `product_slug` to filter comments by product.

    Example:
        GET /product/<product_slug>/comments/  -> list user's comments
        POST /product/<product_slug>/comments/ -> create a comment
        PUT /product/<product_slug>/comments/<id>/ -> update a comment

    """
    serializer_class = CommentSerializer
    queryset =Comment.objects.all()

    def get_queryset(self ): 
        queryset =Comment.objects.all()
        product_slug = self.kwargs['product_slug']
        queryset = queryset.filter(product__slug = product_slug , user = self.request.user)
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        product_slug = self.kwargs['product_slug']
        product =Product.objects.get(slug =product_slug )
        serializer.save(user = self.request.user , product = product)

    def perform_update(self, serializer):
        obj = self.get_object()
        if obj.status == "approved":
            serializer.save(status="pending")
        else :
             serializer.save()


class LikeViewSet(viewsets.ViewSet):
    """
    Toggle like/dislike on a comment.

    - POST: Create or remove a like/dislike for the authenticated user.
    - If the user already liked the comment, it will be removed.
    - Request: {"comment": <id>, "is_like": true/false}
    - Response: {"message": "liked" / "disLiked" / "Like removed"}
    """

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
               
    

        
        


    
