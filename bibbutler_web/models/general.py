from django.db import models
from bibbutler_web.models.entrytypes import *


class User(models.Model):
    first_name = models.CharField("user's first name", max_length=30, blank=True)
    last_name = models.CharField("user's last name", max_length=30, blank=True)
    username = models.CharField(max_length=30, db_index=True)


class Bibliography(models.Model):
    document_name = models.CharField(max_length=50, db_index=True, help_text="The name of the document in which this bibliography is needed")
    document_url = models.URLField(help_text="The url of the document in which this bibliography is needed")

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)


class Entry(models.Model):
    biblatex_key = models.CharField(max_length=40, unique=True, db_index=True)

    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE)
    entry_type = models.ForeignKey(EntryType, on_delete=models.CASCADE)
