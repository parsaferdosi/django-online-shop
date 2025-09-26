from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator , MinValueValidator
from django.db.models import Avg
from PIL import Image, ImageEnhance
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
    
    APPROVAL_STATUS = [
        ('pending', 'در انتظار تایید'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
    ]

    PUBLISH_STATUS = [
        ('draft', 'پیشنویس'),
        ('published', 'منتشر شده'),
    ]


    title = models.CharField(max_length=250)
    slug = models.SlugField(unique= True)
    image = models.ImageField(upload_to='products/%Y/%m/%d' , null= True , blank=True)
    description = models.TextField()
    category = models.ManyToManyField(Category , related_name="cat_products")
    price = models.PositiveIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICE , max_length=100)
    approval = models.CharField(choices=APPROVAL_STATUS , default='pending')
    publish = models.CharField(choices=PUBLISH_STATUS , default='draft')
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user_products")
    created_at = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now=True)
    

    def average_stars(self):
        result = self.comments.filter(status = 'approved').aggregate(avg=Avg("stars"))["avg"]
        return result or 0
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # اول ذخیره بشه

        # آدرس فایل ذخیره‌شده
        img_path = self.image.path
        img = Image.open(img_path)

        # واترمارک رو باز کنیم (فرض کن watermark.png داریم)
        watermark = Image.open("static/watermark.jpg").convert("RGBA")

        # تغییر اندازه واترمارک به نسبت تصویر اصلی
        ratio = img.width / 5
        wpercent = (ratio / float(watermark.size[0]))
        hsize = int((float(watermark.size[1]) * float(wpercent)))
        watermark = watermark.resize((int(ratio), hsize), Image.Resampling.LANCZOS)

        # محل قرارگیری واترمارک (پایین-راست)
        position = (img.width - watermark.width - 10, img.height - watermark.height - 10)

        # ترکیب دو تصویر
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        transparent = Image.new('RGBA', img.size, (0,0,0,0))
        transparent.paste(img, (0,0))
        transparent.paste(watermark, position, mask=watermark)
        transparent = transparent.convert('RGB')  # برای ذخیره jpg

        # دوباره ذخیره کنیم
        transparent.save(img_path, 'JPEG')
    
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):

    STATUS_CHOICES = [
        ('approved', 'تأیید شده'),
        ('pending', 'در انتظار تأیید'),
        ('rejected', 'رد شده'),
    ]


    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='comments')
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    stars = models.PositiveIntegerField(default=0 , validators=[MinValueValidator(0),MaxValueValidator(5)])
    text = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES , default='pending',max_length=28)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"
    
    def like_count(self):
        return self.likes.filter(is_like = True).count()
    
    def dislike_count(self):
        return self.likes.filter(is_like = False).count()



class Like(models.Model):

    comment = models.ForeignKey(Comment , on_delete=models.CASCADE , related_name="likes")
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    is_like = models.BooleanField() # False = dislike , True = like

    class Meta :
        unique_together = ("user","comment") #User can be just have one like 
