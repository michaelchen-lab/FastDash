from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AuctionListing, Comment, Bid, Category, User, WatchList

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Category)

admin.site.register(User, UserAdmin)
admin.site.register(WatchList)
