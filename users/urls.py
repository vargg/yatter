from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup',
    ),
    path(
        '<str:username>/edit_profile/',
        views.edit_profile,
        name='edit_profile',
    )
]
