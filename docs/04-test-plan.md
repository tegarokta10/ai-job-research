# Rencana dan Hasil Pengujian

## Tujuan

Memastikan input divalidasi, analyzer menghasilkan data terstruktur, judul lowongan dikenali, skor dihitung konsisten, dan hasil dapat disimpan ke JSON.

## Lingkungan

- OS: Windows
- Python: 3.14.4 pada virtualenv di direktori workspace induk
- Framework: `unittest` dari standard library
- Uji provider OpenAI dan Gemini memakai client tiruan; tidak mengirim request jaringan

Jalankan perintah dari direktori proyek:

```powershell
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Kasus Pengujian Otomatis

| ID | Kasus | Hasil yang diharapkan |
|---|---|---|
| TC-01 | Input kosong | Validasi melempar `ValueError` |
| TC-02 | Lowongan memiliki skill cocok dan tidak cocok | Daftar skill, skor, dan rekomendasi sesuai input |
| TC-03 | Judul memiliki label `Posisi:` | Judul diekstrak dengan benar |
| TC-04 | Pipeline memakai berkas masukan dan output sementara | JSON berisi field skema dan tersimpan di lokasi output |
| TC-05 | Provider OpenAI diberi client tiruan | Hasil OpenAI diproses tanpa jaringan |
| TC-06 | Provider Gemini diberi client tiruan | Hasil Gemini diproses tanpa jaringan |

## Hasil Terakhir

Pada 28 Oktober 2026, perintah otomatis di atas menghasilkan **4 tes lulus dan 0 gagal**. Cakupannya meliputi input kosong, pipeline dan `job_title`, serta adaptor OpenAI dan Gemini dengan client tiruan.

`output/result.json` saat dokumen ini diperbarui berisi hasil untuk lowongan **Data Analyst Game**: 5 skill wajib, 4 cocok, skor **80**, rekomendasi **Cocok**. Skema output belum menyimpan nama provider maupun waktu eksekusi.

## Uji Provider Live

Dalam percobaan live Gemini pada 28 Oktober 2026, API dua kali mengembalikan `503 UNAVAILABLE` karena model sedang ramai. File hasil yang saat ini tersedia tidak membuktikan bahwa percobaan tersebut berhasil; ulangi `python src/main.py` untuk memastikan hasil live terbaru. Panggilan live mengirim deskripsi pekerjaan dan profil kandidat ke penyedia model serta dapat memakai kuota akun.
