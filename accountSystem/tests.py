# Create your tests here.
from django.test import TestCase

from .models import Server


class ServerTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_list(self):
        serverObjs = Server.objects.all()
        for serverObj in serverObjs:
            print(serverObj.ip)
        resp = self.client.get('/all-keeper/server')
        self.assertEqual(resp.status_code, 200)
