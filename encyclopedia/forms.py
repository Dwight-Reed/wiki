from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import Entry, Image, User


class EntryContentUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "placeholder": "Content",
                "class": "form-control row content",
            }),
        }
        labels = {
            "content": "",
        }

    # This prevents the history field from tracking edits that changed nothing
    def clean_content(self):
        data = self.cleaned_data["content"]
        if data == self.instance.content:
            raise ValidationError("Content was not modified")
        return data


class EntryTalkUpdateForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["talk"]
        widgets = {
            "talk": forms.Textarea(attrs={
                "placeholder": "Content",
                "class": "form-control row content",
            }),
        }
        labels = {
            "talk": "",
        }

    def clean_talk(self):
        data = self.cleaned_data["talk"]
        if data == self.instance.talk:
            raise ValidationError("Content was not modified")
        return data


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

        validators = [
            # Prevent title from conflicting with "talk:" prefix
            RegexValidator("\:", inverse_match=True),
        ]


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image

        fields = ["name", "image"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "name",
                "class": "form-control",
                "autofocus": "true",
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
