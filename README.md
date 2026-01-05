# DL Translate (Côte d’Ivoire Driver License)

DL Translate is a backend service designed to convert foreign driver license documents (specifically Côte d’Ivoire licenses) into structured, DMV-ready English translations.

This project focuses on document understanding rather than generic translation. Instead of translating raw text line-by-line, it extracts key identity fields, normalizes them, and outputs a certified translation PDF suitable for administrative use.

The architecture emphasizes:
- Deterministic parsing
- Transparency of extracted fields
- Predictable and auditable outputs

This makes the system well-suited for compliance-driven workflows where accuracy, traceability, and formatting matter more than linguistic creativity.

---

## What This Project Is (and Is Not)

This project is not a full AI-powered system and does not claim to be perfect.

It is an engineering-first prototype that demonstrates:
- OCR-driven data extraction
- Rule-based parsing and normalization
- Document formatting for official use cases

Some edge cases, OCR noise, and layout variations are expected and accepted at this stage.  
The goal is clarity, structure, and correctness — not black-box intelligence.

Future versions may integrate:
- AI-assisted field correction
- Confidence scoring
- Interactive validation via a frontend or chatbot

---

## API Endpoints

- `/ocr/civ` → JSON extraction + normalized fields  
- `/pdf/civ` → Downloadable certified translation PDF

---

## Project Structure

```text
dl-translate/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── ocr/
│   │   ├── parsers/
│   │   ├── pdf/
│   │   └── translate/
│   ├── uploads/
│   ├── outputs/
│   └── requirements.txt
├── frontend/  # (future work)
├── .gitignore
├── README.md
└── requirements.txt

---
## 🚀 Run Locally

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload







