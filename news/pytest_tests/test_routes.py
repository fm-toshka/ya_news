import pytest
from django.urls import reverse
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('id_for_news')),
    ),
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('id_for_news')),
    ),
)
def test_pages_availability_for_auth_user(admin_client, name, args):
    url = reverse(name, args=args)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('id_for_comm')),
        ('news:edit', pytest.lazy_fixture('id_for_comm')),
    ),
)
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('id_for_comm')),
        ('news:edit', pytest.lazy_fixture('id_for_comm')),
    ),
)
def test_pages_availability_for_different_users(
        parametrized_client, name, expected_status, args
):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
    