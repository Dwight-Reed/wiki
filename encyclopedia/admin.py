from django.contrib import admin

from .models import *


class EntryHistoryAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Entry, EntryHistoryAdmin)
