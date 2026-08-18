from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'benkizapi'


    def ready(self):
        # Runs ONCE when Django starts
        from main.models import CakeCategory
        if not CakeCategory.objects.exists():
            CakeCategory.createMissingCategories()