                   USER
                     │
                     ▼
             Job Description
                     │
                     ▼
              Input Processor
                     │
                     ▼
                LLM Agent
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Extract     Compare     Score
      Skills      Profile     Match
          │          │          │
          └──────────┼──────────┘
                     ▼
              Structured JSON
                     │
                     ▼
                Result Store
                     │
                     ▼
                  Output


# System Design

## Components

### Input Processor
Receives and validates job description.

### Analyzer Abstraction
`src/llm.py` memilih implementasi melalui `LLM_PROVIDER`.

- `mock`: analyzer lokal berbasis kata kunci untuk pengembangan offline.
- `openai`: `src/openai_llm.py` memakai OpenAI Responses API dan Structured Outputs untuk mengambil judul serta skill.
- `gemini`: `src/gemini_llm.py` memakai Google Gen AI SDK dan JSON terstruktur untuk mengambil judul serta skill.

Skor, skill yang kurang, dan rekomendasi dihitung secara deterministik oleh aplikasi di `src/schemas.py`.

### Output Processor
Converts the LLM response into structured data.

### Storage
Stores the analysis results for later review.

## Request Flow

1. `src/main.py` membaca dan memvalidasi dua berkas masukan.
2. Provider terpilih menganalisis judul, skill wajib, dan skill kandidat yang cocok.
3. Aplikasi menormalisasi daftar skill, lalu menghitung skor dan rekomendasi.
4. Hasil tervalidasi ditulis ke `output/result.json`.

OpenAI provider memerlukan `OPENAI_API_KEY`, dan Gemini memerlukan `GEMINI_API_KEY` pada `.env`; provider lokal tidak membutuhkan koneksi jaringan.
