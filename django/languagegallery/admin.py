from django.contrib import admin
from languagegallery import models


@admin.register(models.MimeType)
class MimeTypeAdmin(admin.ModelAdmin):
  list_display = ('mimetype', 'extension', 'identifier')
  ordering = ('mimetype', )
  search_fields = ('mimetype', 'extension')


@admin.register(models.MediaTag)
class MimeTypeAdmin(admin.ModelAdmin):
  search_fields = ('name', )


@admin.register(models.FileInfo)
class FileInfoAdmin(admin.ModelAdmin):
  list_display = ('basename', 'title', 'mimetype')
  ordering = ('basename', 'title')
  search_fields = ('basename', 'title', 'mimetype__mimetype', 'mimetype__extension')

