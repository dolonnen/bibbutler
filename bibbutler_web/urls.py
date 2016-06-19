from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^bib/$', views.BibListView.as_view(), name='bib_list'),
    url(r'^bib/new/$', views.BibCreateView.as_view(), name='new_bib'),
    url(r'^bib/(?P<pk>[0-9]+)/$', views.BibDetailView.as_view(), name='bib_detail'),
    url(r'^bib/(?P<pk>[0-9]+)/delete/$', views.BibDeleteView.as_view(), name='bib_delete'),
    url(r'^bib/(?P<pk>[0-9]+)/duplicate/$', views.BibDuplicateView.as_view(), name='bib_duplicate'),
    url(r'^bib/(?P<pk>[0-9]+)/generate/$', views.BibGenerateView.as_view(), name='bib_generate'),

    url(r'^bib/(?P<pk>[0-9]+)/entries/$', views.EntryListView.as_view(), name='entry_list'),
    url(r'^bib/(?P<pk>[0-9]+)/entries/new/$', views.EntryCreateView.as_view(), name='new_entry'),

    url(r'^entry/(?P<pk>[0-9]+)/$', views.EntryDetailView.as_view(), name='entry_detail'),
    url(r'^entry/(?P<pk>[0-9]+)/edit/$', views.EntryEditView.as_view(), name='entry_edit'),
    url(r'^entry/(?P<pk>[0-9]+)/delete/$', views.EntryDeleteView.as_view(), name='entry_delete'),
]