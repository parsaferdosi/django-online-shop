from django.shortcuts import render
from rest_framework import viewsets , filters
from .serializers import ProductSerializer
from .models import Product
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
