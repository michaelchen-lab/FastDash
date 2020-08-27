from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search-results", views.search, name="search"),
    path("create", views.createPage, name="createPage"),
    path("edit/<title>", views.editPage, name="editPage"),
    path("random", views.randomPage, name="random"),
    path("<title>", views.wikiPage, name="wikiPage")
]
