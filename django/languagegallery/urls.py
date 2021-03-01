from django.urls import path, register_converter
from . import views, converters

register_converter(converters.FileHash, 'filehash')
register_converter(converters.FileExtension, 'extension')

app_name = 'languagegallery'
urlpatterns = [
  path('', views.index, name='index'),
  path('file/<filehash:hash>.<extension:extension>', views.file, name='file'),
  path('show/<filehash:hash>.html', views.frame, name='show'),
  path('thumb/<filehash:hash>.jpeg', views.thumbnail, name='thumb'),

  path('upload/', views.upload, name='upload'),
  path('update/<filehash:hash>', views.update, name='update'),
  path('remove/tag/<filehash:hash>/<int:tag>', views.delete_tag, name='deltag'),
]

