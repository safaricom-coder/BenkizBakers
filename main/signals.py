from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import CakeCategory


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    categories = [
        'redvelvet',
        'cupcake',
        'biscuit',
        'cookies',
        'all',
        'wedding',
        'macarons',
        'cake',
        'anniversarycake',
        'birthdaycake',
    ]

    for category in categories:
        CakeCategory.objects.get_or_create(name=category)


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    # Only run for your app (prevents running for every migration)
    if sender.name != "main":
        return

    CakeCategory = apps.get_model("main", "CakeCategory")

    categories = [
        "Birthday Cakes",
        "Wedding Cakes",
        "Celebration Cakes",
        "Custom Cakes",
        "Photo Cakes",
        "Kids Cakes",
        "Anniversary Cakes",

        "Cupcakes",
        "Muffins",
        "Cookies",
        "Donuts",
        "Brownies",
        "Pastries",
        "Bread & Rolls",

        "Graduation Cakes",
        "Baby Shower Cakes",
        "Corporate Cakes",
        "Valentine Cakes",
        "Christmas Cakes",
        "Eid Cakes",
        "Special Offers",

        "Best Sellers",
        "New Arrivals",
        "Trending",
        "Discounted",
    ]

    for name in categories:
        CakeCategory.objects.get_or_create(name=name)