from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import WARNING

User = get_user_model()


TESTING_NOTES_NUMBER = 3


class TestNoteCreation(TestCase):

    NOTE_TITLE = 'Test_note'
    NOTE_TEXT = "It's me Note!"
    NOTE_SLUG = 'test_note'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='author')
        cls.url = reverse('notes:add')
        cls.url_redirect = reverse('notes:success')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, self.url_redirect)
        notes_count = Note.objects.count()

        self.assertEqual(notes_count, 1)

        note = Note.objects.get()

        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, self.NOTE_SLUG)
        self.assertEqual(note.author, self.user)


class TestNoteEditDelete(TestCase):

    NOTE_TITLE = 'Note'
    NOTE_TEXT = 'Initial note text.'
    NOTE_SLUG = 'note'
    NOTE_NEW_TEXT = 'This is new note text.'

    @classmethod
    def setUpTestData(cls):
        # Создаём необходимых юзеров и их клиенты

        # Автор заметки
        cls.author = User.objects.create(username='Author')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        # Не автор заметки
        cls.not_author = User.objects.create(username='Not_author')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        # Формируем заметку и форму для POST запроса на её изменение
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author,
        )

        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_NEW_TEXT,
            'slug': cls.NOTE_SLUG,
        }

        # Форируем нужные пути
        cls.edit_note_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_note_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_note_url)
        self.assertRedirects(response, self.success_url)
        notes_count = Note.objects.count()
        self.assertEquals(notes_count, 0)

    def test_user_can_delete_anothers_note(self):
        response = self.not_author_client.delete(self.delete_note_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEquals(notes_count, 1)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.edit_note_url,
            data=self.form_data,
        )
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_NEW_TEXT)

    def test_user_cant_edit_anothers_note(self):
        response = self.not_author_client.post(
            self.edit_note_url,
            data=self.form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)


class TestSlug(TestCase):
    """Проверка правильного занесения автоматического slug заметки."""

    NOTES_URL = reverse('notes:list')
    NOTE_ADD_URL = reverse('notes:add')
    NOTE_TITLE = 'Note'
    NOTE_TEXT = 'Initial note text.'
    NOTE_SLUG = 'note'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            author=cls.author,
        )

        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }

    def test_slugyfied_title(self):
        self.client.force_login(self.author)
        note = Note.objects.get()
        self.assertEqual(note.slug, self.NOTE_SLUG)

    def test_unique_slug(self):
        self.client.force_login(self.author)
        response = self.client.post(self.NOTE_ADD_URL, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{self.note.slug}{WARNING}',
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
