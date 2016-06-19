from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


# class User(models.Model):
#     first_name = models.CharField("user's first name", max_length=30, blank=True)
#     last_name = models.CharField("user's last name", max_length=30, blank=True)
#     username = models.CharField(max_length=30, db_index=True)
#
#     def __str__(self):
#         return self.username


class Bibliography(models.Model):

    document_name = models.CharField(max_length=350, db_index=True, help_text="The name of the document in which this bibliography is needed")
    document_url = models.URLField(blank=True, null=True, default=None, help_text="The url of the document in which this bibliography is needed")
    addition = models.CharField(blank=True, max_length=10, help_text="additional infos like version or something")
    date = models.DateField(blank=True, null=True, default=timezone.now, help_text="The date of the bibliography")
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self):
        return 'bibliography for ' + self.document_name

    def get_absolute_url(self):
        return reverse('bib_detail', args=[self.id])