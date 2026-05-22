from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Checkout, Movie, StoreUser


# ----------------------------
# Page views
# ----------------------------
def home(request):
    return render(request, "bricksmasher/home.html")


def account_page(request):
    return render(request, "bricksmasher/account.html")


def movie_page(request):
    return render(request, "bricksmasher/movie.html")


def rent_page(request):
    return render(request, "bricksmasher/rent.html")


# ----------------------------
# JSON helpers
# ----------------------------
def error(message, status=400):
    return JsonResponse({"error": message}, status=status)

# Following three functions all convert their respective model into a JSON-safe dictionary
def user_json(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
    }


def movie_json(movie):
    return {
        "id": movie.id,
        "title": movie.title,
        "in_stock": movie.in_stock,
        "checked_out": movie.checked_out_count,
    }


def checkout_json(checkout):
    return {
        "id": checkout.id,
        "user": checkout.user.id,
        "movie": checkout.movie.id,
        "title": checkout.movie.title,
        "email": checkout.user.email,
    }


# Returns every movie using the default alphabetical model ordering
def all_movies_json():
    return [movie_json(movie) for movie in Movie.objects.all()]


# Returns all checked out movies for one user
def user_checkouts_json(user):
    checkouts = Checkout.objects.filter(user=user).select_related("movie", "user")
    return [checkout_json(checkout) for checkout in checkouts]


# Following two methods return an object or None when the id is invalid
def get_user(user_id):
    try:
        return StoreUser.objects.get(id=user_id)
    except StoreUser.DoesNotExist:
        return None

def get_movie(movie_id):
    try:
        return Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return None


# ----------------------------
# User AJAX endpoint
# ----------------------------
@require_http_methods(["GET", "POST"])
def db_user(request):
    # Routes user AJAX requests by HTTP method
    if request.method == "GET":
        return find_user_by_email(request)

    return create_user(request)


# Looks up and verifies a member account by email address
def find_user_by_email(request):
    email = request.GET.get("email", "").strip()

    if not email:
        return error("Email is required")

    try:
        user = StoreUser.objects.get(email=email)
    except StoreUser.DoesNotExist:
        return error("User not found", status=404)

    return JsonResponse(user_json(user))


# Creates a new member account when the email is unique
def create_user(request):
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name", "").strip()
    email = request.POST.get("email", "").strip()

    if not first_name or not last_name or not email:
        return error("First name, last name, and email are required")

    try:
        user = StoreUser.objects.create(first_name=first_name, last_name=last_name, email=email)
    except IntegrityError:
        return error("An account with that email already exists")

    return JsonResponse(user_json(user))


# ----------------------------
# Movie AJAX endpoint
# ----------------------------
@require_http_methods(["GET", "POST"])
def db_movie(request):
    # Routes movie AJAX requests by HTTP method
    if request.method == "GET":
        return JsonResponse(all_movies_json(), safe=False)

    action = request.POST.get("action", "").strip()

    if action == "new":
        problem = create_movie(request)
    elif action == "add":
        problem = change_movie_stock(request, amount=1)
    elif action == "remove":
        problem = change_movie_stock(request, amount=-1)
    elif action == "delete":
        problem = delete_movie(request)
    else:
        return error("Invalid movie action")

    if problem:
        return problem

    return JsonResponse(all_movies_json(), safe=False)


def create_movie(request):
    title = request.POST.get("title", "").strip()

    # Ensures that a user can't add a blank movie title or one that exceeds 75 chars
    if not title:
        return error("Movie title cannot be blank")
    
    if len(title) > 75:
        return error("Movie title cannot be longer than 75 characters")

    try:
        Movie.objects.create(title=title, in_stock=1)
    except IntegrityError:
        return error("That movie already exists")

    return None


# Permanently removes a movie that has no copies currently checked out
def delete_movie(request):
    movie = get_movie(request.POST.get("id"))

    if movie is None:
        return error("Invalid movie id")

    if movie.checked_out_count > 0:
        return error("Cannot delete a movie while copies are checked out")

    movie.delete()
    return None


# Adds or removes one available copy from an existing movie
def change_movie_stock(request, amount):
    movie = get_movie(request.POST.get("id"))

    if movie is None:
        return error("Invalid movie id")

    if amount < 0 and movie.in_stock == 0:
        return error("In-stock copies cannot go below zero")

    movie.in_stock += amount
    movie.save()

    return None


# ----------------------------
# Rental AJAX endpoint
# ----------------------------
@require_http_methods(["GET", "POST"])
def db_rent(request):
    # Routes rental AJAX requests by HTTP method and action 
    if request.method == "GET":
        return get_checkouts(request)

    action = request.POST.get("action", "").strip()

    if action == "rent":
        return rent_movie(request)

    if action == "return":
        return return_movie(request)

    return error("Invalid rental action")


# Gets checkout records with optional user and movie filters
def get_checkouts(request):
    user_id = request.GET.get("user")
    movie_id = request.GET.get("movie")
    checkouts = Checkout.objects.select_related("user", "movie")

    if user_id:
        if get_user(user_id) is None:
            return error("Invalid user id")
        checkouts = checkouts.filter(user_id=user_id)

    if movie_id:
        if get_movie(movie_id) is None:
            return error("Invalid movie id")
        checkouts = checkouts.filter(movie_id=movie_id)

    return JsonResponse([checkout_json(checkout) for checkout in checkouts], safe=False)


# Gets the user and movie needed for rent or return actions
def get_rental_items(request):
    user = get_user(request.POST.get("user"))
    movie = get_movie(request.POST.get("movie"))

    if user is None or movie is None:
        return None, None, error("Invalid user or movie id")

    return user, movie, None


# Checks out one movie after passing all the rental rules, and updates the movie's in-stock count
def rent_movie(request):
    user, movie, problem = get_rental_items(request)

    if problem:
        return problem

    if user.checkouts.count() >= 3:
        return error("A member can only check out 3 movies at a time")

    if Checkout.objects.filter(user=user, movie=movie).exists():
        return error("This member already has this movie checked out")

    if movie.in_stock <= 0:
        return error("This movie is not currently in stock")

    Checkout.objects.create(user=user, movie=movie)
    movie.in_stock -= 1
    movie.save()

    return JsonResponse(user_checkouts_json(user), safe=False)


# Returns one checked out movie back to available stock, and deletes the checkout record
def return_movie(request):
    user, movie, problem = get_rental_items(request)

    if problem:
        return problem

    try:
        checkout = Checkout.objects.get(user=user, movie=movie)
    except Checkout.DoesNotExist:
        return error("Checkout record not found")

    checkout.delete()
    movie.in_stock += 1
    movie.save()

    return JsonResponse(user_checkouts_json(user), safe=False)
