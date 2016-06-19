from django.views.generic import View, TemplateView, ListView, DetailView, UpdateView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from bibbutler_web.models.general import Bibliography
from bibbutler_web.models.entry import *
from bibbutler_web.tools import duplicate_bib


class IndexView(TemplateView):
    template_name = 'bibbutler_web/index.html'


class BibListView(ListView):
    template_name = 'bibbutler_web/bib_list.html'
    model = Bibliography


class BibDetailView(DetailView):
    template_name = 'bibbutler_web/bib_detail.html'
    model = Bibliography

    def get_context_data(self, **kwargs):
        context = super(BibDetailView, self).get_context_data(**kwargs)
        entry_list = Entry.objects.filter(bibliography_id=self.kwargs['pk'])
        context['bibtex_generate'] = render_to_string('bibbutler_web/bibliography.html', {'entry_list': entry_list})
        return context


class EntryListView(ListView):
    template_name = 'bibbutler_web/entry_list.html'
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(bibliography_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(EntryListView, self).get_context_data(**kwargs)
        bib = Bibliography.objects.get(id=self.kwargs['pk'])
        context['bib'] = bib
        return context


class EntryDetailView(DetailView):
    template_name = 'bibbutler_web/entry_detail.html'
    model = Entry
    context_object_name = 'entry'


class EntryEditView(UpdateView):
    template_name = 'bibbutler_web/entry_edit_form.html'
    queryset = Entry.objects.all()
    fields = '__all__'


class EntryCreateView(CreateView):
    template_name = 'bibbutler_web/entry_create_form.html'
    fields = '__all__'

    def get_queryset(self):
        return entry_types[self.request.GET['entrytype']].objects.all()

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        entry_class = entry_types[self.request.GET['entrytype']]
        context['entry_type'] = entry_class._meta.verbose_name
        return context


class EntryDeleteView(View):
    def get(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=kwargs['pk'])
        bib_id = entry.bibliography_id
        entry.delete()

        return redirect('entry_list', pk=bib_id)


class BibCreateView(CreateView):
    template_name = 'bibbutler_web/bib_create_form.html'
    model = Bibliography
    fields = '__all__'


class BibDeleteView(View):
    def get(self, request, *args, **kwargs):
        bib = get_object_or_404(Bibliography, pk=kwargs['pk'])
        bib.delete()
        return redirect('bib_list')


class BibDuplicateView(View):
    def get(self, request, *args, **kwargs):
        old_bib = get_object_or_404(Bibliography, pk=kwargs['pk'])
        duplicate_bib(old_bib)
        return redirect('bib_list')


class BibGenerateView(ListView):
    template_name = 'bibbutler_web/bibliography.html'
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(bibliography_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BibGenerateView, self).get_context_data(**kwargs)
        bib = Bibliography.objects.get(id=self.kwargs['pk'])
        context['bib'] = bib
        return context
