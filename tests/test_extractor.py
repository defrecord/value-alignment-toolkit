"""
Unit tests for the value extractor module.
"""
import unittest
from src.extraction.extractor import ValueExtractor

class TestValueExtractor(unittest.TestCase):
    """Test suite for ValueExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = ValueExtractor()
    
    def test_extract_from_text(self):
        """Test basic value extraction from text."""
        text = "I'm committed to helping you with clarity and transparency."
        values = self.extractor.extract_from_text(text)
        
        # Check that some values were extracted
        self.assertTrue(len(values) > 0)
        
        # Check for specific expected values
        extracted_values = [v["value"] for v in values]
        self.assertIn("helpfulness", extracted_values)
        self.assertIn("transparency", extracted_values)
    
    def test_extract_from_conversation(self):
        """Test extracting values from a conversation transcript."""
        messages = [
            {"role": "user", "content": "Can you help me understand this concept?"},
            {"role": "assistant", "content": "I'll help you understand with clarity and thoroughness."},
            {"role": "user", "content": "Thanks, that's clear now."},
            {"role": "assistant", "content": "I'm glad I could help. Let me know if you need anything else."}
        ]
        
        values = self.extractor.extract_from_conversation(messages)
        
        # Check that values were extracted from both assistant messages
        self.assertTrue(len(values) >= 2)
        
        # Check for message indices
        for value in values:
            self.assertTrue("message_index" in value)
            self.assertTrue(value["message_index"] in [1, 3])  # Assistant message indices

if __name__ == "__main__":
    unittest.main()
