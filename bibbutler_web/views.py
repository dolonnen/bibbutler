from django.views.generic import TemplateView, ListView, DetailView
from bibbutler_web.models.general import Bibliography
from bibbutler_web.models.entry import *


class IndexView(TemplateView):
    template_name = 'bibbutler_web/index.html'


class BibListView(ListView):
    template_name = 'bibbutler_web/bib_list.html'
    model = Bibliography


class BibDetailView(DetailView):
    template_name = 'bibbutler_web/bib_detail.html'
    model = Bibliography


class EntryListView(ListView):
    template_name = 'bibbutler_web/entry_list.html'
    model = Entry


class EntryDetailView(DetailView):
    template_name = 'bibbutler_web/entry_detail.html'
    model = Entry
    context_object_name = 'entry'