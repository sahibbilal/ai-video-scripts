"""Ollama AI client for generating ideas, discussions, and scripts."""

import ollama
from typing import List, Dict, Optional


class OllamaClient:
    """Client for interacting with Ollama models."""
    
    def __init__(self, host: str = "http://localhost:11434"):
        """
        Initialize Ollama client.
        
        Args:
            host: Ollama server host URL
        """
        self.host = host
        try:
            self.client = ollama.Client(host=host)
        except Exception:
            # Fallback if Client initialization fails
            self.client = None
    
    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            if self.client is None:
                self.client = ollama.Client(host=self.host)
            self.client.list()
            return True
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Ollama models.
        
        Returns:
            List of model names
        """
        try:
            if self.client is None:
                self.client = ollama.Client(host=self.host)
            response = self.client.list()
            if isinstance(response, dict) and 'models' in response:
                return [model['name'] for model in response['models']]
            elif isinstance(response, list):
                return [model['name'] for model in response]
            return []
        except Exception:
            return []
    
    def generate_ideas(self, category: str = "Any", model: str = "llama3") -> List[str]:
        """
        Generate trending topic ideas for video creation.
        
        Args:
            category: Topic category (AI, WordPress, Robotics, General Tech, Any)
            model: Ollama model to use
        
        Returns:
            List of idea strings
        """
        prompt = f"""Generate 5 trending video topic ideas for today related to {category}.
Each idea should be:
- Current and relevant
- Engaging for viewers
- Suitable for a 1-5 minute video
- Include a brief one-sentence description

Format each idea as:
1. [Title] - [Brief description]
2. [Title] - [Brief description]
...

Focus on the latest trends and developments in {category}."""

        try:
            if self.client is None:
                self.client = ollama.Client(host=self.host)
            
            response = self.client.generate(
                model=model,
                prompt=prompt,
                stream=False
            )
            
            # Parse response into list of ideas
            if isinstance(response, dict):
                ideas_text = response.get('response', '')
            else:
                ideas_text = str(response)
            ideas = self._parse_ideas(ideas_text)
            return ideas[:5]  # Return up to 5 ideas
            
        except Exception as e:
            raise Exception(f"Failed to generate ideas: {str(e)}")
    
    def discuss_idea(self, idea: str, user_question: str, conversation_history: List[Dict], 
                     model: str = "llama3") -> str:
        """
        Discuss and refine an idea through conversation.
        
        Args:
            idea: The original idea being discussed
            user_question: User's question or refinement request
            conversation_history: Previous conversation messages
            model: Ollama model to use
        
        Returns:
            AI response string
        """
        # Build context from conversation history
        context = f"Original idea: {idea}\n\n"
        
        if conversation_history:
            context += "Previous conversation:\n"
            for msg in conversation_history[-6:]:  # Last 3 exchanges
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                context += f"{role.capitalize()}: {content}\n"
        
        context += f"\nUser: {user_question}\nAssistant:"
        
        prompt = f"""You are helping refine a video script idea. The user wants to discuss and improve their idea.

{context}

Provide a helpful, constructive response that:
- Answers their question
- Suggests improvements if relevant
- Helps clarify or expand the idea
- Maintains a conversational, friendly tone"""

        try:
            if self.client is None:
                self.client = ollama.Client(host=self.host)
            
            response = self.client.generate(
                model=model,
                prompt=prompt,
                stream=False
            )
            
            if isinstance(response, dict):
                return response.get('response', 'I apologize, but I encountered an error processing your request.')
            else:
                return str(response)
            
        except Exception as e:
            raise Exception(f"Failed to discuss idea: {str(e)}")
    
    def generate_script(self, idea: str, keywords: str = "", target_length_chars: int = 600,
                       tone: str = "Professional", language: str = "English", model: str = "llama3", 
                       include_images: bool = False, image_type: str = "descriptions") -> str:
        """
        Generate a complete video script.
        
        Args:
            idea: The finalized idea/topic
            keywords: Additional keywords or points to include
            target_length_chars: Target character count for the script
            tone: Script tone (Professional, Casual, Educational)
            model: Ollama model to use
        
        Returns:
            Generated script text
        """
        keywords_text = f"\nAdditional keywords/points to include: {keywords}" if keywords else ""
        
        # Language instruction
        language_instruction = ""
        if language and language != "English":
            language_instruction = f"\n\nLANGUAGE REQUIREMENT: Write the ENTIRE script in {language} language. "
            if language == "Urdu":
                language_instruction += "Use Urdu script (اردو) and write naturally in Urdu. "
            language_instruction += f"All text including hook, paragraphs, and call-to-action must be in {language}."
        
        # Image-related instructions
        image_instructions = ""
        if include_images:
            if image_type == "descriptions":
                image_instructions = """

