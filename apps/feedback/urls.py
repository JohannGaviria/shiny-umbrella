from django.urls import path
from . import views


# Urls para los endpoints de surveys
urlpatterns = [
    path('feedbacks/survey/<str:survey_id>/comment/add', views.add_comment_survey, name='add_comment_survey'),
    path('feedbacks/survey/<str:survey_id>/comment/all', views.get_all_comments_survey, name='get_all_comment_survey'),
    path('feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/update', views.update_comment_survey, name='update_comment_survey'),
    path('feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/delete', views.delete_comment_survey, name='delete_comment_survey'),
    path('feedbacks/survey/<str:survey_id>/qualify/add', views.add_qualify_survey, name='add_qualify_survey'),
    path('feedbacks/survey/<str:survey_id>/qualify/all', views.get_all_qualifies_survey, name='get_all_qualifies_survey'),
    path('feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/update', views.update_qualify_survey, name='update_qualify_survey'),
    path('feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/delete', views.delete_qualify_survey, name='delete_qualify_survey'),
]