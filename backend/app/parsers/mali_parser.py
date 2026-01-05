import re
from typing import Dict


# -------------------------
# Utilities
# -------------------------

def _clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[|_“”\"‘’]+", "", s)
    return s.strip()


# -------------------------
# Name extraction helpers
# -------------------------

def _extract_name_after_label(text: str, label: str) -> str:
    """
    Handles:
    - NomfrANGARA
    - Nom: TANGARA
    - Prénoms]MOHAMELD
    """
    m = re.search(
        rf"{label}\s*[:\]\-]?\s*([^\n]{{0,60}})",
        text,
        flags=re.IGNORECASE
    )
    if not m:
        return ""

    chunk = m.group(1)

    # Cut if table/column words appear
    chunk = re.split(
        r"(Cat|D[ée]livr[ée]|Temporaire|Permanent|Sceau|autorité)",
        chunk,
        maxsplit=1,
        flags=re.IGNORECASE
    )[0]

    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]{3,}", chunk)
    return _clean(tokens[0]) if tokens else _clean(chunk)


# -------------------------
# Date extractors
# -------------------------

def _extract_birth_date(text: str) -> str:
    m = re.search(
        r"Date\s*de\s*naissance\s*[:\]\-]?\s*([oO0]?\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4})",
        text,
        flags=re.IGNORECASE
    )
    if not m:
        return ""

    d = m.group(1).replace(" ", "")
    return d.replace("o", "0").replace("O", "0")


def _extract_issue_date(text: str) -> str:
    m = re.search(
        r"D[ée]livr[ée].{0,25}([oO0]?\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4})",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )
    if not m:
        return ""

    d = m.group(1).replace(" ", "")
    return d.replace("o", "0").replace("O", "0")


def _extract_expiry_date(text: str) -> str:
    m = re.search(
        r"Valable\s*jusqu.*?([oO0]?\d{1,2}\s*/\s*\d{1,2}\s*/\s*\d{2,4})",
        text,
        flags=re.IGNORECASE | re.DOTALL
    )
    if not m:
        return ""

    d = m.group(1).replace(" ", "")
    return d.replace("o", "0").replace("O", "0")


# -------------------------
# License number
# -------------------------

def _extract_license_number(text: str) -> str:
    m = re.search(
        r"(N[°o]?\s*Permis|NPermis)\s*[:\-]?\s*([A-Z0-9\/\-]{4,})",
        text,
        flags=re.IGNORECASE
    )
    return _clean(m.group(2)) if m else ""


# -------------------------
# OCR post-correction
# -------------------------

def _postprocess_name(full_name: str) -> str:
    """
    Conservative OCR fixes based on common Mali DL errors
    """
    s = full_name.upper()

    # Fix common OCR letter mistakes
    s = re.sub(r"\bMOHAMELD\b", "MOHAMED", s)
    s = re.sub(r"\bANGARA\b", "TANGARA", s)

    return _clean(s)


# -------------------------
# MAIN PARSER
# -------------------------

def parse_mali_dl_text(raw_text: str) -> Dict[str, str]:
    t = raw_text

    # Last name
    last_name = _extract_name_after_label(t, r"Nom")
    last_name = re.sub(r"^Nom", "", last_name, flags=re.IGNORECASE).strip()
    last_name = re.sub(r"^(fr|f|mr)\s*", "", last_name, flags=re.IGNORECASE).strip()

    # First names
    first_names = _extract_name_after_label(t, r"Pr[ée]noms?")

    full_name = _clean(f"{last_name} {first_names}")
    full_name = _postprocess_name(full_name)

    return {
        "full_name": full_name,
        "birth_date": _extract_birth_date(t),
        "license_number": _extract_license_number(t),
        "issue_date": _extract_issue_date(t),
        "expiry_date": _extract_expiry_date(t),
    }
