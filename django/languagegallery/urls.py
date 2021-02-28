from django.urls import path, register_converter

from . import views, converters

register_converter(converters.FileHash, 'filehash')
register_converter(converters.FileExtension, 'extension')

app_name = 'languagegallery'
urlpatterns = [
  path('', views.index, name='index'),
  path('upload/', views.upload, name='upload'),

  path('file/<filehash:hash>.<extension:extension>', views.file, name='file'),
  path('show/<filehash:hash>.html', views.frame, name='show'),
  path('thumb/<filehash:hash>.jpeg', views.thumbnail, name='thumb')]

