from unittest import TestCase

from app import app

class AppTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get("/")
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Hello, pomidorka!', rv.data)
        self.assertEqual("text/html", rv.mimetype)
        pass

    def test_form(self):
        rv = self.app.post('/form/', data={'first_name': "Jesse", 'last_name': "Pinkman"})
        self.assertEqual(b'{"first_name":"Jesse","last_name":"Pinkman"}\n', rv.data)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
