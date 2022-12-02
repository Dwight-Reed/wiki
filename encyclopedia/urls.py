from django.conf.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("wiki/<str:entry>/", views.wiki, name="wiki"),
    # path("search", views.search2, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("wiki/random", views.random, name="random"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # TODO: remove
    path("testsearch", views.test_search, name="testsearch"),

    # API
    path("search", views.search, name="search"),
]
