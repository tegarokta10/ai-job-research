"""FastAPI web application and JSON API for AI Job Research."""

import logging
import sys
from functools import lru_cache
from pathlib import Path
from typing import Annotated

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from google.genai import errors as gemini_errors
from pydantic import BaseModel, ConfigDict, Field

# Keep the existing flat `src/*.py` imports working when Vercel imports `src.app`.
SOURCE_DIR = Path(__file__).resolve().parent
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from llm import JobAnalyzer, get_analyzer
from main import analyze_text
from schemas import AnalysisResult

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"


class AnalyzeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    job_description: Annotated[str, Field(min_length=1, max_length=100_000)]
    candidate_profile: Annotated[str, Field(min_length=1, max_length=100_000)]


@lru_cache(maxsize=1)
def _configured_analyzer() -> JobAnalyzer:
    return get_analyzer()


def create_app(analyzer: JobAnalyzer | None = None) -> FastAPI:
    application = FastAPI(title="AI Job Research API", version="1.0.0")
    application.state.analyzer = analyzer

    @application.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Never echo submitted text or Pydantic's raw `input` values.
        errors = []
        for error in exc.errors():
            location = error.get("loc", ())
            field = location[-1] if location else "request"
            error_type = error.get("type")
            if error_type == "missing":
                message = "Field wajib diisi."
            elif error_type == "string_too_long":
                message = "Teks melebihi batas 100.000 karakter."
            elif error_type == "string_too_short":
                message = "Teks tidak boleh kosong."
            else:
                message = "Format request tidak valid."
            errors.append({"field": str(field), "message": message})
        return JSONResponse(
            status_code=422,
            content={"detail": "Request tidak valid.", "errors": errors},
        )

    @application.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.post("/api/analyze", response_model=AnalysisResult)
    def analyze(payload: AnalyzeRequest, request: Request) -> AnalysisResult:
        try:
            selected_analyzer = request.app.state.analyzer or _configured_analyzer()
            return analyze_text(
                payload.job_description,
                payload.candidate_profile,
                analyzer=selected_analyzer,
            )
        except httpx.TimeoutException:
            logger.warning("AI provider request timed out")
            raise HTTPException(status_code=504, detail="Layanan AI terlalu lama merespons.")
        except httpx.RequestError:
            logger.warning("AI provider connection failed")
            raise HTTPException(
                status_code=502,
                detail="Tidak dapat menghubungi layanan AI.",
            )
        except gemini_errors.APIError as exc:
            status = getattr(exc, "code", None)
            logger.warning("Gemini upstream request failed; status=%s", status)
            if status == 429:
                raise HTTPException(
                    status_code=429,
                    detail="Layanan AI sedang membatasi permintaan. Coba lagi nanti.",
                )
            if status in {503, 504}:
                raise HTTPException(
                    status_code=503,
                    detail="Layanan AI sementara tidak tersedia. Coba lagi nanti.",
                )
            raise HTTPException(
                status_code=502,
                detail="Layanan AI gagal memproses permintaan.",
            )
        except ValueError:
            logger.warning("AI provider configuration or response is invalid")
            raise HTTPException(
                status_code=503,
                detail="Provider AI belum siap. Periksa konfigurasi server.",
            )
        except Exception as exc:
            # Keep provider exception contents, prompts, and credentials out of logs/responses.
            logger.error("Unexpected analysis failure; type=%s", type(exc).__name__)
            raise HTTPException(
                status_code=500,
                detail="Terjadi kesalahan server saat menganalisis.",
            )

    @application.get("/", include_in_schema=False)
    def frontend() -> FileResponse:
        return FileResponse(FRONTEND_DIR / "index.html")

    application.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="frontend-static")
    return application


app = create_app()
