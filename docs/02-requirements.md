# Kebutuhan Sistem

## Kebutuhan Fungsional

| ID | Kebutuhan | Status |
|---|---|---|
| FR-01 | Menerima Job Description dan Candidate Profile dari browser | Selesai; `POST /api/analyze` memakai request model Pydantic |
| FR-02 | Memvalidasi teks masukan | Selesai; non-kosong, maksimum 100.000 karakter per field, field tambahan ditolak |
| FR-03 | Menganalisis judul dan skill melalui analyzer | Selesai; mock, Gemini, dan OpenAI menggunakan abstraction yang sama |
| FR-04 | Menghitung skill cocok/kurang, skor, rekomendasi | Selesai; menggunakan `AnalysisResult` dan kalkulasi lokal |
| FR-05 | Mengembalikan hasil terstruktur | Selesai; FastAPI `response_model=AnalysisResult` |
| FR-06 | Menyediakan status layanan | Selesai; `GET /api/health` mengembalikan `{"status":"ok"}` |
| FR-07 | Menampilkan loading, hasil, dan error pada UI | Selesai; vanilla JavaScript mengirim `fetch` ke backend |
| FR-08 | Mempertahankan CLI | Selesai; `src/main.py` tetap bisa dijalankan |

## Kebutuhan Nonfungsional

| ID | Kebutuhan | Status |
|---|---|---|
| NFR-01 | Menggunakan Python, FastAPI, Pydantic, HTML, CSS, dan vanilla JavaScript | Selesai |
| NFR-02 | Error API aman dan terkontrol | Selesai untuk validasi, timeout, koneksi, Gemini 429/503, dan error internal; tidak mengirim traceback atau input kembali ke browser |
| NFR-03 | API key tidak ada di browser atau Git | Selesai secara konfigurasi; key dibaca backend dari environment dan `.env` di-ignore |
| NFR-04 | Mendukung lokal dan Vercel | Selesai pada level source/config dasar; deployment belum dilakukan |
| NFR-05 | Tidak memakai database atau autentikasi untuk V1 | Sesuai ruang lingkup |
| NFR-06 | Tes berjalan tanpa API key | Selesai; memakai fake analyzer |

## Batasan

- Maksimum 100.000 karakter untuk masing-masing teks.
- Provider live membutuhkan internet, key, model yang tersedia, dan kuota.
- Belum ada rate limiting aplikasi, autentikasi, penyimpanan, atau pemantauan produksi.
