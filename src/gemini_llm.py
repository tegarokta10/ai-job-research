"""Google Gemini implementation of the job analyzer abstraction."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

from mock_llm import extract_job_title
from schemas import AnalysisResult, create_analysis_result

ROOT = Path(__file__).resolve().parents[1]


class GeminiFields(BaseModel):
    job_title: str
    required_skills: list[str]
    matching_skills: list[str]


class GeminiAnalyzer:
    def __init__(self, client=None, model: str | None = None):
        load_dotenv(ROOT / ".env")
        api_key = os.getenv("GEMINI_API_KEY")
        if client is None and not api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan. Isi file .env terlebih dahulu.")
        self.client = client or genai.Client(api_key=api_key)
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    def analyze(self, job_description: str, candidate_profile: str) -> AnalysisResult:
        response = self.client.models.generate_content(
            model=self.model,
            contents=(
                "Analisis kecocokan lowongan dengan profil kandidat. Ekstrak job_title hanya "
                "jika jelas disebutkan; jika tidak, tulis 'Tidak disebutkan'. Ekstrak semua skill "
                "yang diminta. Masukkan ke matching_skills hanya skill lowongan yang didukung "
                "profil kandidat. Jawab dalam bahasa Indonesia.\n\n"
                f"DESKRIPSI PEKERJAAN:\n{job_description}\n\n"
                f"PROFIL KANDIDAT:\n{candidate_profile}"
            ),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=GeminiFields,
            ),
        )

        parsed = getattr(response, "parsed", None)
        if parsed is None:
            response_text = getattr(response, "text", None)
            if not response_text:
                raise RuntimeError("Gemini tidak mengembalikan hasil analisis terstruktur.")
            parsed = json.loads(response_text)
        extracted = GeminiFields.model_validate(parsed)

        title = extracted.job_title.strip()
        if not title or title.lower() == "tidak disebutkan":
            title = extract_job_title(job_description)
        return create_analysis_result(title, extracted.required_skills, extracted.matching_skills)
