"""
Core value extraction implementation based on the Values in the Wild paper methodology.
"""
import re
import json
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

class ValueExtractor:
    """
    Extracts values from conversation text using both rule-based and embedding-based approaches.
    
    Implements methodologies from the Values in the Wild paper for identifying value
    expressions in AI assistant conversations.
    """
    
    def __init__(self, values_taxonomy_path: str = None, model_name: str = "all-mpnet-base-v2"):
        """
        Initialize the value extractor with a taxonomy and embedding model.
        
        Args:
            values_taxonomy_path: Path to the values taxonomy JSON file
            model_name: Name of the sentence transformer model to use
        """
        self.values_taxonomy = self._load_taxonomy(values_taxonomy_path)
        self.model = None  # Lazy-load embedding model
        self.model_name = model_name
    
    def _load_taxonomy(self, taxonomy_path: Optional[str]) -> Dict:
        """Load the values taxonomy from a JSON file or use the default taxonomy."""
        if taxonomy_path and Path(taxonomy_path).exists():
            with open(taxonomy_path, 'r') as f:
                return json.load(f)
        else:
            # Default to empty taxonomy that will be populated during extraction
            return {
                "practical_values": {},
                "epistemic_values": {},
                "social_values": {},
                "protective_values": {},
                "personal_values": {}
            }
    
    def _load_model(self):
        """Lazy-load the sentence transformer model."""
        if self.model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self.model = SentenceTransformer(self.model_name)
            except ImportError:
                raise ImportError(
                    "sentence-transformers is required for embedding-based extraction. "
                    "Install with 'pip install sentence-transformers'."
                )
    
    def extract_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract values from a text string.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of extracted values with metadata
        """
        # Implementation will be expanded based on the paper's methodology
        # This is a placeholder for the actual extraction logic
        extracted_values = []
        
        # Example extraction logic - to be replaced with actual implementation
        if "helpfulness" in text.lower():
            extracted_values.append({"value": "helpfulness", "category": "practical_values"})
        
        if "transparency" in text.lower():
            extracted_values.append({"value": "transparency", "category": "epistemic_values"})
        
        return extracted_values
    
    def extract_from_conversation(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Extract values from a conversation transcript.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            
        Returns:
            List of extracted values with metadata including message index
        """
        all_values = []
        
        for i, message in enumerate(messages):
            if message.get('role') == 'assistant':
                values = self.extract_from_text(message.get('content', ''))
                for value in values:
                    value['message_index'] = i
                all_values.extend(values)
        
        return all_values


# Example usage
if __name__ == "__main__":
    extractor = ValueExtractor()
    sample_text = "I'm here to help you understand this concept with clarity and transparency."
    values = extractor.extract_from_text(sample_text)
    print(f"Extracted values: {values}")
