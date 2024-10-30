from django.urls import path
from . import views


# Urls para los endpoints de surveys
urlpatterns = [
    path('surveys/create', views.create_survey, name='create_survey'),
    path('surveys/get/<str:survey_id>', views.get_survey_id, name='get_survey_id')
]