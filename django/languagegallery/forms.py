from django import forms
from languagegallery import models


def choices_tags():
  return [(tag.id, tag.name) for tags in models.MediaTag.objects.all()]


class UploadForm(forms.Form):
  title = forms.CharField(max_length=100, required=False)
  upload  = forms.FileField()
  tags  = forms.MultipleChoiceField(choices=choices_tags, required=False)


class UpdateFile(forms.ModelForm):
  class Meta:
    model = models.FileInfo
    fields = ['title', 'tags']

