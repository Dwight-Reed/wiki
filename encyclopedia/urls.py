from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>/", views.wiki, name="wiki"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("wiki/random", views.random, name="random")
]
