"""Validated result model and deterministic result calculations."""

from typing import Literal

from pydantic import BaseModel, Field


class AnalysisResult(BaseModel):
    job_title: str
    required_skills: list[str]
    matching_skills: list[str]
    missing_skills: list[str]
    match_score: int = Field(ge=0, le=100)
    recommendation: Literal["Cocok", "Pertimbangkan", "Kurang cocok"]


def create_analysis_result(
    job_title: str,
    required_skills: list[str],
    matching_skills: list[str],
) -> AnalysisResult:
    """Normalize skills and calculate score/recommendation in application code."""
    required = list(dict.fromkeys(skill.strip().lower() for skill in required_skills if skill.strip()))
    requested_matches = {skill.strip().lower() for skill in matching_skills if skill.strip()}
    matching = [skill for skill in required if skill in requested_matches]
    missing = [skill for skill in required if skill not in requested_matches]
    score = round(100 * len(matching) / len(required)) if required else 0
    recommendation = "Cocok" if score >= 70 else "Pertimbangkan" if score >= 40 else "Kurang cocok"
    return AnalysisResult(
        job_title=job_title.strip() or "Tidak disebutkan",
        required_skills=required,
        matching_skills=matching,
        missing_skills=missing,
        match_score=score,
        recommendation=recommendation,
    )
