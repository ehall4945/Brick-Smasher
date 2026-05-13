from django.urls import path

from . import views


# App routes for pages and AJAX endpoints
urlpatterns = [
    path("", views.home, name="home"),
    path("account/", views.account_page, name="account"),
    path("movie/", views.movie_page, name="movie"),
    path("rent/", views.rent_page, name="rent"),
    path("dbUser/", views.db_user, name="db_user"),
    path("dbMovie/", views.db_movie, name="db_movie"),
    path("dbRent/", views.db_rent, name="db_rent"),
]
