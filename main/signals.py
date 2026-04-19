from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name != "main":
        return

    CakeCategory = apps.get_model("main", "CakeCategory")

    categories = [
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

    for category in categories:
        CakeCategory.objects.get_or_create(name=category)