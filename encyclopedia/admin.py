from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *


class EntryHistoryAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Entry, EntryHistoryAdmin)
