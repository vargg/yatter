from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment_view',
)
router.register(
    r'posts',
    PostViewSet,
    basename='post_view',
)
router.register(
    r'group',
    GroupViewSet,
    basename='group_view',
)
router.register(
    r'follow',
    FollowViewSet,
    basename='follow_view',
)

urlpatterns = [
    path(
        'v1/',
        include(router.urls)
    ),
    path(
        'v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
