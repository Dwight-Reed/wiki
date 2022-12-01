from django import forms
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from markdown2 import markdown
from os import listdir
from os.path import splitext
from random import choice
from . import util

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


def search(request):

    query = request.GET.get('q', '')
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

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Content", "style": "width: 100%; max-height: 100%;", "rows": "100"}), label="")

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
