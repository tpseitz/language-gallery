from django.contrib import admin
from django.urls import include, path

urlpatterns = [
  path('sysadmin/', admin.site.urls),
  path('', include('languagegallery.urls')),
]
