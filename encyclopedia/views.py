from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from os import listdir
from os.path import splitext
from random import choice

from . import util
from .forms import EditForm, NewPageForm, LoginForm, RegisterForm
from .models import Entry, User

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_old(request, entry):
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

def wiki(request, title):
    try:
        content = Entry.objects.get(title=title).content
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "encyclopedia/not_found.html", {
            "title": title,
        }))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        # TODO: Check what safe mode allows
        "content": markdown(content, safe_mode=True)
    })


def search_results_old(request):

    query = request.GET.get("q")
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


def search_results(request):
    query = request.GET.get("q")
    results = util.generic_search(query)
    title_matches = list(Entry.objects.filter(title__icontains=query).values_list("title", flat=True).order_by("title"))
    content_matches = list(Entry.objects.filter(content__icontains=query).values_list("title", flat=True))
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results,
        "result_count": len(results)
    })

def search(request):
    query = request.GET.get("q")

    results = list(Entry.objects.filter(title__icontains=query).values_list("title", flat=True))
    return JsonResponse({"results": results})

@login_required
def new_page_old(request):

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

# TODO: Create new page link broken when not logged in
@login_required
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.data["title"]
            content = form.data["content"]
            if Entry.objects.filter(title=title).exists():
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "message": f'Page "{title}" already exists',
                })

            Entry.objects.create(title=title, content=content)
            return HttpResponseRedirect(reverse("wiki", args={title}))

        return render(request, "encyclopedia/new_page.html", {
            "form": form,
            "message": "Invalid form",
        })

    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm(),
    })

@login_required
def edit_old(request, entry):
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

@login_required
def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            content = form.data["content"]
            entry = Entry.objects.get(title=title)
            entry.content = content
            entry.save()
            return HttpResponseRedirect(reverse("wiki", args={title}))
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            # TODO: don't use generic message
            "message": "invalid form",
        })


    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": EditForm({
            "content": Entry.objects.get(title=title).content
        })
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
                "form": form,
                "message": "Invalid Form",
            })
        username = form.data["username"]
        email = form.data["email"]
        password = form.data["password"]
        confirm = form.data["confirm"]

        if password != confirm:
            # TODO: don't reload page
            return render(request, "registration/register.html", {
                "form": form,
                "message": "Passwords must match",
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "registration/register.html", {
                "form": form,
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
        if user == None:
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
