import PyPDF2
from docx import Document
import re

class DocumentProcessor:
    def __init__(self):
        self.text_cleaners = [
            self._remove_headers_footers,
            self._remove_extra_whitespace,
            self._remove_page_numbers
        ]
    
    def process_document(self, file_path):
        """Process a document and return cleaned text."""
        text = self._extract_text(file_path)
        for cleaner in self.text_cleaners:
            text = cleaner(text)
        return text
    
    def _extract_text(self, file_path):
        """Extract text from PDF or DOCX file."""
        if file_path.lower().endswith('.pdf'):
            return self._extract_pdf_text(file_path)
        elif file_path.lower().endswith('.docx'):
            return self._extract_docx_text(file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def _extract_pdf_text(self, file_path):
        """Extract text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_docx_text(self, file_path):
        """Extract text from DOCX file."""
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    def _remove_headers_footers(self, text):
        """Remove common header and footer patterns."""
        # Remove page numbers
        text = re.sub(r'\n\d+\n', '\n', text)
        # Remove common header/footer patterns
        text = re.sub(r'Page \d+ of \d+', '', text)
        return text
    
    def _remove_extra_whitespace(self, text):
        """Remove extra whitespace and normalize newlines."""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _remove_page_numbers(self, text):
        """Remove standalone page numbers."""
        return re.sub(r'^\d+$', '', text, flags=re.MULTILINE) 