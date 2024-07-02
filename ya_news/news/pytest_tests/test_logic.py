import random
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError, assertRedirects

from news.pytest_tests.constants import COMMENT_DATA
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(
        client, url_news_detail
):
    """Анонимный пользователь не может отправить комментарий."""
    start_comment_count = Comment.objects.count()
    client.post(url_news_detail, data=COMMENT_DATA)
    assert Comment.objects.count() == start_comment_count


def test_user_can_create_comment(auth_client, url_news_detail):
    """Авторизованный пользователь может отправить комментарий."""
    start_comment_count = Comment.objects.count()
    auth_client.post(url_news_detail, data=COMMENT_DATA)
    assert Comment.objects.count() == start_comment_count + 1
    new_comment = Comment.objects.get()
    assert new_comment.text == COMMENT_DATA['text']


def test_user_cant_use_bad_words(auth_client, news, url_news_detail):
    """
    Если комментарий содержит запрещённые слова, он не будет опубликован,
    а форма вернёт ошибку.
    """
    start_comment_count = Comment.objects.count()
    random_word = random.choice(BAD_WORDS)
    bad_words_data = {'text': f'Какой-то текст, {random_word}, еще текст'}
    response = auth_client.post(url_news_detail, data=bad_words_data)
    assert Comment.objects.count() == start_comment_count
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )


def test_author_can_delete_comment(
    auth_client, url_news_detail, url_comment_delete
):
    """Авторизованный пользователь может удалять свои комментарии."""
    start_comment_count = Comment.objects.count()
    response = auth_client.delete(url_comment_delete)
    assertRedirects(response, url_news_detail + '#comments')
    assert Comment.objects.count() == start_comment_count - 1


def test_author_can_edit_comment(
        auth_client, comment, url_news_detail, url_comment_edit
):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = auth_client.post(url_comment_edit, data=COMMENT_DATA)
    assertRedirects(response, url_news_detail + '#comments')
    comment.refresh_from_db()
    assert comment.text == COMMENT_DATA['text']


def test_user_cant_edit_comment_of_another_user(
        another_author, comment, url_comment_edit
):
    """Авторизованный пользователь не может редактировать чужие комментарии."""
    start_comment_data = Comment.objects.get(pk=comment.pk)
    response = another_author.post(url_comment_edit, data=COMMENT_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == start_comment_data.text
    assert comment.news == start_comment_data.news
    assert comment.author == start_comment_data.author


def test_user_cant_delete_comment_of_another_user(
        another_author, url_comment_delete
):
    """Авторизованный пользователь не может удалять чужие комментарии."""
    start_comment_count = Comment.objects.count()
    response = another_author.delete(
        url_comment_delete, data=COMMENT_DATA
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == start_comment_count
