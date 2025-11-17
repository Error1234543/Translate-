import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file.
    Returns full text as string.
    """
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text