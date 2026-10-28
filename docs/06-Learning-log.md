# Catatan Pembelajaran Proyek

Dokumen ini mencatat konsep yang sudah diterapkan dalam kode serta hal yang masih perlu dipelajari dan diuji.

## Fase 1 — Python dan Struktur Proyek

### Sudah diterapkan

- Pembagian kode ke modul input, analyzer, schema, dan entry point.
- Penggunaan virtualenv dan `requirements.txt` untuk dependensi.
- Penggunaan `pathlib` untuk lokasi berkas dan `json` untuk output.
- Penggunaan `.env` dan `.gitignore` untuk memisahkan kredensial lokal dari Git.

### Lanjutan

- Memastikan dependency freeze hanya mencakup paket yang dibutuhkan proyek dan menjaga kompatibilitas versi.

## Fase 2 — Integrasi LLM

### Sudah diterapkan

- Provider dipilih melalui `LLM_PROVIDER`.
- Mock, OpenAI, dan Gemini menerapkan kontrak analyzer yang sama.
- Gemini memakai Google Gen AI SDK dan schema JSON; OpenAI memakai Responses API dengan schema Pydantic.
- API key dibaca dari environment, dan model dikonfigurasi terpisah.

### Lanjutan

- Menangani rate limit, timeout, model overload, dan kuota secara konsisten.
- Mengevaluasi kualitas ekstraksi judul dan skill terhadap contoh lowongan yang lebih beragam.

## Fase 3 — Validasi dan Pengujian

### Sudah diterapkan

- Input kosong ditolak sebelum dianalisis.
- Pydantic memvalidasi bentuk hasil dan rentang skor.
- Tes otomatis menguji pipeline serta adaptor provider menggunakan client tiruan.
- Empat tes terakhir lulus tanpa mengirim request ke layanan AI.

### Lanjutan

- Tambahkan kasus untuk rekomendasi pada setiap batas skor, daftar skill kosong, kegagalan provider, dan format respons tidak valid.
- Tambahkan integration test live yang dijalankan secara terpisah dan tercatat agar tidak bergantung pada layanan saat tes rutin.

## Fase 4 — AI Agent

Implementasi sekarang adalah pipeline analisis dengan provider LLM. Sistem belum menjadi agent otonom: belum mencari lowongan sendiri, memakai tools, atau merencanakan beberapa langkah. Pengembangan agent dapat dilakukan setelah sumber lowongan, kebutuhan tools, dan batas tindakan ditentukan.

## Fase 5 — Status Integrasi Gemini

Provider Gemini sudah ada di `src/gemini_llm.py`. Model `gemini-1.5-flash` yang sebelumnya terkonfigurasi sudah dihentikan, sehingga konfigurasi diperbarui ke model Gemini yang lebih baru. Percobaan live sempat menerima `503 UNAVAILABLE`; lihat `07-project-status.md` untuk status dan langkah berikutnya.
