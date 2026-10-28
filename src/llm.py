"""Provider abstraction and configuration for job description analysis."""

import os
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv

from schemas import AnalysisResult

ROOT = Path(__file__).resolve().parents[1]


class JobAnalyzer(Protocol):
    def analyze(self, job_description: str, candidate_profile: str) -> AnalysisResult:
        """Compare a job description with a candidate profile."""


def get_analyzer() -> JobAnalyzer:
    """Select a provider using LLM_PROVIDER; mock remains safe by default."""
    load_dotenv(ROOT / ".env")
    provider = os.getenv("LLM_PROVIDER", "mock").strip().lower()
    if provider == "mock":
        from mock_llm import MockAnalyzer

        return MockAnalyzer()
    if provider == "openai":
        from openai_llm import OpenAIAnalyzer

        return OpenAIAnalyzer()
    if provider == "gemini":
        from gemini_llm import GeminiAnalyzer

        return GeminiAnalyzer()
    raise ValueError("LLM_PROVIDER harus bernilai 'mock', 'openai', atau 'gemini'")
