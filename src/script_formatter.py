"""Module for formatting and structuring scripts."""

from typing import Optional, Tuple
from .utils import count_characters, DEFAULT_SPEAKING_PACE


class ScriptFormatter:
    """Formats and structures AI-generated scripts."""
    
    def __init__(self, target_chars: int = 600):
        """
        Initialize script formatter.
        
        Args:
            target_chars: Target character count
        """
        self.target_chars = target_chars
    
    def format_script(self, raw_script: str) -> str:
        """
        Format raw AI output into simple, easy-to-read script.
        
        Args:
            raw_script: Raw script text from AI
        
        Returns:
            Formatted script string
        """
        # Clean up the script
        script = raw_script.strip()
        
        # Enhance section markers for better visibility
        script = self._enhance_simple_format(script)
        
        # Add spacing for readability
        script = self._add_spacing(script)
        
        return script
    
    def _enhance_simple_format(self, script: str) -> str:
        """Enhance the simple format markers for better visibility."""
        lines = script.split('\n')
        formatted_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # Make section markers more prominent
            if '🎣' in line or 'START WITH THIS HOOK' in line.upper() or 'HOOK' in line.upper():
                if not line_stripped.startswith('🎣'):
                    formatted_lines.append("")
                    formatted_lines.append("🎣 START WITH THIS HOOK (read this first):")
                    formatted_lines.append("=" * 60)
                else:
                    formatted_lines.append(line)
                    if '=' not in line:
                        formatted_lines.append("=" * 60)
            elif '📝' in line or 'NOW READ THESE' in line.upper() or 'PARAGRAPHS' in line.upper():
                if not line_stripped.startswith('📝'):
                    formatted_lines.append("")
                    formatted_lines.append("📝 NOW READ THESE PARAGRAPHS (read one by one):")
                    formatted_lines.append("-" * 60)
                else:
                    formatted_lines.append(line)
                    if '-' not in line:
                        formatted_lines.append("-" * 60)
            elif '✅' in line or 'END WITH THIS' in line.upper() or 'WRAP UP' in line.upper():
                if not line_stripped.startswith('✅'):
                    formatted_lines.append("")
                    formatted_lines.append("✅ END WITH THIS (read this to wrap up):")
                    formatted_lines.append("=" * 60)
                else:
                    formatted_lines.append(line)
                    if '=' not in line:
                        formatted_lines.append("=" * 60)
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def validate_length(self, script: str, tolerance: float = 0.2) -> Tuple[bool, int, int]:
        """
        Validate script length against target.
        
        Args:
            script: Script text to validate
            tolerance: Acceptable deviation (20% by default)
        
        Returns:
            Tuple of (is_valid, actual_chars, target_chars)
        """
        actual_chars = count_characters(script)
        min_chars = int(self.target_chars * (1 - tolerance))
        max_chars = int(self.target_chars * (1 + tolerance))
        
        is_valid = min_chars <= actual_chars <= max_chars
        
        return (is_valid, actual_chars, self.target_chars)
    
    def _ensure_sections(self, script: str) -> str:
        """Ensure script has proper section headers."""
        sections = ["HOOK", "INTRODUCTION", "KEY POINTS", "CONCLUSION", "CALL-TO-ACTION"]
        
        # Check if sections are already present
        script_upper = script.upper()
        has_sections = any(section in script_upper for section in sections)
        
        if has_sections:
            return script
        
        # If no sections found, try to add them (basic implementation)
        # This is a fallback - ideally AI should format correctly
        lines = script.split('\n')
        formatted_lines = []
        
        # Simple heuristic: if script doesn't have clear sections, return as-is
        # The AI prompt should handle formatting
        return script
    
    def _add_spacing(self, script: str) -> str:
        """Add proper spacing between sections for readability."""
        lines = script.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Skip empty lines at the start
            if not line_stripped and not formatted_lines:
                continue
            
            # Check if this is a section marker
            is_section_marker = any(marker in line for marker in ['🎣', '📝', '✅']) or \
                               any(marker in line.upper() for marker in ['START WITH', 'NOW READ', 'END WITH'])
            
            # Add spacing before section markers
            if is_section_marker and formatted_lines and formatted_lines[-1].strip():
                formatted_lines.append("")
            
            formatted_lines.append(line)
            
            # Add spacing after section markers (but before content)
            if is_section_marker and i < len(lines) - 1:
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                if next_line and not any(marker in next_line for marker in ['🎣', '📝', '✅', '=', '-']):
                    formatted_lines.append("")
        
        return '\n'.join(formatted_lines)
    
    def adjust_length(self, script: str) -> str:
        """
        Attempt to adjust script length to match target.
        This is a basic implementation - full adjustment would require AI regeneration.
        
        Args:
            script: Script to adjust
        
        Returns:
            Adjusted script (may be unchanged if adjustment not possible)
        """
        actual_chars = count_characters(script)
        
        # If within 20% tolerance, return as-is
        if abs(actual_chars - self.target_chars) / self.target_chars <= 0.2:
            return script
        
        # For now, just return the script with a note
        # Full implementation would require AI to regenerate with adjusted length
        return script
