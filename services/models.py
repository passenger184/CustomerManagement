from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Custmor(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(null=True, default='a.png', blank=True)


    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
   
    def __str__(self):
        return self.name    
    


    
class Product(models.Model):
    CATAGORY = (
        ('Indoor', 'Indoor'), 
        ('Outdoor', 'Outdoor'),
    )
    
    tags = models.ManyToManyField(Tag)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    catagory = models.CharField(max_length=200, null=True, choices=CATAGORY)
    description = models.CharField(max_length=200, null=True, blank=True)   
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name

    
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    
    
    customer = models.ForeignKey(Custmor, on_delete=models.SET_NULL, null=True)   
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)   
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=200, null=True)
    
    
    def __str__(self):
        return self.product.name    
    