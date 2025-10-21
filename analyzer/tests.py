from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
import json


class AnalyzerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.post_url = "/api/strings"
        self.list_url = "/api/strings/"
        self.nlp_url = "/api/strings/filter-by-natural-language"

    def test_post_and_get_string(self):
        body = {"value": "madam"}
        r = self.client.post(self.post_url, data=json.dumps(body), content_type='application/json')
        self.assertEqual(r.status_code, 201)
        data = r.json()
        self.assertEqual(data['value'], 'madam')
        self.assertTrue(data['properties']['is_palindrome'])

        gr = self.client.get(f"/api/strings/madam")
        self.assertEqual(gr.status_code, 200)
        self.assertEqual(gr.json()['value'], 'madam')

    def test_duplicate_post_returns_409(self):
        body = {"value": "hello"}
        r1 = self.client.post(self.post_url, data=json.dumps(body), content_type='application/json')
        self.assertEqual(r1.status_code, 201)
        r2 = self.client.post(self.post_url, data=json.dumps(body), content_type='application/json')
        self.assertEqual(r2.status_code, 409)

    def test_list_filters(self):
        self.client.post(self.post_url, data=json.dumps({"value": "madam"}), content_type='application/json')
        self.client.post(self.post_url, data=json.dumps({"value": "hello world"}), content_type='application/json')
        r = self.client.get(self.list_url + '?is_palindrome=true')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['count'], 1)

    def test_nlp_parser(self):
        self.client.post(self.post_url, data=json.dumps({"value": "madam"}), content_type='application/json')
        r = self.client.get(self.nlp_url + '?query=all%20single%20word%20palindromic%20strings')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['count'], 1)

    def test_delete(self):
        r = self.client.post(self.post_url, data=json.dumps({"value": "delete me"}), content_type='application/json')
        self.assertEqual(r.status_code, 201)

        dr = self.client.delete(f"/api/strings/delete me/delete")
        self.assertEqual(dr.status_code, 204)

        gr = self.client.get(f"/api/strings/delete me")
        self.assertEqual(gr.status_code, 404)
