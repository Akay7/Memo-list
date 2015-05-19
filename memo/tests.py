import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Memo, Category


class MemoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Gordon', password='qwerty')
        self.memo = Memo.objects.create(title="FirstTODO", owner=self.user)
        self.user = User.objects.create_user(
            username='Aliance', password='123')
        self.alien_memo = Memo.objects.create(title="Control", owner=self.user)

    def test_memo_creating(self):
        self.assertEqual(self.memo.title, "FirstTODO")
        self.assertEqual(self.memo.owner.username, "Gordon")

    def test_memo_static_html_page(self):
        response = self.client.get('/note/%s' % self.memo.id)
        self.assertEqual(response.status_code, 404)

        self.memo.published = True
        self.memo.save()
        response = self.client.get('/note/%s' % self.memo.id)
        self.assertContains(response, "FirstTODO")

    def test_add_memo_with_new_category(self):
        category = Category.objects.create(name='ToDo')
        todo = Memo.objects.create(
            title="Kill headcrab",
            category=category,
            owner=self.user,
        )
        self.assertEqual(todo.category, category)

    def test_get_memo_list_json(self):
        response = self.client.get('/note/get_all/')
        self.assertNotContains(response, self.memo.title)
        self.client.post(
            '/auth/',
            {'operation': 'login',
             'username': 'Gordon',
             'password': 'qwerty'}
        )

        self.assertNotContains(response, self.alien_memo.title)

    def test_del_item(self):
        c = Client()
        response = c.post(
            '/note/api/',
            {'operation': 'remove', 'id': self.memo.id}
        )
        self.assertContains(response, 'false')
        c.post(
            '/auth/',
            {'operation': 'login',
             'username': 'Gordon',
             'password': 'qwerty'}
        )
        response = c.post(
            '/note/api/',
            {'operation': 'remove', 'id': self.memo.id}
        )
        self.assertContains(response, 'true')
        self.assertEqual(Memo.objects.filter(id=self.memo.id).first(), None)
        response = c.post(
            '/note/api/',
            {'operation': 'remove', 'id': self.alien_memo.id}
        )
        self.assertContains(response, 'false')

    def test_memo_edit(self):
        c = Client()
        c.post(
            '/auth/',
            {'operation': 'login',
             'username': 'Gordon',
             'password': 'qwerty'}
        )

        response = c.post(
            '/note/api/',
            {'id': self.memo.id, 'title': 'EditedTODO'}
        )
        self.assertContains(response, 'true')

        self.assertEqual(Memo.objects.get(id=self.memo.id).title, 'EditedTODO')

    def test_memo_create(self):
        self.client.post(
            '/note/api/',
            {'title': 'NewMemo'}
        )
        m = Memo.objects.filter(title='NewMemo').first()


class CategoryTest(TestCase):
    def setUp(self):
        Category.objects.create(name='ToDo')
        Category.objects.create(name='bla bla bla')

    def test_get_all_category(self):
        response = self.client.get(
            '/note/category_all/'
        )
        self.assertContains(response, 'ToDo')
        self.assertContains(response, 'true')


class AuthApiTest(TestCase):
    def test_create_user(self):
        response = self.client.post(
            '/auth/',
            {'operation': 'register',
             'username': 'Gordon',
             'password': 'qwerty'}
        )
        self.assertContains(response, 'true')

    def test_login_not_created_user(self):
        response = self.client.post(
            '/auth/',
            {'operation': 'login',
             'username': 'Gordon',
             'password': 'qwerty'}
        )
        self.assertContains(response, 'false')
