from django.db import models
from seller.models import Product

# Create your models here.
## Buyer table

class Buyer(models.Model):
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    address = models.TextField(max_length = 200)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length = 15)
    password = models.CharField(max_length = 50)
    pic = models.FileField(upload_to= "profile", default="avtar.webp",null=True)
    dob = models.DateField(null= True ,blank=True)
    gender = models.CharField(max_length = 10)

    def __str__(self)-> str:
        return self.first_name
    


class Cart(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.buyer.first_name