import pytest
from news.models import Comment, News
from django.conf import settings
from django.urls import reverse



@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client',
    (
        pytest.lazy_fixture('admin_client'),
        pytest.lazy_fixture('author_client'),
    ),
)
def test_news_count(parametrized_client):
    url = reverse('news:home')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client',
    (
        pytest.lazy_fixture('admin_client'),
        pytest.lazy_fixture('author_client'),
    ),
)
def test_news_order(parametrized_client):
    url = reverse('news:home')
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news):
    url = reverse('news:detail', args=(news.id,)) 
    response = client.get(url)
    new = response.context['news']
    all_comments = new.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news):
    url = reverse('news:detail', args=(news.id,)) 
    response = client.get(url)
    assert 'form' not in response.context

@pytest.mark.django_db
def test_authorized_client_has_form(author_client, news):
    url = reverse('news:detail', args=(news.id,)) 
    response = author_client.get(url)
    assert 'form' in response.context