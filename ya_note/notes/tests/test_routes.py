from http import HTTPStatus

from notes.tests.base_test_class_and_const import (
    ADD_NOTE_URL, BaseTest, DETAIL_NOTE_URL, DELETE_NOTE_URL, EDIT_NOTE_URL,
    HOME_NOTES_URL, LIST_NOTES_URL, SUCCESS_NOTE_URL, USER_LOGIN_URL,
    USER_LOGOUT_URL, USER_SIGNUP_URL,
)


class TestRoutes(BaseTest):
    """Тесты маршрутов."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    # Также как и pytest не совсем понимаю, как объеденить
    # Два разных статуса для анонимного опльзователя
    def test_pages_availability_for_anonymous_client(self):
        """Проверка доступа к домашней странице, и формам логирования."""
        urls = (
            HOME_NOTES_URL,
            USER_LOGIN_URL,
            USER_LOGOUT_URL,
            USER_SIGNUP_URL,
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_detail_edit_and_delete(self):
        """Проверка доступа не автора к операциям с чужими заметками."""
        users_statuses = (
            (self.author_client, HTTPStatus.OK),
            (self.second_author_client, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            for url in (EDIT_NOTE_URL, DELETE_NOTE_URL, DETAIL_NOTE_URL):
                with self.subTest(user=user, name=url):
                    response = user.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректов для неавторизированного юзера."""
        urls = (
            EDIT_NOTE_URL,
            DELETE_NOTE_URL,
            DETAIL_NOTE_URL,
            LIST_NOTES_URL,
            SUCCESS_NOTE_URL,
            ADD_NOTE_URL,
        )
        for url in urls:
            with self.subTest(name=url):
                redirect_url = f'{USER_LOGIN_URL}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
