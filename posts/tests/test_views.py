import os
import shutil

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from yatter.settings import BASE_DIR

from ..models import Follow, Group, Post

User = get_user_model()


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'temp_dir'))
class PostPagesTests(TestCase):
    '''Check view functions return expected context.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        cls.user = User.objects.create_user(
            'user_name',
            password='dfltusrpsswrd',
        )
        cls.follower = User.objects.create_user(
            'follower',
            password='dfltusrpsswrd',
        )
        cls.group = Group.objects.create(
            title='Название группы',
            slug='test_group',
            description='Описание группы',
        )
        cls.one_more_group = Group.objects.create(
            title='Название дополнительной группы',
            slug='test_one_more_group',
            description='Описание дополнительной группы',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif',
        )
        cls.post = Post.objects.create(
            text='Тело поста',
            author=cls.user,
            group=cls.group,
            image=uploaded,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        '''Create an unauthorized and an authorized client;
        create a dictionary "url name: url".'''
        self.guest_client = Client()
        self.authorized_client = Client()
        self.follower_client = Client()
        self.authorized_client.force_login(PostPagesTests.user)
        self.follower_client.force_login(PostPagesTests.follower)
        self.urls = {
            'index': reverse('posts:index'),
            'group_posts': reverse(
                'posts:group_posts',
                kwargs={
                    'slug': PostPagesTests.group.slug,
                }
            ),
            'profile': reverse(
                'posts:profile',
                kwargs={
                    'username': PostPagesTests.user.username,
                }
            ),
            'post': reverse(
                'posts:post',
                kwargs={
                    'username': PostPagesTests.user.username,
                    'post_id': PostPagesTests.post.id,
                }
            ),
            'follow_index': reverse('posts:follow_index'),
            'new_post': reverse('posts:new_post'),
            'post_edit': reverse(
                'posts:post_edit',
                kwargs={
                    'username': PostPagesTests.user.username,
                    'post_id': PostPagesTests.post.id,
                }
            ),
            'add_comment': reverse(
                'posts:add_comment',
                kwargs={
                    'username': PostPagesTests.user.username,
                    'post_id': PostPagesTests.post.id,
                }
            ),
            'profile_follow': reverse(
                'posts:profile_follow',
                kwargs={
                    'username': PostPagesTests.user.username,
                }
            ),
            'profile_unfollow': reverse(
                'posts:profile_unfollow',
                kwargs={
                    'username': PostPagesTests.user.username,
                }
            ),
        }

    def test_home_page(self):
        '''Check home page context.'''
        name = 'index'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        latest_post = response.context['page'][0]
        self.assertEqual(latest_post.text, PostPagesTests.post.text)
        self.assertEqual(latest_post.image, PostPagesTests.post.image)

    def test_home_page_cache(self):
        '''Check home page cache.'''
        name = 'index'
        url = self.urls[name]
        start_response = self.guest_client.get(url)
        Post.objects.create(
            text='Дополнительный пост',
            author=PostPagesTests.user,
        )
        intermediate_response = self.guest_client.get(url)
        self.assertEqual(
            start_response.content,
            intermediate_response.content,
        )
        cache.clear()
        end_response = self.guest_client.get(url)
        self.assertNotEqual(
            start_response.content,
            end_response.content,
        )

    def test_group_page(self):
        '''Check group page context;
        check the post is in the correct group.'''
        name = 'group_posts'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        latest_post = response.context['page'][0]
        group = response.context['group']
        one_more_group_posts_qty = Post.objects.filter(
            group=PostPagesTests.one_more_group
        ).count()
        self.assertEqual(latest_post.text, PostPagesTests.post.text)
        self.assertEqual(latest_post.image, PostPagesTests.post.image)
        self.assertEqual(group.title, PostPagesTests.group.title)
        self.assertEqual(one_more_group_posts_qty, 0)

    def test_new_post_page(self):
        '''Check form fields on the new post page.'''
        name = 'new_post'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_single_post_page(self):
        '''Check single post page context.'''
        name = 'post'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        latest_post = response.context['post']
        self.assertEqual(latest_post.text, PostPagesTests.post.text)
        self.assertEqual(latest_post.image, PostPagesTests.post.image)

    def test_post_edit_page(self):
        '''Check edit post page context.'''
        name = 'post_edit'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        field_text = response.context['form']['text'].value()
        self.assertEqual(field_text, PostPagesTests.post.text)

    def test_new_comment_page(self):
        '''Check form field on the new comment page.'''
        name = 'add_comment'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        form_field = response.context['form'].fields['text']
        self.assertIsInstance(form_field, forms.fields.CharField)

    def test_user_profile(self):
        '''Check user profile page context.'''
        name = 'profile'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        latest_post = response.context['page'][0]
        self.assertEqual(latest_post.image, PostPagesTests.post.image)
        self.assertEqual(latest_post.text, PostPagesTests.post.text)

    def test_follow(self):
        '''Check user can subscribe to another user.'''
        name = 'profile_follow'
        url = self.urls[name]
        subscriptions_start = Follow.objects.filter(
            user=PostPagesTests.follower,
        ).count()
        self.follower_client.get(url)
        subscriptions_end = Follow.objects.filter(
            user=PostPagesTests.follower,
        ).count()
        self.assertEqual(
            subscriptions_start,
            0,
        )
        self.assertEqual(
            subscriptions_end,
            subscriptions_start + 1,
        )

    def test_unfollow(self):
        '''Check user can unsubscribe.'''
        name = 'profile_unfollow'
        url = self.urls[name]
        Follow.objects.create(
            user=PostPagesTests.follower,
            following=PostPagesTests.user,
        )
        unsubscriptions_start = Follow.objects.filter(
            user=PostPagesTests.follower,
        ).count()
        self.follower_client.get(url)
        unsubscriptions_end = Follow.objects.filter(
            user=PostPagesTests.follower,
        ).count()
        self.assertEqual(
            unsubscriptions_start,
            1,
        )
        self.assertEqual(
            unsubscriptions_end,
            unsubscriptions_start - 1,
        )

    def test_follow_index(self):
        '''Check the new post only in subscribers feed.'''
        one_more_user = User.objects.create_user(
            'im_just_passing_by',
            password='dfltusrpsswrd',
        )
        one_more_client = Client()
        one_more_client.force_login(one_more_user)
        Follow.objects.create(
            user=PostPagesTests.follower,
            following=PostPagesTests.user,
        )
        name = 'follow_index'
        url = self.urls[name]
        follower_response = self.follower_client.get(url)
        one_more_user_response = one_more_client.get(url)
        follower_feed_qty = len(follower_response.context['page'])
        follower_last_post = follower_response.context['page'][0]
        one_more_user_qty = len(one_more_user_response.context['page'])
        self.assertEqual(
            follower_feed_qty,
            1,
        )
        self.assertEqual(
            follower_last_post.text,
            PostPagesTests.post.text,
        )
        self.assertEqual(
            one_more_user_qty,
            0,
        )

    def test_paginator(self):
        '''Check that paginator correctly divides posts by pages.'''
        posts = [
            Post(
                text=f'Тело поста {i}',
                author=PostPagesTests.user,
            ) for i in range(15)
        ]
        Post.objects.bulk_create(posts)
        name = 'index'
        url = self.urls[name]
        response = self.authorized_client.get(url)
        self.assertEqual(
            len(
                response.context.get('page')
            ),
            10,
        )
        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2'
        )
        self.assertEqual(
            len(
                response.context.get('page')
            ),
            6,
        )
