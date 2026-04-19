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