from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedAtModel, PublishedModel


User = get_user_model()


class Category(PublishedModel):
    """
    Модель категории.

    Атрибуты:
        title (str): Заголовок категории.
        description (str): Описание категории.
        slug (slug): Слаг категории.
        is_published (bool): Флаг категории, True - опубликовано.
        created_at (datetime): Дата и время добавления записи в базу.
    """

    title = models.CharField(max_length=256,
                             verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает название категории."""
        return self.title


class Location(CreatedAtModel):
    """
    Модель локации.

    Атрибуты:
        name (str): Название локации.
        is_published (bool): Флаг локации, True - опубликовано.
        created_at (datetime): Дата и время добавления записи в базу.
    """

    name = models.CharField(max_length=256, verbose_name='Название места')
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Возвращает название локации."""
        return self.name


class Post(PublishedModel):
    """
    Модель публикации (пост) для блога.

    Атрибуты:
        title (str): Заголовок поста.
        text (str): Основной текст публикации.
        pub_date (datetime): Дата и время публикации.
        created_at (datetime): Дата и время добавления записи в базу.
        is_published (bool): Флаг публикации, True - опубликовано.
        author (User): Пользователь, создавший пост.
        location (Location | None): Местоположение, может быть пустым.
        category (Category): Категория поста, обязательна.
    """

    title = models.CharField(max_length=256,
                             verbose_name='Заголовок')

    text = models.TextField(verbose_name='Текст')

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
        default_related_name = '%(app_label)s_%(model_name)s'
        ordering = ('-pub_date',)

    def __str__(self):
        """Возвращает заголовок публикации."""
        return self.title
