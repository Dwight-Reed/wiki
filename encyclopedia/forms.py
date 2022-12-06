from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Content",
        # TODO: move to styles.css
        "style": "width: 100%; max-height: 100%;",
        "rows": "100",
        "class": "form-control",
        }), label="")

class NewPageForm(EditForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title"}), label="")

    # place title before content
    field_order = ["title", "content"]

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
