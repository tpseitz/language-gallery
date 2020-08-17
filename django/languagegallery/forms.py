from django import forms

def choices_tags():
  return [(tag.id, tag.name) for tags in MediaTag.objects.all()]

class UploadForm(forms.Form):
  title = forms.CharField(max_length=100, required=False)
  upload  = forms.FileField()
  tags  = forms.MultipleChoiceField(choices=choices_tags, required=False)

