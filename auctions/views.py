from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone


from .models import User, Listings, Bids, Comments, Watchlist, Winners
from .forms import ListingsForm


def index(request):
    listings = Listings.objects.all()      
    return render(request, "auctions/index.html", {
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

def list_product(request):
    context = {}
    context['form'] = ListingsForm()

    if request.method == 'POST':
        form = ListingsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            image_url = form.cleaned_data['image_url']

            listing = Listings(title=title, owner=request.user, description=description,
                                price=price, image_url=image_url,
                                posted_date=timezone.now(),
                                open=True)
            listing.save()
            messages.success(request, 'Added to Watchlist succesfuly')
            return redirect('index')

    return render(request, "auctions/list_product.html", context)

def listing_page(request, listing_id):
    listing = get_object_or_404(Listings, id=listing_id)
    in_list = False
    winner = False

    # Check user is signed in
    if request.user.is_authenticated:
        # Check wheather listing is watchlist already
        is_in_watchlist = Watchlist.objects.filter(watchlist_owner=request.user, item=listing).exists()
        if is_in_watchlist:
            in_list = True
        if request.method == "POST":
            action = request.POST.get('action')
            if in_list and action == 'remove':
                Watchlist.objects.filter(watchlist_owner=request.user, item=listing).delete()
                messages.success(request, 'Remove From Wathclist Succesfully')
                return redirect('listing_page', listing_id=listing_id)
            elif not in_list and action == 'add':
                watchlist = Watchlist(item=listing, watchlist_owner=request.user)
                watchlist.save()
                messages.success(request, 'Added to Watchlist succesfuly')
                return redirect(reverse('listing_page', args=[listing_id]))
            to_bid = request.POST.get('to_bid')
            if to_bid == 'bid':
                bid = float(request.POST.get('bid'))
                bidding(request, listing_id, request.user, bid)
                return redirect(reverse('listing_page', args=[listing_id]))
            to_close = request.POST.get('to_close') 
            if to_close == 'close':
                close_auction(request, listing_id, request.user, listing.owner)
                winner = True
    if listing.open:
        return render(request, "auctions/listing_page.html", {
            "listing": listing,
            "in_list": in_list,
            "winner": winner,
            "owner": listing.owner
        })

def close_auction(request, listing_id, current_user, bidder):
    listing = Listings.objects.get(id=listing_id)
    print("Check current user and owner",current_user, listing.owner)
    if current_user == listing.owner:
        print("Check current user and owner",current_user, listing.owner)
        winner = Winners(winner=bidder, listing_won=listing)
        listing.open = False
        listing.save()
        winner.save()
    else:
        print("You are not the owner")
        
def bidding(request, listing_id, bidder, bid):

    listing = Listings.objects.get(id=listing_id)
    if bid <= listing.price:
        messages.warning(request, "Your bid is lower than current price or bet")
        return redirect(reverse('listing_page', args=[listing_id]))
    else:
        bid = Bids(bid=bid, bidder=bidder, listing=listing)
        bid.save()
        new_bid = Bids.objects.get(id=bid.id)
        listing.price = new_bid.bid
        listing.save()
        messages.success(request, "Your bid was successfully submitted!")


def watchlist(request):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(watchlist_owner=request.user)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })