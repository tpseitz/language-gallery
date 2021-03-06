from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FileHash, 'filehash')
register_converter(converters.FileExtension, 'extension')

app_name = 'languagegallery'
urlpatterns = [
  path('', views.list_or_upload, name='list_update'),
  path('<filehash:hash>', views.frame_or_update, name='show_update'),
  path('<int:size>/<filehash:hash>.jpeg', views.thumbnail, name='thumb'),
  path('<filehash:hash>.<extension:extension>', views.get_file, name='get_file'),
]

