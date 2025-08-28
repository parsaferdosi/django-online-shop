from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.
class cart(models.Model):
    '''
     Each cart is associated with a user and has a status and payment information
     there is no need for an extra table for ordering cuase cart will handle everything
     A cart can have multiple cart items, each representing a product and its quantity
     this is cart model
    '''
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_cart')
    created_at=models.DateTimeField(auto_now_add=True)
    cart_status=models.ForeignKey('cart_status',null=True,blank=False,on_delete=models.SET_NULL)
    #this is payment status and details
    #we use payment_status table to store the status of the payment in development and in product we should use real payment gateway
    payment_status=models.ForeignKey('payment_status',null=True,blank=False,on_delete=models.SET_NULL)
    #paymet details specially for payment gateway
    #we gonna get payment token from payment gateway and store it here
    payment_token=models.CharField(null=False,default="Payment_Unknown")
    #then use a webhook to update the payment status
    #we can also store the payment date here via webhook
    payment_date=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return f"Cart of {self.user_id.username} - Status: {self.cart_status} - Payment Status: {self.payment_status}"
class cart_item(models.Model):
    cart_id=models.ForeignKey(cart,on_delete=models.CASCADE,related_name='cart_items')
    product_id=models.ForeignKey('products.Product',on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    total_price=models.PositiveIntegerField(default=0)
    def save(self, *args, **kwargs):
    # Automatically calculate total_price based on product price × quantity
        self.total_price = self.product_id.price * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Item: {self.product_id.title} (x{self.quantity}) in Cart ID: {self.cart_id.id}"
class cart_status(models.Model):
    title=models.CharField(max_length=250)
    def __str__(self):
        return self.title
class payment_status(models.Model):
    title=models.CharField(max_length=250)
    def __str__(self):
        return self.title