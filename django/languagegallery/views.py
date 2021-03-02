import datetime, os.path
from django.template import loader
from django.conf import settings
from django.db.models import Q
from django.http import (HttpResponse, FileResponse, JsonResponse,
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import models, converters, forms, operations


TIME_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def list_files(request):
  if request.user.is_authenticated:
    files = models.FileInfo.objects.filter(Q(creator=request.user) | Q(is_public=True))
  else:
    files = models.FileInfo.objects.filter(is_public=True)

  files = files.order_by('title', 'basename', 'created')

  return files


def index(request):
  context = {
    'upload_form': forms.UploadForm(),
    'file_list': list_files(request),
  }
  template = loader.get_template('gallery.html')
  return HttpResponse(template.render(context, request))


def frame(request, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)

    if not (file_object.is_public or file_object.creator == request.user):
      return HttpResponseForbidden()

    context = {
      'file': file_object,
      'tags': file_object.tags.all(),
    }

    template = loader.get_template('frame.html')
    return HttpResponse(template.render(context, request))

  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseForbidden('Permission denied')


@csrf_exempt
def upload(request):
  user = request.user
  if not user.is_authenticated:
    return HttpResponseForbidden('Permission denied')

  if request.method == 'POST':
    form = forms.UploadForm(request.POST, request.FILES)
    if form.is_valid():
      file_object = operations.handle_upload(request.POST, request.FILES['upload'], user)
      return HttpResponseRedirect(
          reverse('languagegallery:show', kwargs={ 'hash': file_object.sha256 }))
    else:
      #TODO Display error page
      return HttpResponse('Invalid form: %r' % (form.errors,))

  return HttpResponseForbidden('Permission denied')


@csrf_exempt
def update(request, hash):
  user = request.user
  if not user.is_authenticated:
    return HttpResponseForbidden('Permission denied')

  if request.method == 'POST':
    form = forms.UpdateFileForm(request.POST)
    if form.is_valid():
      file_object = models.FileInfo.objects.get(sha256=hash)

      if file_object.creator != user:
        return HttpResponseForbidden('Permission denied')

      data = form.cleaned_data

      if 'title' in data: file_object.title = data['title']

      if 'is_public' in data: file_object.is_public = data['is_public']

      if data.get('add_tag'):
        tag_name = data['add_tag'].lower()
        if len(file_object.tags.filter(name=tag_name)) == 0:
          tag, isnew = models.MediaTag.objects.get_or_create(
              name=tag_name, defaults={ 'creator': user })
          if isnew:
            tag.full_clean()
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
    response = HttpResponse(file_object.file.open(), content_type=file_object.mimetype.mimetype)
    response['Expires'] = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime(TIME_FORMAT)
    return response
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseForbidden('Permission denied')


def thumbnail(request, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
    response = FileResponse(file_object.thumbnail.open(),
        content_type=file_object.mimetype.mimetype)
    response['Expires'] = (datetime.datetime.now()+datetime.timedelta(days=7)).strftime(TIME_FORMAT)
    return response
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseRedirect(settings.STATIC_URL + 'gallery/icon_broken.png')

