from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_details, name="listing_details"),
    path("select_category", views.select_category, name="select_category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("makeBid/<int:id>", views.makeBid, name="makeBid"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing")
]
