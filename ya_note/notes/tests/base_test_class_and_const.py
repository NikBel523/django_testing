from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

TESTING_NOTES_NUMBER = 3

NOTE_SLUG_FOR_URL = 'zametka'

LIST_NOTES_URL = reverse('notes:list')
ADD_NOTE_URL = reverse('notes:add')
SUCCESS_NOTE_URL = reverse('notes:success')
HOME_NOTES_URL = reverse('notes:home')
USER_LOGIN_URL = reverse('users:login')
USER_LOGOUT_URL = reverse('users:logout')
USER_SIGNUP_URL = reverse('users:signup')

EDIT_NOTE_URL = reverse('notes:edit', args=(NOTE_SLUG_FOR_URL,))
DELETE_NOTE_URL = reverse('notes:delete', args=(NOTE_SLUG_FOR_URL,))
DETAIL_NOTE_URL = reverse('notes:detail', args=(NOTE_SLUG_FOR_URL,))

User = get_user_model()


class BaseTest(TestCase):

    NOTE_TITLE = 'Заметка'
    NOTE_TEXT = 'Текст заметки'
    NOTE_SLUG = NOTE_SLUG_FOR_URL

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.second_author = User.objects.create(username='Второй автор')
        cls.second_author_client = Client()
        cls.second_author_client.force_login(cls.second_author)

        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author,
        )

        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }
