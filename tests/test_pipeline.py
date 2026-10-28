import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from main import run_analysis
from validator import validate_text


class PipelineTests(unittest.TestCase):
    def test_validation_rejects_empty_text(self):
        with self.assertRaises(ValueError):
            validate_text("  ", "input")

    def test_pipeline_writes_structured_result(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            job = temp / "job.txt"
            profile = temp / "profile.txt"
            job.write_text("Mencari Python dan SQL", encoding="utf-8")
            profile.write_text("Saya menggunakan Python", encoding="utf-8")
            result = run_analysis(job, profile)
        self.assertEqual(result["matching_skills"], ["python"])
        self.assertEqual(result["missing_skills"], ["sql"])


if __name__ == "__main__":
    unittest.main()
