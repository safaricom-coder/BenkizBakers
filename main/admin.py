from django.contrib import admin
from .models import * 
from benkizapi.models import *

admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)
admin.site.register(WishItem)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Location)
admin.site.register(Message)
admin.site.register(Social)
admin.site.register(BlogPost)
admin.site.register(View)
admin.site.register(Lesson)
admin.site.register(LearnerProfile)
admin.site.register(CourseBasket)
admin.site.register(Transaction)
admin.site.register(HeroBanner)

admin.site.register(CakeCategory)