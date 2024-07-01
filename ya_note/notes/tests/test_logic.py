from notes.forms import WARNING
from notes.models import Note
from notes.tests.constants import PAGE_NOT_FOUND, PAGE_OK
from notes.tests.notes_fixtures import NotesTestCase
from pytils.translit import slugify


class TestLogic(NotesTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.note_form_data = {
            'title': 'Заголовок формы',
            'text': 'Текст заметки в форме',
            'slug': 'note-form-slug'
        }

    def test_create_note_for_regular_user(self):
        """Тест создания заметки авторизованным пользователем."""
        Note.objects.all().delete()
        start_notes_count = Note.objects.count()
        self.first_author_client.post(
            self.url_notes_add, data=self.note_form_data
        )
        self.assertEqual(Note.objects.count(), start_notes_count + 1)
        added_note = Note.objects.get()
        self.assertEqual(added_note.text, self.note_form_data['text'])

    def test_create_note_for_anon_user(self):
        """Тест создания заметки анонимным пользователем."""
        start_notes_count = Note.objects.count()
        response = self.client.post(
            self.url_notes_add, data=self.note_form_data
        )
        self.assertEqual(Note.objects.count(), start_notes_count)
        self.assertRedirects(
            response, f'{self.url_login}?next={self.url_notes_add}'
        )

    def test_unique_slug(self):
        """Тестирование уникальности slug заметки."""
        start_notes_count = Note.objects.count()
        self.first_author_client.post(
            self.url_notes_add, data=self.note_form_data
        )
        response = self.first_author_client.post(
            self.url_notes_add, data=self.note_form_data
        )
        self.assertEqual(Note.objects.count(), start_notes_count + 1)
        self.assertFormError(response, form='form', field='slug',
                             errors=f'{self.note_form_data["slug"]}{WARNING}')

    def test_empty_slug(self):
        """Тестирование невозможности создания заметки с пустым slug."""
        Note.objects.all().delete()
        slug_name = slugify(self.note_form_data['title'])
        del self.note_form_data['slug']
        self.first_author_client.post(
            self.url_notes_add, data=self.note_form_data
        )
        added_note = Note.objects.get()
        self.assertEqual(added_note.slug, slug_name)

    def test_edit_note_by_author(self):
        """Тестирование возможности редактирования заметки автором."""
        self.first_author_client.post(
            self.url_notes_edit, data=self.note_form_data
        )
        self.note_from_first_author.refresh_from_db()
        self.assertEqual(
            self.note_from_first_author.title, self.note_form_data['title']
        )
        self.assertEqual(
            self.note_from_first_author.text, self.note_form_data['text']
        )
        self.assertEqual(
            self.note_from_first_author.slug, self.note_form_data['slug']
        )

    def test_delete_note_by_author(self):
        """Тестирование возможности удаления заметки автором."""
        start_notes_count = Note.objects.count()
        response = self.first_author_client.delete(self.url_notes_delete)
        self.assertEqual(Note.objects.count(), start_notes_count - 1)
        self.assertRedirects(response, self.url_success)

    def test_edit_note_by_second_author(self):
        """Тестирование невозможности редактирования чужих заметок."""
        start_notes_count = Note.objects.count()
        response = self.second_author_client.delete(self.url_notes_delete)
        self.assertEqual(response.status_code, PAGE_NOT_FOUND)
        self.assertEqual(Note.objects.count(), start_notes_count)
