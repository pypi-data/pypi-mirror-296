from concurrent.futures import ThreadPoolExecutor

import PyPDF2
from pdfminer.high_level import extract_text

class PDFProcessor:
    def __init__(self, pdf_file):
        self.pdf_file = pdf_file
        self.num_pages = self.get_pages()
        self.text_content = self.extract_text()

    def get_pages(self):
        try:
            with open(self.pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                return len(pdf_reader.pages)
        except (FileNotFoundError, Exception) as e:
            print(f'Помилка при читані файлу: {e}')

    def _extract_text_from_page(self, page_number):
        try:
            return extract_text(self.pdf_file, page_numbers=[page_number])
        except (FileNotFoundError, Exception) as e:
            raise Exception('Помилка при конвертації сторінки')

    def extract_text(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            page_numbers = list(range(self.num_pages))
            text_chunks = list(executor.map(self._extract_text_from_page, page_numbers))
            return '\n'.join(text_chunks)

    def get_text(self):
        return self.text_content