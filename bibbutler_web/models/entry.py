from django.db import models
from .bibtex_key import get_bibtex_key
from polymorphic.models import PolymorphicModel
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.urlresolvers import reverse


class Entry(PolymorphicModel):
    bibliography = models.ForeignKey('Bibliography', on_delete=models.CASCADE, editable=True)

    title = models.CharField(max_length=300)
    subtitle = models.CharField(blank=True, max_length=300)
    # addendum = models.TextField(blank=True, max_length=200)
    # note = models.TextField(blank=True, max_length=200)
    language = models.CharField(blank=True, max_length=15)
    # PUBSTATE_CHOICES = (
    #     ('iprep', 'in preparation'),
    #     ('sbmit', 'submitted'),
    #     ('focom', 'forthcoming'),
    #     ('ipres', 'in press'),
    #     ('prpub', 'pre-published'),
    # )
    # pubstate = models.CharField(blank=True, max_length=5, choices=PUBSTATE_CHOICES, default='')

    ## required once of them
    date = models.DateField(blank=True, null=True, default=timezone.now)
    year = models.PositiveSmallIntegerField(blank=True, null=True, default=timezone.now().year, validators=[MaxValueValidator(timezone.now().year, message=_('year is in future'))])

    class Meta:
        verbose_name = _('Generic entry')
        verbose_name_plural = _('Generic entries')

    def clean(self):
        if not self.date and not self.year:
            raise ValidationError(_('one of the both fields date and year have to be set.'), code='requirements not set')
        super().clean()

    def get_absolute_url(self):
        return reverse('entry_detail', args=[self.id])

    def get_bibtex_key(self):
        # if self.manual_bibtex_key:
        #     return self.manual_bibtex_key
        return get_bibtex_key(self)


    def get_fields(self):
        return self._meta.get_fields()

    def get_attributes_without_id_and_relations(self):
        blacklist = ('id', 'polymorphic_ctype_id', 'bibliography_id', 'entry_ptr_id')
        for field in self.get_fields():
            if field.attname not in blacklist:
                yield field.verbose_name, getattr(self, field.name)

    @classmethod
    def get_subentrytypes(cls):
        for subentrytyp in cls.__subclasses__():
            yield from subentrytyp.get_subentrytypes()
            yield subentrytyp


class AuthorOrEditorRequired(models.Model):
    # required once of them
    author = models.CharField(blank=True, max_length=200)
    editor = models.CharField(blank=True, max_length=200)
    # editortype

    def clean(self):
        if not self.author and not self.editor:
            raise ValidationError(_('one of the both fields author and editor have to be set.'), code='requirements not set')
        super().clean()

    class Meta:
        abstract = True


class EntryBook(Entry):
    author = models.CharField(max_length=200)
    editor = models.CharField(blank=True, max_length=200)
    publisher = models.CharField(blank=True, max_length=200)
    url = models.URLField(blank=True, null=True)
    urldate = models.DateField('url date', blank=True, null=True)
    location = models.CharField(blank=True, max_length=200)
    isbn = models.CharField(blank=True, max_length=17)
    titleaddon = models.URLField(blank=True, null=True, max_length=60)

    def __str__(self):
        return self.title + ', ' + self.author

    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')

    def clean(self):
        super().clean()


class EntryOnline(Entry, AuthorOrEditorRequired):
    titleaddon = models.CharField(blank=True, null=True, max_length=60)
    version = models.CharField(blank=True, max_length=20)
    url = models.URLField(blank=False, null=True)
    urldate = models.DateField('url date', blank=True, null=True)
    organization = models.CharField(blank=True, max_length=60)
    month = models.PositiveSmallIntegerField(blank=True, null=True, choices=MONTHS.items())

    def __str__(self):
        return self.title + ', ' + self.author if self.author else self.editor

    class Meta:
        verbose_name = _('online')
        verbose_name_plural = _('online entries')

    def clean(self):
        super().clean()


class EntryManual(Entry, AuthorOrEditorRequired):
    organization = models.CharField(blank=True, max_length=60)
    titleaddon = models.CharField(blank=True, null=True, max_length=60)
    version = models.CharField(blank=True, max_length=20)
    url = models.URLField(blank=True, null=True)
    urldate = models.DateField('url date', blank=True, null=True)
    isbn = models.CharField(blank=True, max_length=17)

    def __str__(self):
        return self.title + ', ' + self.organization if self.organization else (self.author if self.author else self.editor)

    class Meta:
        verbose_name = _('manual')
        verbose_name_plural = _('manuals')

    def clean(self):
        super().clean()


class EntryMisc(Entry, AuthorOrEditorRequired):
    howpublished = models.CharField(blank=True, null=True, max_length=60)
    titleaddon = models.CharField(blank=True, null=True, max_length=60)
    version = models.CharField(blank=True, max_length=20)
    url = models.URLField(blank=True, null=True)
    urldate = models.DateField('url date', blank=True, null=True)
    organization = models.CharField(blank=True, max_length=60)

    def __str__(self):
        return self.title + ', ' + self.organization if self.organization else (self.author if self.author else self.editor)

    class Meta:
        verbose_name = _('misc')
        verbose_name_plural = _('misc entries')

    def clean(self):
        super().clean()


entry_types = {
    'book': EntryBook,
    'manual': EntryManual,
    'misc': EntryMisc,
    'online': EntryOnline
}