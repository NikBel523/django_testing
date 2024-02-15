from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тесты маршрутов."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Человек занятой')
        cls.invaider = User.objects.create(username='Человек шпион')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='note',
            author=cls.author
        )

    def test_pages_availability(self):
        """Проверка доступа к домашней странице, и формам логирования."""
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_detail_edit_and_delete(self):
        """Проверка доступа не автора к операциям с чужими заметками."""
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.invaider, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete', 'notes:detail'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректов для неавторизированного юзера."""
        login_url = reverse('users:login')
        slug = (self.note.slug,)
        urls = (
            ('notes:edit', slug),
            ('notes:delete', slug),
            ('notes:detail', slug),
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
