from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from markdown import markdown
from random import choice

from . import util, wiki_syntax, diff_generator
from .forms import EntryContentUpdateForm, EntryCreateForm, \
    EntryTalkUpdateForm, ImageCreateForm, RegisterForm
from .models import Entry, Image, User


class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImageCreateForm

    # Fill title field when linked from a 404 page
    def get_initial(self):
        name = self.request.GET.get("name")
        return {
            "name": name,
        }

    def form_valid(self, form):
        # Save form for use when redirecting in self.get_success_url()
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        name = self.form.cleaned_data["name"]
        return reverse("image", args={name})


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryCreateForm

    def get_initial(self):
        title = self.request.GET.get("title")
        return {
            "title": title,
        }

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        title = self.form.cleaned_data["title"]
        return reverse("wiki", args={title})


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryContentUpdateForm
    template_name_suffix = "_update_form"

    # Set form based on title format
    # (EntryTalkUpdateForm if title starts with "wiki:")
    def get_form_class(self):
        is_talk = util.strip_title(self.kwargs.get("title"))[1]
        if is_talk:
            return EntryTalkUpdateForm
        return EntryContentUpdateForm

    # Set title for use in templates
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.kwargs.get("title")
        return context

    # Get object based on title (remove "talk:" prefix if necessary)
    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        title = self.kwargs.get("title")
        stripped_title = util.strip_title(title)[0]
        obj = queryset.get(title=stripped_title)
        return obj

    def get_success_url(self):
        return reverse("wiki", args={self.kwargs.get("title")})


def index(request):
    return render(request, "encyclopedia/index.html", {
        "titles": list(Entry.objects.values_list("title", flat=True)),
    })


def wiki(request, title):
    stripped_title, is_talk = util.strip_title(title)
    try:
        entry = Entry.objects.get(title__iexact=stripped_title)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(
            request, "encyclopedia/entry_not_found.html", {
                "title": stripped_title,
            }
        ))

    if is_talk:
        content = entry.talk
        template = "encyclopedia/talk.html"
    else:
        content = entry.content
        template = "encyclopedia/entry.html"

    # markdown raises an exception when the input is empty
    # (talk pages can be empty)
    if not content:
        content = "## This talk page has no content"

    processed_content = markdown(
        content,
        output_format="html5",
        extensions=[
            wiki_syntax.WikiSyntax(),
            "abbr",
            "attr_list",
            "codehilite",
            "fenced_code",
            "footnotes",
            "sane_lists",
            "tables",
            "toc",
        ],
    )

    return render(request, template, {
        "title": title,
        "content": processed_content,
    })


def history(request, title):
    stripped_title, is_talk = util.strip_title(title)
    hist = []
    # To determine if a change was made to the talk or the content page,
    # check which field changed since the last record
    for record in Entry.objects.get(title=stripped_title).history.all():
        try:
            if is_talk:
                if record.talk != record.prev_record.talk:
                    hist.append(record)
            elif record.content != record.prev_record.content:
                hist.append(record)
        except AttributeError:
            if is_talk:
                if record.talk:
                    hist.append(record)
            else:
                hist.append(record)

    return render(request, "encyclopedia/history.html", {
        "title": title,
        "history": hist,
    })


def history_diff(request, title, pk):
    stripped_title, is_talk = util.strip_title(title)
    record = Entry.objects.get(title=stripped_title).history.get(pk=pk)
    if is_talk:
        try:
            new = record.talk.splitlines()
        except AttributeError:
            new = ""
        try:
            old = record.prev_record.talk.splitlines()
        except AttributeError:
            old = ""
    else:
        new = record.content.splitlines()
        try:
            old = record.prev_record.content.splitlines()
        except AttributeError:
            old = ""

    d = diff_generator.CustomHtmlDiff()
    output = d.make_table(old, new, context=True, numlines=2)
    return render(request, "encyclopedia/diff.html", {
        "title": title,
        "diff": output,
    })


def image(request, name):
    try:
        image = Image.objects.get(name=name)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(
            request, "encyclopedia/image_not_found.html", {
                "name": name,
            }
        ))

    return render(request, "encyclopedia/image.html", {
        "image": image,
    })


def search_results(request):
    query = request.GET.get("q")
    results = util.generic_search(query)
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results,
        "result_count": len(results),
    })


def search(request):
    query = request.GET.get("q")

    results = list(Entry.objects.filter(
        title__icontains=query).values_list("title", flat=True))
    return JsonResponse({"results": results})


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
