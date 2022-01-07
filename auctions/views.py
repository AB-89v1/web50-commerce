from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.forms import ModelChoiceField, HiddenInput

from .models import User, Categories, Listings, Bids, Watchlists, posts

def index(request):
    listings = Listings.objects.filter(closed=False)
    
    bids = {}
    
    for listing in listings:
    
        try:
            bids[listing.title] = Bids.objects.filter(listing=listing).order_by('-bid')[0]
        except IndexError:
            bids[listing.title] = None
    
    return render(request, "auctions/index.html", {
        "listings": listings,
        "bids": bids
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

class NewListingForm(forms.Form):
    title = forms.CharField(label="*Listing Title:")
    description = forms.CharField(widget=forms.Textarea(),label="*Item Description:")
    image = forms.URLField(label="Image URL: ", required=False)
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label="*Category: ")
    start_bid = forms.DecimalField(decimal_places=2,initial="0.00",label="*Starting Bid: $")
    
class BidForm(forms.Form):
    bid = forms.FloatField(label="Place Bid: $")

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
        
def new_listing(request):
    if request.method == "POST":
#       Set values from POST
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        category = request.POST["category"]
        bid = request.POST["start_bid"]
        user = request.POST["username"]
        
#       Get category from Categories model
        category = Categories.objects.get(id=category)

#        Get user from User model
        seller=User.objects.get(username=user)
        
#       Add values to Listings
        Listings.objects.create(title=title, description=description,image=image,category=category,start_bid=bid,seller=seller)
        
#       Redirect to homepage
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_listing.html", {
            "listingform": NewListingForm
                      })
def listing(request, listing_id):

    listing = Listings.objects.get(pk=listing_id)
    watchlist = Watchlists.objects.filter(listing=listing)
    comments = posts.objects.filter(listing=listing).order_by('-time')
        
    try:
        bids = Bids.objects.filter(listing=listing).order_by('-bid')[0]
    except IndexError:
        bids = None
    
    
    watchers = []
    
    for item in watchlist:
        watchers.append(item.user)
    
    if request.method == "GET":
    
        if listing.closed == True:
            
            return render(request, "auctions/closed_listing.html", {
                "listing": listing,
                "bids": bids,
                "comments": comments,
                "watchers": watchers
                          })
        
        else:
        
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids": bids,
                "watchers": watchers,
                "bidform": BidForm,
                "comments": comments
                          })
    
    else:
        user = request.POST["user"]
        
        if request.POST["bid"] is not None:
            bid = request.POST["bid"]
            user = User.objects.get(username=user)
            Bids.objects.create(listing=listing,bidder=user,bid=bid)
            
            
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def watchlist(request):
    
    user = request.POST["user"]
    user = User.objects.get(username=user)
    
    listing = request.POST["listing"]
    listing = Listings.objects.get(pk=listing)
    
    if 'add' in request.POST:
        Watchlists.objects.create(user=user, listing=listing)
    elif 'remove' in request.POST:
        Watchlists.objects.filter(user=user, listing=listing).delete()
    
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
            
def comments(request):

    user = request.POST["user"]
    user = User.objects.get(username=user)
    
    listing = request.POST["listing"]
    listing = Listings.objects.get(pk=listing)
    
    comment = request.POST["comment"]
    
    posts.objects.create(user=user, listing=listing, comment=comment)
    
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    
def close_listing(request):
    
    listing = request.POST["listing"]
    listing = Listings.objects.get(pk=listing)
    
    listing.closed = True
    
    listing.save()
    
    return HttpResponseRedirect(reverse("listing", args=(listing.id,)))
    
def watchlist_page(request, username):

    user = User.objects.get(username=username)
    watchlist = Watchlists.objects.filter(user=user)
    
    bids = {}
    
    for item in watchlist:
        
        try:
            bids[item.listing.title] = Bids.objects.filter(listing=item.listing).order_by('-bid')[0]
        except IndexError:
            bids[item.listing.title] = None
        
        
    return render(request, "auctions/watchlist_page.html", {
        "watchlist": watchlist,
        "bids": bids
                  })
                  
def category_list(request):
    
    categories = Categories.objects.all()
    
    return render(request, "auctions/categories.html", {
        "categories": categories
                  })

def category_listings(request, category):

    category = Categories.objects.get(category=category)

    listings = Listings.objects.filter(category=category)
    
    bids = {}
    
    for listing in listings:
        
        try:
            bids[listing.title] = Bids.objects.filter(listing=listing).order_by('-bid')[0]
        except IndexError:
            bids[listing.title] = None
            
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings,
        "bids": bids
                  })
