# Status Proyek

**Terakhir diperbarui:** 28 Oktober 2026  
**Versi:** prototipe command line  
**Commit terakhir:** `5d7187f` — `Gemini Model`

## Selesai

- [x] Struktur proyek dan dokumen kebutuhan tersedia.
- [x] Pipeline membaca deskripsi lowongan dan profil kandidat dari berkas lokal.
- [x] Validasi input kosong dan schema output diterapkan.
- [x] Analyzer mock tersedia untuk proses offline.
- [x] Abstraksi provider dan adaptor OpenAI/Gemini tersedia.
- [x] Skor, skill yang belum cocok, dan rekomendasi dihitung secara lokal.
- [x] Hasil ditulis ke `output/result.json`.
- [x] API key dikecualikan dari Git melalui `.gitignore`.
- [x] Empat tes otomatis terakhir lulus.

## Hasil Saat Ini

`output/result.json` berisi analisis lowongan **Data Analyst Game**: 5 skill wajib, 4 skill cocok, 1 skill kurang, skor **80**, dan rekomendasi **Cocok**. File hasil belum mencatat provider atau waktu pembuatannya.

Konfigurasi Gemini ada pada `.env`, yang tetap lokal dan tidak dilacak Git. Nilai API key tidak dicatat dalam dokumen ini. Model lama `gemini-1.5-flash` sudah dihentikan; konfigurasi diperbarui ke `gemini-3.8-flash`.

## Kendala dan Batasan

- Dua panggilan live Gemini pada sesi pengembangan terakhir menerima `503 UNAVAILABLE` karena kapasitas model sedang tinggi. Hasil JSON yang ada tidak dianggap sebagai bukti bahwa panggilan tersebut berhasil.
- Aplikasi masih memakai file lokal; belum ada UI, endpoint HTTP, database, atau pencarian lowongan otomatis.
- Penanganan error jaringan belum diringkas menjadi pesan pengguna yang konsisten.

## Langkah Berikutnya

1. Jalankan `python src/main.py` kembali saat Gemini tersedia dan periksa hasilnya.
2. Simpan metadata provider, model, dan waktu analisis bersama hasil agar asal output jelas.
3. Tambahkan tes untuk skill kosong, ambang skor, error API, dan respons model yang gagal divalidasi.
4. Setelah pipeline stabil, pertimbangkan API HTTP dan antarmuka pengguna.
