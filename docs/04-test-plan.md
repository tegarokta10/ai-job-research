# Test Plan

## 1. Objective

Pengujian memastikan pipeline AI Job Research dapat:

- membaca deskripsi pekerjaan dan profil kandidat;
- menolak masukan yang kosong atau bukan teks;
- menemukan keterampilan yang didukung analyzer lokal dan membandingkannya;
- menghasilkan skor dan rekomendasi yang konsisten;
- mengembalikan hasil dengan struktur yang ditentukan;
- menyimpan hasil pada `output/result.json`.

## 2. Test Environment

- OS: Windows
- Python: 3.10 atau lebih baru
- Framework: `unittest` dari standard library
- Analyzer offline: pencocokan kata kunci lokal (`src/mock_llm.py`)
- Provider OpenAI dan Gemini: uji unit memakai client tiruan; tidak mengirim permintaan jaringan

Jalankan perintah dari direktori utama proyek.

## 3. Test Cases

| ID | Test case | Hasil yang diharapkan |
|---|---|---|
| TC-01 | Masukan valid dengan skill yang cocok dan tidak cocok | Skill terbagi ke daftar cocok dan kurang; skor dihitung dari skill yang ditemukan |
| TC-02 | Deskripsi pekerjaan kosong | Validasi melempar `ValueError` |
| TC-03 | Profil kandidat kosong | Validasi melempar `ValueError` |
| TC-04 | Menjalankan pipeline dengan file masukan | Hasil berupa objek JSON dengan field sesuai skema |
| TC-05 | Menjalankan pipeline | Hasil disimpan sebagai JSON valid di `output/result.json` |
| TC-06 | Judul ditulis dengan label seperti `Posisi:` | Judul diekstrak dari baris pertama |
| TC-07 | Provider OpenAI diberi client tiruan | Hasil terstruktur dinormalisasi dan skor dihitung oleh aplikasi |
| TC-08 | Provider Gemini diberi client tiruan | Hasil terstruktur dinormalisasi dan skor dihitung oleh aplikasi |

## 4. Test Execution

Jalankan tes otomatis:

```bash
python -m unittest discover -s tests -v
```

Uji alur aplikasi secara manual dengan contoh berkas:

```bash
python src/main.py
```

Periksa `output/result.json` untuk memastikan output dapat dibaca sebagai JSON dan berisi `job_title`, `required_skills`, `matching_skills`, `missing_skills`, `match_score`, serta `recommendation`. Tes otomatis tidak memanggil layanan AI; uji langsung memerlukan API key dan dapat memakai kuota akun.

## 5. Test Results

Eksekusi terakhir: 28 Oktober 2026.

```text
Command: ..\.venv\Scripts\python.exe -m unittest discover -s tests -v
Result: 4 tests passed, 0 failed.
Coverage: validasi input kosong, pipeline dan ekstraksi job_title, serta OpenAIAnalyzer dan GeminiAnalyzer dengan client tiruan (tanpa request jaringan).
```

Tes live Gemini dicoba dua kali setelah tes offline, tetapi API mengembalikan `503 UNAVAILABLE` karena model mengalami permintaan tinggi. Tidak ada hasil live baru yang ditulis ke `output/result.json`.
