from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("create_listing", views.createListing_view, name="createListing"),
    path("listing/<listing_pk>", views.listing_view, name="viewListing"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("category", views.categoryList_view, name="categoryList"),
    path("category/<category_pk>", views.category_view, name="category")
]
