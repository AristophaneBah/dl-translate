# backend/app/main.py

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import uuid

from app.ocr.mali_ocr import ocr_mali_french
from app.parsers.civ_parser import parse_civ_dl_text
from app.pdf.civ_pdf import build_civ_translation_pdf

app = FastAPI(title="DL Translate AI", version="0.1.0")

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


def _save_upload(file: UploadFile) -> tuple[str, Path]:
    ext = Path(file.filename).suffix.lower() or ".jpg"
    safe_name = f"{uuid.uuid4().hex}{ext}"
    save_path = UPLOAD_DIR / safe_name
    return safe_name, save_path


def _require_image(file: UploadFile):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file (jpg/png).")


@app.post("/ocr/civ")
async def ocr_civ(file: UploadFile = File(...)):
    _require_image(file)

    safe_name, save_path = _save_upload(file)

    try:
        content = await file.read()
        save_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        result = ocr_mali_french(str(save_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {e}")

    normalized = parse_civ_dl_text(result.text)

    # ✅ French table fields (close to the driver license)
    fields_fr = {
        "header_classes": "[A][B][C][D][E]",
        "license_categories": ["A", "B", "C", "D", "E"],
        "country": "RÉPUBLIQUE DE CÔTE D’IVOIRE",
        "issuing_authority": "MINISTÈRE DES TRANSPORTS",
        "document_title": "PERMIS DE CONDUIRE",

        "Nom": normalized.get("last_name", ""),
        "Prénoms": normalized.get("first_names", ""),
        "Nom complet": normalized.get("full_name", ""),
        "Date et lieu de naissance": f"{normalized.get('birth_date','')} {normalized.get('birth_place','')}".strip(),
        "Date et lieu de délivrance": f"{normalized.get('issue_date','')} {normalized.get('issue_place','')}".strip(),
        "Numéro du permis de conduire": normalized.get("license_number", ""),

        # ✅ UPDATED: restrictions logic
        "Restriction(s)": (
            "Néant"
            if normalized.get("restrictions") in ("", None, "None indicated")
            else normalized.get("restrictions", "Néant")
        ),
    }

    # ✅ English table fields
    fields_en = {
        "Header Classes": "[A][B][C][D][E]",
        "License Categories": ["A", "B", "C", "D", "E"],
        "Country": "REPUBLIC OF CÔTE D’IVOIRE",
        "Issuing Authority": "MINISTRY OF TRANSPORTATION",
        "Document Title": "DRIVER'S LICENSE",

        "Last Name": normalized.get("last_name", ""),
        "First Names": normalized.get("first_names", ""),
        "Full Name": normalized.get("full_name", ""),
        "Date of Birth": normalized.get("birth_date", ""),
        "Place of Birth": normalized.get("birth_place", ""),
        "Issue Date": normalized.get("issue_date", ""),
        "Issue Place": normalized.get("issue_place", ""),
        "License Number": normalized.get("license_number", ""),

        # ✅ UPDATED: restrictions logic
        "Restrictions": normalized.get("restrictions", "None indicated"),
    }

    return JSONResponse(
        {
            "filename": file.filename,
            "saved_as": safe_name,
            "meta": result.meta,
            "raw_text": result.text,
            "fields_fr": fields_fr,
            "fields_en": fields_en,
            "normalized": normalized,
        }
    )


@app.post("/pdf/civ")
async def pdf_civ(file: UploadFile = File(...)):
    """
    Returns the PDF directly (download from browser/Swagger).
    This endpoint does OCR + parse + builds the PDF in one call.
    """
    _require_image(file)

    safe_name, save_path = _save_upload(file)

    try:
        content = await file.read()
        save_path.write_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    try:
        result = ocr_mali_french(str(save_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {e}")

    normalized = parse_civ_dl_text(result.text)

    # same table content as /ocr/civ
    fields_fr = {
        "header_classes": "[A][B][C][D][E]",
        "license_categories": ["A", "B", "C", "D", "E"],
        "country": "RÉPUBLIQUE DE CÔTE D’IVOIRE",
        "issuing_authority": "MINISTÈRE DES TRANSPORTS",
        "document_title": "PERMIS DE CONDUIRE",

        "Nom": normalized.get("last_name", ""),
        "Prénoms": normalized.get("first_names", ""),
        "Nom complet": normalized.get("full_name", ""),
        "Date et lieu de naissance": f"{normalized.get('birth_date','')} {normalized.get('birth_place','')}".strip(),
        "Date et lieu de délivrance": f"{normalized.get('issue_date','')} {normalized.get('issue_place','')}".strip(),
        "Numéro du permis de conduire": normalized.get("license_number", ""),

        "Restriction(s)": (
            "Néant"
            if normalized.get("restrictions") in ("", None, "None indicated")
            else normalized.get("restrictions", "Néant")
        ),
    }

    fields_en = {
        "Header Classes": "[A][B][C][D][E]",
        "License Categories": ["A", "B", "C", "D", "E"],
        "Country": "REPUBLIC OF CÔTE D’IVOIRE",
        "Issuing Authority": "MINISTRY OF TRANSPORTATION",
        "Document Title": "DRIVER'S LICENSE",

        "Last Name": normalized.get("last_name", ""),
        "First Names": normalized.get("first_names", ""),
        "Full Name": normalized.get("full_name", ""),
        "Date of Birth": normalized.get("birth_date", ""),
        "Place of Birth": normalized.get("birth_place", ""),
        "Issue Date": normalized.get("issue_date", ""),
        "Issue Place": normalized.get("issue_place", ""),
        "License Number": normalized.get("license_number", ""),

        "Restrictions": normalized.get("restrictions", "None indicated"),
    }

    # build pdf
    try:
        pdf_path = build_civ_translation_pdf(
            fields_fr=fields_fr,
            fields_en=fields_en,
            normalized=normalized,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF build failed: {e}")

    return FileResponse(
        path=str(pdf_path),
        media_type="application/pdf",
        filename="civ_driver_license_translation.pdf",
    )

