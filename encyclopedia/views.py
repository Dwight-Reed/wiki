from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from os import listdir
from os.path import splitext
from random import choice

from . import util
from .models import Entry, User

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    content = util.get_entry(entry)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": markdown(content)
        })
    else:
        return HttpResponseNotFound(render(request, "encyclopedia/not_found.html", {
        "entry": entry
        }))


def search2(request):

    query = request.GET.get("q", "")
    content = util.get_entry(query)
    if content:
        return HttpResponseRedirect(f"wiki/{query}")
    else:
        results = []
        for entry in util.list_entries():
            if entry.lower().find(query.lower()) != -1:
                results.append(entry)

        return render(request, "encyclopedia/search.html", {
            "query": query,
            "results": results,
            "result_count": len(results)
        })

def search(request):
    query = request.GET.get("q")

    results = list(Entry.objects.filter(title__icontains=query).values_list("title", flat=True))
    return JsonResponse({"results": results})

# TODO: remove
def test_search(request):
    return render(request, "encyclopedia/search.html")

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

    # check if page already exists
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")

        if util.get_entry(title):
            self.add_error("title", f'Page "{title}" already exists')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "username",
        "class": "form-control",
    }),
        label="",
    )

    password = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "password",
        "class": "form-control",
        "type": "password",
    }),
        label="",
    )

class RegisterForm(LoginForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "placeholder": "email",
        "class": "form-control",
    }),
        label="",
    )
    confirm = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "confirm password",
        "class": "form-control",
        "type": "password",
    }),
        label="",
    )
    field_order = ["username", "email", "password", "confirm"]


@login_required
def new_page(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)

        # validate form
        if form.is_valid():
            form.clean()
            if form.errors:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form
                })

            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            # write file to disk
            with open(f"entries/{title}.md", "w") as file:
                file.write(content)

            return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })

    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })

@login_required
def edit(request, entry):
    if request.method == "POST":
        form = EditForm(request.POST)

        # validate form
        if form.is_valid():
            content = form.cleaned_data["content"]
            entry = form.data["entry"]

            # write file to disk
            with open(f"entries/{entry}.md", "w") as file:
                file.write(content)

            return HttpResponseRedirect(f"wiki/{entry}")
        else:
            print(form)
            print("Invalid Form")
            print(form.errors)
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })

    else:
        return render(request, "encyclopedia/edit.html", {
            "form": EditForm({
                "content": util.get_entry(entry)
            }),
            "entry": entry
        })

# random page
def random(request):
    return HttpResponseRedirect(reverse("wiki", args={
            splitext(choice(listdir("entries")))[0]
        }))

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if not form.is_valid():
            # TODO: replace generic invalid form when possible (e.g. invalid email)
            return render(request, "registration/register.html", {
                "message": "Invalid Form",
            })
        username = form.data["username"]
        email = form.data["email"]
        password = form.data["password"]
        confirm = form.data["confirm"]

        if password != confirm:
            # TODO: don't reload page
            return render(request, "registration/register.html", {
                "message": "Passwords must match",
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "registration/register.html", {
                "message": "Username is already taken"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "registration/register.html", {
        "form": RegisterForm(),
    })

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "registration/login.html", {
                "message": "invalid form",
                "form": form,
            })

        user = authenticate(request, username=form.data["username"], password=form.data["password"])
        print("user:", user)
        if user == None:
            print("user is None")
            return render(request, "registration/login.html", {
                "message": "Incorrect username or password",
                "form": form,
            })
        else:
            login(request, user)


        return HttpResponseRedirect(reverse("index"))

    return render(request, "registration/login.html", {
        "form": LoginForm(),
    })



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
