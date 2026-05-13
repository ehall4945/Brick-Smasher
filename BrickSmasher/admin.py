from django.contrib import admin

from .models import Checkout, Movie, StoreUser


# Makes the project models available in the Django admin
admin.site.register(StoreUser)
admin.site.register(Movie)
admin.site.register(Checkout)
