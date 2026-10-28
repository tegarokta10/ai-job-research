# Rencana dan Hasil Pengujian

## Tujuan

Memastikan API memvalidasi input, memanggil analyzer yang diinjeksi, mengembalikan schema yang benar, melayani UI, serta mengubah error provider menjadi respons HTTP aman.

## Lingkungan

- OS: Windows
- Python: 3.14.4 pada virtualenv workspace induk
- Framework tes: `unittest`; `pytest` juga tersedia
- API test memakai `TestClient` dan fake analyzer; tidak memakai key atau mengirim request Gemini live

## Kasus Otomatis

| Kasus | Hasil yang diharapkan |
|---|---|
| `GET /api/health` | HTTP 200 dan `{"status":"ok"}` |
| Job Description kosong | HTTP 422, error menyebut field tanpa mengulang teks input |
| Candidate Profile kosong | HTTP 422 |
| Body JSON malformed | HTTP 422 terkontrol |
| Request valid dengan fake analyzer | HTTP 200 dan response valid sebagai `AnalysisResult` |
| Gemini 503 | HTTP 503 generik tanpa detail upstream |
| Provider timeout | HTTP 504 generik |
| Provider gagal koneksi | HTTP 502 generik |
| Frontend dan JavaScript | Halaman dan aset dapat diakses |
| Pipeline/adapter lama | Mock, Gemini, OpenAI, dan validasi pipeline tetap berjalan dengan fake/mock |

## Hasil Eksekusi

Pada 29 Oktober 2026:

```text
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
Ran 13 tests — OK

..\.venv\Scripts\python.exe -m pytest -v
13 passed, 2 warnings
```

Peringatan pytest terdiri dari deprecation warning pada Google Gen AI SDK dan cache warning karena lingkungan tidak mengizinkan pembuatan direktori `.pytest_cache`; semua tes tetap lulus.

## Verifikasi yang Belum Dilakukan

- Belum ada browser manual test lintas browser/resolusi.
- Tes API menggunakan fake analyzer; belum ada tes end-to-end web yang mengirim input browser ke Gemini live.
- Deployment Vercel belum dilakukan.
