from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


# Urls globales
urlpatterns = [
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.surveys.urls')),
    path('api/', include('apps.feedback.urls')),
    path('api/', include('apps.analysis.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
