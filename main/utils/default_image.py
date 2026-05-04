import cloudinary.api
from django.conf import settings


def get_default_image_url():
    # If already set, return it
    if settings.DEFAULT_IMAGE_URL:
        return settings.DEFAULT_IMAGE_URL

    # If Cloudinary disabled (PythonAnywhere free tier)
    if not getattr(settings, "CLOUDINARY_ENABLED", False):
        return settings.DEFAULT_IMAGE_URL

    try:
        result = cloudinary.api.resource(
            f"{settings.DEFAULT_FOLDER}/{settings.DEFAULT_PUBLIC_ID}"
        )
        return result["secure_url"]
    except Exception:
        return None