"""OpenAI Responses API implementation of the analyzer abstraction."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

from mock_llm import extract_job_title
from schemas import AnalysisResult, create_analysis_result

ROOT = Path(__file__).resolve().parents[1]


class LLMFields(BaseModel):
    """Fields extracted by the model; score is calculated locally."""

    job_title: str
    required_skills: list[str]
    matching_skills: list[str]


class OpenAIAnalyzer:
    def __init__(self, client: OpenAI | None = None, model: str | None = None):
        load_dotenv(ROOT / ".env")
        api_key = os.getenv("OPENAI_API_KEY")
        if client is None and not api_key:
            raise ValueError("OPENAI_API_KEY tidak ditemukan. Isi file .env terlebih dahulu.")
        self.client = client or OpenAI(api_key=api_key)
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-6-luna")

    def analyze(self, job_description: str, candidate_profile: str) -> AnalysisResult:
        response = self.client.responses.parse(
            model=self.model,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Analisis kecocokan lowongan dan kandidat dalam bahasa Indonesia. "
                        "Ekstrak judul hanya jika disebutkan jelas; jika tidak, gunakan 'Tidak disebutkan'. "
                        "Daftarkan skill teknis maupun nonteknis yang benar-benar diminta. "
                        "Tandai skill cocok hanya jika didukung profil kandidat. "
                        "Kembalikan hanya field sesuai schema."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"DESKRIPSI PEKERJAAN:\n{job_description}\n\n"
                        f"PROFIL KANDIDAT:\n{candidate_profile}"
                    ),
                },
            ],
            text_format=LLMFields,
        )
        extracted = response.output_parsed
        if extracted is None:
            raise RuntimeError("Model tidak mengembalikan hasil analisis terstruktur.")

        title = extracted.job_title.strip()
        if not title or title.lower() == "tidak disebutkan":
            title = extract_job_title(job_description)
        return create_analysis_result(title, extracted.required_skills, extracted.matching_skills)
