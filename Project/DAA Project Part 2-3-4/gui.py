import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import timeit
import os

#try to import pyglet for font loading, fallback if not available
try:
    import pyglet
    PYGLET_AVAILABLE = True
except ImportError:
    PYGLET_AVAILABLE = False
    print("Warning: pyglet not installed. Install it with 'pip install pyglet' for custom font support.")

from algorithms import DivideConquerAlgorithms
from generator import InputGenerator

class DivideConquerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Divide and Conquer Algorithms Analyzer")
        self.root.geometry("1800x1500")
        self.root.minsize(1400, 1000)
        self.root.configure(bg='#000000')
        self.colors = {
            'primary': '#ffffff',  # White instead of blue
            'secondary': '#2ecc71',
            'accent': '#e74c3c',
            'dark_bg': '#000000',  # Black
            'light_bg': '#000000',
            'text': '#ffffff',  # White text
            'headings': '#ffffff',  # White headings
            'success': '#27ae60',
            'warning': '#f39c12'
        }
        self.algorithms = DivideConquerAlgorithms()
        self.current_points = []
        self.current_integers = []
        self.setup_fonts()
        self.setup_styles()
        self.setup_ui()
    
    def setup_fonts(self):
        """Load Poppins fonts from local files using pyglet"""
        fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
        font_family = "Poppins"
        
        #try to load Poppins fonts using pyglet
        if PYGLET_AVAILABLE:
            try:
                regular_path = os.path.join(fonts_dir, "Poppins-Regular.ttf")
                bold_path = os.path.join(fonts_dir, "Poppins-Bold.ttf")
                semibold_path = os.path.join(fonts_dir, "Poppins-SemiBold.ttf")
                medium_path = os.path.join(fonts_dir, "Poppins-Medium.ttf")
                
                # Load fonts using pyglet to make them available to Tkinter
                if os.path.exists(regular_path):
                    pyglet.font.add_file(regular_path)
                if os.path.exists(bold_path):
                    pyglet.font.add_file(bold_path)
                if os.path.exists(semibold_path):
                    pyglet.font.add_file(semibold_path)
                if os.path.exists(medium_path):
                    pyglet.font.add_file(medium_path)
                
            except Exception as e:
                print(f"Warning: Could not load Poppins fonts with pyglet: {e}")
                font_family = "Arial"
        else:
            # Check if Poppins is installed system-wide
            try:
                # Try to create a test font to see if Poppins is available
                test_font = Font(family="Poppins", size=10)
                # If no error, Poppins is available
            except:
                font_family = "Arial"
        
        # Verify font is available by checking font families
        try:
            from tkinter import font as tkfont
            available_families = list(tkfont.families())
            if font_family not in available_families:
                # Try alternative names
                poppins_variants = [f for f in available_families if 'Poppins' in f or 'poppins' in f.lower()]
                if poppins_variants:
                    font_family = poppins_variants[0]
                else:
                    font_family = "Arial"
                    print("Warning: Poppins font not found, using Arial as fallback")
        except:
            font_family = "Arial"
        
        #create font variants with different sizes
        try:
            self.font_regular = Font(family=font_family, size=10)
            self.font_medium = Font(family=font_family, size=10)
            self.font_semibold = Font(family=font_family, size=10)
            self.font_bold = Font(family=font_family, size=10, weight="bold")
            
            self.font_title = Font(family=font_family, size=18, weight="bold")
            self.font_subtitle = Font(family=font_family, size=12)  
            self.font_label = Font(family=font_family, size=12, weight="bold")
            self.font_button = Font(family=font_family, size=10, weight="bold")
            self.font_text = Font(family=font_family, size=11)  
        except:
            #fallback to Arial if Poppins fails
            font_family = "Arial"
            self.font_regular = Font(family=font_family, size=10)
            self.font_medium = Font(family=font_family, size=10)
            self.font_semibold = Font(family=font_family, size=10)
            self.font_bold = Font(family=font_family, size=10, weight="bold")
            self.font_title = Font(family=font_family, size=18, weight="bold")
            self.font_subtitle = Font(family=font_family, size=12)
            self.font_label = Font(family=font_family, size=12, weight="bold")
            self.font_button = Font(family=font_family, size=10, weight="bold")
            self.font_text = Font(family=font_family, size=11)
        
        self.font_code = Font(family="Consolas", size=10)
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TFrame', background=self.colors['dark_bg'])
        style.configure('Title.TLabel', 
                       background=self.colors['dark_bg'],
                       foreground=self.colors['headings'],
                       font=self.font_title)
        style.configure('Card.TLabelframe', 
                       background=self.colors['light_bg'],
                       foreground=self.colors['text'],
                       bordercolor='#ffffff', 
                       relief='raised',
                       padding=10)
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['light_bg'],
                       foreground=self.colors['headings'],
                       font=self.font_label)
        style.configure('Accent.TButton',
                       background='#333333',
                       foreground=self.colors['text'],
                       font=self.font_button,
                       padding=(20, 10))
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground=self.colors['text'],
                       font=self.font_button,
                       padding=(20, 10)) 
        style.configure('TButton',
                       font=self.font_button,
                       padding=(20, 10))
        style.configure('TRadiobutton',
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.font_text)
        style.map('TRadiobutton',
                 background=[('active', self.colors['light_bg'])],
                 foreground=[('active', self.colors['text'])])
        style.configure('TLabel',
                       background=self.colors['light_bg'],
                       foreground=self.colors['text'],
                       font=self.font_text)
        style.configure('TNotebook',
                       background=self.colors['light_bg'])
        style.configure('TNotebook.Tab',
                       background=self.colors['light_bg'],
                       foreground=self.colors['text'],
                       font=self.font_text,
                       padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', '#333333')], 
                 foreground=[('selected', self.colors['text'])])
        style.configure('TCombobox',
                       fieldbackground=self.colors['dark_bg'],
                       background=self.colors['dark_bg'],
                       foreground=self.colors['text'],
                       font=self.font_text)
        style.map('Accent.TButton',
                 background=[('active', '#555555'),  # Lighter grey on hover instead of green
                           ('pressed', '#222222')])  # Darker grey on press instead of red
    
    def setup_ui(self):
        #creating main frame
        main_frame = ttk.Frame(self.root, style='Modern.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        #grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        self.create_header(main_frame)
        
        self.create_file_section(main_frame)
        
        self.create_algorithm_section(main_frame)
        
        self.create_results_section(main_frame)
        
        self.create_stats_section(main_frame)
        
        self.create_footer(main_frame)
    
    def create_header(self, parent):
        #creating the header section
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        
        #title
        title_label = ttk.Label(header_frame, 
                               text="Divide and Conquer Algorithms Analyzer", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        #subtitle
        subtitle_label = ttk.Label(header_frame,
                                  text="Advanced Algorithm Analysis with Visualizations",
                                  background=self.colors['dark_bg'],
                                  foreground=self.colors['text'],
                                  font=self.font_subtitle)
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        #status indicator
        self.status_var = tk.StringVar(value="🟢 Ready To Analyze Algorithms")
        status_label = ttk.Label(header_frame,
                                textvariable=self.status_var,
                                background=self.colors['dark_bg'],
                                foreground=self.colors['success'],
                                font=self.font_text)
        status_label.grid(row=0, column=1, rowspan=2, sticky=tk.E)
    
    def create_file_section(self, parent):
        #file selection section
        file_frame = ttk.LabelFrame(parent, text="📁 Data Source", style='Card.TLabelframe')
        file_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(1, weight=1)
        
        #file selection row
        ttk.Label(file_frame, text="Select Dataset:", 
                 background=self.colors['light_bg'],
                 foreground=self.colors['text'],
                 font=self.font_text).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.file_var = tk.StringVar()
        self.file_combo = ttk.Combobox(file_frame, textvariable=self.file_var, 
                                      state="readonly", width=50)
        self.file_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        #button row
        button_frame = ttk.Frame(file_frame, style='Modern.TFrame')
        button_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="📂 Browse", 
                  command=self.browse_file, style='TButton').grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="📊 Load File", 
                  command=self.load_file, style='TButton').grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="⚡ Generate Datasets", 
                  command=self.generate_datasets,
                  style='TButton').grid(row=0, column=2, padx=(0, 10))
        
        ttk.Button(button_frame, text="🔄 Clear Results", 
                  command=self.clear_results,
                  style='TButton').grid(row=0, column=3)
        
        #file info display
        self.file_info_var = tk.StringVar(value="No file loaded")
        file_info_label = ttk.Label(file_frame, textvariable=self.file_info_var,
                                   background=self.colors['light_bg'],
                                   foreground=self.colors['text'],
                                   font=self.font_text)
        file_info_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(10, 0))
    
    def create_algorithm_section(self, parent):
        #algorithm selection section w/ Run button
        algo_frame = ttk.LabelFrame(parent, text="⚙️ Algorithm Selection", style='Card.TLabelframe')
        algo_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        algo_frame.columnconfigure(0, weight=1)
        
        #main content frame
        content_frame = ttk.Frame(algo_frame, style='Modern.TFrame')
        content_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=0)
        
        #algorithm choices with icons
        self.algo_var = tk.StringVar(value="closest_pair")
        
        algo_choice_frame = ttk.Frame(content_frame, style='Modern.TFrame')
        algo_choice_frame.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Radiobutton(algo_choice_frame, text="📍 Closest Pair of Points", 
                       variable=self.algo_var, value="closest_pair",
                       style='TRadiobutton').grid(row=0, column=0, sticky=tk.W, padx=(0, 30))
        
        ttk.Radiobutton(algo_choice_frame, text="🧮 Integer Multiplication (Karatsuba)", 
                       variable=self.algo_var, value="integer_mult",
                       style='TRadiobutton').grid(row=0, column=1, sticky=tk.W)
        
        #run button
        self.run_button = ttk.Button(content_frame, text="🚀 Run Algorithm", 
                                    command=self.run_algorithm, 
                                    style='TButton',
                                    width=20)
        self.run_button.grid(row=0, column=1, padx=(20, 0), sticky=tk.E)
    
    def create_results_section(self, parent):
        #Create results display section
        results_frame = ttk.LabelFrame(parent, text="📈 Results & Analysis", style='Card.TLabelframe')
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        #creating notebook for different views
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Ensure notebook can expand properly - already configured above but ensuring it's clear
        
        #text results tab
        text_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(text_frame, text="📋 Text Results")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        #text widget with scrollbar
        text_container = ttk.Frame(text_frame, style='Modern.TFrame')
        text_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_container.columnconfigure(0, weight=1)
        text_container.rowconfigure(0, weight=1)
        
        self.results_text = tk.Text(text_container, wrap=tk.WORD, width=80, height=15,  # Reduced to give more space to visualization
                                   bg='#1a1a1a', fg='#00ff00',
                                   font=self.font_code,
                                   insertbackground='white')
        
        scrollbar = ttk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        #visualisation tab - configure with scrollbars
        self.viz_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(self.viz_frame, text="📊 Visualisation")
        self.viz_frame.columnconfigure(0, weight=1)
        self.viz_frame.rowconfigure(0, weight=1)
        
        # Create a canvas for scrolling
        self.viz_canvas = tk.Canvas(self.viz_frame, bg='#000000', highlightthickness=0)  # Black background
        self.viz_scrollbar_v = ttk.Scrollbar(self.viz_frame, orient=tk.VERTICAL, command=self.viz_canvas.yview)
        self.viz_scrollbar_h = ttk.Scrollbar(self.viz_frame, orient=tk.HORIZONTAL, command=self.viz_canvas.xview)
        
        # Frame inside canvas to hold the matplotlib figure
        self.viz_canvas_frame = ttk.Frame(self.viz_canvas, style='Modern.TFrame')
        self.viz_canvas_window = self.viz_canvas.create_window((0, 0), window=self.viz_canvas_frame, anchor="nw")
        
        # Configure scrollbars
        self.viz_canvas.configure(yscrollcommand=self.viz_scrollbar_v.set, xscrollcommand=self.viz_scrollbar_h.set)
        
        # Grid layout
        self.viz_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.viz_scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.viz_scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure weights
        self.viz_frame.columnconfigure(0, weight=1)
        self.viz_frame.rowconfigure(0, weight=1)
        
        # Update scroll region when canvas frame size changes
        def configure_scroll_region(event):
            # Update scroll region to include all content
            bbox = self.viz_canvas.bbox("all")
            if bbox:
                self.viz_canvas.configure(scrollregion=bbox)
            # Make sure canvas window fills the canvas width
            canvas_width = event.width
            self.viz_canvas.itemconfig(self.viz_canvas_window, width=canvas_width)
        
        self.viz_canvas_frame.bind("<Configure>", configure_scroll_region)
        self.viz_canvas.bind("<Configure>", lambda e: self.viz_canvas.itemconfig(self.viz_canvas_window, width=e.width))
        
        # Mouse wheel scrolling - Windows and Linux/Mac compatible
        def on_mousewheel(event):
            # Windows uses delta, Linux/Mac uses different event
            if event.num == 4 or event.delta > 0:
                self.viz_canvas.yview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.viz_canvas.yview_scroll(1, "units")
        
        def on_shift_mousewheel(event):
            # Horizontal scrolling with Shift+Wheel
            if event.num == 4 or event.delta > 0:
                self.viz_canvas.xview_scroll(-1, "units")
            elif event.num == 5 or event.delta < 0:
                self.viz_canvas.xview_scroll(1, "units")
        
        # Bind mouse wheel events for different platforms
        self.viz_canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        self.viz_canvas.bind("<Button-4>", on_mousewheel)  # Linux
        self.viz_canvas.bind("<Button-5>", on_mousewheel)  # Linux
        self.viz_canvas.bind("<Shift-MouseWheel>", on_shift_mousewheel)  # Windows
        self.viz_canvas.bind("<Shift-Button-4>", on_shift_mousewheel)  # Linux
        self.viz_canvas.bind("<Shift-Button-5>", on_shift_mousewheel)  # Linux
        
        # Also bind to the canvas frame for better coverage
        self.viz_canvas_frame.bind("<MouseWheel>", on_mousewheel)
        self.viz_canvas_frame.bind("<Button-4>", on_mousewheel)
        self.viz_canvas_frame.bind("<Button-5>", on_mousewheel)
    
    def create_stats_section(self, parent):
        #statistics section
        stats_frame = ttk.LabelFrame(parent, text="📊 Performance Statistics", style='Card.TLabelframe')
        stats_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        stats_frame.columnconfigure(0, weight=1)
        
        self.stats_text = tk.Text(stats_frame, wrap=tk.WORD, width=80, height=4,  # Reduced height to give more space to visualization
                                bg=self.colors['light_bg'], fg=self.colors['text'],
                                font=self.font_text,
                                relief='flat')
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.stats_text.insert(tk.END, "💡 Select an algorithm & run it to see performance statistics here...")
        self.stats_text.config(state=tk.DISABLED)
    
    def create_footer(self, parent):
        #footer section
        footer_frame = ttk.Frame(parent, style='Modern.TFrame')
        footer_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        footer_frame.columnconfigure(0, weight=1)
        
        footer_label = ttk.Label(footer_frame,
                                text="Divide and Conquer Algorithms | DAA Project | 5th Semester | Syed Ukkashah & Ibrahim Johar",
                                background=self.colors['dark_bg'],
                                foreground=self.colors['text'],
                                font=self.font_text)
        footer_label.grid(row=0, column=0, sticky=tk.W)
        
        #progress bar
        self.progress = ttk.Progressbar(footer_frame, mode='indeterminate')
        self.progress.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(20, 0))
        footer_frame.columnconfigure(1, weight=1)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select dataset file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
            self.file_info_var.set(f"📄 Selected: {os.path.basename(filename)}")
    
    def generate_datasets(self):
        try:
            self.status_var.set("🔄 Generating datasets...")
            self.progress.start()
            self.root.update()
            
            points_files, integers_files = InputGenerator.generate_all_datasets()
            all_files = points_files + integers_files
            self.file_combo['values'] = all_files
            
            self.status_var.set("✅ Datasets generated successfully!")
            messagebox.showinfo("Success", 
                              f"🎉 Generated 20 datasets!\n"
                              f"• 10 points datasets\n"
                              f"• 10 integers datasets\n"
                              f"Saved in 'datasets' folder")
        except Exception as e:
            self.status_var.set("❌ Dataset generation failed")
            messagebox.showerror("Error", f"Failed to generate datasets: {str(e)}")
        finally:
            self.progress.stop()
    
    def clear_results(self):
        #clear all results & reset interface
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, "💡 Select an algorithm & run it to see performance statistics here...")
        self.stats_text.config(state=tk.DISABLED)
        
        #visualisation
        for widget in self.viz_frame.winfo_children():
            widget.destroy()
        
        self.status_var.set("🟢 Ready to analyze algorithms")
        self.file_info_var.set("No file loaded")
    
    def load_file(self):
        filename = self.file_var.get()
        if not filename:
            messagebox.showwarning("Warning", "📝 Please select a file first")
            return
        
        try:
            self.status_var.set("🔄 Loading file...")
            self.progress.start()
            self.root.update()
            
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            self.current_points = []
            self.current_integers = []
            
            #clearing previous results but keeping the text widget editable
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            
            if 'points' in filename.lower():
                #load points
                for line in lines:
                    if line.strip():
                        x, y = map(int, line.strip().split(','))
                        self.current_points.append((x, y))
                
                self.results_text.insert(tk.END, f"✅ SUCCESS: Loaded {len(self.current_points)} points\n")
                self.results_text.insert(tk.END, f"📊 Dataset: {os.path.basename(filename)}\n")
                self.results_text.insert(tk.END, f"🎯 Ready for Closest Pair algorithm\n\n")
                self.file_info_var.set(f"📍 Points dataset: {len(self.current_points)} points")
                
            elif 'integers' in filename.lower():
                #load integers
                for line in lines:
                    if line.strip():
                        x, y = map(int, line.strip().split(','))
                        self.current_integers.append((x, y))
                
                self.results_text.insert(tk.END, f"✅ SUCCESS: Loaded {len(self.current_integers)} integer pairs\n")
                self.results_text.insert(tk.END, f"📊 Dataset: {os.path.basename(filename)}\n")
                self.results_text.insert(tk.END, f"🎯 Ready for Karatsuba multiplication\n\n")
                self.file_info_var.set(f"🧮 Integers dataset: {len(self.current_integers)} pairs")
                
                #sample
                if self.current_integers:
                    self.results_text.insert(tk.END, f"🔍 Sample pair analysis:\n")
                    self.results_text.insert(tk.END, f"   X: {self.current_integers[0][0]}\n")
                    self.results_text.insert(tk.END, f"   Y: {self.current_integers[0][1]}\n")
                    self.results_text.insert(tk.END, f"   Digit lengths: {len(str(self.current_integers[0][0]))} and {len(str(self.current_integers[0][1]))}\n")
            
            self.status_var.set("✅ File loaded successfully! Click 'Run Algorithm' to proceed.")
            self.results_text.see(tk.END)
            
        except Exception as e:
            self.status_var.set("❌ File loading failed")
            messagebox.showerror("Error", f"📂 Failed to load file: {str(e)}")
        finally:
            self.progress.stop()

    def run_algorithm(self):
        algorithm = self.algo_var.get()
        
        if algorithm == "closest_pair":
            if self.current_points:
                self.run_closest_pair()
            else:
                messagebox.showwarning("Warning", 
                    "📍 No points data loaded!\n"
                    "Please load a points dataset file first.")
        
        elif algorithm == "integer_mult":
            if self.current_integers:
                self.run_integer_multiplication()
            else:
                messagebox.showwarning("Warning",
                    "🧮 No integers data loaded!\n"
                    "Please load an integers dataset file first.")
    
    def run_closest_pair(self):
        if not self.current_points:
            return
        
        self.status_var.set("🔄 Running Closest Pair Algorithm...")
        self.progress.start()
        self.root.update()
        
        #clear previous results but keep styling
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, "\n" + "═" * 60 + "\n")
        self.results_text.insert(tk.END, "📍 CLOSEST PAIR ALGORITHM EXECUTION\n")
        self.results_text.insert(tk.END, "═" * 60 + "\n")
        
        start_time = time.time()
        min_dist, closest_pair = self.algorithms.closest_pair(self.current_points)
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.results_text.insert(tk.END, f"📊 Results:\n")
        self.results_text.insert(tk.END, f"   • Number of points: {len(self.current_points)}\n")
        self.results_text.insert(tk.END, f"   • Closest pair: {closest_pair[0]} and {closest_pair[1]}\n")
        self.results_text.insert(tk.END, f"   • Minimum distance: {min_dist:.4f}\n")
        self.results_text.insert(tk.END, f"   • Execution time: {execution_time:.6f} seconds\n")
        
        #updating statistics
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"📍 Algorithm: Closest Pair\n")
        self.stats_text.insert(tk.END, f"📦 Input size: {len(self.current_points)} points\n")
        self.stats_text.insert(tk.END, f"⏱️  Execution time: {execution_time:.6f} seconds\n")
        self.stats_text.insert(tk.END, f"📏 Minimum distance: {min_dist:.4f}\n")
        self.stats_text.config(state=tk.DISABLED)
        
        #visualization
        self.visualize_closest_pair(self.current_points, closest_pair)
        self.status_var.set("✅ Closest Pair algorithm completed!")
        self.results_text.see(tk.END)
        self.progress.stop()

    def run_integer_multiplication(self):
        if not self.current_integers:
            return
        
        self.status_var.set("🔄 Running Karatsuba Multiplication...")
        self.progress.start()
        self.root.update()
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, "\n" + "═" * 60 + "\n")
        self.results_text.insert(tk.END, "🧮 KARATSUBA MULTIPLICATION ALGORITHM\n")
        self.results_text.insert(tk.END, "═" * 60 + "\n")
        
        #test w/ first few pairs to avoid long computation
        test_pairs = self.current_integers[:3]
        
        total_karatsuba_time = 0
        total_standard_time = 0
        total_naive_time = 0
        successful_pairs = 0
        results_data = []
        
        for i, (x, y) in enumerate(test_pairs):
            try:
                self.results_text.insert(tk.END, f"\n{'='*40}\n")
                self.results_text.insert(tk.END, f"TEST CASE {i+1}\n")
                self.results_text.insert(tk.END, f"{'='*40}\n")
                self.results_text.insert(tk.END, f"Number 1 (X): {x}\n")
                self.results_text.insert(tk.END, f"Number 2 (Y): {y}\n")
                self.results_text.insert(tk.END, f"Digit lengths: {len(str(x))} and {len(str(y))}\n\n")
                
                #karatsuba multiplication - use timeit with many iterations for accuracy
                self.results_text.insert(tk.END, "🧮 Running Karatsuba Algorithm... ")
                self.results_text.update()
                # Run many times to get accurate timing (Karatsuba is slower, so fewer iterations needed)
                karatsuba_timer = timeit.Timer(lambda: self.algorithms.karatsuba_multiply(x, y))
                # Run 50 times, repeat 3 times, take minimum
                karatsuba_times = karatsuba_timer.repeat(repeat=3, number=50)
                karatsuba_time = min(karatsuba_times) / 50.0  # Average per operation
                result_karatsuba = self.algorithms.karatsuba_multiply(x, y)
                total_karatsuba_time += karatsuba_time
                self.results_text.insert(tk.END, f"Done! ({karatsuba_time:.9f}s)\n")
                
                #standard multiplication - use timeit with MANY iterations for accuracy
                self.results_text.insert(tk.END, "➗ Running Standard Multiplication (Python's built-in)... ")
                self.results_text.update()
                # Run MANY times since standard is extremely fast - need to measure over longer period
                standard_timer = timeit.Timer(lambda: self.algorithms.standard_multiply(x, y))
                # Run 10,000 times, repeat 3 times, take minimum - this ensures we measure over a meaningful duration
                standard_times = standard_timer.repeat(repeat=3, number=10000)
                standard_time = min(standard_times) / 10000.0  # Average per operation
                result_standard = self.algorithms.standard_multiply(x, y)
                
                # Also test naive Python multiplication for fair comparison
                self.results_text.insert(tk.END, "📚 Running Naive Python Multiplication (for fair comparison)... ")
                self.results_text.update()
                naive_timer = timeit.Timer(lambda: self.algorithms.naive_python_multiply(x, y))
                # Run fewer times since naive is slower
                naive_times = naive_timer.repeat(repeat=3, number=10)
                naive_time = min(naive_times) / 10.0  # Average per operation
                result_naive = self.algorithms.naive_python_multiply(x, y)
                total_standard_time += standard_time
                total_naive_time += naive_time
                self.results_text.insert(tk.END, f"Done! ({standard_time:.9f}s)\n")
                self.results_text.insert(tk.END, f"Done! ({naive_time:.9f}s)\n\n")
                
                #verifying results
                results_match = (result_karatsuba == result_standard == result_naive)
                self.results_text.insert(tk.END, f"✅ Results match: {results_match}\n")
                
                if results_match:
                    self.results_text.insert(tk.END, f"🎯 Multiplication successful!\n")
                else:
                    self.results_text.insert(tk.END, f"❌ ERROR: Results don't match!\n")
                
                #performance comparison - compare Karatsuba vs Naive Python (fair comparison)
                self.results_text.insert(tk.END, f"\n📊 Performance Comparison:\n")
                self.results_text.insert(tk.END, f"   • Python's built-in *: {standard_time:.9f}s (C-optimized)\n")
                self.results_text.insert(tk.END, f"   • Naive Python: {naive_time:.9f}s (O(n²))\n")
                self.results_text.insert(tk.END, f"   • Karatsuba Python: {karatsuba_time:.9f}s (O(n^1.585))\n\n")
                
                # Compare Karatsuba vs Naive (fair comparison - both in Python)
                if karatsuba_time > 0 and naive_time > 0:
                    karatsuba_vs_naive = naive_time / karatsuba_time
                    if karatsuba_vs_naive > 1:
                        self.results_text.insert(tk.END, f"✅ Karatsuba is {karatsuba_vs_naive:.2f}x faster than Naive Python\n")
                    elif karatsuba_vs_naive < 1:
                        self.results_text.insert(tk.END, f"⚠️  Naive is {1/karatsuba_vs_naive:.2f}x faster than Karatsuba\n")
                        self.results_text.insert(tk.END, f"   (For {len(str(x))}-digit numbers, Python overhead dominates)\n")
                        self.results_text.insert(tk.END, f"   (Karatsuba's advantage appears at 500+ digits)\n")
                    else:
                        self.results_text.insert(tk.END, f"⚡ Karatsuba and Naive are equally fast\n")
                
                # Compare Python's built-in vs Karatsuba (unfair but informative)
                if karatsuba_time > 0 and standard_time > 0:
                    builtin_vs_karatsuba = standard_time / karatsuba_time
                    self.results_text.insert(tk.END, f"\nℹ️  Note: Python's built-in * is {1/builtin_vs_karatsuba if builtin_vs_karatsuba > 0 else 'much'}x faster\n")
                    self.results_text.insert(tk.END, f"   (It's C-optimized and may use Karatsuba internally)\n")
                
                #storing data for visualization (karatsuba, standard, naive)
                results_data.append((karatsuba_time, standard_time, naive_time))
                successful_pairs += 1
                
            except Exception as e:
                self.results_text.insert(tk.END, f"💥 Error processing pair {i+1}: {str(e)}\n")
                continue
        
        #visualisation
        if successful_pairs > 0:
            self.visualize_integer_multiplication(test_pairs[:successful_pairs], results_data)
        
        #updating statistics
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, f"Algorithm: Karatsuba Multiplication\n")
        self.stats_text.insert(tk.END, f"Test cases completed: {successful_pairs}/{len(test_pairs)}\n")
        
        if successful_pairs > 0:
            avg_karatsuba = total_karatsuba_time / successful_pairs
            avg_standard = total_standard_time / successful_pairs
            avg_naive = total_naive_time / successful_pairs
            
            self.stats_text.insert(tk.END, f"\nAverage Execution Times:\n")
            self.stats_text.insert(tk.END, f"  • Python's built-in *: {avg_standard:.9f}s (C-optimized)\n")
            self.stats_text.insert(tk.END, f"  • Naive Python: {avg_naive:.9f}s (O(n²))\n")
            self.stats_text.insert(tk.END, f"  • Karatsuba Python: {avg_karatsuba:.9f}s (O(n^1.585))\n")
            
            # Compare Karatsuba vs Naive (fair comparison)
            if avg_karatsuba > 0 and avg_naive > 0:
                karatsuba_vs_naive = avg_naive / avg_karatsuba
                self.stats_text.insert(tk.END, f"\nFair Comparison (Python vs Python):\n")
                if karatsuba_vs_naive > 1:
                    self.stats_text.insert(tk.END, f"  ✅ Karatsuba is {karatsuba_vs_naive:.2f}x faster than Naive\n")
                elif karatsuba_vs_naive < 1:
                    self.stats_text.insert(tk.END, f"  ⚠️  Naive is {1/karatsuba_vs_naive:.2f}x faster than Karatsuba\n")
                else:
                    self.stats_text.insert(tk.END, f"  ⚡ Both are equally fast\n")
            
            # Compare Python's built-in vs Karatsuba (informational)
            if avg_karatsuba > 0 and avg_standard > 0:
                builtin_vs_karatsuba = avg_standard / avg_karatsuba
                self.stats_text.insert(tk.END, f"\nNote: Python's built-in * is {1/builtin_vs_karatsuba if builtin_vs_karatsuba > 0 else 'much'}x faster\n")
                self.stats_text.insert(tk.END, f"(C-optimized, may use Karatsuba internally)\n")
        
        self.stats_text.config(state=tk.DISABLED)
        self.status_var.set("✅ Karatsuba multiplication completed!")
        self.results_text.see(tk.END)
        self.progress.stop()

    def visualize_closest_pair(self, points, closest_pair):
        #clear previous visualization - clear the canvas frame, not the main frame
        for widget in self.viz_canvas_frame.winfo_children():
            widget.destroy()
        
        #matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 7))
        fig.patch.set_facecolor('#000000')  # Black background
        ax.set_facecolor('#1a1a1a')  # Very dark grey
        
        #extract coordinates
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        #plot all points - use white/grey instead of blue
        ax.scatter(x_coords, y_coords, color='#ffffff', alpha=0.7, s=50, label='All Points')
        
        #highlight closest pair
        cp_x = [closest_pair[0][0], closest_pair[1][0]]
        cp_y = [closest_pair[0][1], closest_pair[1][1]]
        ax.scatter(cp_x, cp_y, color='#e74c3c', s=150, label='Closest Pair', zorder=5)
        ax.plot(cp_x, cp_y, 'r-', linewidth=3, alpha=0.8)
        
        #styling
        ax.set_xlabel('X Coordinate', color='white', fontsize=12)
        ax.set_ylabel('Y Coordinate', color='white', fontsize=12)
        ax.set_title('Closest Pair of Points Visualization', color='white', fontsize=14, pad=20)
        ax.legend(facecolor='#000000', edgecolor='white', labelcolor='white')
        ax.grid(True, alpha=0.3, color='white')
        ax.tick_params(colors='white')
        
        #embed in tkinter - place in scrollable canvas frame
        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Update scroll region after canvas is drawn
        self.viz_canvas.update_idletasks()
        self.viz_canvas.configure(scrollregion=self.viz_canvas.bbox("all"))

    def visualize_integer_multiplication(self, test_pairs, results):
        #clear previous visualisation - clear the canvas frame, not the main frame
        for widget in self.viz_canvas_frame.winfo_children():
            widget.destroy()
        
        # Increase figure size significantly for better visibility - taller to prevent squeezing
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9), dpi=100)
        fig.patch.set_facecolor('#000000')  # Black background
        
        for ax in [ax1, ax2]:
            ax.set_facecolor('#1a1a1a')  # Very dark grey instead of blue-grey
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        #plot 1: performance comparison - now includes naive
        digit_lengths = []
        karatsuba_times = []
        standard_times = []
        naive_times = []
        
        for i, ((x, y), (karatsuba_time, standard_time, naive_time)) in enumerate(zip(test_pairs, results)):
            digit_lengths.append(max(len(str(x)), len(str(y))))
            karatsuba_times.append(karatsuba_time)
            standard_times.append(standard_time)
            naive_times.append(naive_time)
        
        # Plot all three algorithms
        ax1.plot(range(len(digit_lengths)), karatsuba_times, 'o-', color='#2ecc71', 
                label='Karatsuba (O(n^1.585))', linewidth=3, markersize=10, markerfacecolor='#27ae60')
        ax1.plot(range(len(digit_lengths)), naive_times, 's-', color='#f39c12', 
                label='Naive Python (O(n²))', linewidth=3, markersize=10, markerfacecolor='#e67e22')
        ax1.plot(range(len(digit_lengths)), standard_times, '^-', color='#e74c3c', 
                label="Python's built-in * (C-optimized)", linewidth=2, markersize=8, markerfacecolor='#c0392b', alpha=0.7)
        
        ax1.set_xlabel('Test Case', color='white', fontsize=12)
        ax1.set_ylabel('Execution Time (seconds)', color='white', fontsize=12)
        ax1.set_title('Algorithm Performance Comparison', color='white', fontsize=14, pad=20)
        ax1.set_xticks(range(len(digit_lengths)))
        ax1.set_xticklabels([f'Case {i+1}\n({digit_lengths[i]}d)' for i in range(len(digit_lengths))], 
                           color='white')
        ax1.legend(facecolor='#000000', edgecolor='white', labelcolor='white', fontsize=10)
        ax1.grid(True, alpha=0.3, color='white')
        
        #plot 2: speedup factor - compare Karatsuba vs Naive (fair comparison)
        speedups = []
        for i in range(len(karatsuba_times)):
            if karatsuba_times[i] > 0 and naive_times[i] > 0:
                speedup = naive_times[i] / karatsuba_times[i]  # How many times faster is Karatsuba vs Naive
                speedups.append(speedup)
            else:
                speedups.append(0)  # Can't calculate if times are too small
        
        colors = ['#27ae60' if speedup > 1 else '#e74c3c' for speedup in speedups]
        bars = ax2.bar(range(len(speedups)), speedups, color=colors, alpha=0.8, edgecolor='white', width=0.6)
        
        ax2.set_xlabel('Test Case', color='white', fontsize=12)
        ax2.set_ylabel('Speedup Factor (x times)', color='white', fontsize=12)
        ax2.set_title('Karatsuba Speedup Over Naive Python', color='white', fontsize=14, pad=20)
        ax2.set_xticks(range(len(speedups)))
        ax2.set_xticklabels([f'Case {i+1}' for i in range(len(speedups))], color='white')
        
        #add value labels on bars
        for i, v in enumerate(speedups):
            if v > 0:
                color = 'white'
                label_text = f'{v:.2f}x' if v >= 0.01 else f'{v:.3f}x'
                ax2.text(i, v + max(speedups) * 0.05, label_text, ha='center', va='bottom', 
                        fontweight='bold', color=color, fontsize=10)
        
        #add horizontal line at 1x
        if max(speedups) > 1:
            ax2.axhline(y=1, color='white', linestyle='--', alpha=0.7, linewidth=2)
            ax2.text(len(speedups)-0.5, 1 + max(speedups) * 0.05, '1x baseline', ha='right', va='bottom', 
                    color='white', fontweight='bold', fontsize=9)
        
        ax2.grid(True, alpha=0.3, color='white')
        
        # Add more padding and adjust layout to prevent text cutoff
        plt.tight_layout(pad=4.0, h_pad=3.0, w_pad=3.0)
        
        #embed in tkinter - place in scrollable canvas frame
        canvas = FigureCanvasTkAgg(fig, self.viz_canvas_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Update scroll region after canvas is drawn
        self.viz_canvas.update_idletasks()
        self.viz_canvas.configure(scrollregion=self.viz_canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = DivideConquerGUI(root)
    root.mainloop()