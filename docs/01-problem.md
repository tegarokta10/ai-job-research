# Pernyataan Masalah

## Latar Belakang

Pencari kerja perlu membaca deskripsi lowongan dan membandingkan persyaratannya dengan keterampilan serta pengalaman mereka. Proses manual ini berulang, memakan waktu, dan menyulitkan kandidat menilai kesesuaian secara konsisten.

## Tujuan

Membangun AI Job Research Assistant yang menerima deskripsi pekerjaan dan profil kandidat, menganalisis kecocokan melalui LLM, lalu menampilkan ringkasan hasil melalui browser.

## Ruang Lingkup Web V1

- Pengguna menempelkan Job Description dan Candidate Profile melalui halaman web.
- Frontend mengirim request JSON ke backend Python FastAPI.
- Backend memvalidasi input dan memakai LLM provider yang sudah ada.
- Provider dipilih melalui `LLM_PROVIDER`: `mock`, `gemini`, atau `openai`.
- Hasil ditampilkan sebagai judul, skill, skor, dan rekomendasi.

Versi ini tidak mencari lowongan otomatis, tidak memiliki autentikasi, database, atau riwayat analisis. CLI lama tetap tersedia.

## Hasil yang Diharapkan

Response analisis berupa JSON dengan `job_title`, `required_skills`, `matching_skills`, `missing_skills`, `match_score`, dan `recommendation`. Skor dihitung aplikasi berdasarkan proporsi skill wajib yang cocok. Hasil adalah alat bantu, bukan keputusan perekrutan.
