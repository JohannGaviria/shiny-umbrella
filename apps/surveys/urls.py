from django.urls import path
from . import views


# Urls para los endpoints de surveys
urlpatterns = [
    path('surveys/create', views.create_survey, name='create_survey'),
    path('surveys/get/<str:survey_id>', views.get_survey_id, name='get_survey_id'),
    path('surveys/get_all', views.get_all_surveys, name='get_all_surveys'),
    path('surveys/search_survey', views.search_surveys, name='search_surveys'),
    path('surveys/update/<str:survey_id>', views.update_survey, name='update_survey'),
    path('surveys/delete/<str:survey_id>', views.delete_survey, name='delete_survey'),
]