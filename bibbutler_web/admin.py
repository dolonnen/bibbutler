from django.contrib import admin

from .models.entrytypes import EntryType_Book, EntryType_Online

# Register your models here.
admin.site.register(EntryType_Book)
admin.site.register(EntryType_Online)
