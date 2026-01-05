\# DL Translate AI (Côte d’Ivoire Driver License)



FastAPI service that:

\- Performs OCR on driver license images (French)

\- Extracts \& normalizes identity fields

\- Generates a DMV-ready certified translation PDF



\## Features

\- `/ocr/civ` → JSON extraction + normalized fields

\- `/pdf/civ` → downloadable certified translation PDF



\## Run locally



```bash

cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload




