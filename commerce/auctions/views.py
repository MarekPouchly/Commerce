from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Message, Bid


def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories
    })


def select_category(request):
    if request.method == "POST":
        formCategory = request.POST["category"]
        category = Category.objects.get(categoryName = formCategory)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activeListings,
            "categories": allCategories
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


def register(request):
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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            price = request.POST["bid"]
            imageUrl = request.POST["imageUrl"]
            category = request.POST["category"]
            
            # who is the user
            currentUser = request.user

            # create a bid
            bid = Bid(
                bid=float(price),
                user=currentUser
            )
            bid.save()

            category_data = Category.objects.get(categoryName=category)
            # create the object
            newListing = Listing(
                title=title,
                description=description,
                bid = bid,
                imageUrl = imageUrl,
                category = category_data,
                owner = currentUser
            )

            # save the object
            newListing.save()

            # redirect to index page
            return HttpResponseRedirect(reverse("index"))

        return render(request, "auctions/create_listing.html", {
            "categories": Category.objects.all()
        })
    else:
        return render(request, "auctions/login.html", {
            "message": "You have to login first to create listings."
        })

def listing_details(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listingInWatchlist = request.user in listing.watchlist.all()
    comments = listing.comments_section.all()
    isOwner = request.user.username == listing.owner.username

    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "listingInWatchlist": listingInWatchlist,
        "comments": comments,
        "isOwner": isOwner
    })

def addWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing_details", args=(id, )))

def removeWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing_details", args=(id, )))

def watchlist(request):
    user = request.user
    listings = user.watchlisted.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def addComment(request, id):
    author = request.user
    listing = Listing.objects.get(pk=id)
    comment = request.POST["addComment"]

    newComment = Message(
        author=author,
        listing=listing,
        message=comment
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing_details", args=(id, )))

def makeBid(request, id):
    bidder = request.user
    listing = Listing.objects.get(pk=id)
    bid = request.POST["make_a_bid"]
    listingInWatchlist = request.user in listing.watchlist.all()
    comments = listing.comments_section.all()
    isOwner = request.user.username == listing.owner.username

    if float(bid) > listing.bid.bid:
        newBid = Bid(
            user=bidder,
            bid=bid
        )
        newBid.save()
        listing.bid = newBid
        listing.save()

        return render(request, "auctions/listing_details.html", {
            "listing": listing,
            "listingInWatchlist": listingInWatchlist,
            "comments": comments,
            "alert": "Bid was updated successfully!",
            "updated": True,
            "isOwner": isOwner
        })
    else:
        return render(request, "auctions/listing_details.html", {
            "listing": listing,
            "listingInWatchlist": listingInWatchlist,
            "comments": comments,
            "alert": "Bid wasn't updated successfully! Might be lower than price.",
            "updated": False,
            "isOwner": isOwner
        })

def closeListing(request, id):
    listing = Listing.objects.get(pk=id)
    listing.isActive = False
    listing.save()
    isOwner = request.user.username == listing.owner.username
    listingInWatchlist = request.user in listing.watchlist.all()
    comments = listing.comments_section.all()

    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "listingInWatchlist": listingInWatchlist,
        "comments": comments,
        "alert": "You closed the auction",
        "updated": True,
        "isOwner": isOwner
    })