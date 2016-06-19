from datetime import date
from django.test import TestCase
from bibbutler_web.models.entry import *
from bibbutler_web.models.general import Bibliography


class EntryTestCase(TestCase):
    def setUp(self):
        Bibliography.objects.create(document_name='Oberwichtige Bachelorarbeit')

    @staticmethod
    def get_full_generic_entry(self):
        return Entry(bibliography=Bibliography.objects.first(),
                     title='Ein funktionierender Testeintrag',
                     subtitle='toller Subtitel',
                     url='http://test.example.com',
                     urldate=date.today(),
                     language='german',
                     pubstate='sbmit',
                     date=date.today(),
                     year=date.today().year)

    @staticmethod
    def get_minimal_generic_entry(self):
        return Entry(bibliography=Bibliography.objects.first(),
                     title='Ein funktionierender Testeintrag',
                     year=date.today().year)


    def test_entry_can_create(self):
        entry = self.get_full_generic_entry(self)
        entry.save()
        self.assertIsInstance(Entry.objects.get(id=entry.id), Entry)
        self.assertEqual(Entry.objects.get(id=entry.id).title, entry.title)

    def test_entry_can_validate(self):
        entry = self.get_full_generic_entry(self)
        entry.full_clean()

    def test_requirement_title(self):
        entry = Entry(year=1111)
        with self.assertRaisesRegexp(ValidationError, 'title'):
            entry.full_clean()

    def test_year_not_in_future(self):
        entry = self.get_minimal_generic_entry(self)
        entry.year = 9876
        with self.assertRaisesRegexp(ValidationError, 'year'):
            entry.full_clean()

    def test_author_or_editor_validate(self):
        online_entry = EntryOnline(bibliography=Bibliography.objects.first(),
                                   title='Ein funktionierender Testeintrag',
                                   year=date.today().year)
        online_entry.url = 'http://blub'
        with self.assertRaisesRegexp(ValidationError, 'url'):
            online_entry.full_clean()


