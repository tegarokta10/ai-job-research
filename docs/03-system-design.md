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

### LLM
Analyzes job requirements and compares them
with the candidate profile.

### Output Processor
Converts the LLM response into structured data.

### Storage
Stores the analysis results for later review.