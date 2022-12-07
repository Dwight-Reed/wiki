from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from markdown2 import markdown
from random import choice

from . import util
from .forms import EditForm, ImageCreateForm, NewPageForm, LoginForm, RegisterForm
from .models import Entry, Image, User


class ImageCreateView(CreateView):
    # template_name="encyclopedia/image_form.html"
    model = Image
    form_class = ImageCreateForm
    # fields = ["name", "image"]

    def get_success_url(self):
        return reverse("index")

    def get_initial(self):
        name = self.request.GET.get("name")
        return {
            "name": name,
        }


def index(request):
    return render(request, "encyclopedia/index.html", {
        "titles": list(Entry.objects.all().values_list("title", flat=True)),
    })


def wiki(request, title):
    try:
        content = Entry.objects.get(title=title).content
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "encyclopedia/entry_not_found.html", {
            "title": title,
        }))
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        # TODO: Check what safe mode allows
        "content": markdown(content, safe_mode=True)
    })


def image(request, name):
    try:
        image = Image.objects.get(name=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, "encyclopedia/image_not_found.html", {
            "name": name,
        }))

    return render(request, "encyclopedia/image.html", {
        "image": image
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


def random_page(request):
    result = choice(Entry.objects.values_list("title", flat=True))
    return HttpResponseRedirect(reverse("wiki", args={result}))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.data.get("username")
            email = form.data.get("email")
            password = form.data.get("password1")
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        return render(request, "registration/register.html", {
            "form": form,
        })

    return render(request, "registration/register.html", {
        "form": RegisterForm(),
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