📸 IMAGE REQUIREMENTS:
- For each paragraph, add a note in brackets [SHOW: description of image to display]
- Describe what image/visual should appear on screen while reading that part
- Make image descriptions clear and specific
- Example: [SHOW: screenshot of WordPress dashboard] or [SHOW: diagram showing AI workflow]"""
            elif image_type == "AI prompts":
                image_instructions = """

📸 AI IMAGE PROMPTS:
- For each paragraph, add an AI image generation prompt in brackets [IMAGE PROMPT: detailed prompt for AI image generator]
- Create detailed prompts that can be used with DALL-E, Midjourney, Stable Diffusion, etc.
- Include style, colors, composition details
- Example: [IMAGE PROMPT: modern WordPress dashboard interface, clean design, blue and white colors, professional screenshot style]"""
            else:  # both
                image_instructions = """

📸 IMAGE REQUIREMENTS:
- For each paragraph, add BOTH:
  1. [SHOW: description of image to display] - what visual to show
  2. [IMAGE PROMPT: detailed AI prompt] - prompt to generate the image with AI
- Make both clear and specific
- Help the creator know exactly what images to use or create"""
        
        prompt = f"""Create a simple, easy-to-read video script for someone just starting to record videos.

Topic: {idea}
{keywords_text}

Target length: Approximately {target_length_chars} characters (for a {target_length_chars // 600:.1f} minute video)
Tone: {tone}
Language: {language}{language_instruction}
{image_instructions}

IMPORTANT: This is for a beginner content creator. Make it simple and easy to read aloud.

Format the script EXACTLY like this:

🎣 START WITH THIS HOOK (read this first to grab attention):
[Write 2-3 sentences that grab attention - make it engaging and make people want to watch]{' [SHOW: description of opening image]' if include_images else ''}

📝 NOW READ THESE PARAGRAPHS (read them one by one):
[Write 2-3 simple paragraphs explaining the main content. Each paragraph should be 3-4 sentences. Make them conversational and easy to read aloud. Break into natural speaking points.]{' Add image descriptions/prompts in brackets after each paragraph as specified above.' if include_images else ''}

✅ END WITH THIS (read this to wrap up):
[Write 1-2 sentences summarizing the main point, then ask viewers to like and subscribe]{' [SHOW: closing image or subscribe button graphic]' if include_images else ''}

Keep it simple! Write in natural, conversational language. No complex words. Just simple sentences that flow when spoken. Make it feel like you're talking to a friend. The total script should be approximately {target_length_chars} characters."""

        try:
            if self.client is None:
                self.client = ollama.Client(host=self.host)
            
            # Increase timeout for non-English languages (they take longer to generate)
            # Use longer timeout for Urdu and other non-Latin scripts
            timeout_seconds = 300 if language != "English" else 180
            
            response = self.client.generate(
                model=model,
                prompt=prompt,
                stream=False
            )
            
            if isinstance(response, dict):
                return response.get('response', '')
            else:
                return str(response)
            
        except Exception as e:
            error_msg = str(e)
            if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                raise Exception(f"Script generation timed out. Non-English languages (like Urdu) can take longer. Please try again or use a faster model. Original error: {error_msg}")
            raise Exception(f"Failed to generate script: {error_msg}")
    
    def generate_series_script(self, idea: str, episode_number: int, total_episodes: int,
                               previous_episodes_summary: str = "", keywords: str = "",
                               target_length_chars: int = 600, tone: str = "Professional",
                               model: str = "llama3", include_images: bool = False,
                               image_type: str = "descriptions") -> str:
        """
        Generate a script for a specific episode in a series.
        
        Args:
            idea: The main topic/idea for the series
            episode_number: Current episode number (1, 2, 3, etc.)
            total_episodes: Total number of episodes in the series
            previous_episodes_summary: Summary of what was covered in previous episodes
            keywords: Additional keywords or points
            target_length_chars: Target character count
            tone: Script tone
            model: Ollama model to use
            include_images: Whether to include image descriptions
            image_type: Type of image content
        
        Returns:
            Generated script text for this episode
        """
        keywords_text = f"\nAdditional keywords/points to include: {keywords}" if keywords else ""
        
        previous_context = ""
        if previous_episodes_summary:
            previous_context = f"\n\nPrevious Episodes Summary:\n{previous_episodes_summary}\n\nIMPORTANT: This is Episode {episode_number}. Build on previous episodes but don't repeat everything. Focus on new content that continues the series."
        else:
            previous_context = f"\n\nThis is Episode {episode_number} of {total_episodes}. Make it a complete standalone video that's part of a series about: {idea}"
        
        # Language instruction
        language_instruction = ""
        if language and language != "English":
            language_instruction = f"\n\nLANGUAGE REQUIREMENT: Write the ENTIRE script in {language} language. "
            if language == "Urdu":
                language_instruction += "Use Urdu script (اردو) and write naturally in Urdu. "
            language_instruction += f"All text including hook, paragraphs, and call-to-action must be in {language}."
        
        # Image-related instructions
        image_instructions = ""
        if include_images:
            if image_type == "descriptions":
                image_instructions = """

📸 IMAGE REQUIREMENTS:
- For each paragraph, add a note in brackets [SHOW: description of image to display]
- Describe what image/visual should appear on screen while reading that part
- Make image descriptions clear and specific"""
            elif image_type == "AI prompts":
                image_instructions = """

📸 AI IMAGE PROMPTS:
- For each paragraph, add an AI image generation prompt in brackets [IMAGE PROMPT: detailed prompt for AI image generator]
- Create detailed prompts that can be used with DALL-E, Midjourney, Stable Diffusion, etc."""
            else:  # both
                image_instructions = """

📸 IMAGE REQUIREMENTS:
- For each paragraph, add BOTH:
  1. [SHOW: description of image to display]
  2. [IMAGE PROMPT: detailed AI prompt]"""
        
        prompt = f"""Create Episode {episode_number} of a {total_episodes}-part video series for someone just starting to record videos.

Main Series Topic: {idea}
{keywords_text}
{previous_context}

Target length: Approximately {target_length_chars} characters (for a {target_length_chars // 600:.1f} minute video)
Tone: {tone}
Language: {language}{language_instruction}
{image_instructions}

IMPORTANT: 
- This is for a beginner content creator. Make it simple and easy to read aloud.
- This is Episode {episode_number} of {total_episodes} - make it clear this is part of a series
- If this is not Episode 1, briefly reference previous episodes but focus on new content
- Each episode should be valuable on its own but also part of the larger series

Format the script EXACTLY like this:

🎣 START WITH THIS HOOK (read this first):
[Write 2-3 sentences that grab attention. Mention this is Episode {episode_number} of the series about {idea}. Make it engaging and make people want to watch]{' [SHOW: series episode number graphic]' if include_images else ''}

📝 NOW READ THESE PARAGRAPHS (read them one by one):
[Write 2-3 simple paragraphs explaining the content for THIS episode. Each paragraph should be 3-4 sentences. Make them conversational and easy to read aloud. Break into natural speaking points.]{' Add image descriptions/prompts in brackets after each paragraph as specified above.' if include_images else ''}

✅ END WITH THIS (read this to wrap up):
[Write 1-2 sentences summarizing this episode's main point. Then mention what's coming in the next episode (if not the last episode) or wrap up the series (if this is the last episode). Ask viewers to like and subscribe.]{' [SHOW: next episode preview or series completion graphic]' if include_images else ''}

Keep it simple! Write in natural, conversational language. No complex words. Just simple sentences that flow when spoken. Make it feel like you're talking to a friend. The total script should be approximately {target_length_chars} characters."""

        try:
            if self.client is None:
                self.client = ollama.Client(host=self.host)
            
            # Increase timeout for non-English languages
            timeout_seconds = 300 if language != "English" else 180
            
            response = self.client.generate(
                model=model,
                prompt=prompt,
                stream=False
            )
            
            if isinstance(response, dict):
                return response.get('response', '')
            else:
                return str(response)
            
        except Exception as e:
            error_msg = str(e)
            if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
                raise Exception(f"Series script generation timed out. Non-English languages (like Urdu) can take longer. Please try again or use a faster model. Original error: {error_msg}")
            raise Exception(f"Failed to generate series script: {error_msg}")
    
    def _parse_ideas(self, ideas_text: str) -> List[str]:
        """
        Parse ideas from AI response text.
        
        Args:
            ideas_text: Raw response text from AI
        
        Returns:
            List of parsed idea strings
        """
        ideas = []
        lines = ideas_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Remove numbering if present
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove leading number, dash, or bullet
                line = line.lstrip('0123456789.-) ')
            
            if line and len(line) > 10:  # Filter out very short lines
                ideas.append(line)
        
        # If parsing didn't work well, return the original text split by lines
        if not ideas:
            ideas = [line.strip() for line in lines if line.strip() and len(line.strip()) > 10]
        
        return ideas[:5]  # Return up to 5 ideas
