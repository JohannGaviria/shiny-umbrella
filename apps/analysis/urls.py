from django.urls import path
from . import views


# Urls para los endpoints de surveys
urlpatterns = [
    path('analysis/survey/<str:survey_id>/export', views.export_analysis_details, name='export_analysis_details'),
]