from django.test import TestCase


class Test(TestCase):
    def test_no_permission(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
