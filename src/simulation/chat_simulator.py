"""
Chat simulation system that creates synthetic conversations with value expressions.
"""
from datetime import datetime
import random
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict

class User:
    """Represents a simulated user in the chat system."""
    
    def __init__(self, user_id: int, username: str, demographics: Optional[Dict[str, Any]] = None):
        self.id = user_id
        self.username = username
        self.demographics = demographics or {}
        self.creation_date = datetime.now()
        self.chats = set()  # Chat IDs this user participates in
        self.values = []    # Values this user expresses

class Chat:
    """Represents a simulated chat conversation."""
    
    def __init__(self, chat_id: int, name: str, creator_id: int):
        self.id = chat_id
        self.name = name
        self.creator_id = creator_id
        self.participants = set([creator_id])
        self.messages = []
        self.creation_date = datetime.now()
    
    def add_participant(self, user_id: int):
        """Add a participant to the chat."""
        self.participants.add(user_id)
    
    def add_message(self, message):
        """Add a message to the chat."""
        self.messages.append(message)

class Message:
    """Represents a message in a chat conversation."""
    
    def __init__(self, message_id: int, chat_id: int, sender_id: int, 
                 content: str, timestamp: Optional[datetime] = None):
        self.id = message_id
        self.chat_id = chat_id
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.extracted_values = None  # Will be populated during value extraction

