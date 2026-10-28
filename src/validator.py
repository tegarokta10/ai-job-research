"""Input validation and normalization for the analysis pipeline."""


def validate_text(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} harus berupa teks yang tidak kosong")
    return value.strip()
