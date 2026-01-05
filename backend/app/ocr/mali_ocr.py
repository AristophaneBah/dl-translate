from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any

from PIL import Image
import pytesseract


@dataclass
class OCRResult:
    text: str
    meta: Dict[str, Any]


def ocr_mali_french(image_path: str) -> OCRResult:
    img = Image.open(image_path).convert("RGB")
    text = pytesseract.image_to_string(img, lang="fra", config="--psm 6")
    return OCRResult(text=text, meta={"engine": "tesseract", "lang": "fra", "psm": 6})

