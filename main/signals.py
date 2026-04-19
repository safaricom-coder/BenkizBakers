from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CakeCategory

CATEGORIES = [
    "Birthday Cakes",
    "Wedding Cakes",
    "Anniversary Cakes",
    "Graduation Cakes",
    "Custom Designer Cakes",
    "Cupcakes",
    "Mini Cakes",
    "Cheesecakes",
    "Chocolate Cakes",
    "Red Velvet Cakes",
    "Fruit Cakes",
    "Kids Cakes",
    "Corporate Cakes",
    "Seasonal Specials"
]

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name != "main":
        return

    if not CakeCategory._meta.db_table:
        return

    for category in CATEGORIES:
        CakeCategory.objects.get_or_create(name=category)