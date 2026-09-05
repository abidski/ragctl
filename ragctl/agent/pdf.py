from pathlib import Path

from fpdf import FPDF
from langchain_core.tools import tool


@tool
def pdf_tool(filename: str, content: str):
    """Create a PDF file with the given content. Use this when the user
    asks you to save, export, or generate a PDF document. The filename
    should not include the .pdf extension - it will be added automatically."""

    output_path = Path.cwd() / f"{filename}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Iosevka", "", "/usr/share/fonts/TTF/IosevkaNerdFont-Regular.ttf")
    pdf.set_font("Iosevka", size=11)
    pdf.multi_cell(0, 8, content)
    pdf.output(str(output_path))

    return f"PDF created successfully at {output_path}"
