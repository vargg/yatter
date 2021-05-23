from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Group(models.Model):
    '''Allows to post posts to groups.'''
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Как будет называться ваше сообщество?',
    )
    slug = models.SlugField(
        max_length=25,
        unique=True,
        verbose_name='Ссылка',
        help_text=(
            'Сообществу нужен адрес. Можно использовать '
            'только латиницу, цифры, дефисы и знаки '
            'подчёркивания'
        ),
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Здесь кратко опишите своё сообщество',
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'posts:group_posts',
            kwargs={
                'slug': self.slug
            }
        )


class Post(models.Model):
    '''Stores user blog posts.'''
    text = models.TextField(
        verbose_name='Текст',
        help_text='Что будем публиковать на этот раз?',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name='group_id',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Опубликовать в сообществе?',
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )

    class Meta():
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:15]

    def get_absolute_url(self):
        return reverse(
            'posts:post',
            kwargs={
                'username': self.author,
                'post_id': self.pk
            },
        )


class Comment(models.Model):
    '''Stores user comments.'''
    text = models.TextField(
        verbose_name='Текст',
        help_text='Можно что-нибудь написать',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta():
        ordering = ['-created']

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписка',
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'following',
                ],
                name='unique_subscription',
            ),
        ]

    def __str__(self):
        return f'{self.user.username} subscribed to {self.following.username}'


class Tag(models.Model):
    '''Allows to mark posts.'''
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Тэг',
    )
    post = models.ForeignKey(
        Post,
        related_name='tags',
        verbose_name='Пост',
        on_delete=models.CASCADE,
    )

    class Meta():
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'post',
                    'title',
                ],
                name='unique_marking',
            ),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'posts:tagged_posts',
            kwargs={
                'tag': self.title
            }
        )
