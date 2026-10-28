# Kebutuhan Sistem

## Kebutuhan Fungsional

| ID | Kebutuhan | Status dan implementasi |
|---|---|---|
| FR-01 | Menerima deskripsi pekerjaan dan profil kandidat | Selesai; dibaca dari dua berkas teks di `data/` |
| FR-02 | Mengidentifikasi judul lowongan dan skill wajib | Selesai pada analyzer; mock memakai daftar kata kunci, provider AI mengekstrak dari teks |
| FR-03 | Membandingkan skill lowongan dengan profil kandidat | Selesai; analyzer mengembalikan skill cocok, aplikasi menormalkan dan memisah skill yang belum cocok |
| FR-04 | Menghitung skor kecocokan | Selesai; dihitung lokal sebagai persentase skill wajib yang cocok, dibulatkan ke bilangan bulat |
| FR-05 | Memberikan rekomendasi | Selesai; `Cocok` untuk skor ≥70, `Pertimbangkan` untuk ≥40, selain itu `Kurang cocok` |
| FR-06 | Menyimpan hasil analisis | Selesai; JSON ditulis ke `output/result.json` |
| FR-07 | Memilih provider LLM | Selesai; `LLM_PROVIDER` mendukung `mock`, `openai`, dan `gemini` |

## Kebutuhan Nonfungsional

| ID | Kebutuhan | Status dan implementasi |
|---|---|---|
| NFR-01 | Menghasilkan JSON dengan struktur tetap | Selesai; `AnalysisResult` divalidasi dengan Pydantic |
| NFR-02 | Menangani masukan tidak valid | Sebagian; input kosong ditolak dengan `ValueError`; penanganan pesan error untuk seluruh kegagalan provider masih dapat ditingkatkan |
| NFR-03 | Melindungi kredensial | Selesai; API key berada di `.env`, dan `.env` dikecualikan oleh `.gitignore` |
| NFR-04 | Mendukung pengembangan tanpa koneksi API | Selesai; provider `mock` bekerja lokal |
| NFR-05 | Memisahkan implementasi provider | Selesai; antarmuka `JobAnalyzer` berada di `src/llm.py` |

## Batasan Saat Ini

- Aplikasi berjalan sebagai command line dan memakai berkas lokal; belum ada endpoint HTTP atau UI.
- Provider live membutuhkan internet, API key aktif, model yang tersedia, dan kuota akun.
- Kualitas ekstraksi dan bobot skill belum dievaluasi pada kumpulan lowongan yang beragam.
