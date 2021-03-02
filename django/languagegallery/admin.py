from django.contrib import admin
from languagegallery import models


@admin.register(models.MimeType)
class MimeTypeAdmin(admin.ModelAdmin):
  list_display  = ('mimetype', 'extension', 'identifier')
  ordering      = ('mimetype', )
  search_fields = ('mimetype', 'extension')


@admin.register(models.MediaTag)
class MediaTagAdmin(admin.ModelAdmin):
  list_display  = ('name', 'creator', 'created')
  ordering      = ('name', )
  search_fields = ('name', 'creator', 'created')


@admin.register(models.FileInfo)
class FileInfoAdmin(admin.ModelAdmin):
  list_display  = ('basename', 'title', 'creator', 'mimetype', 'created', 'modified')
  ordering      = ('basename', )
  search_fields = ('basename', 'title', 'mimetype__mimetype', 'mimetype__extension')

