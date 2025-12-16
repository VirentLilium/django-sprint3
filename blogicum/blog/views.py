from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .constants import POSTS_ON_MAIN_PAGE
from .models import Category, Post


def get_post_objects():
    """
    Возвращает QuerySet постов с join по заданным полям и фильтрацией.

    - поля для select_related: 'author', 'location', 'category'.
    - фильтры: дата не позднее текущего времени, пост опубликован.
    """
    query_set = (Post.objects
                 .select_related('author', 'location', 'category')
                 .filter(pub_date__lte=timezone.now(),
                         is_published=True)
                 )

    return query_set


def index(request):
    """
    Главная страница блога.

    Отображает список публикаций:
    - с датой не позднее текущего времени,
    - опубликованных,
    - из опубликованных категорий.

    Шаблон:
        blog/index.html
    """
    post_list = (get_post_objects()
                 .filter(category__is_published=True)[:POSTS_ON_MAIN_PAGE]
                 )

    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """
    Отображает страницу поста в соответствии с его идентификатором.

    Публикация отображается, если:
    - дата публикации не позже текущего времени,
    - публикация опубликована,
    - категория опубликована.

    Иначе возвращает ошибку 404.

    Шаблон:
        blog/detail.html
    """
    post = (get_object_or_404(
        get_post_objects()
        .filter(category__is_published=True),
        pk=post_id)
    )

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """
    Отображает страницу категории в зависимости от слага category_slug.

    Выводятся только те публикации в категории, которые:
    - принадлежат выбранной категории,
    - опубликованы,
    - дата публикации — не позже текущего времени.

    Если категория не опубликована, возвращает ошибку 404.

    Шаблон:
        blog/category.html
    """
    category = (get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    )

    post_list = get_post_objects().filter(category=category)

    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)
