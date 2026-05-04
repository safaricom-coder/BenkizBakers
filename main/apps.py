from django.apps import AppConfig
from django.conf import settings
import cloudinary.uploader
import cloudinary.api

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):

        import main.signals
        global DEFAULT_IMAGE_URL

        try:
            # for checking if default image has been uploaded to cludinary

            result = cloudinary.api.resource(
                f"{settings.DEFAULT_FOLDER}/{settings.DEFAULT_PUBLIC_ID}"
            )

            # if the image exists we store its url
            settings.DEFAULT_IMAGE_URL = result['secure_url']
        except cloudinary.exceptions.NotFound:
            # upload the local default image to cloudinary
            result=cloudinary.uploader.upload(
                settings.LOCAL_DEFAULT_IMAGE,
                folder = settings.DEFAULT_FOLDER,
                public_id=settings.DEFAULT_PUBLIC_ID,
                overwrite = True
            )
        settings.DEFAULT_IMAGE_URL = result['secure_url']
