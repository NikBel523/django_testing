from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(form_data, detail_url, client):
    client.post(detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author_client, form_data, detail_url, author, news, comment_text
):
    response = author_client.post(detail_url, data=form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(admin_client, detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = admin_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, author_comment):
    url_delete = reverse('news:delete', args=(author_comment.id,))
    author_client.delete(url_delete)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        reader_client, author_comment,
):
    url_delete = reverse('news:delete', args=(author_comment.id,))
    response = reader_client.delete(url_delete)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client, author_comment,
        form_data_new, detail_url, comment_text_new,
):
    edit_url = reverse('news:edit', args=(author_comment.id,))
    response = author_client.post(edit_url, data=form_data_new)
    assertRedirects(response, f'{detail_url}#comments')
    author_comment.refresh_from_db()
    assert author_comment.text == comment_text_new


def test_user_cant_edit_comment_of_another_user(
        reader_client, author_comment, form_data_new, comment_text,
):
    edit_url = reverse('news:edit', args=(author_comment.id,))
    response = reader_client.post(edit_url, data=form_data_new)
    assert response.status_code == HTTPStatus.NOT_FOUND
    author_comment.refresh_from_db()
    assert author_comment.text == comment_text
