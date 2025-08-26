from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator , MinValueValidator
# Create your models here.

User =get_user_model()

class Category(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique= True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE , null=True , blank= True , related_name="children")
    

    def __str__(self):
        return self.title

class Product(models.Model):

    STATUS_CHOICE = [
        ('available', 'موجود'),
        ('unavailable', 'ناموجود'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique= True)
    image = models.ImageField(upload_to='products/%Y/%m/%d' , null= True , blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    stars = models.PositiveIntegerField(default=0 , validators=[MinValueValidator(0),MaxLengthValidator(5)])
    status = models.CharField(choices=STATUS_CHOICE , max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    seller = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user_products")
    created_at = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    