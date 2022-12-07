from django.conf.urls import include
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.index, name="index"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("search", views.search_results, name="search_results"),
    path("new_page", views.new_page, name="new_page"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/random", views.random_page, name="random"),
    path("login", auth_views.LoginView.as_view(authentication_form=LoginForm, redirect_field_name=views.index), name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # API
    path("api/search", views.search, name="search"),
]
