from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_closed = models.BooleanField()
    imageLink = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    auctionListing = models.OneToOneField(
        AuctionListing,
        on_delete=models.CASCADE,
        primary_key=True
    )
    ## User property only filled if bid by someone else
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.pk)

class Comment(models.Model):
    auctionListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # auctionListing = models.OneToOneField(
    #     AuctionListing,
    #     on_delete=models.CASCADE,
    #     primary_key=True
    # )
    comment = models.TextField()

    def __str__(self):
        return str(self.pk)

class Category(models.Model):
    name = models.CharField(max_length=200)
    listings = models.ManyToManyField(
        AuctionListing,
        blank=True,
        related_name="listings"
    )

    def __str__(self):
        return self.name

class WatchList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    listings = models.ManyToManyField(AuctionListing, blank=True, related_name="watchedListings")

    def __str__(self):
        return self.user.username
