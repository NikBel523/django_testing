from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


TESTING_NOTES_NUMBER = 3

User = get_user_model()


class TestOrdering(TestCase):
    """Test for notes contetnt."""

    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        Note.objects.bulk_create(
            Note(
                title=f'Заметка {index}',
                text='Текст заметки.',
                slug=index,
                author=cls.author,
            )
            for index in range(TESTING_NOTES_NUMBER)
        )

    def test_notes_order(self):
        """Проверка сортировки записей от первой к последней."""
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        notes_ids = [note.id for note in object_list]
        sorted_notes_ids = sorted(notes_ids)
        self.assertEqual(notes_ids, sorted_notes_ids)


class TestNoteInContext(TestCase):

    NOTES_URL = reverse('notes:list')
    NOTE_ADD_URL = reverse('notes:add')
    NOTE_TITLE = 'Note'
    NOTE_TEXT = 'Initial note text.'
    NOTE_SLUG = 'note'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.second_author = User.objects.create(username='Второй автор')
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
            author=cls.author,
        )
        cls.url_edit = reverse('notes:edit', args=(cls.note.slug,))

        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }

    def test_note_in_context_when_needed(self):
        users_cases = (
            (self.author, 1),
            (self.second_author, 0),
        )
        for user, note in users_cases:
            self.client.force_login(user)
            with self.subTest(user=user):
                response = self.client.get(self.NOTES_URL)
                object_list = response.context['object_list']
                self.assertEqual(object_list.count(), note)

    def test_form_in_edit_add(self):
        urls = (self.NOTE_ADD_URL, self.url_edit)
        for url in urls:
            response = self.author_client.get(url)
            with self.subTest(response):
                self.assertIn('form', response.context)
