from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list_product", views.list_product, name="list_product"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path('watchlist', views.watchlist, name="watchlist")
]
