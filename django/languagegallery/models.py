from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


User = get_user_model()


class MimeType(models.Model):
  identifier = models.CharField(max_length=10,  verbose_name=_('identifier'))
  mimetype   = models.CharField(max_length=110, verbose_name=_('mimetype'))
  extension  = models.CharField(max_length=10,  verbose_name=_('file extension'))

  class Meta:
    verbose_name = _('mimetype')
    verbose_name_plural = _('mimetypes')

  def __str__(self):
    return self.mimetype


class MediaTag(models.Model):
  creator = models.ForeignKey(User, models.CASCADE, verbose_name=_('creator'))
  created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)

  name    = models.CharField(max_length=50, verbose_name=_('name'), unique=True)

  class Meta:
    verbose_name = _('tag')
    verbose_name_plural = _('tags')

  def __str__(self):
    return self.name


class FileInfo(models.Model):
  creator   = models.ForeignKey(User, models.CASCADE, verbose_name=_('uploader'))
  created   = models.DateTimeField(verbose_name=_('uploaded'), auto_now_add=True)
  modified  = models.DateTimeField(verbose_name=_('modified'), auto_now=True)

  sha256    = models.BinaryField(max_length=32, unique=True, verbose_name=_('checksum, SHA256'))
  basename  = models.CharField(max_length=200, verbose_name=_('basename'))
  mimetype  = models.ForeignKey(MimeType, models.PROTECT, verbose_name=_('mimetype'))

  file      = models.FileField(upload_to='media', verbose_name=_('file'))
  thumbnail = models.ImageField(upload_to='thumbnails', verbose_name=_('thumbnails'))

  title     = models.CharField(max_length=100, default='', verbose_name=_('title'), blank=True)
  width     = models.BigIntegerField(verbose_name=_('width'), null=True)
  height    = models.BigIntegerField(verbose_name=_('height'), null=True)

  tags      = models.ManyToManyField(MediaTag, related_name='files', verbose_name=_('tags'), blank=True)
  is_public = models.BooleanField(verbose_name=_("Is public"), default=False)

  class Meta:
    verbose_name = _('file info')
    verbose_name_plural = _('file info')

  def __str__(self):
    return self.title or self.basename

