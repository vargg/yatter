import datetime as dt

from django.db.models import Count

from .models import Group, Tag


def year(request):
    current_year = dt.datetime.now().year
    return {
        'year': current_year,
    }


def all_groups(request):
    '''Display a list of all groups by the number of posts in them.'''
    all_groups = Group.objects.annotate(
        num_posts=Count('group_id')
    ).order_by(
        '-num_posts',
    )[:10]
    return {
        'all_groups': all_groups,
    }


def all_tags(request):
    '''Display a list of all groups by the number of marked posts.'''
    all_tags = Tag.objects.annotate(
        num_posts=Count('post')
    ).order_by(
        '-num_posts',
    )[:10]
    return {
        'all_tags': all_tags,
    }
