"""Module for generating trending topic ideas."""

from typing import List
from .ai_client import OllamaClient


class IdeaGenerator:
    """Generates trending video topic ideas using Ollama."""
    
    def __init__(self, ollama_client: OllamaClient):
        """
        Initialize idea generator.
        
        Args:
            ollama_client: Ollama client instance
        """
        self.client = ollama_client
    
    def generate_ideas(self, category: str = "Any", model: str = "llama3") -> List[str]:
        """
        Generate multiple trending topic ideas.
        
        Args:
            category: Topic category (AI, WordPress, Robotics, General Tech, Any)
            model: Ollama model to use
        
        Returns:
            List of idea strings (3-5 ideas)
        """
        try:
            ideas = self.client.generate_ideas(category=category, model=model)
            return ideas if ideas else []
        except Exception as e:
            raise Exception(f"Failed to generate ideas: {str(e)}")
