import unittest
import os
import tempfile
from document_processor import DocumentProcessor
from fpdf import FPDF

class TestDocumentProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DocumentProcessor()
        # Create a temporary PDF test file
        self.test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        self.test_file.close()
        
        # Create a simple PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Test content", ln=1, align="C")
        pdf.cell(200, 10, txt="Page 1", ln=1, align="C")
        pdf.cell(200, 10, txt="More content", ln=1, align="C")
        pdf.output(self.test_file.name)

    def tearDown(self):
        # Clean up the test file
        os.unlink(self.test_file.name)

    def test_process_document_metadata(self):
        """Test that process_document returns both text and metadata"""
        text, metadata = self.processor.process_document(self.test_file.name)
        
        # Check that we got both text and metadata
        self.assertIsNotNone(text)
        self.assertIsNotNone(metadata)
        
        # Check metadata fields
        self.assertIn('filename', metadata)
        self.assertIn('file_type', metadata)
        self.assertIn('processed_date', metadata)
        
        # Check metadata values
        self.assertEqual(metadata['filename'], os.path.basename(self.test_file.name))
        self.assertEqual(metadata['file_type'], '.pdf')

    def test_text_cleaning(self):
        """Test that text cleaning functions work correctly"""
        text, _ = self.processor.process_document(self.test_file.name)
        
        # Check that page numbers are removed
        self.assertNotIn('Page 1', text)
        
        # Check that extra whitespace is removed
        self.assertNotIn('  ', text)  # No double spaces
        self.assertNotIn('\n\n\n', text)  # No triple newlines

if __name__ == '__main__':
    unittest.main() 