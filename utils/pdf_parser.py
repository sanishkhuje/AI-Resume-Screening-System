from pathlib import Path
import pypdfium2 as pdfium


class PDFParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def extract_text(self) -> str:
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        try:
            pdf = pdfium.PdfDocument(str(self.file_path))
            pages_text = []

            for page in pdf:
                text_page = page.get_textpage()
                pages_text.append(text_page.get_text_range())

            pdf.close()
            return "\n".join(pages_text).strip()

        except Exception as e:
            raise RuntimeError(f"PDF parsing failed: {e}")
