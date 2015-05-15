from django.test import TestCase
from django.contrib.auth.models import User
from .models import Memo, Category


class MemoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Gordon', 'gordon_freeman@city17.com')
        self.memo = Memo.objects.create(title="Title", owner=self.user)

    def test_memo_creating(self):
        self.assertEqual(self.memo.title, "Title")
        self.assertEqual(self.memo.owner.username, "Gordon")

    def test_memo_static_html_page(self):
        response = self.client.get('/note/%s' % self.memo.id)
        self.assertContains(response, "Title")

    def test_add_memo_with_new_category(self):
        category = Category.objects.create(name='ToDo')
        todo = Memo.objects.create(
            title="Kill headcrab",
            category=category,
            owner=self.user,
        )
        self.assertEqual(todo.category, category)