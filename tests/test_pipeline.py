import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import run_analysis
from gemini_llm import GeminiAnalyzer, GeminiFields
from mock_llm import MockAnalyzer
from openai_llm import LLMFields, OpenAIAnalyzer
from validator import validate_text


class PipelineTests(unittest.TestCase):
    def test_validation_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            validate_text("  ", "input")

    def test_pipeline_writes_structured_result(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            temp = Path(directory)
            job = temp / "job.txt"
            profile = temp / "profile.txt"
            output = temp / "result.json"
            job.write_text("Posisi: Data Analyst\nMembutuhkan Python dan SQL", encoding="utf-8")
            profile.write_text("Saya menggunakan Python", encoding="utf-8")
            result = run_analysis(job, profile, output, analyzer=MockAnalyzer())
            self.assertTrue(output.is_file())
        self.assertEqual(result["matching_skills"], ["python"])
        self.assertEqual(result["missing_skills"], ["sql"])
        self.assertEqual(result["job_title"], "Data Analyst")

    def test_openai_analyzer_uses_structured_result_without_network(self):
        class Responses:
            def parse(self, **kwargs):
                self.kwargs = kwargs
                return type(
                    "ParsedResponse",
                    (),
                    {"output_parsed": LLMFields(
                        job_title="Product Analyst",
                        required_skills=["SQL", "Communication"],
                        matching_skills=["sql"],
                    )},
                )()

        class FakeClient:
            responses = Responses()

        result = OpenAIAnalyzer(client=FakeClient()).analyze(
            "Posisi: Product Analyst", "Berpengalaman dengan SQL"
        )
        self.assertEqual(result.job_title, "Product Analyst")
        self.assertEqual(result.match_score, 50)
        self.assertEqual(result.missing_skills, ["communication"])

    def test_gemini_analyzer_uses_structured_result_without_network(self):
        class Models:
            def generate_content(self, **kwargs):
                self.kwargs = kwargs
                return type(
                    "ParsedResponse",
                    (),
                    {"parsed": GeminiFields(
                        job_title="Data Analyst",
                        required_skills=["Python", "SQL"],
                        matching_skills=["Python"],
                    )},
                )()

        class FakeClient:
            models = Models()

        result = GeminiAnalyzer(client=FakeClient(), model="test-model").analyze(
            "Posisi: Data Analyst", "Berpengalaman dengan Python"
        )
        self.assertEqual(result.job_title, "Data Analyst")
        self.assertEqual(result.required_skills, ["python", "sql"])
        self.assertEqual(result.match_score, 50)


if __name__ == "__main__":
    unittest.main()
