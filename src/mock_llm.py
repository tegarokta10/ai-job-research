"""Deterministic local analyzer used until a real LLM is connected."""

import re

from schemas import AnalysisResult, create_analysis_result

SKILL_TERMS = (
    "python", "sql", "machine learning", "data analysis", "communication",
    "project management", "javascript", "java", "aws", "docker", "Unity Programmer"
)


def extract_job_title(job_description: str) -> str:
    """Extract a title from a labeled first line; avoid guessing if absent."""
    first_line = next((line.strip() for line in job_description.splitlines() if line.strip()), "")
    title_match = re.match(
        r"^(?:contoh\s+lowongan|job\s+title|judul\s+pekerjaan|posisi|lowongan)\s*:\s*(.+)$",
        first_line,
        flags=re.IGNORECASE,
    )
    if title_match:
        return title_match.group(1).strip().rstrip(".") or "Tidak disebutkan"

    if first_line.startswith("#"):
        heading = first_line.lstrip("# ").strip()
        if heading:
            return heading
    return "Tidak disebutkan"


class MockAnalyzer:
    """Offline implementation of the analyzer interface."""

    def analyze(self, job_description: str, candidate_profile: str) -> AnalysisResult:
        job_lower = job_description.lower()
        profile_lower = candidate_profile.lower()
        required = [skill for skill in SKILL_TERMS if skill in job_lower]
        matching = [skill for skill in required if skill in profile_lower]
        return create_analysis_result(extract_job_title(job_description), required, matching)


def analyze(job_description: str, candidate_profile: str) -> AnalysisResult:
    """Backward-compatible functional entry point for the mock analyzer."""
    return MockAnalyzer().analyze(job_description, candidate_profile)
