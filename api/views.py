from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from posts.models import Comment, Follow, Group, Post
from rest_framework import filters, viewsets

from .filters import PostsInGroupFilter
from .permissions import ReadOnlyOrIsAuthenticatedOrIsAuthor
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    '''Provide access to objects of the Post model:
    get a given post or get all posts - works for
    all users (including unauthorized); create a new
    post - works for any authorized user; edit or delete
    a given post if the user is the author of this post.'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        ReadOnlyOrIsAuthenticatedOrIsAuthor,
    ]
    lookup_url_kwarg = 'post_id'
    filterset_class = PostsInGroupFilter

    def perform_create(self, serializer):
        group_id = self.request.data.get('group')
        if group_id:
            group = get_object_or_404(
                Group,
                id=group_id,
            )
            return serializer.save(author=self.request.user, group=group)
        return serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    '''Provide access to objects of the Comment model:
    get a given comment or get all comments for a given post - works for all
    users (including unauthorized); create a new comment for a given
    post - works for any authorized user; edit or delete a given comment
    for a given post if the user is the author of this comment.'''
    serializer_class = CommentSerializer
    permission_classes = [
        ReadOnlyOrIsAuthenticatedOrIsAuthor,
    ]
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ModelViewSet):
    '''Provide access to objects of the Group model:
    get a given group or get all groups - works for all users
    (including unauthorized); create a new group - works for
    any authorized user.'''
    http_method_names = [
        'get',
        'post',
    ]
    permission_classes = [
        ReadOnlyOrIsAuthenticatedOrIsAuthor,
    ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_url_kwarg = 'group_id'


class FollowViewSet(viewsets.ModelViewSet):
    '''Provide access to objects of the Follow model.'''
    http_method_names = [
        'get',
        'post',
    ]
    serializer_class = FollowSerializer
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        'user__username',
    ]

    def get_queryset(self):
        user = get_object_or_404(
            User,
            pk=self.request.user.pk
        )
        return Follow.objects.filter(following=user)

    def perform_create(self, serializer):
        following = get_object_or_404(
            User,
            username=self.request.data.get('following')
        )
        return serializer.save(user=self.request.user, following=following)
