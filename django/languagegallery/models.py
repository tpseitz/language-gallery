from django.db import models
from django.utils.translation import gettext as _


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
  name  = models.CharField(max_length=50, verbose_name=_('name'), null=False, blank=False)

  class Meta:
    verbose_name = _('tag')
    verbose_name_plural = _('tags')

  def __str__(self):
    return self.name


class FileInfo(models.Model):
  sha256    = models.BinaryField(max_length=32, unique=True, verbose_name=_('checksum, SHA256'))
  basename  = models.CharField(max_length=50, verbose_name=_('basename'))
  mimetype  = models.ForeignKey('Mimetype', models.PROTECT, verbose_name=_('mimetype'))
  width     = models.BigIntegerField(null=True, verbose_name=_('width'))
  height    = models.BigIntegerField(null=True, verbose_name=_('height'))
  title     = models.CharField(max_length=100, null=False, default='', verbose_name=_('title'))
  tags      = models.ManyToManyField('MediaTag', related_name='files', verbose_name=_('tags'))
  file      = models.FileField(upload_to='media', verbose_name=_('file'))
  thumbnail = models.ImageField(upload_to='thumbnails', verbose_name=_('thumbnails'))

  class Meta:
    verbose_name = _('file info')
    verbose_name_plural = _('file info')

  def __str__(self):
    return self.title or self.basename

