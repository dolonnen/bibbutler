from bibbutler_web.models.general import Bibliography
from bibbutler_web.models.entry import *
from django.utils import timezone

def duplicate_bib(old_bib):
    new_bib = Bibliography()
    new_bib.document_name = old_bib.document_name
    new_bib.document_url = old_bib.document_url
    new_bib.addition = old_bib.addition + '_copy'
    # new_bib.date = timezone.now
    new_bib.save()

    for old_entry in Entry.objects.filter(bibliography=old_bib):
        new_entry = old_entry
        new_entry.bibliography = new_bib
        new_entry.id = None
        new_entry.pk = None
        new_entry.save()