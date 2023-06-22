import pytest
from news.models import Comment, News
from django.conf import settings
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from pytest_django.asserts import assertFormError, assertRedirects
from http import HTTPStatus


COMMENT_TEXT = 'Текст нового комментария'
form_data = {'text': COMMENT_TEXT}


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 2


@pytest.mark.django_db
def test_auth_user_can_create_comment(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 3


@pytest.mark.django_db
def test_user_cant_use_bad_words(news, author_client):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
            response,
            form='form',
            field='text',
            errors=WARNING
        )
    comments_count = Comment.objects.count()
    assert comments_count == 2


@pytest.mark.django_db
def test_author_can_delete_comment(author_client, news, comment):
    comments_count = Comment.objects.count()
    assert comments_count == 3
    news_url = reverse('news:detail', args=(news.id,)) 
    url_to_comments = news_url + '#comments'
    delete_url = reverse('news:delete', args=(comment.id,))
    response = author_client.delete(delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 2


@pytest.mark.django_db
def test_user_cant_delete_comment_of_another_user(reader_client, admin_client, news, comment):
    comments_count = Comment.objects.count()
    assert comments_count == 3
    delete_url = reverse('news:delete', args=(comment.id,))
    response = reader_client.post(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 3


@pytest.mark.django_db
def test_author_can_edit_comment(author_client, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = author_client.post(url, form_data)
    comment.refresh_from_db()
    assert comment.text == form_data['text']


@pytest.mark.django_db
def test_other_author_cant_edit_comment(admin_client, comment):
    url = reverse('news:edit', args=(comment.id,))
    response = admin_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get(id=comment.id)
    assert comment.text == comment_from_db.text
    