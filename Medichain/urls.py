from django.contrib import admin
from django.urls import path, include



urlpatterns = [
    path('',include('core.urls')),
    path('parties/',include('parties.urls')),
    path("admin/", admin.site.urls),
    path('chain/', include('chain.urls')),
    path('auth_server/', include('auth_server.urls')),
]
