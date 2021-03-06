import datetime, os.path
from io import BytesIO
from PIL import Image
from django.template import loader
from django.conf import settings
from django.db.models import Q
from django.http import (HttpResponse, FileResponse, JsonResponse,
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from . import models, converters, forms, operations


TIME_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def _serialize_file_object(file_object):
  return {
    'basename':  file_object.basename,
    'mimetype':  file_object.mimetype.mimetype,
    'extension':  file_object.mimetype.extension,
    'file':      reverse('languagegallery:show_update', kwargs={ 'hash': file_object.sha256 }),
    'thumbnail': reverse('languagegallery:thumb', kwargs={ 'hash': file_object.sha256 }),
    'title':     file_object.title,
    'width':     file_object.width,
    'height':    file_object.height,
    'tags':      [(tag.pk, tag.name) for tag in file_object.tags.all()],
    'is_public': file_object.is_public,
  }


def _list_files(request):
  if request.user.is_authenticated:
    files = models.FileInfo.objects.filter(Q(creator=request.user) | Q(is_public=True))
  else:
    files = models.FileInfo.objects.filter(is_public=True)

  files = files.order_by('basename')

  return files


def file_gallery(request):
  context = {
    'upload_form':  forms.UploadForm(),
    'file_list':    _list_files(request),
    'thumb_width':  settings.THUMBNAIL_WIDTH,
    'thumb_height': settings.THUMBNAIL_HEIGHT,
  }

  display = request.GET.get('display')
  if display == 'list':
    template = loader.get_template('list.html')
  else:
    template = loader.get_template('gallery.html')

  return HttpResponse(template.render(context, request))


def file_upload(request):
  user = request.user
  if not user.is_authenticated:
    return HttpResponseForbidden('Permission denied')

  if request.method != 'POST':
    return HttpResponseForbidden('Permission denied')

  form = forms.UploadForm(request.POST, request.FILES)

  if not form.is_valid():
    #TODO Display error page
    return HttpResponse('Invalid form: %r' % (form.errors,))

  file_object = operations.handle_upload(request.POST, request.FILES['upload'], user)

  return HttpResponseRedirect(reverse('languagegallery:show_update',
      kwargs={ 'hash': file_object.sha256 }))


def file_frame(request, hash, form=None):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseForbidden('Permission denied')

  if not (file_object.is_public or file_object.creator == request.user):
    return HttpResponseForbidden('Permission denied')

  context = {
    'file': file_object,
    'tags': file_object.tags.all(),
    'form': form,
    'show_edit': file_object.creator == request.user,
  }

  template = loader.get_template('frame.html')
  return HttpResponse(template.render(context, request))


def file_update(request, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseForbidden('Permission denied')

  if file_object.creator != request.user:
    return HttpResponseForbidden('Permission denied')

  user = request.user

  if request.method == 'POST':
    form = forms.UpdateFileForm(request.POST)
  elif set(request.GET):
    form = forms.UpdateFileForm(request.GET)
  else:
    return HttpResponseForbidden('Permission denied')

  if not form.is_valid():
    if request.content_type == 'application/json':
      return JsonResponse(form.errors)
    else:
      return file_frame(request, hash, form)

  if file_object.creator != user:
    return HttpResponseForbidden('Permission denied')

  data = form.cleaned_data

  if data.get('title'):
    file_object.title = data['title']

  if data.get('is_public') is not None:
    file_object.is_public = data['is_public']

  if data.get('add_tag'):
    tag_name = data['add_tag'].lower()
    if len(file_object.tags.filter(name=tag_name)) == 0:
      tag, isnew = models.MediaTag.objects.get_or_create(name=tag_name, defaults={'creator': user})
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
    return JsonResponse(_serialize_file_object(file_object))
  else:
    return HttpResponseRedirect(reverse('languagegallery:show_update', kwargs={ 'hash': hash }))


def thumbnail(request, size, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseRedirect(settings.STATIC_URL + 'gallery/icon_broken.png')

  if not (file_object.is_public or file_object.creator == request.user):
    return HttpResponseRedirect(settings.STATIC_URL + 'gallery/icon_broken.png')

  if size < settings.THUMBNAIL_HEIGHT:
    img, buf = Image.open(file_object.thumbnail.open()), BytesIO()
    img.thumbnail((size, size))
    img.save(buf, 'JPEG')
    response = FileResponse(BytesIO(buf.getbuffer()), content_type='image/jpeg')
  else:
    response = FileResponse(file_object.thumbnail.open(), content_type='image/jpeg')

  response['Expires'] = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime(TIME_FORMAT)
  return response


def get_file(request, hash, extension):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseForbidden('Permission denied')

  if not (file_object.is_public or file_object.creator == request.user):
    return HttpResponseForbidden('Permission denied')

  response = HttpResponse(file_object.file.open(), content_type=file_object.mimetype.mimetype)
  response['Expires'] = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime(TIME_FORMAT)
  return response


def list_or_upload(request):
  if request.method == 'POST':
    return file_upload(request)
  else:
    return file_gallery(request)


def frame_or_update(request, hash):
  if request.method == 'POST' or set(request.GET):
    return file_update(request, hash)
  else:
    return file_frame(request, hash)

