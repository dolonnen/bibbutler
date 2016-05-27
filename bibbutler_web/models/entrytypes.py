from abc import ABC
from datetime import date, datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


class EntryType(models.Model):
    title = models.CharField(max_length=60)
    subtitle = models.CharField(max_length=60)
    urldate = models.DateField('url date',blank=True, default=timezone.now)
    url = models.URLField(blank=True, null=True)
    addendum = models.TextField(blank=True, max_length=200)
    note = models.TextField(blank=True, max_length=200)
    language = models.CharField(blank=True, max_length=15)
    PUBSTATE_CHOICES = (
        ('iprep', 'in preparation'),
        ('sbmit', 'submitted'),
        ('focom', 'forthcoming'),
        ('ipres', 'in press'),
        ('prpub', 'pre-published'),
    )
    pubstate = models.CharField(blank=True, max_length=5, choices=PUBSTATE_CHOICES, default=None)

    # required once of them
    date = models.DateField(blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(datetime.today().year, message='year is in future')])
    def clean(self):
        if not self.date and not self.year:
            raise ValidationError(_('one of the both fields date and year have to be set.'), code='requirements not set')
        super().clean()

    class Meta:
        abstract = True


class AuthorOrEditorRequired(models.Model):
    # required once of them
    author = models.CharField(blank=True, max_length=150)
    editor = models.CharField(blank=True, max_length=150)
    # editortype
    def clean(self):
        if not self.author and not self.editor:
            raise ValidationError(_('one of the both fields author and editor have to be set.'), code='requirements not set')
        super().clean()

    class Meta:
        abstract = True

# class EditorXAndType(models.Model):
#     raise NotImplementedError


class EntryType_Book(EntryType):
    author = models.CharField(max_length=150)
    editor = models.CharField(blank=True, max_length=150)
    publisher = models.CharField(blank=True, max_length=100)
    location = models.CharField(blank=True, max_length=100)
    isbn = models.CharField(blank=True, max_length=16)
    titleaddon = models.URLField(blank=True, null=True, max_length=60)

    def clean(self):
        super().clean()


class EntryType_Online(EntryType, AuthorOrEditorRequired):
    titleaddon = models.URLField(blank=True, null=True, max_length=60)
    version = models.CharField(blank=True, max_length=20)
    organization = models.CharField(blank=True, max_length=60)
    month = models.PositiveSmallIntegerField(blank=True, null=True, choices=MONTHS.items())

    def clean(self):
        super().clean()
# make url field required on online entry type
EntryType_Online._meta.get_field('url').blank = False
EntryType_Online._meta.get_field('url').null = False



entry_types = {
    'article' : EntryType_Online,
    'book' : EntryType_Book
}