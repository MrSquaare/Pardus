"""
    Pardus URL Configuration
"""

#
# Documentation Django sur la distribution des URLs :
# https://docs.djangoproject.com/fr/2.0/topics/http/urls/
#

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Pardus import settings

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
