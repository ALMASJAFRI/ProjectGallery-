from django.db import models
from seller.models import project,project_detail
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your models here.
class Variant(models.Model):
    var_name=models.CharField()
    def __str__(self):
        return self.var_name
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)
class Cartitem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    det=models.ForeignKey(project_detail,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    variant=models.ForeignKey(Variant,on_delete=models.CASCADE,null=True,blank=True)

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    review=models.TextField()
    def __str__(self):
        return self.review
        
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    project=models.ForeignKey(project,on_delete=models.CASCADE)
    det=models.ForeignKey(project_detail,on_delete=models.CASCADE)
    price=models.CharField(null=True,blank=True)
    variant=models.CharField(max_length=100,null=True,blank=True)
    order_id=models.CharField()
    date_in=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    payu_payment_id=models.CharField(null=True,blank=True)
    hashs=models.CharField(null=True,blank=True)
    
    
    

    
