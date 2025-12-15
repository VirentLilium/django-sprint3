from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )

    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение',
        related_name='posts'
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name='Категория',
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        """Возвращает заголовок публикации."""
        return self.title


class Category(models.Model):
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

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает название категории."""
        return self.title


class Location(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Добавлено')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Возвращает название локации."""
        return self.name
