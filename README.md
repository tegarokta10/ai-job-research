# AI Job Research

Prototype untuk membandingkan keterampilan pada deskripsi lowongan dengan profil kandidat. Provider dapat dipilih antara analyzer lokal, OpenAI Responses API, dan Gemini API.

## Menjalankan

Gunakan Python 3.10 atau lebih baru:

```bash
python src/main.py
```

Hasil analisis ditulis ke `output/result.json`. Ubah contoh masukan pada `data/job_description.txt` dan `data/candidate_profile.txt` untuk mencoba profil lain.

Untuk menggunakan Gemini:

1. Isi `GEMINI_API_KEY` di `.env`.
2. Atur `LLM_PROVIDER=gemini` dan `GEMINI_MODEL`.
3. Jalankan perintah yang sama.

Abstraksi provider berada di `src/llm.py`. Integrasi Gemini memakai JSON terstruktur, sedangkan skor dan rekomendasi dihitung aplikasi dari daftar skill. Provider `mock` tetap tersedia untuk penggunaan offline; provider OpenAI juga tersedia melalui `LLM_PROVIDER=openai`.

## Tes

```bash
python -m unittest discover -s tests
```

## Konfigurasi

Jangan simpan API key ke Git. File `.env` sudah dikecualikan oleh `.gitignore`.
