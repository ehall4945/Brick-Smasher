from django.db import models


class StoreUser(models.Model):
    # Stores customer account information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        # Shows a readable account label in the admin
        return f"{self.first_name} {self.last_name} ({self.email})"


class Movie(models.Model):
    # Stores a movie title and the number of available copies
    title = models.CharField(max_length=200, unique=True)
    in_stock = models.PositiveIntegerField(default=1)

    class Meta:
        # Keeps movie lists alphabetical by default
        ordering = ["title"]

    def __str__(self):
        # Shows the movie title in the admin
        return self.title

    @property
    def checked_out_count(self):
        # Counts how many copies are currently checked out
        return self.checkouts.count()


class Checkout(models.Model):
    # Connects one user to one movie they currently have checked out
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name="checkouts")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="checkouts")
    checked_out_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents one member from checking out the same movie twice
        unique_together = ("user", "movie")

    def __str__(self):
        # Shows a readable checkout label in the admin
        return f"{self.user.email} checked out {self.movie.title}"
