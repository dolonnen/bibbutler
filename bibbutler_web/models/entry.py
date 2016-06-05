from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils.translation import ugettext_lazy as _
from django.utils.dates import MONTHS
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


class Entry(PolymorphicModel):
    bibliography = models.ForeignKey('Bibliography', on_delete=models.CASCADE)

    title = models.CharField(max_length=60)
    subtitle = models.CharField(blank=True, max_length=60)
    url = models.URLField(blank=True, null=True)
    urldate = models.DateField('url date', blank=True, null=True)
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
    pubstate = models.CharField(blank=True, max_length=5, choices=PUBSTATE_CHOICES, default='')

    # required once of them
    date = models.DateField(blank=True, null=True, default=timezone.now)
    year = models.PositiveSmallIntegerField(blank=True, null=True, default=timezone.now().year, validators=[MaxValueValidator(timezone.now().year, message=_('year is in future'))])

    class Meta:
        verbose_name = _('Generic entry')
        verbose_name_plural = _('Generic entries')

    def clean(self):
        if not self.date and not self.year:
            raise ValidationError(_('one of the both fields date and year have to be set.'), code='requirements not set')
        super().clean()

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
    author = models.CharField(blank=True, max_length=150)
    editor = models.CharField(blank=True, max_length=150)
    # editortype

    def clean(self):
        if not self.author and not self.editor:
            raise ValidationError(_('one of the both fields author and editor have to be set.'), code='requirements not set')
        super().clean()

    class Meta:
        abstract = True


class EntryBook(Entry):
    author = models.CharField(max_length=150)
    editor = models.CharField(blank=True, max_length=150)
    publisher = models.CharField(blank=True, max_length=100)
    location = models.CharField(blank=True, max_length=100)
    isbn = models.CharField(blank=True, max_length=17)
    titleaddon = models.URLField(blank=True, null=True, max_length=60)

    def __str__(self):
        return self.title + ', ' + self.author

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def clean(self):
        super().clean()


class EntryOnline(Entry, AuthorOrEditorRequired):
    titleaddon = models.URLField(blank=True, null=True, max_length=60)
    version = models.CharField(blank=True, max_length=20)
    organization = models.CharField(blank=True, max_length=60)
    month = models.PositiveSmallIntegerField(blank=True, null=True, choices=MONTHS.items())

    def __str__(self):
        return self.title + ', ' + self.author if self.author else self.editor

    class Meta:
        verbose_name = _('Online')
        verbose_name_plural = _('Online entrys')

    def clean(self):
        super().clean()

# make url field required on online entry type
EntryOnline._meta.get_field('url').blank = False
EntryOnline._meta.get_field('url').null = False


entry_types = {
    'book': EntryBook,
    'online': EntryOnline
}