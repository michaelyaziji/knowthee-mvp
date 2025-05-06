import PyPDF2
from docx import Document
import re
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
import openai
import os
from openai import OpenAI

@dataclass
class DocumentMetadata:
    document_type: str
    source_file: str
    processed_date: datetime
    classification_reasoning: str

class DocumentProcessor:
    def __init__(self, openai_api_key: str = None):
        self.text_cleaners = [
            self._remove_headers_footers,
            self._remove_extra_whitespace,
            self._remove_page_numbers
        ]
        if openai_api_key is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
            if not openai_api_key:
                raise ValueError("OpenAI API key must be provided either as an argument or in the OPENAI_API_KEY environment variable.")
        self.openai_client = OpenAI(api_key=openai_api_key)
    
    def process_document(self, file_path: str) -> tuple[str, DocumentMetadata]:
        """Process a document and return cleaned text with metadata."""
        text = self._extract_text(file_path)
        for cleaner in self.text_cleaners:
            text = cleaner(text)
        
        # Classify the document using LLM
        doc_type, reasoning = self._classify_document_with_llm(text)
        
        # Create metadata
        metadata = DocumentMetadata(
            document_type=doc_type,
            source_file=file_path,
            processed_date=datetime.now(),
            classification_reasoning=reasoning
        )
        
        return text, metadata
    
    def _classify_document_with_llm(self, text: str) -> tuple[str, str]:
        """
        Use LLM to classify the document based on its content.
        Returns a tuple of (document_type, reasoning)
        """
        # Take first 4000 characters for classification to stay within token limits
        sample_text = text[:4000]
        
        prompt = f"""Please analyze this document and classify what type of document it is. 
        Also provide a brief explanation of why you classified it this way.
        Focus on the overall purpose and content of the document.

        Document sample:
        {sample_text}

        Please respond in this format:
        Type: [document type]
        Reasoning: [your explanation]"""

        response = self.openai_client.chat.completions.create(
            model="gpt-4.1-2025-04-14",
            messages=[
                {"role": "system", "content": "You are a document classification expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # Parse the response
        response_text = response.choices[0].message.content
        type_line = [line for line in response_text.split('\n') if line.startswith('Type:')][0]
        reasoning_line = [line for line in response_text.split('\n') if line.startswith('Reasoning:')][0]
        
        doc_type = type_line.replace('Type:', '').strip()
        reasoning = reasoning_line.replace('Reasoning:', '').strip()
        
        return doc_type, reasoning
    
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