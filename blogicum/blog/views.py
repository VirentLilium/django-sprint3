from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


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
    post_list = (
        Post.objects
        .select_related('author', 'location', 'category')
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True)
        .order_by('-pub_date')[:5]
    )

    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, post_id):
    """
    Отображает страницу поста в соответствии с идентификатором.

    Публикация отображается, если:
    - дата публикации не позже текущего времени,
    - публикация опубликована,
    - категория опубликована.

    Иначе возвращает ошибку 404.

    Шаблон:
        blog/detail.html
    """
    post = get_object_or_404(
        Post.objects.select_related('author', 'location', 'category'),
        pk=post_id,
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
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

    Если категория не опубликована возвращает ошибку 404.

    Шаблон:
        blog/category.html
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = (
        Post.objects
        .select_related('author', 'location', 'category')
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category=category)
        .order_by('-pub_date')
    )

    context = {'category': category, 'post_list': post_list}
    return render(request, 'blog/category.html', context)
