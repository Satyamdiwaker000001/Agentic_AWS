import unittest

from fastapi.testclient import TestClient

from app.main import app


class OrganizerApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_malformed_json_body_returns_http_200(self):
        response = self.client.post('/organize', json='not-an-object')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def test_missing_folder_returns_http_200(self):
        response = self.client.post('/organize', json={'path': '/definitely/not/here'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')

    def test_invalid_payload_returns_http_200(self):
        response = self.client.post('/organize', json={'wrong': 'field'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'error')


if __name__ == '__main__':
    unittest.main()
