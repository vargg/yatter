import os
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test import override_settings
from django.urls import reverse

from yatter.settings import BASE_DIR
from ..models import Comment, Group, Post

User = get_user_model()


@override_settings(MEDIA_ROOT=os.path.join(BASE_DIR, 'temp_dir'))
class CreatePostFormTests(TestCase):
    '''Check correct creation of a new post and editing.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        cls.user = User.objects.create_user(
            'user_name',
            password='dfltusrpsswrd'
        )
        cls.group = Group.objects.create(
            title='Название группы',
            slug='test_group',
            description='Описание группы',
        )
        Post.objects.create(
            text='Тело поста',
            author=cls.user,
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        '''Create an authorized client.'''
        self.authorized_client = Client()
        self.authorized_client.force_login(CreatePostFormTests.user)

    def test_create_new_post(self):
        '''Checking if a new post has been added;
        control the number of posts before and after;
        control the number of posts in group before and after;
        performed for an authorized user;
        checking redirection after creation.'''
        post_count_before = Post.objects.count()
        group_post_count_before = Post.objects.filter(
            group=CreatePostFormTests.group
        ).count()
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
            content_type='image/gif'
        )
        form_data = {
            'text': 'Пост',
            'group': CreatePostFormTests.group.id,
            'image': uploaded,
        }
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True,
        )
        post_count_after = Post.objects.count()
        group_post_count_after = Post.objects.filter(
            group=CreatePostFormTests.group
        ).count()
        self.assertRedirects(response, reverse('posts:index'))
        self.assertTrue(Post.objects.filter(
            image='posts/small.gif').exists())
        self.assertEqual(
            post_count_after,
            post_count_before + 1,
        )
        self.assertEqual(
            group_post_count_after,
            group_post_count_before + 1,
        )
        print(Post.objects.last().text)

    def test_edit_post(self):
        '''Edit post, check edited post and redirect;
        performed for an authorized user (author of the post).'''
        edit_post_url = reverse(
            'posts:post_edit',
            kwargs={
                'username': CreatePostFormTests.user,
                'post_id': 1,
            }
        )
        form_data = {
            'text': 'Изменённое тело поста',
        }
        response = self.authorized_client.post(
            edit_post_url,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse(
                'posts:post',
                kwargs={
                    'username': CreatePostFormTests.user,
                    'post_id': 1,
                }
            )
        )
        self.assertEqual(
            Post.objects.get(pk=1).text,
            'Изменённое тело поста'
        )


class CreateCommentFormTests(TestCase):
    '''Check correct creation of a new comment.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        cls.user = User.objects.create_user(
            'user_name',
            password='dfltusrpsswrd'
        )
        cls.post = Post.objects.create(
            text='Тело поста',
            author=cls.user,
        )
        Comment.objects.create(
            text='Первый',
            post=cls.post,
            author=cls.user,
        )

    def setUp(self):
        '''Create an authorized client.'''
        self.authorized_client = Client()
        self.authorized_client.force_login(CreateCommentFormTests.user)

    def test_create_new_comment(self):
        '''Checking if a new comment has been added;
        control the number of comments before and after;
        performed for an authorized user;
        checking redirection after creation.'''
        comment_count_before = Comment.objects.filter(
            post=CreateCommentFormTests.post
        ).count()
        form_data = {
            'text': 'Коммент',
            'post': CreateCommentFormTests.post,
            'author': CreateCommentFormTests.user,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={
                    'username': CreateCommentFormTests.user.username,
                    'post_id': CreateCommentFormTests.post.id,
                },
            ),
            data=form_data,
            follow=True,
        )
        comment_count_after = Comment.objects.filter(
            post=CreateCommentFormTests.post
        ).count()
        self.assertRedirects(
            response,
            reverse(
                'posts:post',
                kwargs={
                    'username': CreateCommentFormTests.user.username,
                    'post_id': CreateCommentFormTests.post.id,
                }
            ),
        )
        self.assertEqual(
            comment_count_after,
            comment_count_before + 1,
        )
