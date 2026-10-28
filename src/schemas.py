"""Data structures returned by the job matching pipeline."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class AnalysisResult:
    job_title: str
    required_skills: list[str]
    matching_skills: list[str]
    missing_skills: list[str]
    match_score: int
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
