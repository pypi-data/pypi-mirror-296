import PyPDF2
from pdfminer.high_level import extract_text

class PDFProcessor:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.num_pages = self.get_pages()
        self.text_content = self._extract_text()

    def get_pages(self):
        try:
            with open(self.pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                return pdf_reader.getNumPages()
        except (FileNotFoundError, Exception) as e:
            print(f'Помилка при читані файлу: {e}')


    def _extract_text(self):
        try:
            return extract_text(self.pdf_file)
        except (FileNotFoundError, Exception) as e:
            print(f'Failed to extract text from PDF file: {e}')


    def get_text(self):
        return self.text_content