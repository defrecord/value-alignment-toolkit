"""
Unit tests for the anonymization module.
"""
import unittest
from datetime import datetime
from src.anonymization.anonymizer import Anonymizer

class TestAnonymizer(unittest.TestCase):
    """Test suite for Anonymizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.anonymizer = Anonymizer(salt="test_salt")
        
        # Sample user data
        self.user_data = {
            "id": 123,
            "username": "johndoe",
            "demographics": {
                "age": 34,
                "location": "San Francisco"
            },
            "chats": [1, 2, 3],
            "values": ["privacy", "honesty"]
        }
        
        # Sample message data
        self.message_data = {
            "id": 456,
            "chat_id": 2,
            "sender_id": 123,
            "content": "I think privacy is really important.",
            "timestamp": datetime.now(),
            "extracted_values": ["privacy", "honesty"]
        }
    
    def test_get_pseudonym(self):
        """Test pseudonym generation."""
        # Test basic pseudonym generation
        pseudonym1 = self.anonymizer.get_pseudonym("123")
        self.assertTrue(pseudonym1.startswith("User"))
        self.assertTrue(len(pseudonym1) > 4)  # "User" + at least one digit
        
        # Test consistency
        pseudonym2 = self.anonymizer.get_pseudonym("123")
        self.assertEqual(pseudonym1, pseudonym2)
        
        # Test context-specific pseudonyms
        context_pseudonym1 = self.anonymizer.get_pseudonym("123", "chat1")
        context_pseudonym2 = self.anonymizer.get_pseudonym("123", "chat2")
        self.assertNotEqual(context_pseudonym1, context_pseudonym2)
    
    def test_anonymize_user(self):
        """Test user anonymization."""
        anon_user = self.anonymizer.anonymize_user(self.user_data)
        
        # Check structure
        self.assertIn("anonymized_id", anon_user)
        self.assertIn("generalized_demographics", anon_user)
        self.assertIn("age_range", anon_user["generalized_demographics"])
        
        # Check demographic generalization
        self.assertEqual(anon_user["generalized_demographics"]["age_range"], "25-34")
        self.assertEqual(anon_user["generalized_demographics"]["region"], "West")
        
        # Check that sensitive information is removed
        self.assertNotIn("username", anon_user)
        self.assertNotIn("password", anon_user)
    
    def test_anonymize_message(self):
        """Test message anonymization."""
        anon_message = self.anonymizer.anonymize_message(self.message_data)
        
        # Check structure
        self.assertIn("anonymized_id", anon_message)
        self.assertIn("sender", anon_message)
        self.assertIn("length", anon_message)
        self.assertIn("timestamp", anon_message)
        
        # Check content anonymization
        self.assertEqual(anon_message["length"], len(self.message_data["content"]))
        self.assertNotIn("content", anon_message)
        
        # Check that values are preserved
        self.assertEqual(anon_message["extracted_values"], self.message_data["extracted_values"])
    
    def test_generalize_age(self):
        """Test age generalization."""
        self.assertEqual(self.anonymizer.generalize_age(17), "under-18")
        self.assertEqual(self.anonymizer.generalize_age(22), "18-24")
        self.assertEqual(self.anonymizer.generalize_age(30), "25-34")
        self.assertEqual(self.anonymizer.generalize_age(40), "35-44")
        self.assertEqual(self.anonymizer.generalize_age(50), "45-54")
        self.assertEqual(self.anonymizer.generalize_age(60), "55-64")
        self.assertEqual(self.anonymizer.generalize_age(70), "65+")
        self.assertEqual(self.anonymizer.generalize_age(None), "unknown")
    
    def test_generalize_timestamp(self):
        """Test timestamp generalization."""
        # Monday morning
        dt = datetime(2023, 1, 2, 10, 0, 0)  # Monday, 10 AM
        self.assertEqual(self.anonymizer.generalize_timestamp(dt), "Monday, morning")
        
        # Tuesday afternoon
        dt = datetime(2023, 1, 3, 14, 0, 0)  # Tuesday, 2 PM
        self.assertEqual(self.anonymizer.generalize_timestamp(dt), "Tuesday, afternoon")
        
        # Friday evening
        dt = datetime(2023, 1, 6, 19, 0, 0)  # Friday, 7 PM
        self.assertEqual(self.anonymizer.generalize_timestamp(dt), "Friday, evening")
        
        # Saturday night
        dt = datetime(2023, 1, 7, 23, 0, 0)  # Saturday, 11 PM
        self.assertEqual(self.anonymizer.generalize_timestamp(dt), "Saturday, night")

if __name__ == "__main__":
    unittest.main()
