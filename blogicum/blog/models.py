"""Модели приложения blog."""

from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedAtModel, PublishedModel


User = get_user_model()


class Category(PublishedModel):
    """Модель категории публикаций."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """
        Возвращает название объекта категории.

        :return: Строковое представление объекта.
        """
        return self.title


class Location(CreatedAtModel):
    """Модель местоположения публикации."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название места',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        """
        Возвращает название объекта локации.

        :return: Строковое представление объекта.
        """
        return self.name


class Post(PublishedModel):
    """Модель публикации блога."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )

    text = models.TextField(
        verbose_name='Текст',
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        """
        Возвращает название объекта поста.

        :return: Строковое представление объекта.
        """
        return self.title
