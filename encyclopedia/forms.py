from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.utils.translation import gettext_lazy as _

from .models import Entry, Image, User


class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Content",
        "class": "form-control row content",
        }), label="")


class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Title",
                "class": "form-control row header",
            }),
            "content": forms.Textarea(attrs={
                "placeholder": "Content",
                "class": "form-control row content",
            }),
        }

        labels = {
            "title": "",
            "content": "",
        }


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image

        fields = ["name", "image"]
        # fields = ["image"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "name",
                "class": "form-control",
                "autofocus": "true"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }

        labels = {
            "name": "",
            "image": "",
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "placeholder": "username",
        "class": "form-control",
        "autofocus": "true",
    }),
        label="",
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "password",
        "class": "form-control",
    }),
        label="",
    )

    class Meta(UserCreationForm.Meta):
        model = User


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "password",
        "class": "form-control",
    }),
        strip=False,
        label="",
    )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "confirm password",
        "class": "form-control",
    }),
        strip=False,
        label="",
    )
    class Meta():
        model = User
        fields = ["username", "email"]
        field_classes = {"username": UsernameField}
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "username",
                "class": "form-control",
            }),
            "email": forms.TextInput(attrs={
                "placeholder": "email",
                "class": "form-control",
            }),
        }
        labels = {
            "username": "",
            "email": "",
        }
        help_texts = {
            "username": "150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        }
