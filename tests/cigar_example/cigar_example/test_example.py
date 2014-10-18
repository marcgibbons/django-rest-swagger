from django.test import TestCase
from io import BytesIO
from rest_framework.parsers import JSONParser


def parseJSON(response):
    stream = BytesIO(response.content)
    json = JSONParser().parse(stream)
    return json


class Test(TestCase):
    def test_no_permission(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_fbv_serializer(self):
        response = self.client.get('/api-docs/api/jambalaya')
        self.assertEqual(response.status_code, 200)
        json = parseJSON(response)
        self.assertTrue('JambalayaSerializer' in json['models'])
