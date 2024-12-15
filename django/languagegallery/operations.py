from io import BytesIO
from hashlib import sha256
from PIL import Image
from . import converters, models
from django.conf import settings

THUMBNAIL_WIDTH  = settings.THUMBNAIL_WIDTH
THUMBNAIL_HEIGHT = settings.THUMBNAIL_HEIGHT

def handle_upload(post, file_data, creator):
  raw = file_data.read()

  # Calculate file hash
  hsh = sha256(raw).digest()
  hshstr = converters.bytes_to_hex(hsh)

  try:
    return models.FileInfo.objects.get(sha256=hsh)
  except models.FileInfo.DoesNotExist as dne:
    pass

  img = Image.open(BytesIO(raw))
  # Read size
  width, height = img.size
  # Get mimetype from database
  mime = models.MimeType.objects.get(identifier=img.format)

  # Create thumbnail and store it ti bytearray
  if img.mode != 'RGB': img = img.convert('RGB')
  img.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT))
  buf = BytesIO()
  img.save(buf, 'JPEG')

  # Create object from all the data
  fo = models.FileInfo(
    creator   = creator,
    sha256    = hsh,
    basename  = file_data.name,
    mimetype  = mime,
    width     = width, height=height,
    title     = post.get('title', ''))
  fo.file.save('%s.%s' % (hshstr, mime.extension), BytesIO(raw))
  fo.thumbnail.save('%s.jpeg' % (hshstr,), buf)
  fo.save()

  return fo

