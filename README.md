# BrickSmasher

BrickSmasher is a Django project for a simple VHS movie rental management system. The application is designed for store employees to create customer accounts, manage movie inventory, and rent or return movies using AJAX requests.

## Features

- Home page with navigation links
- Customer account creation
- Unique email validation for accounts
- Movie inventory table
- Add new movie titles
- Add or remove in-stock movie copies
- Member lookup by email
- Rent movies to registered members
- Return checked-out movies
- Basic rental rule validation
- AJAX endpoints for users, movies, and rentals

## Project Structure

```text
BrickSmasher/
  manage.py
  requirements.txt
  README.md

  BrickSmasher/
    settings.py
    urls.py
    asgi.py
    wsgi.py

  bricksmasher/
    admin.py
    apps.py
    models.py
    urls.py
    views.py
    migrations/
    templates/
      bricksmasher/
        home.html
        account.html
        movie.html
        rent.html
    static/
      bricksmasher/
        style.css
        account.js
        movie.js
        rent.js
```

## Main Pages

```text
/           Home page
/account/   Account creation page
/movie/     Manage movies page
/rent/      Rent and return movies page
```

## AJAX Endpoints

```text
/dbUser/    Handles user lookup and account creation
/dbMovie/   Handles movie listing and inventory updates
/dbRent/    Handles checkout lookup, rentals, and returns
```

## Database Models

The project uses three main database models:

```text
StoreUser
Movie
Checkout
```

`StoreUser` stores customer account information.

`Movie` stores movie titles and available in-stock copies.

`Checkout` connects a user to a movie they currently have checked out.

## Setup Instructions

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the project in the browser:

```text
http://127.0.0.1:8000/
```

## Optional Admin Setup

Create a superuser:

```bash
python manage.py createsuperuser
```

Open the admin panel:

```text
http://127.0.0.1:8000/admin/
```

## Notes

This project is intended as a clean boilerplate starting point for the BrickSmasher assignment. It includes the main Django project structure, app structure, models, routes, templates, static files, and AJAX endpoint scaffolding needed to continue development.
