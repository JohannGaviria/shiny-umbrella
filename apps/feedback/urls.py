from django.urls import path
from . import views


# Urls para los endpoints de surveys
urlpatterns = [
    path('feedbacks/survey/<str:survey_id>/comment/add', views.add_comment_survey, name='add_comment_survey'),
]