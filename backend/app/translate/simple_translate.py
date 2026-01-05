# backend/app/translate/simple_translate.py

def to_english_labels(fields_fr: dict) -> dict:
    """
    Converts normalized keys OR table-style French keys to English keys.
    """
    mapping = {
        # normalized keys
        "last_name": "Last Name",
        "first_names": "First Names",
        "full_name": "Full Name",
        "birth_date": "Date of Birth",
        "birth_place": "Place of Birth",
        "issue_date": "Issue Date",
        "issue_place": "Issue Place",
        "license_number": "License Number",
        "birth_date_iso": "birth_date_iso",
        "issue_date_iso": "issue_date_iso",

        # table-style keys (CIV)
        "Nom": "Last Name",
        "Prénoms": "First Names",
        "Nom complet": "Full Name",
        "Date et lieu de naissance": "Date and place of birth",
        "Date et lieu de délivrance": "Date and place of issue",
        "Numéro du permis de conduire": "License Number",
        "Restriction(s)": "Restrictions",
        "header_classes": "Header Classes",
        "country": "Country",
        "issuing_authority": "Issuing Authority",
        "document_title": "Document Title",
    }

    out = {}
    for k, v in fields_fr.items():
        out[mapping.get(k, k)] = v
    return out
