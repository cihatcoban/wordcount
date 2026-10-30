"""Integration tests for FastAPI REST API and Web Routes."""

import unittest
from starlette.testclient import TestClient
from wordcount.presentation.web.app import create_app
from wordcount.infrastructure.config import Settings, get_settings


class TestWebAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        test_settings = Settings(
            app_name="WordCount Test",
            max_text_length=5000,
            debug=True
        )
        cls.app = create_app(test_settings)
        cls.app.dependency_overrides[get_settings] = lambda: test_settings
        cls.client = TestClient(cls.app)

    @classmethod
    def tearDownClass(cls):
        cls.app.dependency_overrides.clear()

    def test_health_check_endpoint(self):
        response = self.client.get("/api/v1/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "WordCount Test")

    def test_web_index_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("WordCount Test", response.text)

    def test_analyze_endpoint_valid_payload(self):
        payload = {
            "text": "Senior level software engineering requires robust test coverage and architectural boundaries.",
            "top_n_keywords": 3,
            "filter_stopwords": False
        }
        response = self.client.post("/api/v1/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("words_total", data)
        self.assertGreater(data["words_total"], 5)
        self.assertIn("readability", data)
        self.assertIn("reading_time", data)

    def test_analyze_endpoint_empty_text(self):
        payload = {
            "text": "",
            "top_n_keywords": 5
        }
        response = self.client.post("/api/v1/analyze", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["words_total"], 0)

    def test_analyze_endpoint_payload_exceeds_limit(self):
        payload = {
            "text": "x" * 6000,
            "top_n_keywords": 5
        }
        response = self.client.post("/api/v1/analyze", json=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
