import os

from django.core.wsgi import get_wsgi_application


# Points WSGI servers to the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BrickSmasher.settings")

application = get_wsgi_application()
