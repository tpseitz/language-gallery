from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FileHash, 'filehash')
register_converter(converters.FileExtension, 'extension')

app_name = 'languagegallery'
urlpatterns = [
  path('', views.file_gallery, name='index'),
  path('show/<filehash:hash>.html', views.file_frame, name='show'),
  path('thumb/<filehash:hash>.jpeg', views.thumbnail, name='thumb'),
  path('file/<filehash:hash>.<extension:extension>', views.file, name='file'),

  path('api/files/', views.file_upload, name='upload'),
  path('api/files/<filehash:hash>', views.file_update, name='update'),
]

