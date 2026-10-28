# Catatan Pembelajaran Proyek

Dokumen ini merangkum konsep yang sudah diterapkan pada Web V1 dan topik yang dapat dipelajari berikutnya.

## 1. HTTP dan REST API

HTTP membawa request dan response antara browser dan server. `GET /api/health` membaca status layanan; `POST /api/analyze` mengirim data untuk diproses. Status code seperti 200, 422, 502, 503, dan 504 memberi tahu hasil request secara konsisten.

## 2. JSON Request dan Response

Browser mengirim object JSON memakai `fetch()` dengan header `Content-Type: application/json`. FastAPI membaca body, memvalidasinya, lalu mengembalikan JSON untuk ditampilkan halaman.

## 3. FastAPI

FastAPI menghubungkan path dan method HTTP ke fungsi Python. `response_model` mendokumentasikan dan memvalidasi bentuk response. `src.app:app` menjadi entrypoint lokal dan Vercel.

## 4. Pydantic Validation

`AnalyzeRequest` memastikan field wajib berupa teks, tidak kosong, tidak melebihi 100.000 karakter, dan tidak menerima field tambahan. `AnalysisResult` menetapkan schema keluaran.

## 5. Pemisahan Frontend dan Backend

Frontend mengumpulkan input, mengirim request, dan menampilkan loading/error/result. Backend memvalidasi input serta memanggil analyzer. Provider LLM melakukan ekstraksi dan pencocokan.

## 6. Environment Variables dan API Security

Key provider tinggal di `.env` lokal atau setting environment server. `.env` di-ignore Git. Frontend tidak memuat key. Error HTTP tidak mengembalikan traceback, key, teks prompt, atau pesan sensitif SDK.

## 7. Dependency Management

`requirements.txt` mencatat dependency. FastAPI membuat API, Uvicorn menjalankan server lokal, dan HTTPX digunakan TestClient serta penanganan timeout/koneksi.

## 8. Serverless Deployment

Vercel mendeteksi FastAPI pada entrypoint yang dikenal dan menjalankan aplikasi sebagai function Python. Environment variable produksi diatur melalui dashboard Vercel. Cold start, durasi function, ukuran bundle, dan ketersediaan provider perlu diperhatikan.

## Hal untuk Diperdalam

- CORS dan kapan diperlukan; V1 menyajikan frontend dan API pada origin yang sama.
- Rate limiting, abuse protection, dan batas ukuran request.
- Observability tanpa mencatat isi profil atau job description.
- Perbedaan deployment preview dan production di Vercel.
- Pengujian timeout serta error provider pada staging.
