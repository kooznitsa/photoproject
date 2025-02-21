from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tags/', include('tags.urls', namespace='tags')),
]

urlpatterns += static(settings.base.MEDIA_URL, document_root=settings.base.MEDIA_ROOT)
