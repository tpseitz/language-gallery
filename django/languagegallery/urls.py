from django.urls import path, register_converter

from . import views, converters

register_converter(converters.FileHash, 'filehash')
register_converter(converters.FileExtension, 'extension')

app_name = 'languagegallery'
urlpatterns = [
  path('', views.index, name='index'),
  path('upload/', views.upload, name='upload'),
  path('files/<filehash:file_hash>.<extension:extension>', views.file, name='thumb'),
  path('thumb/<filehash:file_hash>.jpeg', views.thumbnail, name='thumb')]

