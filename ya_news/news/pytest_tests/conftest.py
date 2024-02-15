import pytest
from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def news():
    news = News.objects.create(title='Заголовок', text='Текст')
    return news


@pytest.fixture
def news_id(news):
    return (news.id,)


@pytest.fixture
def author_comment(news, author):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def author_comment_id(author_comment):
    return (author_comment.id,)


@pytest.fixture
def news_list():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Текст новости.',
            date=today - timedelta(days=index),
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_list(news, author):
    now = timezone.now()
    for index in range(10):
        # Создаём объект и записываем его в переменную.
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        # Сразу после создания меняем время создания комментария.
        comment.created = now + timedelta(days=index)
        # И сохраняем эти изменения.
        comment.save()


@pytest.fixture
def comment_text():
    return 'Текст комментария'


@pytest.fixture
def form_data(comment_text):
    return {
        'text': comment_text,
    }


@pytest.fixture
def comment_text_new():
    return 'Новый текст комментария'


@pytest.fixture
def form_data_new(comment_text_new):
    return {
        'text': comment_text_new,
    }


@pytest.fixture
def detail_url(news_id):
    return reverse('news:detail', args=news_id)
