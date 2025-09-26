from rest_framework.response import Response
from rest_framework import viewsets , status , generics , mixins
from core.products.serializers import ProductSerializer , LikeSerializer , CommentSerializer
from core.products.models import Product , Like , Comment
from django.db.models import Avg
from rest_framework.permissions import IsAuthenticated
from core.products.permissions import IsOwnerOrReadOnly

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
    queryset = Product.objects.filter(publish = "published" , approval = "approved")
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.request.query_params.get("category")
        if slug :
            queryset = queryset.filter(category__slug = slug ,publish = "published" , approval = "approved")

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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
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
    permission_classes = [IsAuthenticated ]
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

class ProductManagerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products owned by the authenticated user.

    Features:
        - List products created by the authenticated user.
        - Create new products (automatically assigned to the current user).
        - Update products (only allowed for the product owner).
        - Delete products (only allowed for the product owner).
        - Filter products by approval status.
        - Filter products by publish status.

    Permissions:
        - Only authenticated users can access this endpoint.
        - Only the owner of a product can update or delete it.
        - Other users have read-only access.

    Query Parameters (optional):
        - approval: Filter products by approval status. 
            Example → /api/products/?approval=approved
        - publish: Filter products by publish status.
            Example → /api/products/?publish=published

    Choice Fields:
        - STATUS_CHOICE:
            * available   → Available (موجود)
            * unavailable → Unavailable (ناموجود)

        - APPROVAL_STATUS:
            * pending  → Pending approval (در انتظار تایید)
            * approved → Approved (تایید شده)
            * rejected → Rejected (رد شده)

        - PUBLISH_STATUS:
            * draft     → Draft (پیشنویس)
            * published → Published (منتشر شده)

    Methods:
        - get_queryset:
            Returns the queryset of products belonging to the current user.
            Applies filters based on 'approval' and 'publish' query parameters
            if they are provided.
        - perform_create:
            Automatically assigns the currently authenticated user as the
            owner when creating a new product.
    """
    permission_classes = [IsAuthenticated , IsOwnerOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


    def get_queryset(self):

        queryset = Product.objects.filter(user = self.request.user)
        approval = self.request.query_params.get("approval")
        publish = self.request.query_params.get("publish")
        if approval :
            queryset = queryset.filter(approval = approval)
            return queryset
        
        if publish :
            queryset = queryset.filter(publish = publish)
            return queryset
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


    
    

        
        


    
