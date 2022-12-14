from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=48)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    bid = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="offer")

    def __str__(self):
        return f"{self.user}: {self.bid}"

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=500)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bids")
    imageUrl = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owned")
    isActive = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlisted")

    def __str__(self):
        return f"{self.owner}: ({self.title})"
    
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comments_section")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} ({self.listing.title}): {self.message}"