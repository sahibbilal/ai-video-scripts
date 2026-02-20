"""Utility functions for character counting, file operations, and validation."""

import os
from datetime import datetime
from pathlib import Path


# Speaking pace configuration
SPEAKING_PACE_SLOW = 600  # characters per minute
SPEAKING_PACE_AVERAGE = 750  # characters per minute
SPEAKING_PACE_FAST = 900  # characters per minute

# Default speaking pace
DEFAULT_SPEAKING_PACE = SPEAKING_PACE_SLOW


def calculate_target_characters(minutes: float, pace: int = DEFAULT_SPEAKING_PACE) -> int:
    """
    Calculate target character count for a video of given length.
    
    Args:
        minutes: Target video length in minutes
        pace: Characters per minute (default: slow pace)
    
    Returns:
        Target character count
    """
    return int(minutes * pace)


def count_characters(text: str) -> int:
    """Count characters in text (excluding newlines for display purposes)."""
    return len(text.replace('\n', ' ').replace('\r', ''))


def generate_filename(idea: str = "script", extension: str = "txt") -> str:
    """
    Generate a filename with timestamp.
    
    Args:
        idea: Base name for the file (will be sanitized)
        extension: File extension
    
    Returns:
        Generated filename
    """
    # Sanitize idea name for filename
    safe_name = "".join(c for c in idea if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_name = safe_name.replace(' ', '_')[:50]  # Limit length
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe_name}_{timestamp}.{extension}"


def save_script(content: str, filename: str = None, output_dir: str = "output", idea: str = None) -> str:
    """
    Save script content to a file.
    
    Args:
        content: Script content to save
        filename: Optional filename (will generate if not provided)
        output_dir: Directory to save the file
        idea: Optional idea/topic name for filename generation
    
    Returns:
        Path to saved file
    """
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        base_name = idea if idea else "script"
        filename = generate_filename(base_name)
    
    # Ensure filename has .txt extension
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    # Save file
    file_path = output_path / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(file_path)


def validate_video_length(minutes: float) -> bool:
    """Validate that video length is positive and reasonable."""
    return 0.1 <= minutes <= 60.0


def validate_model_name(model: str) -> bool:
    """Validate that model name is not empty."""
    return bool(model and model.strip())


def manage_conversation_history(history: list, user_message: str, ai_response: str, max_history: int = 10) -> list:
    """
    Manage conversation history, keeping only recent messages.
    
    Args:
        history: Current conversation history
        user_message: New user message
        ai_response: New AI response
        max_history: Maximum number of message pairs to keep
    
    Returns:
        Updated conversation history
    """
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ai_response})
    
    # Keep only recent history
    if len(history) > max_history * 2:
        history = history[-max_history * 2:]
    
    return history
