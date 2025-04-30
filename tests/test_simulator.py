"""
Unit tests for the chat simulator module.
"""
import unittest
from src.simulation.chat_simulator import ChatSimulator, User, Chat, Message

class TestChatSimulator(unittest.TestCase):
    """Test suite for ChatSimulator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.simulator = ChatSimulator()
    
    def test_create_users(self):
        """Test user creation."""
        num_users = 5
        users = self.simulator.create_users(num_users)
        
        # Check number of users
        self.assertEqual(len(users), num_users)
        self.assertEqual(len(self.simulator.users), num_users)
        
        # Check user properties
        for user in users:
            self.assertIsInstance(user, User)
            self.assertTrue(hasattr(user, 'id'))
            self.assertTrue(hasattr(user, 'username'))
            self.assertTrue(hasattr(user, 'demographics'))
            self.assertTrue(hasattr(user, 'chats'))
    
    def test_create_chats(self):
        """Test chat creation."""
        # Create users first
        self.simulator.create_users(5)
        
        # Create chats
        chats_per_user = 3
        chats = self.simulator.create_chats(chats_per_user)
        
        # Check that chats were created
        self.assertGreater(len(chats), 0)
        self.assertEqual(len(self.simulator.chats), len(chats))
        
        # Check chat properties
        for chat in chats.values():
            self.assertIsInstance(chat, Chat)
            self.assertTrue(hasattr(chat, 'id'))
            self.assertTrue(hasattr(chat, 'name'))
            self.assertTrue(hasattr(chat, 'participants'))
            
            # Check that chat has participants
            self.assertGreater(len(chat.participants), 0)
    
    def test_generate_messages(self):
        """Test message generation."""
        # Set up users and chats
        self.simulator.create_users(3)
        self.simulator.create_chats(2)
        
        # Generate messages
        messages_per_chat = 4
        messages = self.simulator.generate_messages(messages_per_chat)
        
        # Check that messages were created
        self.assertGreater(len(messages), 0)
        
        # Check message properties
        for message in messages:
            self.assertIsInstance(message, Message)
            self.assertTrue(hasattr(message, 'id'))
            self.assertTrue(hasattr(message, 'chat_id'))
            self.assertTrue(hasattr(message, 'sender_id'))
            self.assertTrue(hasattr(message, 'content'))
            self.assertTrue(hasattr(message, 'timestamp'))
    
    def test_run_simulation(self):
        """Test complete simulation run."""
        # Run a small simulation
        results = self.simulator.run_simulation(num_users=2, chats_per_user=2, messages_per_chat=3)
        
        # Check results structure
        self.assertIn('summary', results)
        self.assertIn('user_count', results['summary'])
        self.assertIn('chat_count', results['summary'])
        self.assertIn('message_count', results['summary'])
        
        # Check counts
        self.assertEqual(results['summary']['user_count'], 2)
        self.assertGreaterEqual(results['summary']['chat_count'], 2)
        self.assertGreaterEqual(results['summary']['message_count'], 6)  # At least 2 chats * 3 messages

if __name__ == "__main__":
    unittest.main()
