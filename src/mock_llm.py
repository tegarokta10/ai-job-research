"""Deterministic local analyzer used until a real LLM is connected."""

from schemas import AnalysisResult

SKILL_TERMS = (
    "python", "sql", "machine learning", "data analysis", "communication",
    "project management", "javascript", "java", "aws", "docker",
)


def analyze(job_description: str, candidate_profile: str) -> AnalysisResult:
    job_lower = job_description.lower()
    profile_lower = candidate_profile.lower()
    required = [skill for skill in SKILL_TERMS if skill in job_lower]
    matching = [skill for skill in required if skill in profile_lower]
    missing = [skill for skill in required if skill not in profile_lower]
    score = round(100 * len(matching) / len(required)) if required else 0
    recommendation = "Cocok" if score >= 70 else "Pertimbangkan" if score >= 40 else "Kurang cocok"
    return AnalysisResult(
        job_title="Tidak disebutkan", required_skills=required,
        matching_skills=matching, missing_skills=missing,
        match_score=score, recommendation=recommendation,
    )
