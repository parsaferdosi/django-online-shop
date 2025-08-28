from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from user.manager import CustomAccountManager
from django.utils.translation import gettext_lazy as _


class Account(AbstractBaseUser,PermissionsMixin):
    #base authentication fields
    email = models.EmailField(_("email adress"),unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number= models.CharField(max_length=15,unique=True,blank=True, null=True)
    #additional fields
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio=models.TextField(blank=True, null=True)
    #status fields
    is_active = models.BooleanField(default=True)
    # is_verified=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    #timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # Meta options
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomAccountManager()

    def __str__(self):
        return self.email
class Addresses(models.Model):
    user_id=models.ForeignKey(Account,on_delete=models.CASCADE,related_name='addresses')
    title=models.CharField(max_length=50)
    description=models.TextField(null=True,blank=True)
    zip_code=models.CharField(max_length=20)
    country=models.ForeignKey('country',null=True,blank=False,on_delete=models.SET_NULL)
    state=models.ForeignKey('state',null=True,blank=False,on_delete=models.SET_NULL)
    city=models.ForeignKey('city',null=True,blank=False,on_delete=models.SET_NULL)
    rest_of_address=models.TextField()
    is_default=models.BooleanField(default=False)
    def save(self,*args,**kwargs):
        if self.is_default:
            Addresses.objects.filter(user_id=self.user_id,is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.user_id.email} - {self.title}"
class Country(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
class State(models.Model):
    name=models.CharField(max_length=50)
    country_id=models.ForeignKey(Country,on_delete=models.CASCADE,related_name='states')
    def __str__(self):
        return self.name
class City(models.Model):
    name=models.CharField(max_length=50)
    state_id=models.ForeignKey(State,on_delete=models.CASCADE,related_name='cities')
    def __str__(self):
        return self.name