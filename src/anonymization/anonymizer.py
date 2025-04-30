"""
Anonymization tools implementing privacy techniques from the Values in the Wild paper.
"""
import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional

class Anonymizer:
    """
    Provides privacy-preserving anonymization techniques for conversation data.
    
    Implements the anonymization methodology from the Values in the Wild paper,
    including pseudonymization, k-anonymity, and other privacy-preserving techniques.
    """
    
    def __init__(self, salt: str = None):
        """
        Initialize the anonymizer.
        
        Args:
            salt: Optional salt for hash-based pseudonymization
        """
        self.salt = salt or str(random.randint(10000, 99999))
        self.pseudonym_map = {}
    
    def get_pseudonym(self, identifier: str, context_id: str = None) -> str:
        """
        Generate a consistent pseudonym for an identifier.
        
        Args:
            identifier: Original identifier (e.g., user ID)
            context_id: Optional context for context-specific pseudonyms
            
        Returns:
            Pseudonymized identifier
        """
        key = f"{identifier}-{context_id}" if context_id else identifier
        
        if key not in self.pseudonym_map:
            # Generate a pseudonym using a hash function
            hash_input = f"{key}-{self.salt}"
            hash_value = hashlib.md5(hash_input.encode('utf-8')).hexdigest()
            pseudonym = f"User{abs(int(hash_value, 16) % 1000)}"
            self.pseudonym_map[key] = pseudonym
        
        return self.pseudonym_map[key]
    
    def anonymize_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an anonymized version of a user.
        
        Args:
            user: Original user data
            
        Returns:
            Anonymized user data
        """
        return {
            "anonymized_id": self.get_pseudonym(str(user["id"])),
            "generalized_demographics": {
                "age_range": self.generalize_age(user.get("demographics", {}).get("age")),
                "region": self.generalize_location(user.get("demographics", {}).get("location")),
            },
            "chat_count": len(user.get("chats", [])),
            "value_count": len(user.get("values", [])),
        }
    
    def anonymize_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an anonymized version of a message.
        
        Args:
            message: Original message data
            
        Returns:
            Anonymized message data
        """
        # Create context-specific pseudonym for the sender
        sender_id = str(message["sender_id"])
        chat_id = str(message["chat_id"])
        
        return {
            "anonymized_id": f"msg-{abs(hash(str(message['id'])) % 10000)}",
            "chat_id": f"chat-{abs(hash(str(chat_id)) % 10000)}",
            "sender": self.get_pseudonym(sender_id, chat_id),  # Context-specific pseudonym
            "length": len(message.get("content", "")),
            "timestamp": self.generalize_timestamp(message.get("timestamp")),
            "extracted_values": message.get("extracted_values", []),
        }
    
    def generalize_age(self, age: Optional[int]) -> str:
        """
        Generalize age into age ranges.
        
        Args:
            age: Original age
            
        Returns:
            Age range
        """
        if not age:
            return "unknown"
        
        if age < 18:
            return "under-18"
        elif age < 25:
            return "18-24"
        elif age < 35:
            return "25-34"
        elif age < 45:
            return "35-44"
        elif age < 55:
            return "45-54"
        elif age < 65:
            return "55-64"
        else:
            return "65+"
    
    def generalize_location(self, location: Optional[str]) -> str:
        """
        Generalize location to region level.
        
        Args:
            location: Original location
            
        Returns:
            Generalized region
        """
        if not location:
            return "unknown"
        
        # Region mapping
        regions = {
            "New York": "Northeast",
            "Boston": "Northeast",
            "Philadelphia": "Northeast",
            "Los Angeles": "West",
            "San Francisco": "West",
            "Seattle": "West",
            "Chicago": "Midwest",
            "Detroit": "Midwest",
            "Dallas": "South",
            "Atlanta": "South",
            "Miami": "South",
        }
        
        return regions.get(location, "Other")
    
    def generalize_timestamp(self, timestamp: Optional[datetime]) -> str:
        """
        Generalize timestamp to day of week and time range.
        
        Args:
            timestamp: Original timestamp
            
        Returns:
            Generalized time description
        """
        if not timestamp:
            return "unknown"
        
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day_of_week = days[timestamp.weekday()]
        
        hour = timestamp.hour
        if 5 <= hour < 12:
            time_range = "morning"
        elif 12 <= hour < 17:
            time_range = "afternoon"
        elif 17 <= hour < 22:
            time_range = "evening"
        else:
            time_range = "night"
        
        return f"{day_of_week}, {time_range}"
    
    def apply_k_anonymity(self, users: List[Dict[str, Any]], k: int, attribute_getter=None):
        """
        Apply k-anonymity to a list of users by grouping similar attribute values.
        
        Args:
            users: List of user data
            k: Anonymity parameter
            attribute_getter: Function to extract attribute from user data
            
        Returns:
            K-anonymized user data
        """
        if attribute_getter is None:
            attribute_getter = lambda u: u.get("demographics", {}).get("location")
        
        groups = {}
        
        # Group users by attribute value
        for user in users:
            attr_value = attribute_getter(user)
            if attr_value not in groups:
                groups[attr_value] = []
            groups[attr_value].append(user)
        
        # Process each group
        anonymized_users = []
        
        for attr_value, group in groups.items():
            if len(group) >= k:
                # Group is large enough - add users normally
                anonymized_users.extend([self.anonymize_user(u) for u in group])
            else:
                # Group is too small - suppress or generalize
                for user in group:
                    anon_user = self.anonymize_user(user)
                    
                    # Generalize the attribute
                    if isinstance(attr_value, str) and attr_value:
                        # For strings, suppress most characters
                        generic_value = f"{attr_value[0]}***"
                        anon_user["generalized_demographics"]["region"] = "generalized"
                    else:
                        anon_user["generalized_demographics"]["region"] = "generalized"
                    
                    anonymized_users.append(anon_user)
        
        return anonymized_users
    
    def create_anonymized_dataset(self, users: Dict[str, Any], chats: Dict[str, Any], 
                                  messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a complete anonymized dataset for research purposes.
        
        Args:
            users: Original user data
            chats: Original chat data
            messages: Original message data
            
        Returns:
            Anonymized research dataset
        """
        anonymized_users = [self.anonymize_user(u) for u in users.values()]
        anonymized_messages = [self.anonymize_message(m) for m in messages]
        
        # Create value frequency analysis without identifying individuals
        value_frequencies = {}
        for message in anonymized_messages:
            for value in message.get("extracted_values", []):
                if value:
                    value_frequencies[value] = value_frequencies.get(value, 0) + 1
        
        return {
            "metadata": {
                "user_count": len(anonymized_users),
                "chat_count": len(chats),
                "message_count": len(anonymized_messages),
                "date_range": {
                    "start": self.generalize_timestamp(datetime.now() - timedelta(days=30)),
                    "end": self.generalize_timestamp(datetime.now()),
                }
            },
            "value_frequencies": value_frequencies,
            "anonymized_users": anonymized_users,
            "anonymized_messages": anonymized_messages,
        }

# Example usage
if __name__ == "__main__":
    anonymizer = Anonymizer()
    
    # Example user data
    user_data = {
        "id": 123,
        "username": "johndoe",
        "demographics": {
            "age": 34,
            "location": "San Francisco"
        },
        "chats": [1, 2, 3],
        "values": ["privacy", "honesty"]
    }
    
    # Example message data
    message_data = {
        "id": 456,
        "chat_id": 2,
        "sender_id": 123,
        "content": "I think privacy is really important.",
        "timestamp": datetime.now(),
        "extracted_values": ["privacy", "honesty"]
    }
    
    # Anonymize examples
    anon_user = anonymizer.anonymize_user(user_data)
    anon_message = anonymizer.anonymize_message(message_data)
    
    print("Anonymized user:")
    print(anon_user)
    print("\nAnonymized message:")
    print(anon_message)
