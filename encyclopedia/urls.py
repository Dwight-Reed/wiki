from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    # Normal pages
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki, name="wiki"),
    path("search/", views.search_results, name="search_results"),
    path("image/<str:name>/", views.image, name="image"),

    # Create
    path("new_page/", views.EntryCreateView.as_view(), name="new_page"),
    path("new_image/", views.ImageCreateView.as_view(), name="new_image"),

    # Edit
    path("wiki/<str:title>/edit/", views.EntryUpdateView.as_view(), name="edit"),

    # Auth
    path("login/", auth_views.LoginView.as_view(authentication_form=LoginForm, redirect_field_name=views.index), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # Other
    path("wiki/random/", views.random_page, name="random"),

    # API
    path("api/search/", views.search, name="search"),
]
