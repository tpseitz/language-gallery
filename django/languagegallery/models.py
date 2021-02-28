from django.db import models


class MimeType(models.Model):
  identifier = models.CharField(max_length=10,  null=False)
  mimetype   = models.CharField(max_length=110, null=False)
  extension  = models.CharField(max_length=10,  null=False)


class MediaTag(models.Model):
  name  = models.CharField(max_length=50)


class FileInfo(models.Model):
  sha256    = models.BinaryField(max_length=32, unique=True, null=False)
  basename  = models.CharField(max_length=50, null=False)
  mimetype  = models.ForeignKey('Mimetype', models.PROTECT, null=False)
  width     = models.BigIntegerField(null=True)
  height    = models.BigIntegerField(null=True)
  title     = models.CharField(max_length=100, null=False, default='')
  tags      = models.ManyToManyField('MediaTag')
  file      = models.FileField(upload_to='media', null=False)
  thumbnail = models.ImageField(upload_to='thumbnails', null=False)

