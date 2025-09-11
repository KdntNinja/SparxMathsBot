"""Image processing and OCR utilities for SparxMathsBot."""

import io
import re
from typing import Optional, Tuple

import easyocr
import pytesseract
from PIL import Image


class ImageProcessor:
    """Handles image processing and OCR operations."""

    def __init__(self, use_gpu: bool = True):
        """Initialize the image processor with EasyOCR reader."""
        self.reader = easyocr.Reader(["en"], gpu=use_gpu)
        self.multiplication_pattern = re.compile(r"(\d+)\s*\*\s*(\d+)\s*=\s*\?")

    def extract_text_pytesseract(self, image: Image.Image) -> str:
        """Extract text from image using pytesseract."""
        return pytesseract.image_to_string(image)

    def extract_text_easyocr(self, image_bytes: bytes) -> str:
        """Extract text from image bytes using EasyOCR."""
        extracted_text = self.reader.readtext(image_bytes, detail=0, paragraph=True)
        return " ".join(extracted_text)

    def find_multiplication_problem(self, text: str) -> Optional[Tuple[int, int]]:
        """Find and parse multiplication problem from text."""
        match = self.multiplication_pattern.search(text)
        if match:
            return tuple(map(int, match.groups()))
        return None

    def crop_image(
        self, image: Image.Image, box: Tuple[int, int, int, int]
    ) -> Image.Image:
        """Crop image to specified box coordinates."""
        return image.crop(box)

    def image_to_bytes(self, image: Image.Image, format: str = "PNG") -> bytes:
        """Convert PIL Image to bytes."""
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=format)
        image_bytes.seek(0)
        return image_bytes.getvalue()
