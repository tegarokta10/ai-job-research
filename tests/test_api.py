import sys
import unittest
from pathlib import Path

import httpx
from fastapi.testclient import TestClient
from google.genai.errors import ServerError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.app import create_app
from schemas import AnalysisResult, create_analysis_result


class FakeAnalyzer:
    def analyze(self, job_description: str, candidate_profile: str):
        return create_analysis_result(
            "Junior Data Analyst",
            ["Python", "SQL", "Data Analysis"],
            ["Python", "SQL"],
        )


class FailedGeminiAnalyzer:
    def analyze(self, job_description: str, candidate_profile: str):
        raise ServerError(503, {"message": "private provider details"})


class TimedOutAnalyzer:
    def analyze(self, job_description: str, candidate_profile: str):
        raise httpx.ReadTimeout("private timeout details")


class DisconnectedAnalyzer:
    def analyze(self, job_description: str, candidate_profile: str):
        raise httpx.ConnectError("private connection details")


class AnalyzeAPITests(unittest.TestCase):
    def test_frontend_and_static_assets_are_served(self):
        client = TestClient(create_app(FakeAnalyzer()))
        page = client.get("/")
        script = client.get("/static/app.js")
        self.assertEqual(page.status_code, 200)
        self.assertIn("AI Job Research", page.text)
        self.assertEqual(script.status_code, 200)
        self.assertIn("fetch('/api/analyze'", script.text)

    def test_health_returns_ok_without_initializing_provider(self):
        response = TestClient(create_app()).get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_empty_job_description_returns_safe_validation_error(self):
        response = TestClient(create_app(FakeAnalyzer())).post(
            "/api/analyze",
            json={"job_description": "  ", "candidate_profile": "Python"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("tidak boleh kosong", response.text)
        self.assertNotIn('"input"', response.text)

    def test_empty_candidate_profile_returns_validation_error(self):
        response = TestClient(create_app(FakeAnalyzer())).post(
            "/api/analyze",
            json={"job_description": "Mencari Python", "candidate_profile": ""},
        )
        self.assertEqual(response.status_code, 422)
        self.assertIn("candidate_profile", response.text)

    def test_malformed_json_returns_controlled_error(self):
        response = TestClient(create_app(FakeAnalyzer())).post(
            "/api/analyze",
            content="{invalid json",
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "Request tidak valid.")

    def test_valid_request_uses_fake_analyzer_and_matches_schema(self):
        response = TestClient(create_app(FakeAnalyzer())).post(
            "/api/analyze",
            json={
                "job_description": "Junior Data Analyst membutuhkan Python dan SQL",
                "candidate_profile": "Berpengalaman menggunakan Python dan SQL",
            },
        )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(
            set(body),
            {
                "job_title",
                "required_skills",
                "matching_skills",
                "missing_skills",
                "match_score",
                "recommendation",
            },
        )
        AnalysisResult.model_validate(body)
        self.assertEqual(body["job_title"], "Junior Data Analyst")
        self.assertEqual(body["match_score"], 67)
        self.assertEqual(body["recommendation"], "Pertimbangkan")

    def test_gemini_503_becomes_safe_service_error(self):
        response = TestClient(create_app(FailedGeminiAnalyzer())).post(
            "/api/analyze",
            json={"job_description": "Lowongan Python", "candidate_profile": "Skill Python"},
        )
        self.assertEqual(response.status_code, 503)
        self.assertIn("Coba lagi nanti", response.json()["detail"])
        self.assertNotIn("private provider details", response.text)

    def test_provider_timeout_becomes_gateway_timeout(self):
        response = TestClient(create_app(TimedOutAnalyzer())).post(
            "/api/analyze",
            json={"job_description": "Lowongan Python", "candidate_profile": "Skill Python"},
        )
        self.assertEqual(response.status_code, 504)
        self.assertNotIn("private timeout details", response.text)

    def test_provider_connection_error_becomes_bad_gateway(self):
        response = TestClient(create_app(DisconnectedAnalyzer())).post(
            "/api/analyze",
            json={"job_description": "Lowongan Python", "candidate_profile": "Skill Python"},
        )
        self.assertEqual(response.status_code, 502)
        self.assertNotIn("private connection details", response.text)


if __name__ == "__main__":
    unittest.main()
