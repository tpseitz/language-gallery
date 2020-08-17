from io import BytesIO
from hashlib import sha256
from PIL import Image
from . import converters, models

THUMBNAIL_SIZE = 140

def handle_upload(post, file_data):
  raw = file_data.read()

  # Calculate file hash
  hsh = sha256(raw).digest()
  hshstr = converters.bytes_to_hex(hsh)

  img = Image.open(BytesIO(raw))
  # REad size
  width, height = img.size
  # Get mimetype from database
  mime = models.MimeType.objects.get(identifier=img.format)

  # Create thumbnail and store it ti bytearray
  if img.mode != 'RGB': img = img.convert('RGB')
  img.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE))
  buf = BytesIO()
  img.save(buf, 'JPEG')

  fo = models.FileInfo(
    sha256    = hsh,
    basename  = file_data.name,
    mimetype  = mime,
    width     = width, height=height,
    title     = post.get('title', ''))
  fo.file.save('%s.%s' % (hshstr, mime.extension), BytesIO(raw))
  fo.thumbnail.save('%s.jpeg' % (hshstr,), buf)
  fo.save()

