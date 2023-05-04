from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "auth_server"

urlpatterns = [
    path('',views.token_detail, name='verify'),
    path('download/<str:path>/', views.download_file, name='download_file'),] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


