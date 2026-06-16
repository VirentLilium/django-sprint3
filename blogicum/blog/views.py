"""Представления приложения blog."""

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from blog.constants import POSTS_ON_MAIN_PAGE
from blog.models import Category, Post


def get_post_objects() -> QuerySet[Post]:
    """
    Возвращает опубликованные посты для отображения на сайте.

    В выборку попадают посты:
    - с датой публикации не позже текущего времени;
    - с флагом is_published=True;
    - из опубликованных категорий.

    :return: QuerySet опубликованных постов.
    """
    return (
        Post.objects
        .select_related('author', 'location', 'category')
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )
    )


def index(request: HttpRequest) -> HttpResponse:
    """
    Отображает главную страницу блога.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с главной страницей.
    """
    post_list = get_post_objects()[:POSTS_ON_MAIN_PAGE]

    return render(
        request,
        'blog/index.html',
        {'post_list': post_list}
    )


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    """
    Отображает страницу отдельной публикации.

    :param request: Объект HTTP-запроса.
    :param post_id: Идентификатор публикации.
    :return: HTTP-ответ со страницей публикации.
    """
    post = get_object_or_404(get_post_objects(), pk=post_id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(
    request: HttpRequest,
    category_slug: str,
) -> HttpResponse:
    """
    Отображает страницу категории с публикациями.

    :param request: Объект HTTP-запроса.
    :param category_slug: Slug категории.
    :return: HTTP-ответ со страницей категории.
    """
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_post_objects().filter(category=category)

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': post_list,
        },
    )
