from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    '''Extension of the User model.'''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        blank=True,
        verbose_name='Пользователь',
    )
    avatar = models.ImageField(
        upload_to='users/avatars/%Y/%m/%d',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )
    status = models.CharField(
        max_length=150,
        verbose_name='Статус',
        blank=True,
    )
    about = models.CharField(
        max_length=500,
        verbose_name='Обо мне',
        blank=True,
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
