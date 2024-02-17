import pytest
from django.conf import settings

from news.forms import CommentForm


def test_news_count(news_list, client, home_url):
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(news_list, client, home_url):
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_order(comment_list, detail_url, client):
    response = client.get(detail_url)
    assert 'news' in response.context
    all_comments = response.context['news'].comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


@pytest.mark.parametrize(
    # Задаём названия для параметров:
    'parametrized_client, form_in_context',
    (
        # Передаём фикстуры в параметры при помощи "ленивых фикстур":
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_form_in_client_context(
        parametrized_client, form_in_context, detail_url,
):
    response = parametrized_client.get(detail_url)
    form = response.context.get('form')
    assert isinstance(form, CommentForm) is form_in_context
