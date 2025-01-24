import tkinter as tk
from tkinter import ttk, messagebox

class UIComponents:
    def __init__(self, root, colors):
        self.root = root
        self.colors = {
            'bg': '#1a1a2e',           # Dark blue background
            'primary': '#16213e',      # Darker blue for main areas
            'secondary': '#0f3460',    # Medium blue for sections
            'accent': '#e94560',       # Pink accent
            'text': '#ffffff',         # White text
            'gold': '#ffd700',        # Gold for winners
            'silver': '#c0c0c0'       # Silver for secondary text
        }
        self.main_frame = None
        self.file_btn = None
        self.file_label = None
        self.canvas = None
        self.name_label = None
        self.start_btn = None
        self.stop_btn = None
        self.next_btn = None
        self.winners_list = None

    def setup_styles(self):
        """Configure custom styles and colors"""
        style = ttk.Style()
        style.configure(
            'Custom.TButton',
            background=self.colors['accent'],
            foreground=self.colors['text'],
            padding=15,
            font=('Montserrat', 12, 'bold')
        )
        self.root.configure(bg=self.colors['bg'])

    def create_ui(self):
        """Create the main user interface"""
        self.main_frame = tk.Frame(
            self.root,
            bg=self.colors['bg'],
            highlightthickness=3,
            highlightbackground=self.colors['accent']
        )
        self.main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        self.create_title()
        self.create_file_section()
        self.create_display_section()
        self.create_controls_section()
        self.create_winners_section()

    def create_title(self):
        """Create the title section"""
        title_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        title_frame.pack(fill='x', pady=(0, 30))
        
        # Add decorative elements
        tk.Label(
            title_frame,
            text="✨",
            font=('Segoe UI Emoji', 32),
            bg=self.colors['bg'],
            fg=self.colors['gold']
        ).pack(side='left', padx=20)
        
        title_label = tk.Label(
            title_frame,
            text="LUCKY DRAW FIS DT HCM",
            font=('Montserrat', 32, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['gold']
        )
        title_label.pack(side='left', expand=True)
        
        tk.Label(
            title_frame,
            text="✨",
            font=('Segoe UI Emoji', 32),
            bg=self.colors['bg'],
            fg=self.colors['gold']
        ).pack(side='right', padx=20)

    def create_file_section(self):
        """Create enhanced file selection section"""
        file_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['secondary'],
            padx=25,
            pady=15,
            relief='flat',
            borderwidth=0
        )
        file_frame.pack(fill='x', pady=(0, 25))
        
        # Add rounded corners effect
        canvas = tk.Canvas(
            file_frame,
            bg=self.colors['secondary'],
            highlightthickness=0,
            height=60
        )
        canvas.pack(fill='x')
        
        self.file_btn = tk.Button(
            canvas,
            text="📂 Select Participants",
            font=('Montserrat', 12, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            padx=25,
            pady=12,
            relief='flat',
            cursor='hand2'
        )
        self.file_btn.pack(side='left')
        
        self.file_label = tk.Label(
            canvas,
            text="No file selected",
            bg=self.colors['secondary'],
            fg=self.colors['silver'],
            font=('Montserrat', 12)
        )
        self.file_label.pack(side='left', padx=25)

    def create_display_section(self):
        """Create enhanced main display area"""
        self.display_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['primary'],
            relief='flat',
            borderwidth=0
        )
        self.display_frame.pack(fill='x', pady=25, padx=25)
        
        # Create gradient effect
        self.canvas = tk.Canvas(
            self.display_frame,
            bg=self.colors['primary'],
            height=350,
            highlightthickness=0
        )
        self.canvas.pack(fill='x', pady=25)
        
        prize_label = tk.Label(
            self.display_frame,
            text="GRAND PRIZE",
            font=('Montserrat', 33, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['gold']
        )
        prize_label.place(relx=0.5, rely=0.15, anchor='center')
        
        self.name_label = tk.Label(
            self.canvas,
            text="Ready to Start",
            font=('Montserrat', 70, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['gold']
        )
        self.name_label.place(relx=0.5, rely=0.5, anchor='center')

    def create_controls_section(self):
        """Create enhanced control buttons section"""
        controls_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        controls_frame.pack(pady=25)
        
        button_styles = {
            'start': {'bg': '#2ecc71', 'text': '▶ Start'},
            'stop': {'bg': '#e74c3c', 'text': '⏹ Stop'},
            'next': {'bg': '#3498db', 'text': '⭮ Next Round'}
        }
        
        for btn_type, style in button_styles.items():
            btn = tk.Button(
                controls_frame,
                text=style['text'],
                font=('Montserrat', 14, 'bold'),
                bg=style['bg'],
                fg=self.colors['text'],
                width=12,
                height=2,
                relief='flat',
                cursor='hand2'
            )
            btn.pack(side='left', padx=15)
            
            # Add hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.configure(bg=self.colors['accent']))
            btn.bind('<Leave>', lambda e, b=btn, c=style['bg']: b.configure(bg=c))
            
            if btn_type == 'start':
                self.start_btn = btn
            elif btn_type == 'stop':
                self.stop_btn = btn
                btn.configure(state='disabled')
            else:
                self.next_btn = btn
                btn.configure(state='disabled')

    def create_winners_section(self):
        """Create enhanced winners display section"""
        winners_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['secondary'],
            relief='flat',
            borderwidth=0
        )
        winners_frame.pack(fill='both', expand=True, pady=25, padx=25)
        
        # Add header with icons
        header_frame = tk.Frame(winners_frame, bg=self.colors['secondary'])
        header_frame.pack(fill='x', pady=15)
        
        tk.Label(
            header_frame,
            text="🏆 Winners Gallery 🏆",
            font=('Montserrat', 20, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['gold']
        ).pack()
        
        # Create stylish listbox
        list_frame = tk.Frame(winners_frame, bg=self.colors['secondary'])
        list_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.winners_list = tk.Listbox(
            list_frame,
            bg=self.colors['primary'],
            fg=self.colors['silver'],
            font=('Montserrat', 12),
            selectmode='none',
            height=8,
            yscrollcommand=scrollbar.set,
            relief='flat',
            borderwidth=0,
            highlightthickness=0
        )
        self.winners_list.pack(fill='both', expand=True)
        scrollbar.config(command=self.winners_list.yview)
