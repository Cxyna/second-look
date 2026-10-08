"""Extract text from screenshot images using local onnxruntime OCR."""
from __future__ import annotations

import io
from typing import BinaryIO

_ocr_engine = None


def get_ocr_engine():
    global _ocr_engine
    if _ocr_engine is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _ocr_engine = RapidOCR()
        except Exception:
            _ocr_engine = False
    return _ocr_engine


def extract_text_from_image(image_bytes_or_file: bytes | BinaryIO) -> str:
    """Extract and order lines of text from an image.
    
    Returns clean plaintext, or an empty string if nothing could be detected.
    """
    engine = get_ocr_engine()
    if not engine:
        return ""

    if hasattr(image_bytes_or_file, "read"):
        raw_bytes = image_bytes_or_file.read()
    else:
        raw_bytes = image_bytes_or_file

    if not raw_bytes:
        return ""

    try:
        results, _ = engine(raw_bytes)
        if not results:
            return ""
        # results are structured as: [[[box_points], text, confidence], ...]
        lines = [line[1].strip() for line in results if len(line) >= 2 and line[1].strip()]
        return "\n".join(lines)
    except Exception:
        return ""
