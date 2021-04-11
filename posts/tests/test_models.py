from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Comment, Group, Post

User = get_user_model()


class GroupModelTest(TestCase):
    '''Check verbose names and help texts of the fields;
    check string representation.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Название группы',
            slug='test_group',
            description='Описание группы',
        )

    def test_title_label(self):
        group = GroupModelTest.group
        field_verboses = {
            'title': 'Название',
            'slug': 'Ссылка',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name,
                    expected
                )

    def test_help_text(self):
        group = GroupModelTest.group
        field_help_text = {
            'title': 'Как будет называться ваше сообщество?',
            'slug': (
                'Сообществу нужен адрес. Можно использовать '
                'только латиницу, цифры, дефисы и знаки '
                'подчёркивания'
            ),
            'description': 'Здесь кратко опишите своё сообщество',
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text,
                    expected
                )

    def test_str_convert(self):
        group = GroupModelTest.group
        expected = group.title
        self.assertEqual(str(group), expected)


class PostModelTest(TestCase):
    '''Check verbose names and help texts of the fields;
    check string representation.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        _user = User.objects.create_user(
            'user_name',
            password='dfltusrpsswrd'
        )
        _group = Group.objects.create(
            title='Название группы',
            slug='test_group',
            description='Описание группы',
        )
        cls.post = Post.objects.create(
            text='Тело поста длиной больше 15 символов',
            author=_user,
            group=_group,
        )

    def test_title_label(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name,
                    expected
                )

    def test_help_text(self):
        post = PostModelTest.post
        field_help_text = {
            'text': 'Что будем публиковать на этот раз?',
            'group': 'Опубликовать в сообществе?',
        }
        for value, expected in field_help_text.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text,
                    expected
                )

    def test_str_convert(self):
        post = PostModelTest.post
        expected = post.text[:15]
        self.assertEqual(str(post), expected)


class CommentModelTest(TestCase):
    '''Check verbose names and help texts of the fields;
    check string representation.'''
    @classmethod
    def setUpClass(cls):
        '''Create test objects in db.'''
        super().setUpClass()
        _user = User.objects.create_user(
            'user_name',
            password='dfltusrpsswrd'
        )
        _post = Post.objects.create(
            text='Тело поста длиной больше 15 символов',
            author=_user,
        )
        cls.comment = Comment.objects.create(
            text='Комментарий к посту',
            post=_post,
            author=_user,
        )

    def test_title_label(self):
        comment = CommentModelTest.comment
        self.assertEqual(
            comment._meta.get_field('text').verbose_name,
            'Текст'
        )

    def test_help_text(self):
        comment = CommentModelTest.comment
        self.assertEqual(
            comment._meta.get_field('text').help_text,
            'Можно что-нибудь написать'
        )

    def test_str_convert(self):
        comment = CommentModelTest.comment
        expected = comment.text[:15]
        self.assertEqual(str(comment), expected)
