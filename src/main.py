"""Run a local job description and candidate profile analysis."""

import json
from pathlib import Path

from llm import JobAnalyzer, get_analyzer
from schemas import AnalysisResult
from validator import validate_text

ROOT = Path(__file__).resolve().parents[1]


def analyze_text(
    job_description: str,
    candidate_profile: str,
    analyzer: JobAnalyzer | None = None,
) -> AnalysisResult:
    """Validate and analyze raw text without reading or writing files."""
    job = validate_text(job_description, "Deskripsi pekerjaan")
    profile = validate_text(candidate_profile, "Profil kandidat")
    return (analyzer or get_analyzer()).analyze(job, profile)


def run_analysis(
    job_path: Path | None = None,
    profile_path: Path | None = None,
    output_path: Path | None = None,
    analyzer: JobAnalyzer | None = None,
) -> dict:
    job_file = job_path or ROOT / "data" / "job_description.txt"
    profile_file = profile_path or ROOT / "data" / "candidate_profile.txt"
    result = analyze_text(
        job_file.read_text(encoding="utf-8"),
        profile_file.read_text(encoding="utf-8"),
        analyzer=analyzer,
    ).model_dump()
    output_file = output_path or ROOT / "output" / "result.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run_analysis(), ensure_ascii=False, indent=2))
