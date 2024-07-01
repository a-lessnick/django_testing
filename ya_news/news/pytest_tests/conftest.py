from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News

COMMENTS_COUNT = 3


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def another_author(django_user_model):
    client = Client()
    client.force_login(
        django_user_model.objects.create(username='Другой автор')
    )
    return client


@pytest.fixture
def auth_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return news


@pytest.fixture
def all_news():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        text='Текст комментария.',
        author=author,
        news=news
    )
    return comment


@pytest.fixture
def comments(author, news):
    now = timezone.now()
    for index in range(COMMENTS_COUNT):
        new_comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        new_comment.created = now + timedelta(days=index)
        new_comment.save()


@pytest.fixture
def url_news_detail(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_comment_delete(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def url_comment_edit(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def url_news_home():
    return reverse('news:home')


@pytest.fixture
def url_user_login():
    return reverse('users:login')


@pytest.fixture
def url_user_logout():
    return reverse('users:logout')


@pytest.fixture
def url_user_signup():
    return reverse('users:signup')
