import os

from django.core.asgi import get_asgi_application


# Points ASGI servers to the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BrickSmasher.settings")

application = get_asgi_application()
