from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    title = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=128)
    price = models.FloatField()
    posted_date = models.DateTimeField()
    image_url = models.URLField(blank=True, null=True)
    open = models.BooleanField(default=True)

class Bids(models.Model):
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)

class Comments(models.Model):
    text = models.CharField(max_length=1024)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField()

class Watchlist(models.Model):
    watchlist_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Listings, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

class Winners(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_won = models.ForeignKey(Listings, on_delete=models.CASCADE)