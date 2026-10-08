import io
from PIL import Image, ImageDraw
import ocr


def test_extract_text_empty():
    assert ocr.extract_text_from_image(b"") == ""


def test_extract_text_invalid_bytes():
    assert ocr.extract_text_from_image(b"not an image") == ""


def test_extract_text_from_synthetic_image():
    img = Image.new("RGB", (400, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((20, 30), "Royal Mail Delivery Alert", fill=(0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    extracted = ocr.extract_text_from_image(buf.getvalue())
    assert "Royal Mail" in extracted or "Delivery" in extracted
