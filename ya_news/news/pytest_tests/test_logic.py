from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(
        comment_form_data, detail_url, client,
):
    client.post(detail_url, data=comment_form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(
        author_client, comment_form_data, detail_url,
        author, news,
):
    response = author_client.post(detail_url, data=comment_form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(admin_client, detail_url, bad_words_data):
    response = admin_client.post(detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING,
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url):
    author_client.delete(delete_url)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_cant_delete_comment_of_another_user(
        reader_client, delete_url,
):
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_author_can_edit_comment(
        author_client, author_comment, edit_url,
        comment_form_data_new, detail_url,
):
    response = author_client.post(edit_url, data=comment_form_data_new)
    assertRedirects(response, f'{detail_url}#comments')
    new_comment = Comment.objects.get(pk=author_comment.id)
    assert new_comment.text == comment_form_data_new['text']
    assert new_comment.news == author_comment.news
    assert new_comment.author == author_comment.author


def test_user_cant_edit_comment_of_another_user(
        reader_client, author_comment, comment_form_data_new, edit_url,
):
    response = reader_client.post(edit_url, data=comment_form_data_new)
    assert response.status_code == HTTPStatus.NOT_FOUND
    new_comment = Comment.objects.get(pk=author_comment.id)
    assert new_comment.text == author_comment.text
    assert new_comment.news == author_comment.news
    assert new_comment.author == author_comment.author
