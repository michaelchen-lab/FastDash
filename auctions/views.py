from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User
from .models import AuctionListing, Bid, WatchList, Comment, Category

def index(request):
    listings = AuctionListing.objects.filter(is_closed=False)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

@login_required
def createListing_view(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        description = request.POST.get("description", "")
        imageURL = request.POST.get("imageURL", "")
        auctionListing = AuctionListing.objects.create(
            user = request.user,
            title = title,
            description = description,
            is_closed = False,
            imageLink = imageURL
        )

        bidPrice = request.POST.get("bidPrice", "")
        bid = Bid.objects.create(
            auctionListing = auctionListing,
            amount = bidPrice
        )

        print(True)
        print(request.POST.get("category", "-"))
        if request.POST.get("category", "-") != "-":
            category = Category.objects.get(name=request.POST.get("category", ""))
            category.listings.add(auctionListing)

        return render(request, "auctions/createListing.html", {
            "success_alert": "Congrats! Your listing has been uploaded."
        })
    else:
        categories = Category.objects.all()
        return render(request, "auctions/createListing.html", {
            "categories": categories
        })

def listing_view(request, listing_pk):
    data = {}
    listing = AuctionListing.objects.get(pk=listing_pk)

    ## A form is submitted
    if request.method == "POST":
        if request.POST.get("bidPrice", "") != "":
            ## Submit a bid
            listing.bid.user = request.user
            listing.bid.amount = request.POST.get("bidPrice", "")
            listing.bid.save()

            data.update({"success_alert": "You have successfully placed your bid."})
        elif request.POST.get("add", "") != "":
            ## Add to watchlist
            request.user.watchlist.listings.add(listing)
            request.user.save()

            data.update({"success_alert": "You have successfully added item to watchlist."})
        elif request.POST.get("remove", "") != "":
            ## Remove from watchlist
            request.user.watchlist.listings.remove(listing)
            request.user.save()
        elif request.POST.get("close", "") != "":
            ## Close listing
            listing.is_closed = True
            listing.save()
        elif request.POST.get("reopen", "") != "":
            ## Close listing
            listing.is_closed = False
            listing.save()

            data.update({"success_alert": "You have successfully removed item from watchlist."})
        elif request.POST.get("comment", "") != "":
            ## Upload a comment
            Comment.objects.create(
                auctionListing = listing,
                user = request.user,
                comment = request.POST.get("comment", "")
            )

            data.update({"success_alert": "You have successfully added a comment."})

    if request.user.is_authenticated:
        watchedListings = request.user.watchlist.listings.all()
    else:
        watchedListings = []
    comments = listing.comments.all()
    data.update({
        "listing": listing,
        "watchedListings": watchedListings,
        "comments": comments
    })
    return render(request, "auctions/listing.html", data)

def watchlist_view(request):
    listings = request.user.watchlist.listings.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def categoryList_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categoryList.html", {
        "categories": categories
    })

def category_view(request, category_pk):
    category = Category.objects.get(pk=category_pk)
    listings = category.listings.filter(is_closed=False)
    return render(request, "auctions/category.html", {
        "category": category.name,
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        watchlist = WatchList.objects.create(
            user = user,
        )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
