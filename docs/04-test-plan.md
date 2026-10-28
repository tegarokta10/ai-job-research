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
- Analyzer: pencocokan kata kunci lokal (`src/mock_llm.py`)

Jalankan perintah dari direktori utama proyek.

## 3. Test Cases

| ID | Test case | Hasil yang diharapkan |
|---|---|---|
| TC-01 | Masukan valid dengan skill yang cocok dan tidak cocok | Skill terbagi ke daftar cocok dan kurang; skor dihitung dari skill yang ditemukan |
| TC-02 | Deskripsi pekerjaan kosong | Validasi melempar `ValueError` |
| TC-03 | Profil kandidat kosong | Validasi melempar `ValueError` |
| TC-04 | Menjalankan pipeline dengan file masukan | Hasil berupa objek JSON dengan field sesuai skema |
| TC-05 | Menjalankan pipeline | Hasil disimpan sebagai JSON valid di `output/result.json` |

## 4. Test Execution

Jalankan tes otomatis:

```bash
python -m unittest discover -s tests -v
```

Uji alur aplikasi secara manual dengan contoh berkas:

```bash
python src/main.py
```

Periksa `output/result.json` untuk memastikan output dapat dibaca sebagai JSON dan berisi `job_title`, `required_skills`, `matching_skills`, `missing_skills`, `match_score`, serta `recommendation`.

## 5. Test Results

Catat tanggal, perintah, jumlah tes yang lulus/gagal, dan hasil pemeriksaan manual setelah tes dijalankan. Jangan menandai kasus sebagai lulus sebelum hasil eksekusinya diverifikasi.
