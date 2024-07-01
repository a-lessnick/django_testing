import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count_on_home_page(client, all_news, url_news_home):
    f"""
    Количество новостей на главной странице — не более 
    {settings.NEWS_COUNT_ON_HOME_PAGE}.
    """
    response = client.get(url_news_home)
    news = response.context['object_list']
    news_count = news.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order_on_home_page(client, all_news, url_news_home):
    """Новости отсортированы от самой свежей к самой старой."""
    response = client.get(url_news_home)
    news = response.context['object_list']
    all_dates = [one_news.date for one_news in news]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, news, comments, url_news_detail):
    """
    Комментарии на странице отдельной новости отсортированы
    старые в начале списка, новые — в конце.
    """
    response = client.get(url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = [
        one_comment.created for one_comment in news.comment_set.all()
    ]
    sorted_comments = sorted(all_comments)
    assert all_comments == sorted_comments


def test_anonymous_client_has_no_form(client, news, url_news_detail):
    """
    Анонимному пользователю недоступна форма для
    отправки комментария на странице отдельной новости.
    """
    response = client.get(url_news_detail)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, news, url_news_detail):
    """
    Авторизованному пользователю доступна форма для отправки
    комментария на странице отдельной новости.
    """
    response = admin_client.get(url_news_detail)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
