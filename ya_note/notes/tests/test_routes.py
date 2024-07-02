from notes.tests.constants import PAGE_NOT_FOUND, PAGE_OK
from notes.tests.notes_fixtures import NotesTestCase


class TestRoutes(NotesTestCase):

    def test_pages_availability(self):
        """Тест доступности страниц анонимному посетителю."""
        urls = (
            self.url_home,
            self.url_login,
            self.url_logout,
            self.url_signup,
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, PAGE_OK)

    def test_pages_availability_for_author(self):
        """Тест доступности страниц для автора заметок."""
        urls = (
            self.url_notes_detail,
            self.url_notes_delete,
            self.url_notes_edit,
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, PAGE_OK)

    def test_pages_availability_for_reader(self):
        """Тест доступности страниц для читателя заметок."""
        urls = (
            self.url_notes_list,
            self.url_success,
            self.url_notes_add,
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.reader_client.get(url)
                self.assertEqual(response.status_code, PAGE_OK)

    def test_pages_not_availability_for_reader(self):
        """Тест недоступности страниц для читателя заметок."""
        urls = (
            self.url_notes_detail,
            self.url_notes_delete,
            self.url_notes_edit,
        )
        for url in urls:
            with self.subTest(name=url):
                response = self.reader_client.get(url)
                self.assertEqual(response.status_code, PAGE_NOT_FOUND)

    def test_redirect_for_anonymous(self):
        """Тест редиректа со страниц для анонимных пользователей."""
        urls = (
            self.url_notes_list,
            self.url_notes_detail,
            self.url_notes_add,
            self.url_notes_edit,
            self.url_notes_delete,
            self.url_success,
        )
        for url in urls:
            with self.subTest(name=url):
                redirect_url = f'{self.url_login}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
