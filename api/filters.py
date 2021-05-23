import django_filters
from posts.models import Post


class PostsInGroupFilter(django_filters.FilterSet):
    group = django_filters.CharFilter(field_name='group__id',)

    class Meta:
        model = Post
        fields = [
            'group',
        ]
