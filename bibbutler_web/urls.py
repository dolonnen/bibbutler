from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^bib/(?P<pk>[0-9]+)/entry/', views.EntryListView.as_view(), name='entry_list'),
    url(r'^bib/(?P<pk>[0-9]+)', views.BibDetailView.as_view(), name='bib_detail'),
    url(r'^bib/', views.BibListView.as_view(), name='bib_list'),
    url(r'^entry/(?P<pk>[0-9]+)', views.EntryDetailView.as_view(), name='entry_detail'),
]