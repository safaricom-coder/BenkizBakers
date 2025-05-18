from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(PaymentDetail)
admin.site.register(WishList)
admin.site.register(WishItem)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Location)
