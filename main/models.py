from django.db import models
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from cloudinary.models import CloudinaryField

# Create your models here.

# Consolas,Lucida Console,Lucida,Lucida Sans Typewriter,Cascadia Code

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = 0
    deliveryfee = 0
    inittotal =0
    totalcost = 0
    vat = 0
    quantity = 0

    @property
    def calcTotal(self):

        totall = float(sum(cart_item.subtotal for cart_item in self.items.all()))
        self.inittotal = totall
        self.total = totall
        self.deliveryfee = totall*.02
        self.vat = round(float(totall *.03),2)
        self.totalcost = totall + self.vat + self.deliveryfee
        self.save()
        return ''

    def __str__(self):
        return f"{self.user.username.capitalize}'s cart"

cakecategories = (
    ('redvelvet','redvelvet'),
    ('cupcake','cupcake'),
    ('biscuit','biscuit'),
    ('cookies','cookies'),
    ('all','all'),
    ('wedding','wedding'),
    ('macarons','macarons'),
    ('cake','cake'),
    ('anniversarycake','anniversarycake'),
    ('birthdaycake','birthdaycake')
)


from django.utils.text import slugify

class CakeCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while CakeCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=50)

    thumbnail = models.URLField(blank=True, null=True)
    thumbnail_public_id = models.CharField(max_length=255, blank=True, null=True)

    
    description = models.CharField(max_length=1000, blank=True)
    additionalinfo = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)

    numberofviews = models.PositiveIntegerField(default=1)
    numberOfItems = models.PositiveIntegerField(default=0)
    soldUnits = models.PositiveIntegerField(default=0)

    category = models.ManyToManyField('main.CakeCategory')

    def __str__(self):
        return self.name
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def subtotal(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in {self.cart.user.username}'s cart"

class Social(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name = 'socialaccount')
    facebook = models.CharField(max_length=200,null=True,default=None)
    twitter = models.CharField(max_length=200,null=True,default=None)
    instagram = models.CharField(max_length=200,null=True,default=None)
    youtube = models.CharField(max_length=200,null=True,default=None)
    
    def __str__(self):
        return self.user.username +"'s Socials."

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userprofile')
    is_normal_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20,blank=True,null=True)
    profilepic = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='profile_pics/default.png'
    )
    choices = [
        ('Chief Baker','chiefbaker'),
        ('Baker','baker'),
        ('Chief Decorator','chiefdecorater'),
        ('Decorator','decorator'),
        ('Delivery Team','deliveryteam')
    ]
    job = models.CharField(max_length=100,choices=choices,default='Staff')
    lastname = models.CharField(max_length=50,blank=True)
    is_team = models.BooleanField(default = False)
    country = models.CharField(max_length=50, default='Kenya',blank=True)
    county = models.CharField(max_length=50,default='Kisii',blank=True)
    address_or_street = models.CharField(max_length=50,blank=True)
    apartment_or_house_name_or_number = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

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


class Rating(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stars = models.IntegerField(blank=True,null=True)
    
    @property
    def createstarlist(self):

        return ' ' * self.stars
    def __str__(self):
        if self.stars:
            return self.user.username + (self.stars * '*') + ' ...'
        else:
            return self.user.username[0:10] + 'has no rating on us ...'

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    rating = models.ForeignKey(Rating,on_delete=models.CASCADE,blank=True,null=True)

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

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField(blank=True,null = True)
    timecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:10] + '...'

blogpostcategories = (
    ('Recipe','Recipe'),
    ('Guide','Guide'),
    ('News','News'),
    ('Video','Video')
)

class BlogPost(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    timecreated = models.DateTimeField(auto_now_add=True)
    numberofviews = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50, choices=blogpostcategories,blank=True,null=True)

    coverimage = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='blog_pics/default.jpg'
    )

    @property
    def blogsample(self):
        return self.content[0:250]
    def __str__(self):
        return self.title


class View(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    blogpost = models.ForeignKey(BlogPost,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + 'view'
    
    
class Lesson(models.Model):
    title = models.CharField(max_length=200,default='Benkiz Class')
    availability = models.BooleanField(default=True)
    description = models.CharField(max_length=100,default='',blank=True)
    price = models.PositiveIntegerField(default=10500)
    thumbnail = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='class-1.jpg'
    )
    thumbnailname=models.CharField(max_length=50,blank=True)
    fineprint = models.TextField(max_length=2000)
    time=models.DateTimeField(auto_now=True)
    timedescription = models.CharField(max_length=200,default='')

    def __str__(self):
        return self.title + ' class'


class CourseBasket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    lessons_selected = models.ManyToManyField(Lesson,blank=True,related_name='selected_courses')
    lessons_enrolled = models.ManyToManyField(Lesson,blank=True,related_name='enrolled_courses')
   
    def __str__(self):
        return self.user.username +"'s Course Basket."

class LearnerProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    phone = models.PositiveIntegerField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    mode_of_learning = models.CharField(max_length=20,null=True,blank=True)
    
    def __str__(self):
        return self.name + 'Learner profile'

class HeroBanner(models.Model):
    text = models.CharField(max_length=500)
    font_size = models.PositiveIntegerField(default=14)
    picture = CloudinaryField(
        'image',
        blank=True,
        null=True
    )
    picture_present = models.BooleanField(default=False)
   
    def __str__(self):
        return self.text[0:10] + " ..."