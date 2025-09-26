from django.contrib import admin
from core.products.models import Product , Category , Comment , Like
# Register your models here.


admin.site.register(Category)

admin.site.register(Like)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title","status","average_stars"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["product","user","like_count","dislike_count"]


