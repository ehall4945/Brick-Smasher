from django.db import models

# Stores customer's account information
class StoreUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# Stores a movie title and the number of available copies
class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    in_stock = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    @property
    def checked_out_count(self):
        # Counts how many copies are currently checked out
        return self.checkouts.count()


# Connects one user to one movie they currently have checked out
class Checkout(models.Model):
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE, related_name="checkouts")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="checkouts")
    checked_out_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents one member from checking out the same movie twice
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.email} checked out {self.movie.title}"
