from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=True)
    email=models.CharField(max_length=50,null= True)

    def __str__(self):
        return self.name
class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False,null=True,blank=False)
    image=models.ImageField(upload_to="Product_images",default=None)
    def __str__(self):
        return self.name
    @property
    def imageURL(self):# burada image nin yolunu belirttik sonra kullanırkende {{Product.imageURL}} olarak kullanacagız
        try:
            url=self.image.url
        except:
            url=""
        return url
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    date_orderd=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null= True)
    def __str__(self):
        return str(self.id)
    @property
    def shipping (self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping 
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total() for item in orderitems])
        return str(total)
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return str(total)
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,blank=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    def get_total(self):
        total=self.product.price*self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models. ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models. ForeignKey (Order, on_delete=models. SET_NULL, null=True)
    address = models. CharField (max_length=200, null=False)
    city = models. CharField(max_length=200, null=False)
    state = models. CharField (max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField (auto_now_add=True)
    def __str__(self):
        return self.address