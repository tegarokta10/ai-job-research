# Pernyataan Masalah

## Latar Belakang

Pencari kerja perlu membaca deskripsi lowongan dan membandingkan persyaratannya dengan keterampilan serta pengalaman mereka. Proses manual ini berulang, memakan waktu, dan menyulitkan kandidat menilai kesesuaian secara konsisten.

## Tujuan

Membangun AI Job Research, sebuah pipeline yang menganalisis satu deskripsi pekerjaan terhadap satu profil kandidat dan menghasilkan ringkasan kecocokan dalam format JSON.

## Ruang Lingkup Versi Saat Ini

- Masukan dibaca dari `data/job_description.txt` dan `data/candidate_profile.txt`.
- Analyzer dapat dipilih melalui `LLM_PROVIDER`: `mock`, `openai`, atau `gemini`.
- Hasil ditulis ke `output/result.json`.
- Judul lowongan, skill yang diminta, skill yang cocok, skill yang belum cocok, skor, dan rekomendasi dimasukkan ke hasil.

Versi saat ini adalah prototipe command line. Pencarian lowongan otomatis, antarmuka web, basis data, dan endpoint HTTP belum termasuk implementasi.

## Hasil yang Diharapkan

```json
{
  "job_title": "Data Analyst",
  "required_skills": ["python", "sql"],
  "matching_skills": ["python"],
  "missing_skills": ["sql"],
  "match_score": 50,
  "recommendation": "Pertimbangkan"
}
```

Skor dihitung aplikasi dari proporsi skill wajib yang cocok. Rekomendasi memakai ambang yang ditetapkan di kode; hasil ini alat bantu evaluasi dan bukan keputusan perekrutan.
