from django.urls import path
from .views import handle_upload
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', handle_upload, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
