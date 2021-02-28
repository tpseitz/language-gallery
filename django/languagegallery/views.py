import os.path
from django.template import loader
from django.conf import settings
from django.http import HttpResponse, FileResponse, \
  HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.db import models as dbmodels
from . import models, converters, forms, operations


def index(request):
  context = {
    'upload_form': forms.UploadForm(),
    'file_list': models.FileInfo.objects.all(),
  }

  template = loader.get_template('gallery.html')
  return HttpResponse(template.render(context, request))


def frame(request, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)

    context = {
      'file': file_object,
      'tags': file_object.tags.all(),
    }

    template = loader.get_template('frame.html')
    return HttpResponse(template.render(context, request))

  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseNotFound('File does not exist')


def upload(request):
  if request.method == 'POST':
    form = forms.UploadForm(request.POST, request.FILES)
    if form.is_valid():
      operations.handle_upload(request.POST, request.FILES['upload'])
      #TODO Print success message
    else:
      return HttpResponse('Invalid form: %r' % (form.errors,)) #XXX

  #TODO Print failed message and return to upload page
  return HttpResponseRedirect(reverse('languagegallery:index'))


def file(request, hash, extension):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
    return HttpResponse(file_object.file.open(),
        content_type=file_object.mimetype.mimetype)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseNotFound('File does not exist')


def thumbnail(request, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
    return FileResponse(file_object.thumbnail.open(),
        content_type=file_object.mimetype.mimetype)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseRedirect(settings.STATIC_URL + 'gallery/icon_broken.png')

