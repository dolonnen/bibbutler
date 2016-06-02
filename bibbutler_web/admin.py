from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin

from .models.general import Bibliography
from .models.entry import *


class EntryChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = Entry

    # By using these `base_...` attributes instead of the regular ModelAdmin `form` and `fieldsets`,
    # the additional fields of the child models are automatically added to the admin form.
    base_form = ...
    base_fieldsets = (
        ...
    )


class EntryBookAdmin(EntryChildAdmin):
    base_model = EntryBook


class EntryOnlineAdmin(EntryChildAdmin):
    base_model = EntryOnline


class EntryParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = Entry
    child_models = (
        (EntryBook, EntryBookAdmin),
        (EntryOnline, EntryOnlineAdmin),
    )


# Register your models here.
admin.site.register(Bibliography)
for entry_type in entry_types.values():
    admin.site.register(entry_type)

# admin.site.register(Entry, EntryParentAdmin)
