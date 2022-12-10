import re

from django.db.models import Q
from .models import Entry


# Returns a list of page titles where either the title or content contain the query (titles come first)
# Used for the search page and API
def generic_search(query):
    # https://stackoverflow.com/a/66060106/15843982
    results = Entry.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return list(results.values_list("title", flat=True))


# Removes 'talk:' prefix from title
def strip_title(title) -> tuple[str, int]:
    return re.subn(r"^talk:", "", title, re.IGNORECASE)
