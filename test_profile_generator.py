import unittest
from profile_generator import ProfileGenerator

class TestProfileGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ProfileGenerator()
        self.test_document_chunks = [
            "Sample leadership assessment: The candidate shows strong strategic thinking and team leadership.",
            "360 feedback: Colleagues report excellent communication skills and adaptability."
        ]
        self.test_metadata = [
            {"filename": "assessment.pdf", "file_type": "Leadership Assessment"},
            {"filename": "feedback.pdf", "file_type": "360 Feedback"}
        ]

    def test_generate_profile(self):
        """Test profile generation with document chunks and metadata"""
        profile = self.generator.generate_profile(self.test_document_chunks, self.test_metadata)
        
        # Check that the response contains the expected sections
        self.assertIn("Leadership Summary", profile)
        self.assertIn("Key Strengths", profile)
        self.assertIn("Potential Derailers", profile)
        self.assertIn("Leadership Style", profile)
        self.assertIn("Role Fit Chart", profile)
        
        # Check that document types are included in the header
        self.assertIn("Documents Used for Analysis", profile)
        self.assertIn("Leadership Assessment", profile)
        self.assertIn("360 Feedback", profile)

    def test_generate_profile_no_metadata(self):
        """Test profile generation without metadata"""
        profile = self.generator.generate_profile(self.test_document_chunks)
        
        # Check that the response contains the expected sections
        self.assertIn("Leadership Summary", profile)
        self.assertIn("Key Strengths", profile)
        self.assertIn("Potential Derailers", profile)
        self.assertIn("Leadership Style", profile)
        self.assertIn("Role Fit Chart", profile)

    def test_answer_question(self):
        """Test question answering functionality"""
        question = "What are the candidate's main strengths according to the feedback?"
        answer = self.generator.answer_question(self.test_document_chunks, question)
        
        # Check that we got a response
        self.assertIsNotNone(answer)
        self.assertGreater(len(answer), 0)

if __name__ == '__main__':
    unittest.main() 