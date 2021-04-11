from django.db.models import QuerySet
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, Tag

User = get_user_model()

POSTS_PER_PAGE = 10


def index(request):
    '''Pagination of all posts.'''
    all_posts = Post.objects.all().select_related(
        'author',
        'group',
        'author__profile',
    )
    page = pagination(request, all_posts)
    return render(
        request,
        'posts/index.html',
        {
            'page': page,
        }
    )


def group_posts(request, slug):
    '''Pagination of all posts in the group.'''
    group = get_object_or_404(Group, slug=slug)
    all_posts = Post.objects.filter(group=group).select_related(
        'author',
        'group',
        'author__profile',
    )
    page = pagination(request, all_posts)
    return render(
        request,
        'posts/group.html',
        {
            'group': group,
            'page': page,
        }
    )


def tagged_posts(request, tag):
    '''Pagination of all posts with the tag.'''
    all_posts = Post.objects.filter(
        tags__title=tag,
    ).select_related(
        'author',
        'group',
        'author__profile',
    )
    page = pagination(request, all_posts)
    return render(
        request,
        'posts/tag.html',
        {
            'page': page,
            'tag': tag,
        }
    )


@login_required
def new_post(request):
    '''Add a new post.'''
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            files=request.FILES or None
        )
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            tags_added = tagging(new_post)
            if tags_added:
                messages.success(
                    request,
                    'Пост добавлен, тэги отмечены.'
                )
            else:
                messages.success(
                    request,
                    'Пост добавлен.'
                )
            return redirect('posts:index')
        return render(
            request,
            'posts/new_post.html',
            {
                'form': form,
            }
        )
    return render(
        request,
        'posts/new_post.html',
        {
            'form': PostForm(),
        }
    )


def profile(request, username):
    '''Pagination of all user posts.'''
    all_posts = Post.objects.filter(author__username=username).select_related(
        'author',
        'group',
    )
    page = pagination(request, all_posts)
    post_author = get_object_or_404(
        User.objects.select_related('profile'),
        username=username,
    )
    subscribers = Follow.objects.filter(author__username=username).count()
    subscriptions = Follow.objects.filter(user__username=username).count()
    if request.user.is_authenticated and request.user != post_author:
        following = Follow.objects.filter(
            user=request.user,
            author=post_author
        ).exists
    else:
        following = False
    return render(
        request,
        'posts/profile.html',
        {
            'page': page,
            'post_author': post_author,
            'subscribers': subscribers,
            'subscriptions': subscriptions,
            'following': following,
        },
    )


def post_view(request, username, post_id):
    '''Display a single post.'''
    post = get_object_or_404(
        Post.objects.select_related(
            'author',
            'group',
            'author__profile',
        ),
        pk=post_id
    )
    posts = Post.objects.filter(author__username=username).count()
    form = CommentForm()
    comments = Comment.objects.filter(post_id=post_id)
    return render(
        request,
        'posts/post.html',
        {
            'post': post,
            'posts': posts,
            'post_author': post.author,
            'form': form,
            'comments': comments,
        },
    )


@login_required
def post_edit(request, username, post_id):
    '''Edit an existing post.'''
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post', username=username, post_id=post_id)
    form = PostForm(
        files=request.FILES or None,
        instance=post,
    )
    if request.method == 'POST':
        form = PostForm(
            request.POST or None,
            files=request.FILES or None,
            instance=post,
        )
        if form.is_valid():
            form.save()
            tags_added = tagging(form.save(commit=False))
            if tags_added:
                messages.success(
                    request,
                    'Тэги отмечены'
                )
            form.save(commit=False)
            return redirect(
                'posts:post',
                username=username,
                post_id=post_id,
            )
    return render(
        request,
        'posts/new_post.html',
        {
            'form': form,
            'post': post,
        }
    )


@login_required
def add_comment(request, username, post_id):
    '''Add a new comment.'''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = Post.objects.get(
                pk=post_id,
            )
            new_comment.save()
            messages.success(
                    request,
                    'Комментарий добавлен.'
                )
            return redirect(
                'posts:post',
                username=username,
                post_id=post_id,
            )
        return render(
            request,
            'posts/add_comment.html',
            {
                'form': form,
            }
        )
    return render(
        request,
        'posts/add_comment.html',
        {
            'form': CommentForm(),
        }
    )


@login_required
def follow_index(request):
    '''Pagination of all posts subscriptions.'''
    subscribed_posts = Post.objects.filter(
        author__following__user=request.user
    ).select_related(
        'author',
        'group',
        'author__profile',
    )
    page = pagination(request, subscribed_posts)
    return render(
        request,
        'posts/follow.html',
        {
            'page': page,
        }
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(
        User,
        username=username,
    )
    if not request.user == author:
        Follow.objects.get_or_create(
            user=request.user,
            author=author,
        )
    return redirect(
        'posts:profile',
        username=username,
    )


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(
        User,
        username=username,
    )
    if Follow.objects.filter(user=request.user, author=author).exists():
        subscription = Follow.objects.get(
            user=request.user,
            author=author,
        )
        subscription.delete()
    return redirect(
        'posts:profile',
        username=username,
    )


def groups(request):
    all_groups = Group.objects.all()
    return render(
        request,
        'posts/groups.html',
        {
            'all_groups': all_groups,
        }
    )


def tags(request):
    all_tags = Tag.objects.all().order_by('title')
    return render(
        request,
        'posts/tags.html',
        {
            'all_tags': all_tags,
        }
    )


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404,
    )


def server_error(request):
    return render(
        request,
        'misc/500.html',
        status=500,
    )


def pagination(request, posts: QuerySet):
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page


def tagging(post: Post):
    import re
    all_tags = re.findall(
        r'#\w+',
        post.text,
    )
    if len(all_tags) > 0:
        for a_tag in all_tags:
            a_tag = a_tag[1:]
            tag_instance = Tag.objects.get_or_create(
                title=a_tag,
            )
            tag_instance[0].post.add(post)
        return True
    return False