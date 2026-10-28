"""Run a local job description and candidate profile analysis."""

import json
from pathlib import Path

from mock_llm import analyze
from validator import validate_text

ROOT = Path(__file__).resolve().parents[1]


def run_analysis(job_path: Path | None = None, profile_path: Path | None = None) -> dict:
    job_file = job_path or ROOT / "data" / "job_description.txt"
    profile_file = profile_path or ROOT / "data" / "candidate_profile.txt"
    job = validate_text(job_file.read_text(encoding="utf-8"), "Deskripsi pekerjaan")
    profile = validate_text(profile_file.read_text(encoding="utf-8"), "Profil kandidat")
    result = analyze(job, profile).to_dict()
    output_file = ROOT / "output" / "result.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(run_analysis(), ensure_ascii=False, indent=2))
