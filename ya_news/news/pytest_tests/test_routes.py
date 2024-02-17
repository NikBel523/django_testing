from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


HOME_URL = pytest.lazy_fixture('home_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')


@pytest.mark.parametrize(
    'url',
    (
        HOME_URL,
        DETAIL_URL,
        LOGIN_URL,
        LOGOUT_URL,
        SIGNUP_URL,
    )
)
def test_pages_availability_for_anonymous_client(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ),
)
@pytest.mark.parametrize(
    'url',
    (EDIT_URL, DELETE_URL),
)
def test_availability_for_comment_edit_and_delete(
    parametrized_client, expected_status, url
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (EDIT_URL, DELETE_URL),
)
def test_redirect_for_anonymous_client(url, client, login_url):
    response = client.get(url)
    redirect_url = f'{login_url}?next={url}'
    assertRedirects(response, redirect_url)
