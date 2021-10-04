from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path(
        '',
        views.index,
        name='index',
    ),
    path(
        'follow/',
        views.follow_index,
        name='follow_index',
    ),
    path(
        'group/<slug:slug>/',
        views.group_posts,
        name='group_posts',
    ),
    path(
        'groups/',
        views.groups,
        name='groups',
    ),
    path(
        'new/',
        views.new_post,
        name='new_post',
    ),
    path(
        'users/<str:username>/',
        views.profile,
        name='profile',
    ),
    path(
        'users/<str:username>/<int:post_id>/',
        views.post_view,
        name='post',
    ),
    path(
        'users/<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit',
    ),
    path(
        'users/<str:username>/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment',
    ),
    path(
        'users/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow',
    ),
    path(
        'users/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow',
    ),
]
