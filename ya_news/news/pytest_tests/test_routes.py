import pytest
from django.test import Client
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from news.pytest_tests.constants import PAGE_NOT_FOUND, PAGE_OK

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (lf('url_news_home'), Client(), PAGE_OK),
        (lf('url_user_login'), Client(), PAGE_OK),
        (lf('url_user_logout'), Client(), PAGE_OK),
        (lf('url_user_signup'), Client(), PAGE_OK),
        (lf('url_news_detail'), Client(), PAGE_OK),
        (lf('url_comment_edit'), lf('auth_client'), PAGE_OK),
        (lf('url_comment_edit'), lf('another_author'), PAGE_NOT_FOUND),
        (lf('url_comment_delete'), lf('auth_client'), PAGE_OK),
        (lf('url_comment_delete'), lf('another_author'), PAGE_NOT_FOUND),
    ),
)
def test_availability_pages_for_users(
        url, parametrized_client, expected_status
):
    """
    Тестирование доступности страниц анонимному
    и зарегистрированным пользователям.
    """
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (lf('url_comment_edit'), lf('url_comment_delete'))
)
def test_availability_pages_edit_delete_for_anonymous_user(
    client, comment, name, url_user_login
):
    """
    Анонимному пользователю не доступно редактирование и удаление
    комментариев он должен перенаправляться на страницу авторизации.
    """
    url = name
    expected_url = f'{url_user_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
