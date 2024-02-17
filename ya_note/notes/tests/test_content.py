from notes.forms import NoteForm
from notes.models import Note
from notes.tests.base_test_class_and_const import (
    BaseTest, LIST_NOTES_URL, ADD_NOTE_URL, EDIT_NOTE_URL,
    TESTING_NOTES_NUMBER,
)


class TestOrdering(BaseTest):
    """Test for notes contetnt."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Note.objects.bulk_create(
            Note(
                title=f'{cls.NOTE_TITLE} {index}',
                text=cls.NOTE_TEXT,
                slug=index,
                author=cls.author,
            )
            for index in range(TESTING_NOTES_NUMBER)
        )

    def test_notes_order(self):
        """Проверка сортировки записей от первой к последней."""
        response = self.author_client.get(LIST_NOTES_URL)
        self.assertIn('object_list', response.context)
        object_list = response.context['object_list']
        notes_ids = [note.id for note in object_list]
        sorted_notes_ids = sorted(notes_ids)
        self.assertEqual(notes_ids, sorted_notes_ids)


class TestNoteInContext(BaseTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_note_in_context_when_needed(self):
        users_cases = (
            (self.author_client, True),
            (self.second_author_client, False),
        )
        for user_client, note in users_cases:
            with self.subTest(user=user_client):
                response = user_client.get(LIST_NOTES_URL)
                object_list = response.context['object_list']
                self.assertIs(self.note in object_list, note)

    def test_form_in_edit_add(self):
        urls = (ADD_NOTE_URL, EDIT_NOTE_URL)
        for url in urls:
            response = self.author_client.get(url)
            with self.subTest(response):
                form = response.context.get('form')
                self.assertIsInstance(form, NoteForm, True)
