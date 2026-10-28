# AI Job Research

Prototype lokal untuk membandingkan keterampilan pada deskripsi lowongan dengan profil kandidat.

## Menjalankan

Gunakan Python 3.10 atau lebih baru:

```bash
python src/main.py
```

Hasil analisis ditulis ke `output/result.json`. Ubah contoh masukan pada `data/job_description.txt` dan `data/candidate_profile.txt` untuk mencoba profil lain.

Analisis saat ini memakai pencocokan kata kunci lokal (`src/mock_llm.py`), bukan layanan LLM.

## Tes

```bash
python -m unittest discover -s tests
```

## Konfigurasi

Salin `.env.example` menjadi `.env` hanya jika integrasi API ditambahkan. Jangan simpan API key ke Git.
