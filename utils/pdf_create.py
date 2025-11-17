from fpdf import FPDF

def create_pdf_from_text(text, output_path):
    """
    Create PDF from text.
    Each line becomes a new paragraph.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 8, line)
    pdf.output(output_path)