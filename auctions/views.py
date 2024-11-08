from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import User, Listings, Bids, Comments, Watchlist
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

            listing = Listings(title=title, description=description,
                                price=price, image_url=image_url,
                                posted_date=timezone.now())
            listing.save()
            messages.success(request, 'Added to Watchlist succesfuly')
            return redirect('index')

    return render(request, "auctions/list_product.html", context)

def listing_page(request, listing_id):
    try:    
        listing = Listings.objects.get(id=listing_id)
    except Listings.DoesNotExist:
        return render(request, "auctions/not_found.hmtl")
        
    in_list = False
    if request.user.is_authenticated:
        item = request.POST.get('listing_id')
        listing_instance = Listings.objects.get(id=item)
        is_in_watchlist = Watchlist.objects.filter(watchlist_owner=request.user, item=listing_instance).exists()
        if is_in_watchlist:
            in_list = True
        if request.method == "POST":
            action = request.POST.get('action')
            if in_list and action == 'remove':
                Watchlist.objects.filter(watchlist_owner=request.user, item=listing_instance).delete()
                messages.success(request, 'Remove From Wathclist Succesfully')
            elif not in_list and action == 'add':
                watchlist = Watchlist(item=listing_instance, watchlist_owner=request.user)
                watchlist.save()
                messages.success(request, 'Added to Watchlist succesfuly')
                return redirect('watchlist')

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "in_list": in_list
    })


def watchlist(request):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(watchlist_owner=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })