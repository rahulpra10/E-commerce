from django.db import models

# Create your models here.
class Seller(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    address = models.TextField(max_length = 200)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length = 15)
    password = models.CharField(max_length = 50)
    pic = models.FileField(upload_to= "seller_profile", default="avtar.webp")
    dob = models.DateField(null= True ,blank=True)
    gender = models.CharField(max_length = 10)

    def __str__(self)-> str:
        return self.first_name


class Product(models.Model):
    p_name = models.CharField(max_length=30)
    des = models.CharField(max_length=300)
    price = models.FloatField(default=0.00)
    dis_price = models.FloatField(default=0.00)
    qua = models.IntegerField(default=0)
    pic = models.FileField(upload_to="n_product",default="cart.png")

    def __str__(self):
        return self.p_name
    