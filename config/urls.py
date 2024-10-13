from django.urls import path, include


# Urls globales
urlpatterns = [
    path('api/', include('apps.users.urls')),
]
