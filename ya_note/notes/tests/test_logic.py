from http import HTTPStatus

from pytils.translit import slugify

from notes.tests.base_test_class_and_const import (
    ADD_NOTE_URL, BaseTest, DELETE_NOTE_URL, EDIT_NOTE_URL, SUCCESS_NOTE_URL,
)
from notes.models import Note
from notes.forms import WARNING


class TestNoteCreation(BaseTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_anonymous_user_cant_create_note(self):
        notes_count_before = Note.objects.count()
        self.client.post(ADD_NOTE_URL, data=self.form_data)
        notes_count_after = Note.objects.count()
        self.assertEqual(notes_count_after, notes_count_before)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(ADD_NOTE_URL, data=self.form_data)
        self.assertRedirects(response, SUCCESS_NOTE_URL)
        notes_count = Note.objects.count()

        self.assertEqual(notes_count, 1)

        note = Note.objects.get()

        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, self.NOTE_SLUG)
        self.assertEqual(note.author, self.author)


class TestNoteEditDelete(BaseTest):

    NOTE_NEW_TEXT = 'Новый текст для заметки.'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_author_can_delete_note(self):
        notes_count_before = Note.objects.count()
        response = self.author_client.delete(DELETE_NOTE_URL)
        self.assertRedirects(response, SUCCESS_NOTE_URL)
        self.assertEqual(Note.objects.count(), notes_count_before - 1)

    def test_user_cant_delete_anothers_note(self):
        notes_count_before = Note.objects.count()
        response = self.second_author_client.delete(DELETE_NOTE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), notes_count_before)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            EDIT_NOTE_URL,
            data={
                'title': self.NOTE_TITLE,
                'text': self.NOTE_NEW_TEXT,
                'slug': self.NOTE_SLUG,
            },
        )
        self.assertRedirects(response, SUCCESS_NOTE_URL)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_NEW_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, self.NOTE_SLUG)

    def test_user_cant_edit_anothers_note(self):
        response = self.second_author_client.post(
            EDIT_NOTE_URL,
            data=self.form_data,
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.slug, self.NOTE_SLUG)
        self.assertEqual(note.author, self.author)


class TestSlug(BaseTest):
    """Проверка правильного занесения автоматического slug заметки."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_slugyfied_title(self):
        self.author_client.delete(DELETE_NOTE_URL)
        self.form_data.pop('slug')
        self.author_client.post(ADD_NOTE_URL, data=self.form_data)
        note = Note.objects.get()
        self.assertEqual(note.slug, slugify(self.NOTE_TITLE))

    def test_unique_slug(self):
        notes_count_before = Note.objects.count()
        response = self.author_client.post(ADD_NOTE_URL, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{self.note.slug}{WARNING}',
        )
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, notes_count_before)
