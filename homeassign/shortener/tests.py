from django.test import TestCase
from .models import UrlRedirect
import requests
import json

class UrlRedirectTest(TestCase):
    # test a url creation
    def test_gen_url(self):
        res = requests.post('http://localhost:8000/create/', data=json.dumps({"url":"https://www.ynet.co.il/"}))
        res = requests.get('http://localhost:8000/s/%s', res.content.decode("utf-8") )
        TestCase.assertEqual(self, res.status_code, 200)

    # test GET instead of POST
    def test_wrong_method(self):
        res = requests.get('http://localhost:8000/create/')
        TestCase.assertEqual(self, res.status_code, 405)

    # test empty request body
    def test_empty_body(self):
        res = requests.post('http://localhost:8000/create/', data=json.dumps({}))
        TestCase.assertEqual(self, res.status_code, 400)

    # test wrong body value
    def test_wrong_body(self):
        res = requests.post('http://localhost:8000/create/', data=json.dumps({'lo':'l'}))
        TestCase.assertEqual(self, res.status_code, 400)
