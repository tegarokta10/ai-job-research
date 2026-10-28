# AI Job Research

Web V1 untuk menganalisis kecocokan deskripsi pekerjaan dan profil kandidat. Backend Python mempertahankan provider abstraction yang sudah ada (`mock`, `gemini`, `openai`); frontend memakai HTML, CSS, dan JavaScript vanilla.

## Jalankan Lokal

> Jalankan perintah dari folder `ai-job-research`.

```powershell
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe -m uvicorn src.app:app --reload
```

Buka <http://127.0.0.1:8000>. Dokumentasi interaktif API tersedia di <http://127.0.0.1:8000/docs>.

Frontend mengirim teks ke server untuk dianalisis. Gemini key tetap berada di backend, tidak di JavaScript. Pastikan `.env` lokal berisi `LLM_PROVIDER=gemini`, `GEMINI_API_KEY`, dan `GEMINI_MODEL`. Jangan timpa `.env` yang sudah berisi key dengan contoh kosong.

Untuk menjalankan CLI lama: `..\.venv\Scripts\python.exe src\main.py`.

## API

### `GET /api/health`

```json
{"status":"ok"}
```

### `POST /api/analyze`

Request:

```json
{
  "job_description": "Mencari Junior Data Analyst dengan Python dan SQL",
  "candidate_profile": "Berpengalaman dengan Python"
}
```

Response mengikuti schema `AnalysisResult`:

```json
{
  "job_title": "Junior Data Analyst",
  "required_skills": ["python", "sql"],
  "matching_skills": ["python"],
  "missing_skills": ["sql"],
  "match_score": 50,
  "recommendation": "Pertimbangkan"
}
```

Setiap input wajib berupa teks non-kosong dan maksimum 100.000 karakter. API memakai `422` untuk request tidak valid, `429` untuk rate limit provider, `502` untuk kegagalan koneksi/provider, `503` saat provider belum siap/tersedia, dan `504` untuk timeout. Error response tidak memuat traceback atau isi input.

## Tes

```powershell
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
..\.venv\Scripts\python.exe -m pytest -v
```

Tes menggunakan fake analyzer; tes tidak memerlukan API key dan tidak memanggil Gemini.

## Environment Variables

- `LLM_PROVIDER`: `gemini`, `openai`, atau `mock`.
- `GEMINI_API_KEY` dan `GEMINI_MODEL` untuk Gemini.
- `OPENAI_API_KEY` dan `OPENAI_MODEL` untuk OpenAI.

`.env` dikecualikan oleh `.gitignore`; jangan commit key.

## Vercel

`.python-version` mematok Python 3.14. FastAPI diekspor sebagai `app` dari `src/app.py`, entrypoint yang dikenali Vercel. `StaticFiles` melayani aset dalam `frontend/`. Vercel dapat mendeteksi FastAPI tanpa `vercel.json`; environment variables deployment tetap perlu diatur di project Vercel.

Referensi: [FastAPI di Vercel](https://vercel.com/docs/frameworks/backend/fastapi), [Python runtime Vercel](https://vercel.com/docs/functions/runtimes/python).

## Batasan V1

Belum ada autentikasi, database, penyimpanan riwayat, atau pencarian lowongan. Satu request mengirim Job Description dan Candidate Profile ke provider AI yang dipilih.
