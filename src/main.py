"""Main GUI application for Video Script Generator Bot."""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from typing import Optional, List, Dict

from .ai_client import OllamaClient
from .idea_generator import IdeaGenerator
from .script_generator import ScriptGenerator
from .utils import save_script, validate_video_length, manage_conversation_history, count_characters


class VideoScriptGeneratorApp:
    """Main application window."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("Video Script Generator Bot - Professional Edition")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f5f5f5")
        
        # Color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'accent': '#9b59b6',
            'bg': '#ffffff',
            'bg_light': '#f8f9fa',
            'border': '#dee2e6'
        }
        
        # Initialize Ollama client
        self.ollama_client = OllamaClient()
        self.idea_generator = IdeaGenerator(self.ollama_client)
        self.script_generator = ScriptGenerator(self.ollama_client)
        
        # Application state
        self.selected_idea: Optional[str] = None
        self.finalized_idea: Optional[str] = None
        self.conversation_history: List[Dict] = []
        self.current_script: Optional[str] = None
        
        # Configure styles
        self.configure_styles()
        
        # Create UI
        self.create_ui()
        
        # Check Ollama connection on startup
        self.check_ollama_connection()
    
    def configure_styles(self):
        """Configure ttk styles for a professional look."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure Notebook style
        style.configure('TNotebook', background=self.colors['bg_light'], borderwidth=0)
        # Make all tabs the same height - use consistent padding
        style.configure('TNotebook.Tab', 
                       padding=[20, 12],
                       font=('Segoe UI', 10, 'bold'),
                       background=self.colors['bg'],
                       foreground=self.colors['dark'],
                       borderwidth=0)
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                            ('active', self.colors['secondary']),
                            ('!selected', self.colors['bg'])],
                 foreground=[('selected', 'white'),
                            ('active', 'white'),
                            ('!selected', self.colors['dark'])],
                 expand=[('selected', [1, 1, 1, 0])])  # Prevent expansion on selected tab
        
        # Configure Combobox style
        style.configure('TCombobox', 
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid',
                       padding=5)
        
        # Configure Button style
        style.configure('Action.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
    
    def create_ui(self):
        """Create the user interface."""
        # Header section
        self.create_header()
        
        # Status bar
        self.create_status_bar()
        
        # Main content area with tabs
        self.create_main_content()
    
    def create_header(self):
        """Create professional header section."""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🎬 Video Script Generator",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            anchor='w'
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="AI-Powered Script Creation Tool",
            font=('Segoe UI', 11),
            bg=self.colors['primary'],
            fg='#bdc3c7',
            anchor='w'
        )
        subtitle_label.pack(side=tk.LEFT, padx=10, pady=20)
    
    def create_status_bar(self):
        """Create professional status bar."""
        status_frame = tk.Frame(self.root, bg=self.colors['dark'], height=40)
        status_frame.pack(fill=tk.X, padx=0, pady=0)
        status_frame.pack_propagate(False)
        
        # Status indicator
        self.status_indicator = tk.Label(
            status_frame,
            text="●",
            font=('Segoe UI', 12),
            bg=self.colors['dark'],
            fg='#95a5a6'
        )
        self.status_indicator.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Checking Ollama connection...",
            font=('Segoe UI', 9),
            bg=self.colors['dark'],
            fg='white',
            anchor='w'
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Spacer
        tk.Label(status_frame, bg=self.colors['dark'], width=1).pack(side=tk.RIGHT, padx=15)
    
    def create_main_content(self):
        """Create main content area with tabs."""
        # Container for tabs with padding
        content_container = tk.Frame(self.root, bg=self.colors['bg_light'])
        content_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_idea_tab()
        self.create_discussion_tab()
        self.create_script_tab()
    
    def create_idea_tab(self):
        """Create the Idea Generation tab."""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="  💡 Generate Ideas  ")
        
        # Main container with padding
        main_container = tk.Frame(tab, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Section title
        section_title = tk.Label(
            main_container,
            text="Discover Trending Video Topics",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            anchor='w'
        )
        section_title.pack(fill=tk.X, pady=(0, 20))
        
        # Configuration panel
        config_frame = tk.LabelFrame(
            main_container,
            text="Configuration",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Model selection row
        model_row = tk.Frame(config_frame, bg=self.colors['bg'])
        model_row.pack(fill=tk.X, pady=10)
        
        tk.Label(
            model_row,
            text="Ollama Model:",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.model_var = tk.StringVar(value="llama3")
        self.model_combo = ttk.Combobox(
            model_row,
            textvariable=self.model_var,
            width=35,
            state="readonly",
            font=('Segoe UI', 10)
        )
        self.model_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        self.refresh_models_button = tk.Button(
            model_row,
            text="🔄 Refresh",
            command=self.refresh_models,
            font=('Segoe UI', 9),
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            padx=15,
            pady=5,
            cursor='hand2',
            activebackground='#2980b9',
            activeforeground='white'
        )
        self.refresh_models_button.pack(side=tk.LEFT)
        
        # Category selection row
        category_row = tk.Frame(config_frame, bg=self.colors['bg'])
        category_row.pack(fill=tk.X, pady=10)
        
        tk.Label(
            category_row,
            text="Topic Category:",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            width=15,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.category_var = tk.StringVar(value="Any")
        category_combo = ttk.Combobox(
            category_row,
            textvariable=self.category_var,
            values=["Any", "AI", "WordPress", "Robotics", "General Tech"],
            state="readonly",
            width=35,
            font=('Segoe UI', 10)
        )
        category_combo.pack(side=tk.LEFT)
        
        # Generate button
        generate_button = tk.Button(
            main_container,
            text="✨ Generate Ideas",
            command=self.generate_ideas,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white'
        )
        generate_button.pack(pady=20)
        
        # Ideas display section
        ideas_section = tk.LabelFrame(
            main_container,
            text="Generated Ideas",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        ideas_section.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Ideas listbox with scrollbar
        listbox_frame = tk.Frame(ideas_section, bg=self.colors['bg'])
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.ideas_listbox = tk.Listbox(
            listbox_frame,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['dark'],
            selectbackground=self.colors['secondary'],
            selectforeground='white',
            relief=tk.SOLID,
            borderwidth=1,
            activestyle='none'
        )
        self.ideas_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.ideas_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ideas_listbox.config(yscrollcommand=scrollbar.set)
        
        # Select idea button
        select_button = tk.Button(
            main_container,
            text="➡️ Select Idea & Continue to Discussion",
            command=self.select_idea,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#8e44ad',
            activeforeground='white'
        )
        select_button.pack(pady=10)
    
    def create_discussion_tab(self):
        """Create the Discuss & Refine tab."""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="  💬 Discuss & Refine  ")
        
        # Create scrollable frame
        canvas = tk.Canvas(tab, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas (works on Windows and Mac)
        def _on_mousewheel(event):
            # Windows and Mac
            if hasattr(event, 'delta'):
                if event.delta > 0:
                    canvas.yview_scroll(-1, "units")
                else:
                    canvas.yview_scroll(1, "units")
            # Linux
            elif event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")
        
        # Windows
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)
        
        # Update scroll region when content changes
        def update_scroll_region(event=None):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        scrollable_frame.bind("<Configure>", update_scroll_region)
        tab.bind("<Configure>", update_scroll_region)
        
        # Main container (now inside scrollable frame)
        main_container = scrollable_frame
        
        # Add padding to main container
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Section title
        section_title = tk.Label(
            main_container,
            text="Refine Your Video Idea",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            anchor='w'
        )
        section_title.pack(fill=tk.X, pady=(0, 20))
        
        # Selected idea display
        idea_frame = tk.LabelFrame(
            main_container,
            text="Selected Idea",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        idea_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.selected_idea_label = tk.Label(
            idea_frame,
            text="No idea selected. Please go to 'Generate Ideas' tab first.",
            font=('Segoe UI', 10),
            bg='#e8f4f8',
            fg=self.colors['dark'],
            wraplength=1000,
            justify=tk.LEFT,
            padx=15,
            pady=15,
            relief=tk.FLAT,
            anchor='w'
        )
        self.selected_idea_label.pack(fill=tk.X)
        
        # Discussion section (with fixed height for better layout)
        discussion_section = tk.LabelFrame(
            main_container,
            text="Discussion History",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        discussion_section.pack(fill=tk.X, pady=(0, 20))
        
        self.discussion_text = scrolledtext.ScrolledText(
            discussion_section,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['dark'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=10,
            pady=10,
            height=12  # Fixed number of lines visible
        )
        self.discussion_text.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.discussion_text.config(state=tk.DISABLED)
        
        # Input section
        input_section = tk.LabelFrame(
            main_container,
            text="Your Question or Refinement",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        input_section.pack(fill=tk.X, pady=(0, 20))
        
        self.discussion_entry = tk.Entry(
            input_section,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.SOLID,
            borderwidth=1,
            insertbackground=self.colors['primary']
        )
        self.discussion_entry.pack(fill=tk.X, padx=10, pady=10)
        self.discussion_entry.bind("<Return>", lambda e: self.discuss_idea())
        
        # Buttons row
        buttons_row = tk.Frame(main_container, bg=self.colors['bg'])
        buttons_row.pack(fill=tk.X, pady=10)
        
        discuss_button = tk.Button(
            buttons_row,
            text="💬 Discuss",
            command=self.discuss_idea,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['warning'],
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor='hand2',
            activebackground='#d68910',
            activeforeground='white'
        )
        discuss_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Make finalize button more prominent
        finalize_button = tk.Button(
            buttons_row,
            text="✅ Finalize Idea & Continue to Script Generation",
            command=self.finalize_idea,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground='#8e44ad',
            activeforeground='white',
            borderwidth=2,
            highlightbackground=self.colors['accent'],
            highlightthickness=2
        )
        finalize_button.pack(side=tk.LEFT, padx=(10, 0))
    
    def create_script_tab(self):
        """Create the Generate Script tab."""
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text="  📝 Generate Script  ")
        
        # Bind tab change to update topic entry
        def on_tab_change(event):
            if event.widget.index("current") == 2:  # Script tab is index 2
                self.update_topic_entry()
        
        self.notebook.bind("<<NotebookTabChanged>>", on_tab_change)
        
        # Create two-panel layout: left for inputs (scrollable), right for script preview
        main_panels = tk.PanedWindow(tab, orient=tk.HORIZONTAL, sashwidth=5, bg=self.colors['bg_light'])
        main_panels.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - scrollable input section
        left_panel = tk.Frame(main_panels, bg=self.colors['bg'])
        main_panels.add(left_panel, width=450, minsize=400)
        
        # Create scrollable frame for left panel
        left_canvas = tk.Canvas(left_panel, bg=self.colors['bg'], highlightthickness=0)
        left_scrollbar = tk.Scrollbar(left_panel, orient="vertical", command=left_canvas.yview)
        scrollable_left = tk.Frame(left_canvas, bg=self.colors['bg'])
        
        scrollable_left.bind(
            "<Configure>",
            lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all"))
        )
        
        left_canvas.create_window((0, 0), window=scrollable_left, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel
        def _on_mousewheel_left(event):
            if hasattr(event, 'delta'):
                if event.delta > 0:
                    left_canvas.yview_scroll(-1, "units")
                else:
                    left_canvas.yview_scroll(1, "units")
            elif event.num == 4:
                left_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                left_canvas.yview_scroll(1, "units")
        
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel_left)
        left_canvas.bind_all("<Button-4>", _on_mousewheel_left)
        left_canvas.bind_all("<Button-5>", _on_mousewheel_left)
        
        # Main container (now inside scrollable frame)
        main_container = scrollable_left
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Section title
        section_title = tk.Label(
            main_container,
            text="Create Your Video Script",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            anchor='w'
        )
        section_title.pack(fill=tk.X, pady=(0, 20))
        
        # Topic/Idea input section
        idea_frame = tk.LabelFrame(
            main_container,
            text="Video Topic / Idea",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        idea_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Info label
        info_label = tk.Label(
            idea_frame,
            text="💡 Enter a topic below, or leave empty to use the finalized idea from discussion tab (or generate for any topic).",
            font=('Segoe UI', 9, 'italic'),
            bg='#f4ecf7',
            fg=self.colors['dark'],
            wraplength=1000,
            justify=tk.LEFT,
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        info_label.pack(fill=tk.X, pady=(0, 10))
        
        # Topic input
        self.topic_entry = tk.Entry(
            idea_frame,
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.SOLID,
            borderwidth=1,
            insertbackground=self.colors['primary']
        )
        self.topic_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.topic_entry.insert(0, "")
        
        # Show finalized idea if available (hidden by default)
        self.finalized_idea_label = tk.Label(
            idea_frame,
            text="",
            font=('Segoe UI', 9),
            bg='#e8f5e9',
            fg=self.colors['dark'],
            wraplength=1000,
            justify=tk.LEFT,
            padx=10,
            pady=8,
            relief=tk.FLAT,
            anchor='w'
        )
        # Don't pack initially - will be shown when idea is finalized
        
        # Script parameters
        params_section = tk.LabelFrame(
            main_container,
            text="Script Parameters",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        params_section.pack(fill=tk.X, pady=(0, 20))
        
        # Video length
        length_row = tk.Frame(params_section, bg=self.colors['bg'])
        length_row.pack(fill=tk.X, pady=10)
        
        tk.Label(
            length_row,
            text="Video Length (minutes):",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.length_var = tk.StringVar(value="1.0")
        length_entry = tk.Entry(
            length_row,
            textvariable=self.length_var,
            width=15,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.SOLID,
            borderwidth=1
        )
        length_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        # Character count display
        self.char_count_label = tk.Label(
            length_row,
            text="Target: 600 characters (1 minute)",
            font=('Segoe UI', 9, 'italic'),
            bg=self.colors['bg'],
            fg=self.colors['dark']
        )
        self.char_count_label.pack(side=tk.LEFT)
        
        length_entry.bind("<KeyRelease>", self.update_char_count)
        
        # Tone
        tone_row = tk.Frame(params_section, bg=self.colors['bg'])
        tone_row.pack(fill=tk.X, pady=10)
        
        tk.Label(
            tone_row,
            text="Tone/Style:",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.tone_var = tk.StringVar(value="Professional")
        tone_combo = ttk.Combobox(
            tone_row,
            textvariable=self.tone_var,
            values=["Professional", "Casual", "Educational"],
            state="readonly",
            width=20,
            font=('Segoe UI', 10)
        )
        tone_combo.pack(side=tk.LEFT)
        
        # Include images option
        image_row = tk.Frame(params_section, bg=self.colors['bg'])
        image_row.pack(fill=tk.X, pady=10)
        
        self.include_images_var = tk.BooleanVar(value=False)
        image_checkbox = tk.Checkbutton(
            image_row,
            text="📸 Include image descriptions and visual cues in script",
            variable=self.include_images_var,
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            activebackground=self.colors['bg'],
            activeforeground=self.colors['dark'],
            selectcolor='white',
            cursor='hand2'
        )
        image_checkbox.pack(side=tk.LEFT)
        
        # Image type option (only shown if include_images is checked)
        self.image_type_var = tk.StringVar(value="descriptions")
        self.image_type_combo = ttk.Combobox(
            image_row,
            textvariable=self.image_type_var,
            values=["descriptions", "AI prompts", "both"],
            state="readonly",
            width=15,
            font=('Segoe UI', 9)
        )
        # Initially hidden
        self.image_type_combo.pack_forget()
        
        def toggle_image_options():
            if self.include_images_var.get():
                self.image_type_combo.pack(side=tk.LEFT, padx=(10, 0))
            else:
                self.image_type_combo.pack_forget()
        
        image_checkbox.config(command=toggle_image_options)
        
        # Keywords
        keywords_row = tk.Frame(params_section, bg=self.colors['bg'])
        keywords_row.pack(fill=tk.X, pady=10)
        
        tk.Label(
            keywords_row,
            text="Additional Keywords:",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.keywords_entry = tk.Entry(
            keywords_row,
            width=50,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.SOLID,
            borderwidth=1
        )
        self.keywords_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Generate buttons row
        buttons_row = tk.Frame(main_container, bg=self.colors['bg'])
        buttons_row.pack(pady=20)
        
        generate_script_button = tk.Button(
            buttons_row,
            text="🚀 Generate Script",
            command=self.generate_script,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['success'],
            fg='white',
            relief=tk.FLAT,
            padx=30,
            pady=15,
            cursor='hand2',
            activebackground='#229954',
            activeforeground='white'
        )
        generate_script_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Series generation section
        series_frame = tk.LabelFrame(
            main_container,
            text="📺 Generate Series (Multiple Episodes)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        series_frame.pack(fill=tk.X, pady=(0, 20))
        
        series_info = tk.Label(
            series_frame,
            text="💡 Generate a series of related scripts based on your successful idea. Each episode builds on the previous one.",
            font=('Segoe UI', 9, 'italic'),
            bg='#fff3e0',
            fg=self.colors['dark'],
            wraplength=1000,
            justify=tk.LEFT,
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        series_info.pack(fill=tk.X, pady=(0, 10))
        
        series_params_row = tk.Frame(series_frame, bg=self.colors['bg'])
        series_params_row.pack(fill=tk.X, pady=5)
        
        tk.Label(
            series_params_row,
            text="Number of Episodes:",
            font=('Segoe UI', 10),
            bg=self.colors['bg'],
            fg=self.colors['dark'],
            width=18,
            anchor='w'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.series_episodes_var = tk.StringVar(value="3")
        series_episodes_entry = tk.Entry(
            series_params_row,
            textvariable=self.series_episodes_var,
            width=10,
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['dark'],
            relief=tk.SOLID,
            borderwidth=1
        )
        series_episodes_entry.pack(side=tk.LEFT, padx=(0, 20))
        
        generate_series_button = tk.Button(
            series_params_row,
            text="📺 Generate Series",
            command=self.generate_series,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['accent'],
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=10,
            cursor='hand2',
            activebackground='#8e44ad',
            activeforeground='white'
        )
        generate_series_button.pack(side=tk.LEFT)
        
        # Right panel - Script preview (always visible)
        right_panel = tk.Frame(main_panels, bg=self.colors['bg'])
        main_panels.add(right_panel, width=600, minsize=500)
        
        # Script preview section
        script_section = tk.LabelFrame(
            right_panel,
            text="Generated Script - Simple Format for Easy Reading",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary'],
            padx=20,
            pady=15,
            relief=tk.FLAT,
            borderwidth=1
        )
        script_section.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info label
        info_label = tk.Label(
            script_section,
            text="💡 Tip: The script shows exactly what to read. Start with the hook, then read the paragraphs one by one.",
            font=('Segoe UI', 9, 'italic'),
            bg='#e8f4f8',
            fg=self.colors['dark'],
            wraplength=550,
            justify=tk.LEFT,
            padx=10,
            pady=8,
            relief=tk.FLAT
        )
        info_label.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        self.script_text = scrolledtext.ScrolledText(
            script_section,
            font=('Segoe UI', 11),  # Slightly smaller to fit better
            bg='white',
            fg=self.colors['dark'],
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=1,
            padx=15,
            pady=15,
            spacing1=5,  # Line spacing
            spacing2=3,
            spacing3=5
        )
        self.script_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Save button
        save_button = tk.Button(
            right_panel,
            text="💾 Save Script",
            command=self.save_script,
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['secondary'],
            fg='white',
            relief=tk.FLAT,
            padx=25,
            pady=12,
            cursor='hand2',
            activebackground='#2980b9',
            activeforeground='white'
        )
        save_button.pack(pady=10)
    
    def check_ollama_connection(self):
        """Check if Ollama is running and update status."""
        def check():
            is_connected = self.ollama_client.check_connection()
            if is_connected:
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['success']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✓ Ollama Connected - Ready to generate",
                    fg='white'
                ))
                self.root.after(0, self.refresh_models)
            else:
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['danger']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✗ Ollama Not Connected - Please start Ollama service",
                    fg='#ec7063'
                ))
        
        threading.Thread(target=check, daemon=True).start()
    
    def refresh_models(self):
        """Refresh available Ollama models."""
        def refresh():
            models = self.ollama_client.get_available_models()
            if models:
                self.root.after(0, lambda: self.model_combo.config(values=models))
                if models and self.model_var.get() not in models:
                    self.root.after(0, lambda: self.model_var.set(models[0]))
            else:
                self.root.after(0, lambda: self.model_combo.config(values=["llama3"]))
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def generate_ideas(self):
        """Generate trending topic ideas."""
        category = self.category_var.get()
        model = self.model_var.get()
        
        if not model:
            messagebox.showerror("Error", "Please select an Ollama model.")
            return
        
        # Update status
        self.status_label.config(text="⏳ Generating ideas...", fg='white')
        self.status_indicator.config(fg=self.colors['warning'])
        
        def generate():
            try:
                ideas = self.idea_generator.generate_ideas(category=category, model=model)
                self.root.after(0, lambda: self.display_ideas(ideas))
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['success']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✓ Ideas generated successfully",
                    fg='white'
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate ideas: {str(e)}"))
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['danger']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✗ Error generating ideas",
                    fg='#ec7063'
                ))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def display_ideas(self, ideas: List[str]):
        """Display generated ideas in the listbox."""
        self.ideas_listbox.delete(0, tk.END)
        for idea in ideas:
            self.ideas_listbox.insert(tk.END, idea)
    
    def select_idea(self):
        """Select an idea and move to discussion tab."""
        selection = self.ideas_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an idea from the list.")
            return
        
        self.selected_idea = self.ideas_listbox.get(selection[0])
        self.selected_idea_label.config(
            text=f"💡 {self.selected_idea}",
            bg='#d5e8f3'
        )
        self.conversation_history = []  # Reset conversation
        
        # Clear discussion text
        self.discussion_text.config(state=tk.NORMAL)
        self.discussion_text.delete(1.0, tk.END)
        self.discussion_text.insert(tk.END, "💬 Start discussing your idea below...\n\n")
        self.discussion_text.config(state=tk.DISABLED)
        
        # Switch to discussion tab
        self.notebook.select(1)
    
    def discuss_idea(self):
        """Discuss and refine the selected idea."""
        if not self.selected_idea:
            messagebox.showwarning("Warning", "Please select an idea first.")
            return
        
        user_question = self.discussion_entry.get().strip()
        if not user_question:
            messagebox.showwarning("Warning", "Please enter a question or refinement.")
            return
        
        model = self.model_var.get()
        
        # Add user message to discussion
        self.discussion_text.config(state=tk.NORMAL)
        self.discussion_text.insert(tk.END, f"👤 You: {user_question}\n\n")
        self.discussion_text.config(state=tk.DISABLED)
        self.discussion_text.see(tk.END)
        
        # Clear entry
        self.discussion_entry.delete(0, tk.END)
        
        # Update status
        self.status_label.config(text="⏳ Processing your question...", fg='white')
        self.status_indicator.config(fg=self.colors['warning'])
        
        def discuss():
            try:
                response = self.ollama_client.discuss_idea(
                    idea=self.selected_idea,
                    user_question=user_question,
                    conversation_history=self.conversation_history,
                    model=model
                )
                
                # Update conversation history
                self.conversation_history = manage_conversation_history(
                    self.conversation_history,
                    user_question,
                    response
                )
                
                # Display response
                self.root.after(0, lambda: self.discussion_text.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.discussion_text.insert(tk.END, f"🤖 Assistant: {response}\n\n"))
                self.root.after(0, lambda: self.discussion_text.config(state=tk.DISABLED))
                self.root.after(0, lambda: self.discussion_text.see(tk.END))
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['success']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✓ Discussion complete",
                    fg='white'
                ))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to discuss idea: {str(e)}"))
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['danger']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✗ Error in discussion",
                    fg='#ec7063'
                ))
        
        threading.Thread(target=discuss, daemon=True).start()
    
    def finalize_idea(self):
        """Finalize the idea and move to script generation tab."""
        if not self.selected_idea:
            messagebox.showwarning("Warning", "Please select an idea from the 'Generate Ideas' tab first.")
            return
        
        # Use selected idea if finalized_idea is not set
        if not self.finalized_idea:
            self.finalized_idea = self.selected_idea
        
        # Update the finalized idea label and show it
        self.finalized_idea_label.config(
            text=f"✅ Finalized idea: {self.finalized_idea} (You can edit the topic input above if needed)",
            bg='#d5f4e6'
        )
        self.finalized_idea_label.pack(fill=tk.X, pady=(5, 0))
        
        # Populate topic entry with finalized idea
        if hasattr(self, 'topic_entry'):
            self.topic_entry.delete(0, tk.END)
            self.topic_entry.insert(0, self.finalized_idea)
        
        # Update status
        self.status_label.config(text="✓ Idea finalized - Ready to generate script", fg='white')
        self.status_indicator.config(fg=self.colors['success'])
        
        # Switch to script tab (index 2 is the third tab - Generate Script)
        try:
            # Get the number of tabs
            num_tabs = self.notebook.index("end")
            if num_tabs > 2:
                self.notebook.select(2)  # Index 2 is the third tab (0-indexed)
                self.update_char_count()
            else:
                # Fallback: try to find by text
                for i in range(num_tabs):
                    tab_text = self.notebook.tab(i, "text")
                    if "Script" in tab_text or "Generate" in tab_text:
                        self.notebook.select(i)
                        self.update_char_count()
                        break
        except Exception as e:
            messagebox.showerror("Error", f"Could not switch to script tab. Please manually select the 'Generate Script' tab.\n\nError: {str(e)}")
    
    def update_topic_entry(self):
        """Update topic entry with finalized idea if available."""
        if hasattr(self, 'topic_entry') and self.finalized_idea:
            current_text = self.topic_entry.get().strip()
            # Only update if entry is empty
            if not current_text:
                self.topic_entry.delete(0, tk.END)
                self.topic_entry.insert(0, self.finalized_idea)
    
    def update_char_count(self, event=None):
        """Update character count display based on video length."""
        try:
            minutes = float(self.length_var.get())
            target_chars = int(minutes * 600)  # 600 chars per minute
            minutes_text = f"{minutes} minute{'s' if minutes != 1 else ''}"
            self.char_count_label.config(
                text=f"Target: {target_chars} characters ({minutes_text})",
                fg=self.colors['dark']
            )
        except ValueError:
            pass
    
    def generate_script(self):
        """Generate the video script."""
        try:
            video_length = float(self.length_var.get())
            if not validate_video_length(video_length):
                messagebox.showerror("Error", "Video length must be between 0.1 and 60 minutes.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid video length.")
            return
        
        # Get topic from input box, or use finalized idea, or use "any"
        topic_input = self.topic_entry.get().strip() if hasattr(self, 'topic_entry') else ""
        
        if topic_input:
            # Use the topic from input box
            idea = topic_input
        elif self.finalized_idea:
            # Use finalized idea from discussion
            idea = self.finalized_idea
        else:
            # Generate for any topic
            idea = "any trending topic"
        
        keywords = self.keywords_entry.get()
        tone = self.tone_var.get()
        model = self.model_var.get()
        include_images = self.include_images_var.get() if hasattr(self, 'include_images_var') else False
        image_type = self.image_type_var.get() if hasattr(self, 'image_type_var') else "descriptions"
        
        # Update status
        status_msg = "⏳ Generating script"
        if include_images:
            status_msg += " with image descriptions/prompts"
        status_msg += "... This may take a moment."
        self.status_label.config(text=status_msg, fg='white')
        self.status_indicator.config(fg=self.colors['warning'])
        self.script_text.delete(1.0, tk.END)
        self.script_text.insert(tk.END, "⏳ Generating your script, please wait...\n\nThis process may take 30-60 seconds depending on your model and system.")
        
        def generate():
            try:
                result = self.script_generator.generate(
                    idea=idea,
                    keywords=keywords,
                    video_length_minutes=video_length,
                    tone=tone,
                    model=model,
                    include_images=include_images,
                    image_type=image_type
                )
                
                script = result["script"]
                actual_chars = result["actual_chars"]
                target_chars = result["target_chars"]
                
                # Display script
                self.root.after(0, lambda: self.script_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.script_text.insert(tk.END, script))
                
                # Update character count
                status_text = f"✓ Script generated - {actual_chars}/{target_chars} characters"
                if result["is_valid_length"]:
                    status_text += " (within target range)"
                    status_color = self.colors['success']
                else:
                    status_text += " (outside target range)"
                    status_color = self.colors['warning']
                
                self.root.after(0, lambda: self.status_indicator.config(fg=status_color))
                self.root.after(0, lambda: self.status_label.config(text=status_text, fg='white'))
                self.root.after(0, lambda: self.char_count_label.config(
                    text=f"Target: {target_chars} | Actual: {actual_chars} characters",
                    fg=self.colors['dark']
                ))
                
                self.current_script = script
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate script: {str(e)}"))
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['danger']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✗ Error generating script",
                    fg='#ec7063'
                ))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def generate_series(self):
        """Generate a series of related scripts."""
        # Get topic
        topic_input = self.topic_entry.get().strip() if hasattr(self, 'topic_entry') else ""
        
        if topic_input:
            idea = topic_input
        elif self.finalized_idea:
            idea = self.finalized_idea
        else:
            messagebox.showwarning("Warning", "Please enter a topic or finalize an idea first.")
            return
        
        try:
            num_episodes = int(self.series_episodes_var.get())
            if num_episodes < 2 or num_episodes > 10:
                messagebox.showerror("Error", "Number of episodes must be between 2 and 10.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of episodes.")
            return
        
        try:
            video_length = float(self.length_var.get())
            if not validate_video_length(video_length):
                messagebox.showerror("Error", "Video length must be between 0.1 and 60 minutes.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid video length.")
            return
        
        keywords = self.keywords_entry.get()
        tone = self.tone_var.get()
        model = self.model_var.get()
        include_images = self.include_images_var.get() if hasattr(self, 'include_images_var') else False
        image_type = self.image_type_var.get() if hasattr(self, 'image_type_var') else "descriptions"
        
        # Update status
        self.status_label.config(
            text=f"⏳ Generating series of {num_episodes} episodes... This will take several minutes.",
            fg='white'
        )
        self.status_indicator.config(fg=self.colors['warning'])
        self.script_text.delete(1.0, tk.END)
        self.script_text.insert(tk.END, f"⏳ Generating series of {num_episodes} episodes...\n\nThis will take {num_episodes * 30}-{num_episodes * 60} seconds.\n\nPlease wait...")
        
        def generate():
            try:
                episodes = self.script_generator.generate_series(
                    idea=idea,
                    num_episodes=num_episodes,
                    keywords=keywords,
                    video_length_minutes=video_length,
                    tone=tone,
                    model=model,
                    include_images=include_images,
                    image_type=image_type
                )
                
                # Combine all episodes into one display
                combined_script = f"📺 SERIES: {idea.upper()}\n"
                combined_script += "=" * 80 + "\n\n"
                
                saved_files = []
                for episode in episodes:
                    ep_num = episode["episode_number"]
                    script = episode["script"]
                    
                    combined_script += f"\n{'=' * 80}\n"
                    combined_script += f"EPISODE {ep_num} of {num_episodes}\n"
                    combined_script += f"{'=' * 80}\n\n"
                    combined_script += script
                    combined_script += f"\n\n[Episode {ep_num} - {episode['actual_chars']}/{episode['target_chars']} characters]\n"
                    combined_script += "\n" + "-" * 80 + "\n\n"
                    
                    # Save individual episode
                    try:
                        filename = save_script(
                            script,
                            filename=f"Episode_{ep_num}_{idea.replace(' ', '_')[:30]}.txt",
                            output_dir="output",
                            idea=f"{idea} - Episode {ep_num}"
                        )
                        saved_files.append(filename)
                    except Exception as e:
                        print(f"Error saving episode {ep_num}: {e}")
                
                # Display combined script
                self.root.after(0, lambda: self.script_text.delete(1.0, tk.END))
                self.root.after(0, lambda: self.script_text.insert(tk.END, combined_script))
                
                # Save combined series file
                try:
                    series_filename = save_script(
                        combined_script,
                        filename=f"Series_{idea.replace(' ', '_')[:30]}_All_Episodes.txt",
                        output_dir="output",
                        idea=f"{idea} - Complete Series"
                    )
                    saved_files.append(series_filename)
                except Exception as e:
                    print(f"Error saving series file: {e}")
                
                # Update status
                files_info = "\n".join([f"• {f}" for f in saved_files[:5]])
                if len(saved_files) > 5:
                    files_info += f"\n• ... and {len(saved_files) - 5} more files"
                
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['success']))
                self.root.after(0, lambda: self.status_label.config(
                    text=f"✓ Series generated successfully! {num_episodes} episodes created.",
                    fg='white'
                ))
                
                self.current_script = combined_script
                
                # Show success message
                self.root.after(0, lambda: messagebox.showinfo(
                    "Series Generated!",
                    f"Successfully generated {num_episodes} episodes!\n\n"
                    f"All episodes have been saved to:\n{files_info}\n\n"
                    f"The complete series is displayed in the script preview."
                ))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate series: {str(e)}"))
                self.root.after(0, lambda: self.status_indicator.config(fg=self.colors['danger']))
                self.root.after(0, lambda: self.status_label.config(
                    text="✗ Error generating series",
                    fg='#ec7063'
                ))
        
        threading.Thread(target=generate, daemon=True).start()
    
    def save_script(self):
        """Save the generated script to a file."""
        if not self.current_script:
            messagebox.showwarning("Warning", "No script to save. Please generate a script first.")
            return
        
        try:
            filename = save_script(self.current_script, filename=None, output_dir="output", idea=self.finalized_idea)
            messagebox.showinfo("Success", f"Script saved successfully!\n\nLocation: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save script: {str(e)}")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = VideoScriptGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
