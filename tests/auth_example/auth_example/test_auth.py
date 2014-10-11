from django.contrib.auth.models import User
from django.test import TestCase


class AuthTest(TestCase):
    def test_no_permission(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "you have no permissions!")

    def test_with_permission(self):
        user = User(username='abc')
        user.set_password('abc')
        user.save()
        self.assertTrue(self.client.login(username='abc', password='abc'))
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Swagger UI" in response.content.decode())
