from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class NotesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.another_author = User.objects.create(username='Автор2')
        cls.reader = User.objects.create(username='Читатель простой')

        cls.author_client = Client()
        cls.another_author_client = Client()
        cls.reader_client = Client()

        cls.author_client.force_login(cls.author)
        cls.another_author_client.force_login(cls.another_author)
        cls.reader_client.force_login(cls.reader)

        cls.note_from_author = Note.objects.create(
            title='Заголовок',
            text='Текст ',
            author=cls.author,
            slug='note-slug'
        )

        cls.note_from_another_author = Note.objects.create(
            title='Заголовок2',
            text='Текст2',
            author=cls.another_author,
            slug='note-slug2'
        )

        cls.url_home = reverse('notes:home')
        cls.url_notes_list = reverse('notes:list')
        cls.url_notes_add = reverse('notes:add')
        cls.url_notes_edit = reverse(
            'notes:edit', args=(cls.note_from_author.slug,)
        )
        cls.url_notes_delete = reverse(
            'notes:delete', args=(cls.note_from_author.slug,)
        )
        cls.url_notes_detail = reverse(
            'notes:detail', args=(cls.note_from_author.slug,)
        )
        cls.url_login = reverse('users:login')
        cls.url_success = reverse('notes:success')

        cls.url_logout = reverse('users:logout')
        cls.url_signup = reverse('users:signup')
