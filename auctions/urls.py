from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("comments", views.comments, name="comments"),
    path("close", views.close_listing, name="close_listing"),
    path("watchlist/<username>", views.watchlist_page, name="watchlist_page"),
    path("categories", views.category_list, name="category_list"),
    path("categories/<category>", views.category_listings, name="category_listings")
]