class ChatSimulator:
    """
    Simulates a chat system with multiple users, conversations, and value expressions.
    
    Implements the simulation methodology from the Values in the Wild paper.
    """
    
    def __init__(self, value_sampler=None):
        """
        Initialize the chat simulator.
        
        Args:
            value_sampler: Optional value sampler for generating values in messages
        """
        self.users = {}
        self.chats = {}
        self.messages = []
        self.next_user_id = 1
        self.next_chat_id = 1
        self.next_message_id = 1
        
        # Create or use value sampler
        if value_sampler:
            self.value_sampler = value_sampler
        else:
            try:
                # Import locally to avoid circular imports
                from simulation.weighted_sampler import WeightedValueSampler
                self.value_sampler = WeightedValueSampler()
            except ImportError:
                print("Warning: WeightedValueSampler not available. Values will not be sampled.")
                self.value_sampler = None
    
    def create_users(self, count: int) -> List[User]:
        """
        Create a specified number of simulated users.
        
        Args:
            count: Number of users to create
            
        Returns:
            List of created User objects
        """
        locations = ["New York", "Los Angeles", "Chicago", "Dallas", "Boston", 
                     "Miami", "Seattle", "Atlanta", "San Francisco"]
        
        created_users = []
        for i in range(count):
            user_id = self.next_user_id
            self.next_user_id += 1
            username = f"user{user_id}"
            
            # Generate demographics
            demographics = {
                "age": 18 + random.randint(0, 50),  # 18-68
                "gender": random.choice(["female", "male", "non-binary"]),
                "location": random.choice(locations)
            }
            
            user = User(user_id, username, demographics)
            self.users[user_id] = user
            created_users.append(user)
        
        print(f"Created {count} users")
        return created_users
    
    def create_chats(self, chat_count_per_user: int) -> Dict[int, Chat]:
        """
        Create chats between users.
        
        Args:
            chat_count_per_user: Average number of chats per user
            
        Returns:
            Dictionary of created Chat objects
        """
        user_ids = list(self.users.keys())
        
        for creator_id in user_ids:
            # Vary chat count by ±30%
            chat_count = max(1, int(chat_count_per_user * (0.7 + random.random() * 0.6)))
            
            for i in range(chat_count):
                chat_id = self.next_chat_id
                self.next_chat_id += 1
                name = f"Chat {chat_id}"
                chat = Chat(chat_id, name, creator_id)
                
                # Add 1-5 random participants
                participant_count = 1 + random.randint(0, 4)
                attempts = 0
                
                while len(chat.participants) < participant_count and attempts < 10:
                    random_user_id = random.choice(user_ids)
                    if random_user_id != creator_id:
                        chat.add_participant(random_user_id)
                        self.users[random_user_id].chats.add(chat_id)
                    attempts += 1
                
                self.chats[chat_id] = chat
                self.users[creator_id].chats.add(chat_id)
        
        print(f"Created {len(self.chats)} chats")
        return self.chats
    
    def generate_messages(self, messages_per_chat: int) -> List[Message]:
        """
        Generate messages in each chat.
        
        Args:
            messages_per_chat: Average number of messages per chat
            
        Returns:
            List of generated Message objects
        """
        message_templates = [
            "Hey, how are you doing?",
            "I need help with something important.",
            "Can you provide some clear information on this topic?",
            "Let's be efficient about how we approach this project.",
            "I believe being honest is the most important thing here.",
            "We need to keep this discussion private and secure.",
            "I think the ethical thing to do is...",
            "As a professional, I recommend that we...",
            "Let me be transparent about what's happening.",
            "I appreciate your thoroughness in explaining this."
        ]
        
        for chat in self.chats.values():
            # Vary message count by ±30%
            message_count = max(2, int(messages_per_chat * (0.7 + random.random() * 0.6)))
            participants = list(chat.participants)
            
            # Create an alternating conversation
            for i in range(message_count):
                sender_id = participants[i % len(participants)]
                
                # AI assistant typically responds every other message
                is_assistant = i % 2 == 1
                
                # Generate content
                if is_assistant:
                    # Sample 1-3 values if this is an assistant message
                    values_count = random.randint(1, 3)
                    sampled_values = []
                    
                    if self.value_sampler:
                        sampled_values = self.value_sampler.sample_values(values_count)
                    
                    # Template-based content generation
                    content = f"I'll help you with that. "
                    
                    # Incorporate sampled values into content
                    if "helpfulness" in sampled_values:
                        content += "I'm here to assist you. "
                    if "transparency" in sampled_values:
                        content += "Let me be transparent about the process. "
                    if "clarity" in sampled_values:
                        content += "I'll explain this clearly. "
                else:
                    # User message
                    content = random.choice(message_templates)
                
                # Add some variation
                if not is_assistant:
                    variations = ["I think ", "In my opinion, ", "Perhaps ", "", "Actually, "]
                    content = random.choice(variations) + content
                
                # Create timestamp with realistic timing
                timestamp = datetime.now()
                
                # Create message
                message = Message(
                    self.next_message_id,
                    chat.id,
                    sender_id,
                    content,
                    timestamp
                )
                self.next_message_id += 1
                
                # Store values if this is an assistant message
                if is_assistant and self.value_sampler:
                    message.extracted_values = sampled_values
                
                self.messages.append(message)
                chat.add_message(message)
        
        print(f"Generated {len(self.messages)} messages")
        return self.messages
    
    def run_simulation(self, num_users=10, chats_per_user=5, messages_per_chat=10):
        """
        Run a complete chat simulation.
        
        Args:
            num_users: Number of users to create
            chats_per_user: Average chats per user
            messages_per_chat: Average messages per chat
            
        Returns:
            Dictionary with simulation results
        """
        print("Starting chat simulation...")
        
        # Create users
        self.create_users(num_users)
        
        # Create chats
        self.create_chats(chats_per_user)
        
        # Generate messages
        self.generate_messages(messages_per_chat)
        
        # Return simulation summary
        return {
            "summary": {
                "user_count": len(self.users),
                "chat_count": len(self.chats),
                "message_count": len(self.messages)
            },
            "data": {
                "users": self.users,
                "chats": self.chats,
                "messages": self.messages
            }
        }

# Example usage
if __name__ == "__main__":
    simulator = ChatSimulator()
    results = simulator.run_simulation(num_users=5, chats_per_user=3, messages_per_chat=5)
    print(f"Simulation complete with {results['summary']['message_count']} messages")
