from notes.tests.notes_test_case import NotesTestCase
from notes.forms import NoteForm


class TestContent(NotesTestCase):

    def test_notes_list_for_first_author(self):
        """
        Тест того, что в список заметок одного пользователя
        попадают его заметки.
        """
        response = self.first_author_client.get(self.url_notes_list)
        self.assertIn(
            self.note_from_first_author, response.context['object_list']
        )

    def test_notes_list_for_second_author(self):
        """
        Тест того, что в список заметок одного пользователя
        не попадают заметки другого пользователя.
        """
        response = self.first_author_client.get(self.url_notes_list)
        self.assertNotIn(
            self.note_from_second_author, response.context['object_list']
        )

    def test_pages_contains_form(self):
        """
        Тестирование передачи формы на страницы создания
        и редактирования заметок.
        """
        urls = (self.url_notes_add, self.url_notes_edit)
        for url in urls:
            with self.subTest(name=url):
                response = self.first_author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
