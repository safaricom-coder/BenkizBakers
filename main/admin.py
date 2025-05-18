from django.contrib import admin
from .models import Item,UserProfile,Cart,CartItem,PaymentDetail

# Register your models here.
admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(PaymentDetail)