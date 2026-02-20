"""Core script generation logic."""

from typing import Optional, List
from .ai_client import OllamaClient
from .script_formatter import ScriptFormatter
from .utils import calculate_target_characters, count_characters


class ScriptGenerator:
    """Orchestrates script generation process."""
    
    def __init__(self, ollama_client: OllamaClient):
        """
        Initialize script generator.
        
        Args:
            ollama_client: Ollama client instance
        """
        self.client = ollama_client
    
    def generate(self, idea: str, keywords: str = "", video_length_minutes: float = 1.0,
                 tone: str = "Professional", language: str = "English", model: str = "llama3",
                 include_images: bool = False, image_type: str = "descriptions") -> dict:
        """
        Generate a complete video script.
        
        Args:
            idea: Finalized idea/topic
            keywords: Additional keywords or points
            video_length_minutes: Target video length in minutes
            tone: Script tone (Professional, Casual, Educational)
            model: Ollama model to use
            include_images: Whether to include image descriptions/prompts
            image_type: Type of image content ("descriptions", "AI prompts", or "both")
        
        Returns:
            Dictionary with script, character counts, and metadata
        """
        # Calculate target character count
        target_chars = calculate_target_characters(video_length_minutes)
        
        # Generate script using AI
        raw_script = self.client.generate_script(
            idea=idea,
            keywords=keywords,
            target_length_chars=target_chars,
            tone=tone,
            language=language,
            model=model,
            include_images=include_images,
            image_type=image_type
        )
        
        # Format the script
        formatter = ScriptFormatter(target_chars=target_chars)
        formatted_script = formatter.format_script(raw_script)
        
        # Validate length
        is_valid, actual_chars, target = formatter.validate_length(formatted_script)
        
        return {
            "script": formatted_script,
            "actual_chars": actual_chars,
            "target_chars": target,
            "is_valid_length": is_valid,
            "video_length_minutes": video_length_minutes,
            "idea": idea,
            "tone": tone
        }
    
    def generate_series(self, idea: str, num_episodes: int, keywords: str = "",
                       video_length_minutes: float = 1.0, tone: str = "Professional",
                       language: str = "English", model: str = "llama3", include_images: bool = False,
                       image_type: str = "descriptions") -> List[dict]:
        """
        Generate a series of related video scripts.
        
        Args:
            idea: Main topic/idea for the series
            num_episodes: Number of episodes to generate
            keywords: Additional keywords or points
            video_length_minutes: Target video length per episode
            tone: Script tone
            model: Ollama model to use
            include_images: Whether to include image descriptions
            image_type: Type of image content
        
        Returns:
            List of dictionaries, each containing an episode script and metadata
        """
        target_chars = calculate_target_characters(video_length_minutes)
        episodes = []
        previous_summaries = []
        
        for episode_num in range(1, num_episodes + 1):
            # Create summary of previous episodes
            previous_summary = ""
            if previous_summaries:
                previous_summary = "\n".join([f"Episode {i+1}: {summary}" for i, summary in enumerate(previous_summaries)])
            
            # Generate script for this episode
            raw_script = self.client.generate_series_script(
                idea=idea,
                episode_number=episode_num,
                total_episodes=num_episodes,
                previous_episodes_summary=previous_summary,
                keywords=keywords,
                target_length_chars=target_chars,
                tone=tone,
                model=model,
                include_images=include_images,
                image_type=image_type
            )
            
            # Format the script
            formatter = ScriptFormatter(target_chars=target_chars)
            formatted_script = formatter.format_script(raw_script)
            
            # Validate length
            is_valid, actual_chars, target = formatter.validate_length(formatted_script)
            
            # Create a simple summary for next episodes
            # Extract first paragraph as summary
            lines = formatted_script.split('\n')
            summary = ""
            for line in lines:
                if line.strip() and not line.strip().startswith('🎣') and not line.strip().startswith('📝'):
                    summary = line.strip()[:100]  # First 100 chars
                    break
            
            previous_summaries.append(summary if summary else f"Episode {episode_num} content")
            
            episodes.append({
                "episode_number": episode_num,
                "script": formatted_script,
                "actual_chars": actual_chars,
                "target_chars": target,
                "is_valid_length": is_valid,
                "video_length_minutes": video_length_minutes,
                "idea": idea,
                "tone": tone
            })
        
        return episodes