from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    '''Check the availability of pages and used templates
    for an unauthorized user, an authorized user
    and, in some cases, for the author of an object.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db:
        new user, new group, new post.'''
        super().setUpClass()
        cls.user = User.objects.create_user(username='user_name')
        cls.common_user = User.objects.create_user(username='common_user')
        cls.group = Group.objects.create(
            title='Группа',
            slug='test_group',
            description='Описание группы',
        )
        cls.post = Post.objects.create(
            text='Тело поста',
            group=cls.group,
            author=cls.user,
        )

    def setUp(self):
        '''Create an unauthorized client,
        an authorized client (common user) and one more
        an authorized client (post author); create a lists
        of public addresses and login requierd addresses;
        create dicts "url name: url" and "url name: template".'''
        self.guest_client = Client()
        self.post_author_authorized_client = Client()
        self.common_authorized_client = Client()
        self.post_author_authorized_client.force_login(PostURLTests.user)
        self.common_authorized_client.force_login(PostURLTests.common_user)
        self.public_url_names = [
            'index',
            'group_posts',
            'profile',
            'post',
        ]
        self.authenticated_url_names = [
            'follow_index',
            'new_post',
            'post_edit',
            'add_comment',
            'profile_follow',
            'profile_unfollow',
        ]
        self.urls = {
            'index': reverse('posts:index'),
            'group_posts': reverse(
                'posts:group_posts',
                kwargs={
                    'slug': PostURLTests.group.slug,
                }
            ),
            'profile': reverse(
                'posts:profile',
                kwargs={
                    'username': PostURLTests.user.username,
                }
            ),
            'post': reverse(
                'posts:post',
                kwargs={
                    'username': PostURLTests.user.username,
                    'post_id': PostURLTests.post.id,
                }
            ),
            'follow_index': reverse('posts:follow_index'),
            'new_post': reverse('posts:new_post'),
            'post_edit': reverse(
                'posts:post_edit',
                kwargs={
                    'username': PostURLTests.user.username,
                    'post_id': PostURLTests.post.id,
                }
            ),
            'add_comment': reverse(
                'posts:add_comment',
                kwargs={
                    'username': PostURLTests.user.username,
                    'post_id': PostURLTests.post.id,
                }
            ),
            'profile_follow': reverse(
                'posts:profile_follow',
                kwargs={
                    'username': PostURLTests.user.username,
                }
            ),
            'profile_unfollow': reverse(
                'posts:profile_unfollow',
                kwargs={
                    'username': PostURLTests.user.username,
                }
            ),
        }
        self.templates = {
            'index': 'posts/index.html',
            'group_posts': 'posts/group.html',
            'profile': 'posts/profile.html',
            'post': 'posts/post.html',
            'follow_index': 'posts/follow.html',
            'new_post': 'posts/new_post.html',
            'post_edit': 'posts/new_post.html',
            'add_comment': 'posts/add_comment.html',
        }

    def test_public_urls(self):
        '''Check the HTTP status codes of the requests and used templates;
        check only public pages by unauthorized user.'''
        for name in self.public_url_names:
            with self.subTest():
                url = self.urls[name]
                template = self.templates[name]
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    f'{url} does not work',
                )
                self.assertTemplateUsed(
                    response,
                    template,
                    f'{url} should use this template: {template}',
                )

    def test_guest_authenticated_url(self):
        '''Check the HTTP status codes of the requests;
        only for pages requiring registration;
        performed for unauthorized user.'''
        for name in self.authenticated_url_names:
            with self.subTest():
                url = self.urls[name]
                response = self.guest_client.get(url)
                self.assertEqual(
                    response.status_code,
                    302,
                    f'{url} does not redirect correctly',
                )
                self.assertRedirects(
                    response,
                    f'/auth/login/?next={url}',
                )

    def test_user_authenticated_url(self):
        '''Check the HTTP status codes of the requests;
        only for pages accessible to all registered users;
        performed for any authorized user.'''
        url_names_list = [
            'follow_index',
            'new_post',
            'add_comment',
        ]
        for name in url_names_list:
            with self.subTest():
                url = self.urls[name]
                template = self.templates[name]
                response = self.common_authorized_client.get(url)
                self.assertEqual(
                    response.status_code,
                    200,
                    f'{url} does not work',
                )
                self.assertTemplateUsed(
                    response,
                    template,
                    f'{url} should use this template: {template}',
                )

    def test_edit_post(self):
        '''Check the HTTP status codes of the requests and used template;
        only for the page to edit the post;
        performed for unauthorized user and post author.'''
        name = 'post_edit'
        url = self.urls[name]
        template = self.templates[name]
        response_author = self.post_author_authorized_client.get(url)
        response_user = self.common_authorized_client.get(url)
        self.assertEqual(
            response_author.status_code,
            200,
        )
        self.assertEqual(
            response_user.status_code,
            302,
        )
        self.assertTemplateUsed(
            response_author,
            template,
        )
        self.assertRedirects(
            response_user,
            self.urls['post'],
        )

    def test_follow(self):
        '''Check the HTTP status codes of the requests.'''
        name = 'profile_follow'
        url = self.urls[name]
        response = self.common_authorized_client.get(url)
        self.assertEqual(
            response.status_code,
            302,
        )

    def test_unfollow(self):
        '''Check the HTTP status codes of the requests.'''
        self.common_authorized_client.get(
            self.urls['profile_follow']
        )
        name = 'profile_unfollow'
        url = self.urls[name]
        response = self.common_authorized_client.get(url)
        self.assertEqual(
            response.status_code,
            302,
        )

    def test_page_not_found(self):
        '''Check the HTTP status code of the request and used template;
        only for the page 404.'''
        missing_url = reverse(
            'posts:group_posts',
            kwargs={
                'slug': 'group_which_is_not',
            }
        )
        response_guest = self.guest_client.get(
            missing_url,
        )
        self.assertEqual(
            response_guest.status_code,
            404,
        )
        self.assertTemplateUsed(
            response_guest,
            'misc/404.html',
        )
