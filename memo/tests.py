import json
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Memo, Category


class MemoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Gordon', 'gordon_freeman@city17.com')
        self.memo = Memo.objects.create(title="FirstTODO", owner=self.user)

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
        self.assertContains(response, self.memo.title)

    def test_del_item(self):
        response = self.client.post(
            '/note/api/',
            {'operation': 'remove', 'item_id': self.memo.id}
        )
        self.assertNotContains(response, self.memo.title)

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
