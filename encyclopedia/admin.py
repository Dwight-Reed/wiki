from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *
# TODO: Add full history to admin (currently only has changes made in admin interface)
class EntryHistoryAdmin(admin.ModelAdmin):
    list_display = ("title",)

admin.site.register(Entry, EntryHistoryAdmin)
