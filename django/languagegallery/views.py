import os.path
from django.template import loader
from django.conf import settings
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
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


def update(request, hash):
  if request.method == 'POST':
    form = forms.UpdateFileForm(request.POST)
    if form.is_valid():
      file_object = models.FileInfo.objects.get(sha256=hash)

      data = form.cleaned_data

      if 'title' in data: file_object.title = data['title']

      if data.get('add_tag'):
        tag_name = data['add_tag'].lower()
        if len(file_object.tags.filter(name=tag_name)) == 0:
          tag, isnew = models.MediaTag.objects.get_or_create(name=tag_name)
          if isnew:
            tag.clean_all()
            tag.save()
          file_object.tags.add(tag)

      if data.get('del_tag'):
        tag = file_object.tags.filter(pk=data['del_tag'])
        if len(tag) > 0:
          file_object.tags.remove(tag[0])

      file_object.save()

      if request.content_type == 'application/json':
        return JsonResponse({
          'title': file_object.title,
          'tags': [tag.name for tag in file_object.tags.all()],
        })

      else:
        return HttpResponseRedirect(
            reverse('languagegallery:show',
            kwargs={ 'hash': hash }))

    else:
      return JsonResponse(form.errors)

  #TODO Print failed message and return to upload page
  return HttpResponseRedirect(reverse('languagegallery:index'))


def delete_tag(request, hash, tag):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)

    tag = file_object.tags.filter(pk=tag)
    if len(tag) > 0: file_object.tags.remove(tag[0])

    return HttpResponseRedirect(
        reverse('languagegallery:show', kwargs={ 'hash': hash }))

  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseNotFound('File does not exist')


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

