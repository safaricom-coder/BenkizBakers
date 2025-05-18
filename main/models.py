from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Consolas,Lucida Console,Lucida,Lucida Sans Typewriter,Cascadia Code


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    @property
    def counting(self):
        counting = sum(cart_item.quantity for cart_item in self.items.all())
        return counting
    total = 0
    deliveryfee = 0
    totalcost = 0
    vat = 0
    
    
    @property
    def calcTotal(self):
        
        totall = sum(cart_item.subtotal for cart_item in self.items.all())
        deliveryfee = totall *.02
        self.deliveryfee = float(deliveryfee)
        self.vat = float(totall *.03)
        totalcost = totall + deliveryfee + self.vat
        self.totalcost = int(totalcost)
        self.total = totall
        return ''
    


    def __str__(self):
        return f"{self.user.username.capitalize}'s cart" 


class Item(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(
        upload_to='item_pics/',
        default='item_pics/default.jpg',
        blank=True
    )
    description = models.CharField(max_length=20,blank=True)
    price = models.PositiveIntegerField(default=30)
    numberOfItems = models.PositiveIntegerField(default=5)

    paginate_by = 4
    
    def __str__(self):
        return self.name.capitalize()
    
class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def subtotal(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.cart.user.username}'s cart"
    

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    profilepic =  models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.png'
    )
    
    lastname = models.CharField(max_length=50,blank=True)
    is_team = models.BooleanField(default = False)
    country = models.CharField(max_length=50, default='Kenya',blank=True)
    county = models.CharField(max_length=50,default='Kisii',blank=True)
    address_or_street = models.CharField(max_length=50,blank=True)
    apartment_or_house_name_or_number = models.CharField(max_length=50,blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

class PaymentDetail(models.Model):
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='profile')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    paidstatus = models.BooleanField(default=False)

class WishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username +"'" +' '+'wishlist'
    
    
class WishItem(models.Model):
    wishlist = models.ForeignKey(WishList,on_delete=models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    name = item.name
    def __str__(self):
        return self.item.name
    

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True,null=True)
    body = models.TextField(blank=True,null=True)

    def __str__(self):
        if self.body:
            return self.body[0:10] + '...'
        else:
            return self.user.username[0:10] + '...'
class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=0,blank=True,null=True)

    def __str__(self):
        if self.body:
            return self.body[0:10] + '...'
        else:
            return self.user.username[0:10] + '...'


class Location(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20,blank=True,null=True)
    mail = models.EmailField(blank=True,null=True)
    
    def __str__(self):
        return self.name[0:10] + '...'