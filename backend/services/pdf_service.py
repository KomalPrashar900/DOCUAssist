# backend/services/pdf_service.py
# used to read pdf files and extract text for RAG ingestion; uses PyMuPDF (fitz) for fast text extraction, with optional OCR fallback for scanned PDFs (requires pytesseract)
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """Extract text per page, return [{page: int, text: str}]"""
    doc = fitz.open(file_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = page.get_text('text').strip()
        if text:                                # skip blank/image-only pages
            pages.append({'page': page_num + 1, 'text': text})
    doc.close()
    return pages

def extract_with_ocr_fallback(file_path: str) -> list[dict]:
    """Use OCR for scanned PDFs with no text layer (requires pytesseract)"""
    import pytesseract
    doc = fitz.open(file_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = page.get_text('text').strip()
        if not text:                            # no text layer — use OCR
            pix = page.get_pixmap(dpi=200)
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(pix.tobytes('png')))
            text = pytesseract.image_to_string(img).strip()
        if text:
            pages.append({'page': page_num + 1, 'text': text})
    doc.close()
    return pages