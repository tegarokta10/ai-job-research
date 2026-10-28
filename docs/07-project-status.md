# Status Proyek

**Tanggal pembaruan:** 29 Oktober 2026

**Versi saat ini:** Web V1 — siap diuji lokal dan dipersiapkan untuk deployment

**Commit terakhir saat inspeksi:** `d1c31ca` — `Update docs gemini learn`

## Selesai

- [x] Analyzer abstraction mock/Gemini/OpenAI dipertahankan.
- [x] `analyze_text()` dipakai bersama oleh CLI dan HTTP.
- [x] FastAPI `src/app.py` dengan Pydantic request/response.
- [x] `GET /api/health` dan `POST /api/analyze`.
- [x] Frontend HTML/CSS/vanilla JS dengan loading, disable button, hasil, dan error.
- [x] Error validasi, malformed request, timeout, koneksi, Gemini 429/503, dan error internal dikendalikan.
- [x] API tests memakai fake analyzer; tidak memerlukan key dan tidak memanggil Gemini.
- [x] Python 3.14 dipin untuk Vercel; FastAPI app diekspor dari `src/app.py`.
- [x] 13 tes lulus dengan unittest dan pytest.

## Arsitektur

```text
Browser → FastAPI → analyze_text → LLM Provider → Gemini/OpenAI/Mock
       ← JSON result ← AnalysisResult dan scoring lokal ←
```

Frontend dan API menggunakan origin yang sama. Tidak ada database atau penyimpanan hasil per pengguna.

## API Endpoints

- `GET /api/health` — health check.
- `POST /api/analyze` — menerima `job_description` dan `candidate_profile`; response mengikuti `AnalysisResult`.
- `GET /` — halaman frontend.

## Status Frontend

Fungsionalitas dasar selesai. Halaman dan JavaScript dites melalui FastAPI `TestClient`; browser manual test lintas perangkat belum dilakukan.

## Hasil Tes

- `..\.venv\Scripts\python.exe -m unittest discover -s tests -v`: 13 tes lulus.
- `..\.venv\Scripts\python.exe -m pytest -v`: 13 passed, 2 warnings (Google Gen AI deprecation dan cache permission).
- Tidak ada tes yang mengirim request ke Gemini.

## In Progress

- Uji end-to-end Web V1 lokal dengan Gemini yang dikonfigurasi.
- Verifikasi deployment preview setelah repository dihubungkan ke Vercel dan environment variables ditambahkan.

## Belum Dimulai

- Deploy Vercel; tidak dilakukan oleh Codex.
- Autentikasi, rate limiting, database, dan riwayat analisis.
- Browser QA dan evaluasi kualitas pada beragam lowongan nyata.

## Known Issues dan Blocker

- Panggilan Gemini live pernah mengembalikan `503 UNAVAILABLE` saat model ramai; riwayat proyek juga menyatakan Gemini pernah berhasil dipakai dari Python lokal. Web API live belum diuji.
- Kedua teks dikirim ke provider AI yang dipilih; jangan masukkan data kandidat yang tidak berwenang diproses.
- Belum ada autentikasi atau rate limiting; batasi akses sebelum aplikasi dibuka ke publik.
- Tidak ada blocker kode yang diketahui untuk menjalankan lokal. Deployment belum terverifikasi.

## Langkah Berikutnya — Satu Milestone

Jalankan Web V1 lokal (`uvicorn src.app:app --reload`), kirim Job Description dan Candidate Profile melalui browser dengan Gemini aktif, lalu catat hasil sebelum menghubungkan repository ke Vercel.
