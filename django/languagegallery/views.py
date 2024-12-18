import datetime, os.path, time, json
import jwt
from io import BytesIO
from PIL import Image
from django.template import loader
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.cache import caches
from django.db.models import Q
from django.http import (HttpResponse, FileResponse, JsonResponse,
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden)
from django.urls import reverse
from django.utils.translation import gettext as _
from . import models, converters, forms, operations

TIME_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'


def _serialize_file_object(file_object):
  return {
    'basename':  file_object.basename,
    'mimetype':  file_object.mimetype.mimetype,
    'extension':  file_object.mimetype.extension,
    'title':     file_object.title,
    'width':     file_object.width,
    'height':    file_object.height,
    'tags':      [(tag.pk, tag.name) for tag in file_object.tags.all()],
    'is_public': file_object.is_public,
    'thumbnail': reverse('languagegallery:thumb',
        kwargs={ 'size': settings.THUMBNAIL_HEIGHT, 'hash': file_object.sha256 }),
    'file':      reverse('languagegallery:show_update',
        kwargs={ 'hash': file_object.sha256 }),
  }


def _list_files(request):
  if request.user.is_authenticated:
    files = models.FileInfo.objects.filter(Q(creator=request.user) | Q(is_public=True))
  else:
    files = models.FileInfo.objects.filter(is_public=True)

  files = files.order_by('basename')

  return files


def _permission_denied(request, errors=[]):
  if request.content_type == 'application/json':
    response = JsonResponse({ 'errors': errors })
    response.status_code=403
    return response
  else:
    return HttpResponseForbidden('Permission denied')


def file_gallery(request):
  if request.content_type == 'application/json':
    return JsonResponse(
        { 'items': list(map(_serialize_file_object, _list_files(request))) })

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
    return _permission_denied(request)

  if request.method != 'POST':
    return _permission_denied(request)

  form = forms.UploadForm(request.POST, request.FILES)

  if not form.is_valid():
    #TODO Display error page
    return HttpResponse('Invalid form: %r' % (form.errors,))

  file_object = operations.handle_upload(request.POST, request.FILES['upload'], user)

  file_url = reverse('languagegallery:show_update', kwargs={ 'hash': file_object.sha256 })

  if request.content_type == 'application/json':
    return JsonResponse(_serialize_file_object(file_object))

  return HttpResponseRedirect(file_url)


def file_frame(request, hash, form=None):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return _permission_denied(request)

  if not (file_object.is_public or file_object.creator == request.user):
    return _permission_denied(request)

  if request.content_type == 'application/json':
    return JsonResponse(_serialize_file_object(file_object))

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
    return _permission_denied(request)

  if file_object.creator != request.user:
    return _permission_denied(request)

  user = request.user

  if file_object.creator != user:
    return _permission_denied(request)

  if request.method == 'POST':
    if request.content_type == 'application/json':
      form = forms.UpdateFileForm(json.loads(request.body))
    else:
      form = forms.UpdateFileForm(request.POST)
  elif set(request.GET):
    form = forms.UpdateFileForm(request.GET)
  else:
    return _permission_denied(request)

  if not form.is_valid():
    if request.content_type == 'application/json':
      return JsonResponse(form.errors)
    else:
      return file_frame(request, hash, form)

  data = form.cleaned_data

  if data.get('title'):
    file_object.title = data['title']

  if data.get('is_public') is not None:
    file_object.is_public = data['is_public']

  if data.get('add_tag'):
    tag_name = data['add_tag'].lower()
    if len(file_object.tags.filter(name=tag_name)) == 0:
      tag, isnew = models.MediaTag.objects.get_or_create(
          name=tag_name, defaults={'creator': user})
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
    return file_frame(request, hash)


def thumbnail(request, size, hash):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return HttpResponseRedirect(settings.STATIC_URL + 'gallery/icon_broken.png')

  if not (file_object.is_public or file_object.creator == request.user):
    return HttpResponseRedirect(settings.STATIC_URL + 'gallery/icon_broken.png')

  if size >= settings.THUMBNAIL_HEIGHT:
    response = FileResponse(file_object.thumbnail.open(), content_type='image/jpeg')

  else:
    if size not in settings.THUMBNAIL_ALLOWED_SIZES:
      sizes = [s for s in settings.THUMBNAIL_ALLOWED_SIZES if s < size]
      if sizes: size = min(sizes)
      else: size = min(settings.THUMBNAIL_ALLOWED_SIZES)
    hexhash = converters.bytes_to_hex(hash)
    cache = caches['files']
    key = f'{hexhash}-{size}'
    data = cache.get(key)
    if data is None:
      img, buf = Image.open(file_object.thumbnail.open()), BytesIO()
      img.thumbnail((size * settings.THUMBNAIL_WIDTH // settings.THUMBNAIL_HEIGHT, size))
      img.save(buf, 'JPEG')
      data = buf.getbuffer().tobytes()
      cache.set(key, data)
    response = FileResponse(BytesIO(data), content_type='image/jpeg')

  response['Expires'] = (datetime.datetime.now() + datetime.timedelta(days=7)).strftime(TIME_FORMAT)
  return response


def get_file(request, hash, extension):
  try:
    file_object = models.FileInfo.objects.get(sha256=hash)
  except models.FileInfo.DoesNotExist as dne:
    return _permission_denied(request)

  if not (file_object.is_public or file_object.creator == request.user):
    return _permission_denied(request)

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


def _generate_token(user):
  return jwt.encode(
      { "uid": user.pk, "exp": int(time.time() + settings.JWT_TOKEN_TTL_SECONDS) },
      settings.SECRET_KEY, algorithm=settings.JWT_DEFAULT_ALGORITHM)


def jwt_auth(request):
  if request.method != 'POST' or request.content_type != 'application/json':
    return _permission_denied(request)

  errors, token = [], None

  data = json.loads(request.body)
  username = data.get('username')
  password = data.get('password')
  if username and password:
    user = authenticate(username=username, password=password)
    if user is None:
      errors.append(_("authentication failed"))
    else:
      token = _generate_token(user)

  else:
    if not username: errors.append(_('Missing username'))
    if not password: errors.append(_('Missing password'))

  if token:
    return JsonResponse({ 'token': token })
  else:
    return JsonResponse({ 'errors': errors })


def jwt_refresh(request):
  if request.user.is_authenticated:
    return JsonResponse({ 'token': _generate_token(request.user) })
  else:
    return JsonResponse({ 'errors': [_('Not authenticated')] })

