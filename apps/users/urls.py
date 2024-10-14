from django.urls import path
from . import views


# Urls para los endpoint de users
urlpatterns = [
    path('users/sign_up', views.sign_up, name='sign_up'),
    path('users/sign_in', views.sign_in, name='sign_in'),
    path('users/sign_out', views.sign_out, name='sign_out'),
    path('users/update_user', views.update_user, name='update_user'),
    path('users/delete_user', views.delete_user, name='delete_user'),
]