import pytest
from news.models import News, Comment
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):  
    return django_user_model.objects.create(username='Чтец')


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture(autouse=True)
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
        )
    return news


@pytest.fixture
def id_for_news(news):
    return news.id,


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        text='Текст коммента',
        author=author
        )
    return comment


@pytest.fixture
def id_for_comm(comment):
    return comment.id,


@pytest.fixture(autouse=True)
def newslist():
    today = datetime.today()
    all_news = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index))
        all_news.append(news)
    News.objects.bulk_create(all_news)



@pytest.fixture(autouse=True)
def comments_list(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


