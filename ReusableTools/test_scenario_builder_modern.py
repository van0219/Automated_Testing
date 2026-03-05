"""
Modern Test Scenario Builder - 2026 Edition

A beautiful, modern GUI for creating FSM test scenarios with automatic
template loading based on interface type selection.

Usage:
    python ReusableTools/test_scenario_builder_modern.py

Requirements:
    - tkinter (included with Python)
    - ttkbootstrap (pip install ttkbootstrap)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
from pathlib import Path
from datetime import datetime

try:
    import ttkbootstrap as ttk_boot
    from ttkbootstrap.constants import *
    MODERN_THEME = True
except ImportError:
    MODERN_THEME = False
    # ttkbootstrap is optional - GUI works fine without it


class ModernTestScenarioBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("FSM Test Scenario Builder")  # Removed emoji - it's in the window icon now

        # Set custom icon (remove default feather)
        try:
            icon_path = Path(__file__).parent / 'app_icon.ico'
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except Exception as e:
            # Fallback: try to hide the icon
            try:
                self.root.iconbitmap(default='')
            except:
                pass  # Keep default if all else fails

        # Maximize window by default
        self.root.state('zoomed')  # Windows maximized state

        # Data storage
        self.scenarios = []
        self.interface_type_selected = False
        self.undo_stack = []  # For undo/redo functionality
        self.redo_stack = []

        # Create main container
        self.create_welcome_screen()

    
    def create_welcome_screen(self):
        """Create modern welcome screen with interface type selection"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container with gradient-like background
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Header section
        header = tk.Frame(main_frame, bg='#2c3e50', height=140)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="🚀 FSM Test Scenario Builder",
            font=('Segoe UI', 28, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(25, 5))
        
        subtitle = tk.Label(
            header,
            text="Create professional test scenarios in minutes",
            font=('Segoe UI', 13),
            bg='#2c3e50',
            fg='#ecf0f1',
            pady=5  # Add vertical padding to prevent clipping
        )
        subtitle.pack(pady=(0, 20))
        
        # Content area
        content = tk.Frame(main_frame, bg='#f8f9fa')
        content.pack(fill='both', expand=True, padx=50, pady=50)
        
        # Welcome message
        welcome_text = tk.Label(
            content,
            text="Let's get started! What type of interface are you testing?",
            font=('Segoe UI', 16),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        welcome_text.pack(pady=(0, 40))
        
        # Interface type cards
        cards_frame = tk.Frame(content, bg='#f8f9fa')
        cards_frame.pack()
        
        # Card data
        interface_types = [
            {
                'type': 'inbound',
                'icon': '📥',
                'title': 'Inbound Interface',
                'desc': 'Data coming INTO FSM',
                'color': '#3498db',
                'scenarios': 3
            },
            {
                'type': 'outbound',
                'icon': '📤',
                'title': 'Outbound Interface',
                'desc': 'Data going OUT of FSM',
                'color': '#e74c3c',
                'scenarios': 3
            },
            {
                'type': 'approval',
                'icon': '✅',
                'title': 'Approval Workflow',
                'desc': 'Approval processes',
                'color': '#2ecc71',
                'scenarios': 3
            }
        ]
        
        for i, card_data in enumerate(interface_types):
            self.create_interface_card(cards_frame, card_data, i)
        
        # Import option
        import_frame = tk.Frame(content, bg='#f8f9fa')
        import_frame.pack(pady=40)
        
        separator = tk.Label(
            import_frame,
            text="— OR —",
            font=('Segoe UI', 12),
            bg='#f8f9fa',
            fg='#95a5a6'
        )
        separator.pack(pady=10)
        
        import_btn = tk.Button(
            import_frame,
            text='📂 Import Existing JSON',
            font=('Segoe UI', 12),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2',
            command=self.import_json
        )
        import_btn.pack()
    def import_json(self):
        """Import existing JSON file"""
        # Start at Projects folder to let user select client
        initial_dir = "Projects"
        if not Path(initial_dir).exists():
            initial_dir = "."  # Fallback to current directory
        
        filename = filedialog.askopenfilename(
            title="Select Test Scenario JSON",
            initialdir=initial_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                self.interface_type = data.get('interface_type', 'inbound')
                self.scenarios = data.get('scenarios', [])
                self.interface_type_selected = True
                self.imported_data = data

                self.create_main_editor()
                self.populate_form_fields(data)

            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import JSON:\n{str(e)}")

    def populate_form_fields(self, data):
        """Populate form fields from imported data"""
        if 'Interface ID' in self.form_fields:
            self.form_fields['Interface ID'].delete(0, 'end')
            self.form_fields['Interface ID'].insert(0, data.get('interface_id', ''))

        if 'Interface Name' in self.form_fields:
            self.form_fields['Interface Name'].delete(0, 'end')
            self.form_fields['Interface Name'].insert(0, data.get('interface_name', ''))

        if 'Client Name' in self.form_fields:
            client_widget = self.form_fields['Client Name']
            if hasattr(client_widget, 'current'):  # It's a Combobox
                client_widget.set(data.get('client_name', ''))
            else:  # It's an Entry
                client_widget.delete(0, 'end')
                client_widget.insert(0, data.get('client_name', ''))

        if 'Author Name' in self.form_fields:
            self.form_fields['Author Name'].delete(0, 'end')
            self.form_fields['Author Name'].insert(0, data.get('author', ''))

        if 'Environment' in self.form_fields:
            self.form_fields['Environment'].delete(0, 'end')
            self.form_fields['Environment'].insert(0, data.get('environment', ''))
        
        if 'File Channel Name' in self.form_fields:
            self.form_fields['File Channel Name'].delete(0, 'end')
            self.form_fields['File Channel Name'].insert(0, data.get('file_channel_name', ''))
        
        if 'SFTP Server' in self.form_fields:
            self.form_fields['SFTP Server'].delete(0, 'end')
            self.form_fields['SFTP Server'].insert(0, data.get('sftp_server', ''))

        if 'User Roles' in self.text_fields:
            self.text_fields['User Roles'].delete('1.0', 'end')
            roles = '\n'.join(data.get('user_roles', []))
            self.text_fields['User Roles'].insert('1.0', roles)

        if 'Test Data' in self.text_fields:
            self.text_fields['Test Data'].delete('1.0', 'end')
            self.text_fields['Test Data'].insert('1.0', data.get('test_data_requirements', ''))

        if 'Configuration' in self.text_fields:
            self.text_fields['Configuration'].delete('1.0', 'end')
            self.text_fields['Configuration'].insert('1.0', data.get('configuration_prerequisites', ''))
    
    def create_interface_card(self, parent, data, column):
        """Create a modern card for interface type selection"""
        card = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            borderwidth=0,
            highlightthickness=2,
            highlightbackground='#ecf0f1',
            highlightcolor=data['color']
        )
        card.grid(row=0, column=column, padx=15, pady=10, sticky='nsew')
        
        # Make card clickable
        card.bind('<Enter>', lambda e: self.on_card_hover(card, data['color']))
        card.bind('<Leave>', lambda e: self.on_card_leave(card))
        card.bind('<Button-1>', lambda e: self.select_interface_type(data['type']))
        
        # Icon
        icon_label = tk.Label(
            card,
            text=data['icon'],
            font=('Segoe UI', 48),
            bg='white'
        )
        icon_label.pack(pady=(30, 10))
        icon_label.bind('<Button-1>', lambda e: self.select_interface_type(data['type']))
        
        # Title
        title_label = tk.Label(
            card,
            text=data['title'],
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title_label.pack(pady=5)
        title_label.bind('<Button-1>', lambda e: self.select_interface_type(data['type']))
        
        # Description
        desc_label = tk.Label(
            card,
            text=data['desc'],
            font=('Segoe UI', 11),
            bg='white',
            fg='#7f8c8d'
        )
        desc_label.pack(pady=5)
        desc_label.bind('<Button-1>', lambda e: self.select_interface_type(data['type']))
        
        # Scenarios count
        count_label = tk.Label(
            card,
            text=f"{data['scenarios']} scenarios included",
            font=('Segoe UI', 10),
            bg='white',
            fg='#95a5a6'
        )
        count_label.pack(pady=(10, 30))
        count_label.bind('<Button-1>', lambda e: self.select_interface_type(data['type']))
        
        # Configure grid
        card.grid_columnconfigure(0, weight=1)
        card.config(width=280, height=300)
        card.grid_propagate(False)
    
    def on_card_hover(self, card, color):
        """Card hover effect"""
        card.config(highlightbackground=color, highlightthickness=3)
        card.config(cursor='hand2')
    
    def on_card_leave(self, card):
        """Card leave effect"""
        card.config(highlightbackground='#ecf0f1', highlightthickness=2)
    
    def select_interface_type(self, interface_type):
        """Handle interface type selection and load scenarios"""
        self.interface_type = interface_type
        self.interface_type_selected = True
        
        # Load predefined scenarios
        self.scenarios = self.get_predefined_scenarios()[self.get_category_name(interface_type)]
        
        # Show main editor
        self.create_main_editor()
    
    def import_json(self):
        """Import existing JSON file"""
        # Start at Projects folder to let user select client
        initial_dir = "Projects"
        if not Path(initial_dir).exists():
            initial_dir = "."  # Fallback to current directory
        
        filename = filedialog.askopenfilename(
            title="Select Test Scenario JSON",
            initialdir=initial_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.interface_type = data.get('interface_type', 'inbound')
                self.scenarios = data.get('scenarios', [])
                self.interface_type_selected = True
                self.imported_data = data
                
                self.create_main_editor()
                
                # Populate form fields after a short delay to ensure widgets exist
                self.root.after(100, lambda: self.populate_form_fields(data))
                
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import JSON:\n{str(e)}")
    
    def populate_form_fields(self, data):
        """Populate form fields from imported data"""
        if hasattr(self, 'form_fields'):
            if 'Interface ID' in self.form_fields:
                self.form_fields['Interface ID'].delete(0, 'end')
                self.form_fields['Interface ID'].insert(0, data.get('interface_id', ''))
            
            if 'Interface Name' in self.form_fields:
                self.form_fields['Interface Name'].delete(0, 'end')
                self.form_fields['Interface Name'].insert(0, data.get('interface_name', ''))
            
            if 'Client Name' in self.form_fields:
                client_widget = self.form_fields['Client Name']
                if hasattr(client_widget, 'current'):  # It's a Combobox
                    client_widget.set(data.get('client_name', ''))
                else:  # It's an Entry
                    client_widget.delete(0, 'end')
                    client_widget.insert(0, data.get('client_name', ''))
            
            if 'Author Name' in self.form_fields:
                self.form_fields['Author Name'].delete(0, 'end')
                self.form_fields['Author Name'].insert(0, data.get('author', ''))
            
            if 'Environment' in self.form_fields:
                self.form_fields['Environment'].delete(0, 'end')
                self.form_fields['Environment'].insert(0, data.get('environment', ''))
        
        if hasattr(self, 'text_fields'):
            if 'User Roles' in self.text_fields:
                self.text_fields['User Roles'].delete('1.0', 'end')
                roles = '\n'.join(data.get('user_roles', []))
                self.text_fields['User Roles'].insert('1.0', roles)
            
            if 'Test Data' in self.text_fields:
                self.text_fields['Test Data'].delete('1.0', 'end')
                self.text_fields['Test Data'].insert('1.0', data.get('test_data_requirements', ''))
            
            if 'Configuration' in self.text_fields:
                self.text_fields['Configuration'].delete('1.0', 'end')
                self.text_fields['Configuration'].insert('1.0', data.get('configuration_prerequisites', ''))
    
    def get_category_name(self, interface_type):
        """Map interface type to category name"""
        mapping = {
            'inbound': 'Inbound Interface',
            'outbound': 'Outbound Interface',
            'approval': 'Approval Workflow'
        }
        return mapping.get(interface_type, 'Inbound Interface')
    
    def create_main_editor(self):
        """Create the main editing interface"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Top bar
        self.create_top_bar(main_frame)
        
        # Content area with sidebar
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True)
        
        # Left sidebar - Interface info
        self.create_sidebar(content_frame)
        
        # Right content - Scenarios
        self.create_scenarios_panel(content_frame)
        
        # Bottom action bar
        self.create_action_bar(main_frame)
    
    def create_top_bar(self, parent):
        """Create modern top navigation bar"""
        top_bar = tk.Frame(parent, bg='#2c3e50', height=70)
        top_bar.pack(fill='x')
        top_bar.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            top_bar,
            text='← Back',
            font=('Segoe UI', 11),
            bg='#34495e',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.create_welcome_screen
        )
        back_btn.pack(side='left', padx=20, pady=15)
        
        # Title
        type_emoji = {'inbound': '📥', 'outbound': '📤', 'approval': '✅'}
        title = tk.Label(
            top_bar,
            text=f"{type_emoji.get(self.interface_type, '📋')} {self.get_category_name(self.interface_type)}",
            font=('Segoe UI', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(side='left', padx=10)
        
        # Scenario count badge
        count_badge = tk.Label(
            top_bar,
            text=f"{len(self.scenarios)} scenarios",
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            padx=12,
            pady=4
        )
        count_badge.pack(side='left', padx=10)
        
        # Store reference for updates
        self.count_badge = count_badge
    
    def create_sidebar(self, parent):
        """Create left sidebar with interface information"""
        # Sidebar container
        sidebar_container = tk.Frame(parent, bg='white', width=350, relief='solid', borderwidth=1)
        sidebar_container.pack(side='left', fill='y', padx=(20, 10), pady=20)
        sidebar_container.pack_propagate(False)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(sidebar_container, bg='white', highlightthickness=0)
        
        # Scrollbar - make it more visible with custom styling
        scrollbar = tk.Scrollbar(
            sidebar_container, 
            orient='vertical', 
            command=canvas.yview,
            width=12,
            bg='#ecf0f1',
            troughcolor='#f8f9fa',
            activebackground='#95a5a6'
        )
        
        # Scrollable frame inside canvas
        sidebar = tk.Frame(canvas, bg='white')
        
        sidebar.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=sidebar, anchor='nw', width=330)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Store canvas reference
        self.sidebar_canvas = canvas
        self.sidebar_container = sidebar_container
        
        # Sidebar title
        title = tk.Label(
            sidebar,
            text="📋 Interface Details",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(anchor='w', padx=20, pady=(20, 15))
        
        # Form fields
        self.create_form_field(sidebar, "Interface ID", "INT_FIN_013")
        self.create_form_field(sidebar, "Interface Name", "GL Transaction Interface")
        
        # Client Name - dropdown with existing clients
        self.create_client_dropdown(sidebar, "Client Name")
        
        self.create_form_field(sidebar, "Author Name", "")
        self.create_form_field(sidebar, "Environment", "TAMICS10_AX1")
        
        # File Channel Name - with visual emphasis
        self.create_form_field(sidebar, "File Channel Name", "TAMICS10-INT-FIN-013-FileChannel", emphasized=True)
        
        # SFTP Server - dropdown with options from .env.passwords
        self.create_dropdown_field(sidebar, "SFTP Server", emphasized=True)
        
        # Prerequisites section
        prereq_title = tk.Label(
            sidebar,
            text="📌 Prerequisites",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        prereq_title.pack(anchor='w', padx=20, pady=(20, 10))
        
        self.create_text_field(sidebar, "User Roles", "Process Server Administrator\nStaff Accountant", height=3)
        self.create_text_field(sidebar, "Test Data", "Sample CSV file with transactions", height=2)
        self.create_text_field(sidebar, "Configuration", "IPA process deployed\nFile Channel configured\nSFTP credentials set up", height=3)
    
    def create_form_field(self, parent, label, placeholder, emphasized=False):
        """Create a modern form field"""
        container = tk.Frame(parent, bg='white')
        container.pack(fill='x', padx=20, pady=8)
        
        # Add visual emphasis for important fields
        if emphasized:
            # Warning icon and emphasized label
            label_frame = tk.Frame(container, bg='white')
            label_frame.pack(anchor='w', fill='x')
            
            warning_icon = tk.Label(
                label_frame,
                text='⚠️',
                font=('Segoe UI', 12),
                bg='white',
                fg='#f39c12'
            )
            warning_icon.pack(side='left', padx=(0, 5))
            
            lbl = tk.Label(
                label_frame,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg='#e74c3c'
            )
            lbl.pack(side='left')
            
            reminder = tk.Label(
                label_frame,
                text='(Update this!)',
                font=('Segoe UI', 8),
                bg='white',
                fg='#e74c3c'
            )
            reminder.pack(side='left', padx=(5, 0))
        else:
            lbl = tk.Label(
                container,
                text=label,
                font=('Segoe UI', 10),
                bg='white',
                fg='#7f8c8d'
            )
            lbl.pack(anchor='w')
        
        # Entry field with emphasis styling if needed
        entry = tk.Entry(
            container,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=2 if emphasized else 1,
            bg='#fff3cd' if emphasized else '#f8f9fa',
            highlightthickness=2 if emphasized else 0,
            highlightbackground='#f39c12' if emphasized else '#f8f9fa',
            highlightcolor='#e74c3c' if emphasized else '#f8f9fa'
        )
        entry.pack(fill='x', pady=(5, 0), ipady=8)
        entry.insert(0, placeholder)
        
        # Store reference
        if not hasattr(self, 'form_fields'):
            self.form_fields = {}
        self.form_fields[label] = entry
        
        return entry
    
    def create_client_dropdown(self, parent, label):
        """Create a dropdown field for Client Name selection"""
        container = tk.Frame(parent, bg='white')
        container.pack(fill='x', padx=20, pady=8)
        
        lbl = tk.Label(
            container,
            text=label,
            font=('Segoe UI', 10),
            bg='white',
            fg='#7f8c8d'
        )
        lbl.pack(anchor='w')
        
        # Get client options from Projects folder
        client_options = self.get_client_options()
        
        # Create combobox (dropdown)
        from tkinter import ttk as tkttk
        dropdown = tkttk.Combobox(
            container,
            font=('Segoe UI', 11),
            values=client_options,
            state='readonly'
        )
        dropdown.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Set default value
        if client_options:
            # Try to find TAMICS10, otherwise use first
            if 'TAMICS10' in client_options:
                dropdown.set('TAMICS10')
            else:
                dropdown.set(client_options[0])
        
        # Store reference
        if not hasattr(self, 'form_fields'):
            self.form_fields = {}
        self.form_fields[label] = dropdown
        
        return dropdown
    
    def get_client_options(self):
        """Get list of existing client folders from Projects directory"""
        projects_dir = Path('Projects')
        
        if not projects_dir.exists():
            return []
        
        # Get all subdirectories in Projects folder
        clients = []
        for item in projects_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                clients.append(item.name)
        
        return sorted(clients)
    
    def create_dropdown_field(self, parent, label, emphasized=False):
        """Create a dropdown field for SFTP Server selection"""
        container = tk.Frame(parent, bg='white')
        container.pack(fill='x', padx=20, pady=8)
        
        # Add visual emphasis for important fields
        if emphasized:
            # Warning icon and emphasized label
            label_frame = tk.Frame(container, bg='white')
            label_frame.pack(anchor='w', fill='x')
            
            warning_icon = tk.Label(
                label_frame,
                text='⚠️',
                font=('Segoe UI', 12),
                bg='white',
                fg='#f39c12'
            )
            warning_icon.pack(side='left', padx=(0, 5))
            
            lbl = tk.Label(
                label_frame,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg='#e74c3c'
            )
            lbl.pack(side='left')
            
            reminder = tk.Label(
                label_frame,
                text='(Update this!)',
                font=('Segoe UI', 8),
                bg='white',
                fg='#e74c3c'
            )
            reminder.pack(side='left', padx=(5, 0))
        else:
            lbl = tk.Label(
                container,
                text=label,
                font=('Segoe UI', 10),
                bg='white',
                fg='#7f8c8d'
            )
            lbl.pack(anchor='w')
        
        # Get SFTP server options from .env.passwords files
        sftp_options = self.get_sftp_server_options()
        
        # Create combobox (dropdown)
        from tkinter import ttk as tkttk
        dropdown = tkttk.Combobox(
            container,
            font=('Segoe UI', 11),
            values=sftp_options,
            state='readonly'
        )
        dropdown.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Set default value
        if sftp_options:
            dropdown.set(sftp_options[0])
        
        # Apply emphasis styling
        if emphasized:
            dropdown.configure(background='#fff3cd')
        
        # Store reference
        if not hasattr(self, 'form_fields'):
            self.form_fields = {}
        self.form_fields[label] = dropdown
        
        return dropdown
    
    def get_sftp_server_options(self):
        """Extract SFTP server names from all .env.passwords files in Projects/*/Credentials/"""
        import os
        import re
        
        sftp_servers = []
        projects_dir = Path('Projects')
        
        if not projects_dir.exists():
            return ['Tamics10_AX1']  # Default fallback
        
        # Scan all client folders
        for client_folder in projects_dir.iterdir():
            if client_folder.is_dir():
                env_passwords_file = client_folder / 'Credentials' / '.env.passwords'
                if env_passwords_file.exists():
                    try:
                        with open(env_passwords_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Look for SFTP_SERVER_NAME=value
                            match = re.search(r'SFTP_SERVER_NAME\s*=\s*(.+)', content)
                            if match:
                                server_name = match.group(1).strip()
                                if server_name and server_name not in sftp_servers:
                                    sftp_servers.append(server_name)
                    except Exception as e:
                        print(f"Warning: Could not read {env_passwords_file}: {e}")
        
        # Return sorted list or default
        return sorted(sftp_servers) if sftp_servers else ['Tamics10_AX1']
    
    def create_text_field(self, parent, label, placeholder, height=3):
        """Create a modern text area field"""
        container = tk.Frame(parent, bg='white')
        container.pack(fill='x', padx=20, pady=8)
        
        lbl = tk.Label(
            container,
            text=label,
            font=('Segoe UI', 10),
            bg='white',
            fg='#7f8c8d'
        )
        lbl.pack(anchor='w')
        
        text = tk.Text(
            container,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa',
            height=height,
            wrap='word'
        )
        text.pack(fill='x', pady=(5, 0))
        text.insert('1.0', placeholder)
        
        # Store reference
        if not hasattr(self, 'text_fields'):
            self.text_fields = {}
        self.text_fields[label] = text
        
        return text
    
    def setup_mousewheel_handler(self):
        """Set up unified mousewheel handler that works for both sidebar and scenarios"""
        def _on_mousewheel(event):
            try:
                # Get mouse position
                x = self.root.winfo_pointerx()
                y = self.root.winfo_pointery()
                
                # Get widget under mouse
                widget = self.root.winfo_containing(x, y)
                
                if not widget:
                    return
                
                # Check if mouse is over sidebar or scenarios panel
                # Walk up the widget tree to find which container we're in
                current = widget
                in_sidebar = False
                in_scenarios = False
                
                while current:
                    if hasattr(self, 'sidebar_container') and current == self.sidebar_container:
                        in_sidebar = True
                        break
                    if hasattr(self, 'scenarios_panel') and current == self.scenarios_panel:
                        in_scenarios = True
                        break
                    try:
                        current = current.master
                    except:
                        break
                
                # Scroll the appropriate canvas
                if in_sidebar and hasattr(self, 'sidebar_canvas'):
                    self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                elif in_scenarios and hasattr(self, 'scenarios_canvas'):
                    self.scenarios_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                    
            except (tk.TclError, AttributeError):
                pass
        
        # Bind to root window - will work everywhere
        self.root.bind_all('<MouseWheel>', _on_mousewheel)
    
    def create_scenarios_panel(self, parent):
        """Create right panel with scenarios"""
        panel = tk.Frame(parent, bg='#f8f9fa')
        panel.pack(side='right', fill='both', expand=True, padx=(10, 20), pady=20)
        
        # Panel header
        header = tk.Frame(panel, bg='#f8f9fa')
        header.pack(fill='x', pady=(0, 15))
        
        title = tk.Label(
            header,
            text="✨ Test Scenarios",
            font=('Segoe UI', 16, 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        title.pack(side='left')
        
        subtitle = tk.Label(
            header,
            text="All scenarios are editable • Add/Delete as needed",
            font=('Segoe UI', 10),
            bg='#f8f9fa',
            fg='#7f8c8d'
        )
        subtitle.pack(side='left', padx=15)
        
        # Buttons container on the right
        buttons_frame = tk.Frame(header, bg='#f8f9fa')
        buttons_frame.pack(side='right')
        
        # Collapse All button
        collapse_all_btn = tk.Button(
            buttons_frame,
            text='▲ Collapse All',
            font=('Segoe UI', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=12,
            pady=6,
            cursor='hand2',
            command=self.collapse_all_scenarios
        )
        collapse_all_btn.pack(side='left', padx=5)
        
        # Expand All button
        expand_all_btn = tk.Button(
            buttons_frame,
            text='▼ Expand All',
            font=('Segoe UI', 9),
            bg='#7f8c8d',
            fg='white',
            relief='flat',
            padx=12,
            pady=6,
            cursor='hand2',
            command=self.expand_all_scenarios
        )
        expand_all_btn.pack(side='left', padx=5)
        
        # Add scenario button
        add_btn = tk.Button(
            buttons_frame,
            text='➕ Add Scenario',
            font=('Segoe UI', 11, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.add_new_scenario
        )
        add_btn.pack(side='left', padx=5)
        
        # Scrollable scenarios container
        canvas = tk.Canvas(panel, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(panel, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        # Store reference for refreshing
        self.scrollable_frame = scrollable_frame
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make canvas window expand with canvas
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', _configure_canvas)
        
        # Display scenarios
        for i, scenario in enumerate(self.scenarios):
            self.create_scenario_card(scrollable_frame, scenario, i)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Store canvas and panel references
        self.scenarios_canvas = canvas
        self.scenarios_panel = panel
        
        # Set up unified mousewheel handler after both canvases exist
        self.setup_mousewheel_handler()
    
    def refresh_scenarios_display(self):
        """Refresh the scenarios display"""
        if hasattr(self, 'scrollable_frame'):
            # Clear existing widgets
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            
            # Display all scenarios
            for i, scenario in enumerate(self.scenarios):
                self.create_scenario_card(self.scrollable_frame, scenario, i)
            
            # Update count badge
            if hasattr(self, 'count_badge'):
                self.count_badge.config(text=f"{len(self.scenarios)} scenarios")
    
    def scroll_to_scenario(self, scenario_index):
        """Scroll to make a specific scenario visible"""
        if hasattr(self, 'scenarios_canvas') and hasattr(self, 'scrollable_frame'):
            self.scenarios_canvas.update_idletasks()
            
            # Get all scenario cards
            cards = self.scrollable_frame.winfo_children()
            if scenario_index < len(cards):
                card = cards[scenario_index]
                
                # Get the card's position relative to the scrollable frame
                card_y = card.winfo_y()
                card_height = card.winfo_height()
                
                # Get canvas dimensions
                canvas_height = self.scenarios_canvas.winfo_height()
                scrollregion = self.scenarios_canvas.cget('scrollregion').split()
                if scrollregion:
                    total_height = int(scrollregion[3])
                    
                    # Calculate scroll position to center the card
                    scroll_position = (card_y + card_height / 2 - canvas_height / 2) / total_height
                    scroll_position = max(0, min(1, scroll_position))  # Clamp between 0 and 1
                    
                    self.scenarios_canvas.yview_moveto(scroll_position)
    
    def collapse_all_scenarios(self):
        """Collapse all scenarios"""
        for scenario in self.scenarios:
            scenario['_collapsed'] = True
        self.refresh_scenarios_display()
    
    def expand_all_scenarios(self):
        """Expand all scenarios"""
        for scenario in self.scenarios:
            scenario['_collapsed'] = False
        self.refresh_scenarios_display()
    
    def add_new_scenario(self):
        """Add a new blank scenario"""
        new_scenario = {
            'title': f'New Test Scenario {len(self.scenarios) + 1}',
            'description': 'Enter scenario description here',
            'test_steps': [
                {
                    'number': 1,
                    'description': 'Enter test step description',
                    'result': 'PASS'
                }
            ],
            'results': []
        }
        
        self.scenarios.append(new_scenario)
        self.refresh_scenarios_display()
        
        # Auto-scroll to bottom to show new scenario
        if hasattr(self, 'scenarios_canvas'):
            self.scenarios_canvas.update_idletasks()
            self.scenarios_canvas.yview_moveto(1.0)
    
    def delete_scenario(self, index):
        """Delete a scenario"""
        if len(self.scenarios) <= 1:
            messagebox.showwarning("Cannot Delete", "You must have at least one scenario")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Delete scenario '{self.scenarios[index]['title']}'?"):
            self.scenarios.pop(index)
            self.refresh_scenarios_display()
    
    def duplicate_scenario(self, index):
        """Duplicate a scenario"""
        original_scenario = self.scenarios[index]
        
        # Manually create a copy without widget references
        duplicated_scenario = {
            'title': f"{original_scenario['title']} (Copy)",
            'description': original_scenario['description'],
            'test_steps': [],
            'results': [],  # Clear results for new scenario
            '_collapsed': original_scenario.get('_collapsed', False)
        }
        
        # Copy test steps manually
        for step in original_scenario['test_steps']:
            new_step = {
                'number': step['number'],
                'description': step['description'],
                'result': step.get('result', 'PASS')
            }
            if 'screenshot' in step:
                new_step['screenshot'] = step['screenshot']
            duplicated_scenario['test_steps'].append(new_step)
        
        # Insert right after the original
        self.scenarios.insert(index + 1, duplicated_scenario)
        self.refresh_scenarios_display()
        
        # Scroll to show the duplicated scenario
        self.root.after(50, lambda: self.scroll_to_scenario(index + 1))
    
    def move_scenario_up(self, index):
        """Move scenario up in the list"""
        if index > 0:
            self.scenarios[index], self.scenarios[index-1] = self.scenarios[index-1], self.scenarios[index]
            self.refresh_scenarios_display()
            # Scroll to the new position
            self.root.after(50, lambda: self.scroll_to_scenario(index - 1))
    
    def move_scenario_down(self, index):
        """Move scenario down in the list"""
        if index < len(self.scenarios) - 1:
            self.scenarios[index], self.scenarios[index+1] = self.scenarios[index+1], self.scenarios[index]
            self.refresh_scenarios_display()
            # Scroll to the new position
            self.root.after(50, lambda: self.scroll_to_scenario(index + 1))
    
    def add_test_step(self, scenario_index):
        """Add a new test step to a scenario"""
        scenario = self.scenarios[scenario_index]
        new_step_number = len(scenario['test_steps']) + 1
        
        new_step = {
            'number': new_step_number,
            'description': 'Enter test step description',
            'result': 'PASS'
        }
        
        scenario['test_steps'].append(new_step)
        self.refresh_scenarios_display()
        
        # Scroll to keep the modified scenario visible
        self.root.after(50, lambda: self.scroll_to_scenario(scenario_index))
    
    def delete_test_step(self, scenario_index, step_index):
        """Delete a test step"""
        scenario = self.scenarios[scenario_index]
        
        if len(scenario['test_steps']) <= 1:
            messagebox.showwarning("Cannot Delete", "Scenario must have at least one test step")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Delete step {step_index + 1}?"):
            scenario['test_steps'].pop(step_index)
            
            # Renumber remaining steps
            for i, step in enumerate(scenario['test_steps']):
                step['number'] = i + 1
            
            self.refresh_scenarios_display()
            
            # Scroll to keep the modified scenario visible
            self.root.after(50, lambda: self.scroll_to_scenario(scenario_index))
    
    def duplicate_test_step(self, scenario_index, step_index):
        """Duplicate a test step"""
        scenario = self.scenarios[scenario_index]
        original_step = scenario['test_steps'][step_index]
        
        # Manually create a copy without widget references
        duplicated_step = {
            'number': original_step['number'],
            'description': original_step['description'],
            'result': original_step.get('result', 'PASS')
        }
        if 'screenshot' in original_step:
            duplicated_step['screenshot'] = original_step['screenshot']
        
        # Insert right after the original
        scenario['test_steps'].insert(step_index + 1, duplicated_step)
        
        # Renumber all steps
        for i, step in enumerate(scenario['test_steps']):
            step['number'] = i + 1
        
        self.refresh_scenarios_display()
        
        # Scroll to keep the modified scenario visible
        self.root.after(50, lambda: self.scroll_to_scenario(scenario_index))
    def setup_mousewheel_handler(self):
        """Set up unified mousewheel handler that works for both sidebar and scenarios"""
        def _on_mousewheel(event):
            try:
                # Get mouse position
                x = self.root.winfo_pointerx()
                y = self.root.winfo_pointery()

                # Get widget under mouse
                widget = self.root.winfo_containing(x, y)

                if not widget:
                    return

                # Check if mouse is over sidebar or scenarios panel
                # Walk up the widget tree to find which container we're in
                current = widget
                in_sidebar = False
                in_scenarios = False

                while current:
                    if hasattr(self, 'sidebar_container') and current == self.sidebar_container:
                        in_sidebar = True
                        break
                    if hasattr(self, 'scenarios_panel') and current == self.scenarios_panel:
                        in_scenarios = True
                        break
                    try:
                        current = current.master
                    except:
                        break

                # Scroll the appropriate canvas
                if in_sidebar and hasattr(self, 'sidebar_canvas'):
                    self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                elif in_scenarios and hasattr(self, 'scenarios_canvas'):
                    self.scenarios_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

            except (tk.TclError, AttributeError):
                pass

        # Bind to root window - will work everywhere
        self.root.bind_all('<MouseWheel>', _on_mousewheel)
    
    def create_scenario_card(self, parent, scenario, index):
        """Create a modern scenario card"""
        card = tk.Frame(
            parent,
            bg='white',
            relief='flat',
            borderwidth=1,
            highlightthickness=1,
            highlightbackground='#e0e0e0'
        )
        card.pack(fill='x', pady=10, padx=5)
        
        # Card header
        header = tk.Frame(card, bg='#3498db', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Scenario number badge
        badge = tk.Label(
            header,
            text=f"#{index + 1}",
            font=('Segoe UI', 12, 'bold'),
            bg='#2980b9',
            fg='white',
            padx=15,
            pady=10
        )
        badge.pack(side='left')
        
        # Scenario title (editable)
        title_entry = tk.Entry(
            header,
            font=('Segoe UI', 13, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            insertbackground='white'
        )
        title_entry.insert(0, scenario['title'])
        title_entry.pack(side='left', fill='x', expand=True, padx=15, pady=10)
        
        # Control buttons
        controls_frame = tk.Frame(header, bg='#3498db')
        controls_frame.pack(side='right', padx=5)
        
        # Duplicate button
        dup_btn = tk.Label(
            controls_frame,
            text='📋',
            font=('Segoe UI', 12),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            padx=8
        )
        dup_btn.pack(side='left')
        dup_btn.bind('<Button-1>', lambda e: self.duplicate_scenario(index))
        
        # Move up button
        if index > 0:
            up_btn = tk.Label(
                controls_frame,
                text='▲',
                font=('Segoe UI', 10),
                bg='#3498db',
                fg='white',
                cursor='hand2',
                padx=8
            )
            up_btn.pack(side='left')
            up_btn.bind('<Button-1>', lambda e: self.move_scenario_up(index))
        
        # Move down button
        if index < len(self.scenarios) - 1:
            down_btn = tk.Label(
                controls_frame,
                text='▼',
                font=('Segoe UI', 10),
                bg='#3498db',
                fg='white',
                cursor='hand2',
                padx=8
            )
            down_btn.pack(side='left')
            down_btn.bind('<Button-1>', lambda e: self.move_scenario_down(index))
        
        # Delete button
        delete_btn = tk.Label(
            controls_frame,
            text='🗑️',
            font=('Segoe UI', 12),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            padx=8
        )
        delete_btn.pack(side='left')
        delete_btn.bind('<Button-1>', lambda e: self.delete_scenario(index))
        
        # Expand/collapse button
        expand_btn = tk.Label(
            header,
            text='▼',
            font=('Segoe UI', 12),
            bg='#3498db',
            fg='white',
            cursor='hand2',
            padx=15
        )
        expand_btn.pack(side='right')
        
        # Card body (collapsible)
        body = tk.Frame(card, bg='white')
        body.pack(fill='both', padx=20, pady=15)
        
        # Description
        desc_label = tk.Label(
            body,
            text="Description:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#7f8c8d'
        )
        desc_label.pack(anchor='w', pady=(0, 5))
        
        desc_text = tk.Text(
            body,
            font=('Segoe UI', 10),
            bg='#f8f9fa',
            relief='solid',
            borderwidth=1,
            height=2,
            wrap='word'
        )
        desc_text.insert('1.0', scenario['description'])
        desc_text.pack(fill='x', pady=(0, 15))
        
        # Test steps
        steps_label = tk.Label(
            body,
            text=f"Test Steps ({len(scenario['test_steps'])} steps):",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#7f8c8d'
        )
        steps_label.pack(anchor='w', pady=(0, 10))
        
        # Add step button
        add_step_btn = tk.Button(
            body,
            text='➕ Add Step',
            font=('Segoe UI', 9),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=10,
            pady=4,
            cursor='hand2',
            command=lambda: self.add_test_step(index)
        )
        add_step_btn.pack(anchor='e', pady=(0, 10))
        
        # Steps container
        for step_idx, step in enumerate(scenario['test_steps']):
            self.create_step_row(body, step, index, step_idx)
        
        # Store references
        scenario['_widgets'] = {
            'title': title_entry,
            'description': desc_text,
            'body': body,
            'expand_btn': expand_btn
        }
        
        # Initialize collapsed state if not exists
        if '_collapsed' not in scenario:
            scenario['_collapsed'] = False
        
        # Apply initial state
        if scenario.get('_collapsed', False):
            body.pack_forget()
            expand_btn.config(text='▶')
        
        # Toggle collapse
        def toggle_collapse():
            if body.winfo_viewable():
                body.pack_forget()
                expand_btn.config(text='▶')
                scenario['_collapsed'] = True
            else:
                body.pack(fill='both', padx=20, pady=15)
                expand_btn.config(text='▼')
                scenario['_collapsed'] = False
        
        expand_btn.bind('<Button-1>', lambda e: toggle_collapse())
    
    def create_step_row(self, parent, step, scenario_index, step_index):
        """Create a modern step row"""
        step_frame = tk.Frame(parent, bg='#ecf0f1', relief='flat')
        step_frame.pack(fill='x', pady=5)
        
        # Step number
        num_label = tk.Label(
            step_frame,
            text=f"Step {step['number']}",
            font=('Segoe UI', 10, 'bold'),
            bg='#34495e',
            fg='white',
            padx=12,
            pady=8
        )
        num_label.pack(side='left')
        
        # Step content
        content_frame = tk.Frame(step_frame, bg='#ecf0f1')
        content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=8)
        
        # Description (editable)
        desc_entry = tk.Text(
            content_frame,
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            relief='flat',
            height=2,
            wrap='word'
        )
        desc_entry.insert('1.0', step['description'])
        desc_entry.pack(fill='x')
        
        # Expected result and screenshot
        result_frame = tk.Frame(content_frame, bg='#ecf0f1')
        result_frame.pack(fill='x', pady=(5, 0))
        
        result_label = tk.Label(
            result_frame,
            text="Expected:",
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        result_label.pack(side='left')
        
        result_entry = tk.Entry(
            result_frame,
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            relief='flat'
        )
        result_entry.insert(0, step.get('result', 'PASS'))
        result_entry.pack(side='left', fill='x', expand=True, padx=10)
        
        # Screenshot name (editable)
        screenshot_label = tk.Label(
            result_frame,
            text="📸",
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            fg='#95a5a6'
        )
        screenshot_label.pack(side='left', padx=(10, 5))
        
        screenshot_entry = tk.Entry(
            result_frame,
            font=('Segoe UI', 9),
            bg='#ecf0f1',
            relief='flat',
            width=25
        )
        screenshot_entry.insert(0, step.get('screenshot', ''))
        screenshot_entry.pack(side='left')
        
        # Check step description for specific keywords
        description_lower = step['description'].lower()
        show_upload_fields = 'upload' in description_lower
        show_sftp_path = any(keyword in description_lower for keyword in ['upload', 'sftp', 'file'])
        
        # Only show test data and browse button if step contains "upload"
        if show_upload_fields:
            # Test data file (optional)
            test_data_frame = tk.Frame(content_frame, bg='#ecf0f1')
            test_data_frame.pack(fill='x', pady=(5, 0))
            
            test_data_label = tk.Label(
                test_data_frame,
                text="📁 Test Data:",
                font=('Segoe UI', 9),
                bg='#ecf0f1',
                fg='#7f8c8d'
            )
            test_data_label.pack(side='left')
            
            test_data_entry = tk.Entry(
                test_data_frame,
                font=('Segoe UI', 9),
                bg='#ecf0f1',
                relief='flat'
            )
            test_data_entry.insert(0, step.get('test_data_file', ''))
            test_data_entry.pack(side='left', fill='x', expand=True, padx=10)
            
            # Browse button for test data
            def browse_test_data():
                # Get client name from form
                client_name = self.form_fields.get('Client Name', tk.Entry()).get().replace(' ', '')
                test_data_dir = f'Projects/{client_name}/TestScripts/test_data'
                
                # Check if directory exists
                from pathlib import Path
                if not Path(test_data_dir).exists():
                    test_data_dir = 'Projects'
                
                filename = filedialog.askopenfilename(
                    title="Select Test Data File",
                    initialdir=test_data_dir,
                    filetypes=[
                        ("CSV files", "*.csv"),
                        ("XML files", "*.xml"),
                        ("JSON files", "*.json"),
                        ("All files", "*.*")
                    ]
                )
                
                if filename:
                    # Store just the filename, not full path
                    from pathlib import Path
                    test_data_entry.delete(0, 'end')
                    test_data_entry.insert(0, Path(filename).name)
            
            browse_btn = tk.Button(
                test_data_frame,
                text='Browse...',
                font=('Segoe UI', 8),
                bg='#95a5a6',
                fg='white',
                relief='flat',
                padx=10,
                pady=2,
                cursor='hand2',
                command=browse_test_data
            )
            browse_btn.pack(side='left', padx=5)
            
            # Store test data entry reference
            step.setdefault('_widgets', {})['test_data_file'] = test_data_entry
        else:
            # Create hidden entry for non-upload steps so data collection still works
            test_data_entry = tk.Entry(content_frame)
            test_data_entry.insert(0, step.get('test_data_file', ''))
            test_data_entry.pack_forget()
            step.setdefault('_widgets', {})['test_data_file'] = test_data_entry
        
        # Only show SFTP path if step contains "upload", "sftp", or "file"
        if show_sftp_path:
            sftp_path_frame = tk.Frame(content_frame, bg='#ecf0f1')
            sftp_path_frame.pack(fill='x', pady=(5, 0))
            
            sftp_path_label = tk.Label(
                sftp_path_frame,
                text="📤 SFTP Path:",
                font=('Segoe UI', 9),
                bg='#ecf0f1',
                fg='#7f8c8d'
            )
            sftp_path_label.pack(side='left')
            
            sftp_path_entry = tk.Entry(
                sftp_path_frame,
                font=('Segoe UI', 9),
                bg='#ecf0f1',
                relief='flat'
            )
            sftp_path_entry.insert(0, step.get('sftp_remote_path', '/Infor_FSM/Inbound/'))
            sftp_path_entry.pack(side='left', fill='x', expand=True, padx=10)
            
            # Help text for SFTP path
            sftp_help = tk.Label(
                sftp_path_frame,
                text="(e.g., /Infor_FSM/Inbound/GLTransactionInterface)",
                font=('Segoe UI', 8),
                bg='#ecf0f1',
                fg='#95a5a6'
            )
            sftp_help.pack(side='left', padx=5)
            
            # Store SFTP path entry reference
            step.setdefault('_widgets', {})['sftp_remote_path'] = sftp_path_entry
        else:
            # Create hidden entry for non-file steps so data collection still works
            sftp_path_entry = tk.Entry(content_frame)
            sftp_path_entry.insert(0, step.get('sftp_remote_path', ''))
            sftp_path_entry.pack_forget()
            step.setdefault('_widgets', {})['sftp_remote_path'] = sftp_path_entry
        
        # Duplicate button
        duplicate_btn = tk.Label(
            step_frame,
            text='📋',
            font=('Segoe UI', 12),
            bg='#ecf0f1',
            fg='#3498db',
            cursor='hand2',
            padx=10
        )
        duplicate_btn.pack(side='right')
        duplicate_btn.bind('<Button-1>', lambda e: self.duplicate_test_step(scenario_index, step_index))
        
        # Delete button
        delete_btn = tk.Label(
            step_frame,
            text='🗑️',
            font=('Segoe UI', 12),
            bg='#ecf0f1',
            fg='#e74c3c',
            cursor='hand2',
            padx=10
        )
        delete_btn.pack(side='right')
        delete_btn.bind('<Button-1>', lambda e: self.delete_test_step(scenario_index, step_index))
        
        # Store widget references (test_data_file and sftp_remote_path already stored above)
        if '_widgets' not in step:
            step['_widgets'] = {}
        step['_widgets'].update({
            'description': desc_entry,
            'result': result_entry,
            'screenshot': screenshot_entry
        })
    
    def create_action_bar(self, parent):
        """Create bottom action bar with save buttons"""
        action_bar = tk.Frame(parent, bg='white', height=80)
        action_bar.pack(fill='x', side='bottom')
        action_bar.pack_propagate(False)
        
        # Separator line
        separator = tk.Frame(action_bar, bg='#e0e0e0', height=1)
        separator.pack(fill='x')
        
        # Buttons container
        btn_container = tk.Frame(action_bar, bg='white')
        btn_container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Save JSON button (primary)
        save_btn = tk.Button(
            btn_container,
            text='💾 Save Test Scenarios',
            font=('Segoe UI', 12, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            command=self.save_json
        )
        save_btn.pack(side='right', padx=5)
        
        # Preview button
        preview_btn = tk.Button(
            btn_container,
            text='👁️ Preview JSON',
            font=('Segoe UI', 11),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=25,
            pady=12,
            cursor='hand2',
            command=self.preview_json
        )
        preview_btn.pack(side='right', padx=5)
        
        # Info label
        info_label = tk.Label(
            btn_container,
            text=f"✨ {len(self.scenarios)} scenarios ready • All fields are editable",
            font=('Segoe UI', 10),
            bg='white',
            fg='#7f8c8d'
        )
        info_label.pack(side='left')
    
    def collect_data(self):
        """Collect all data from form"""
        # Get form fields
        interface_id = self.form_fields.get('Interface ID', tk.Entry()).get()
        interface_name = self.form_fields.get('Interface Name', tk.Entry()).get()
        
        # Get Client Name from dropdown (could be Entry or Combobox)
        client_widget = self.form_fields.get('Client Name')
        if hasattr(client_widget, 'current'):  # It's a Combobox
            client_name = client_widget.get()
        else:  # It's an Entry
            client_name = client_widget.get()
        
        author = self.form_fields.get('Author Name', tk.Entry()).get()
        environment = self.form_fields.get('Environment', tk.Entry()).get()
        file_channel_name = self.form_fields.get('File Channel Name', tk.Entry()).get()
        
        # Get SFTP Server from dropdown (could be Entry or Combobox)
        sftp_widget = self.form_fields.get('SFTP Server')
        if hasattr(sftp_widget, 'current'):  # It's a Combobox
            sftp_server = sftp_widget.get()
        else:  # It's an Entry
            sftp_server = sftp_widget.get()
        
        # Get text fields
        user_roles = self.text_fields.get('User Roles', tk.Text()).get('1.0', 'end').strip().split('\n')
        test_data = self.text_fields.get('Test Data', tk.Text()).get('1.0', 'end').strip()
        config_prereqs = self.text_fields.get('Configuration', tk.Text()).get('1.0', 'end').strip()
        
        # Collect updated scenarios
        updated_scenarios = []
        for scenario in self.scenarios:
            if '_widgets' in scenario:
                updated_scenario = {
                    'title': scenario['_widgets']['title'].get(),
                    'description': scenario['_widgets']['description'].get('1.0', 'end').strip(),
                    'test_steps': [],
                    'results': scenario.get('results', [])
                }
                
                # Collect updated steps
                for step in scenario['test_steps']:
                    if '_widgets' in step:
                        updated_step = {
                            'number': int(step['number']) if isinstance(step['number'], str) else step['number'],
                            'description': step['_widgets']['description'].get('1.0', 'end').strip(),
                            'result': step['_widgets']['result'].get()
                        }
                        # Get screenshot name from entry field
                        screenshot_name = step['_widgets']['screenshot'].get().strip()
                        if screenshot_name:
                            updated_step['screenshot'] = screenshot_name
                        # Get test data file from entry field
                        test_data_file = step['_widgets']['test_data_file'].get().strip()
                        if test_data_file:
                            updated_step['test_data_file'] = test_data_file
                        # Get SFTP remote path from entry field
                        sftp_remote_path = step['_widgets']['sftp_remote_path'].get().strip()
                        if sftp_remote_path:
                            updated_step['sftp_remote_path'] = sftp_remote_path
                        updated_scenario['test_steps'].append(updated_step)
                
                updated_scenarios.append(updated_scenario)
        
        return {
            'interface_id': interface_id,
            'interface_name': interface_name,
            'interface_type': self.interface_type,
            'client_name': client_name,
            'author': author,
            'environment': environment,
            'file_channel_name': file_channel_name,
            'sftp_server': sftp_server,
            'user_roles': [r for r in user_roles if r.strip()],
            'test_data_requirements': test_data,
            'configuration_prerequisites': config_prereqs,
            'scenarios': updated_scenarios
        }
    
    def validate_client_structure(self, client_folder, interface_type):
        """Validate that client folder has proper structure, offer to create if missing"""
        client_path = Path(f"Projects/{client_folder}")
        
        # Check if client folder exists
        if not client_path.exists():
            response = messagebox.askyesno(
                "Client Folder Missing",
                f"Client folder 'Projects/{client_folder}' does not exist.\n\n"
                f"Would you like to create the full project structure?"
            )
            if response:
                self.create_full_project_structure(client_folder)
                return True
            else:
                return False
        
        # Check if TestScripts/{interface_type} exists
        test_scripts_path = client_path / "TestScripts" / interface_type
        if not test_scripts_path.exists():
            response = messagebox.askyesno(
                "Folder Missing",
                f"Folder 'TestScripts/{interface_type}' does not exist for {client_folder}.\n\n"
                f"Create this folder?"
            )
            if response:
                test_scripts_path.mkdir(parents=True, exist_ok=True)
                return True
            else:
                return False
        
        return True
    
    def create_full_project_structure(self, client_folder):
        """Create complete project folder structure for a new client"""
        base_path = Path(f"Projects/{client_folder}")
        
        # Create all required subfolders
        folders = [
            "Credentials",
            "TestScripts/inbound",
            "TestScripts/outbound",
            "TestScripts/approval",
            "TestScripts/test_data",
            "TES-070/Generated_TES070s",
            "Temp"
        ]
        
        for folder in folders:
            (base_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Create README.md
        readme_content = f"""# {client_folder} Project

## Overview
This folder contains all testing artifacts for the {client_folder} FSM implementation.

## Structure
- `Credentials/` - FSM credentials (.env.fsm, .env.passwords, *.ionapi)
- `TestScripts/` - Test scenario JSON files and test data
  - `inbound/` - Inbound interface test scenarios
  - `outbound/` - Outbound interface test scenarios
  - `approval/` - Approval workflow test scenarios
  - `test_data/` - CSV/JSON test data files
- `TES-070/Generated_TES070s/` - Generated test results documents
- `Temp/` - Test execution screenshots and temporary files

## Getting Started
1. Add credentials to `Credentials/` folder
2. Create test scenarios using the Test Scenario Builder
3. Execute tests using Step 2 hook
4. Generate TES-070 documents using Step 3 hook
"""
        
        with open(base_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        messagebox.showinfo(
            "Project Created",
            f"Full project structure created for {client_folder}!\n\n"
            f"Don't forget to add credentials to the Credentials/ folder."
        )
    
    def preview_json(self):
        """Show JSON preview"""
        data = self.collect_data()
        
        # Create preview window
        preview_window = tk.Toplevel(self.root)
        preview_window.title("JSON Preview")
        preview_window.geometry("800x600")
        
        # Header
        header = tk.Frame(preview_window, bg='#2c3e50', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="📄 JSON Preview",
            font=('Segoe UI', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=15)
        
        # JSON content
        text_area = scrolledtext.ScrolledText(
            preview_window,
            font=('Consolas', 10),
            bg='#2c3e50',
            fg='#2ecc71',
            insertbackground='white',
            wrap='word'
        )
        text_area.pack(fill='both', expand=True, padx=20, pady=20)
        text_area.insert('1.0', json.dumps(data, indent=2))
        text_area.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(
            preview_window,
            text='Close',
            font=('Segoe UI', 11),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2',
            command=preview_window.destroy
        )
        close_btn.pack(pady=15)
    
    def save_json(self):
        """Save JSON file"""
        data = self.collect_data()
        
        if not data['interface_id']:
            messagebox.showwarning("Missing Data", "Please fill in Interface ID")
            return
        
        # Validate client folder structure
        client_folder = data['client_name'].replace(' ', '')
        if not self.validate_client_structure(client_folder, data['interface_type']):
            return
        
        # Determine save path
        default_path = f"Projects/{client_folder}/TestScripts/{data['interface_type']}"
        default_name = f"{data['interface_id']}_test_scenarios.json"
        
        filename = filedialog.asksaveasfilename(
            initialdir=default_path,
            initialfile=default_name,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Success message
            success_window = tk.Toplevel(self.root)
            success_window.title("Success!")
            success_window.configure(bg='white')
            
            # Set icon to match main window
            try:
                icon_path = Path(__file__).parent / 'app_icon.ico'
                if icon_path.exists():
                    success_window.iconbitmap(str(icon_path))
            except:
                pass
            
            # Set size and center on screen
            dialog_width = 600
            dialog_height = 450
            screen_width = success_window.winfo_screenwidth()
            screen_height = success_window.winfo_screenheight()
            x = (screen_width - dialog_width) // 2
            y = (screen_height - dialog_height) // 2
            success_window.geometry(f"{dialog_width}x{dialog_height}+{x}+{y}")
            
            # Success icon
            icon = tk.Label(
                success_window,
                text='✅',
                font=('Segoe UI', 48),
                bg='white'
            )
            icon.pack(pady=30)
            
            # Success message
            msg = tk.Label(
                success_window,
                text='Test Scenarios Saved Successfully!',
                font=('Segoe UI', 16, 'bold'),
                bg='white',
                fg='#2ecc71'
            )
            msg.pack()
            
            # File path with wrapping
            path_label = tk.Label(
                success_window,
                text=f"Saved to:\n{filename}",
                font=('Segoe UI', 10),
                bg='white',
                fg='#7f8c8d',
                wraplength=550,  # Wrap text to fit dialog width
                justify='center'
            )
            path_label.pack(pady=20)
            
            # Next steps
            next_steps = tk.Label(
                success_window,
                text="✨ Next: Click 'Step 2: Execute Tests in FSM' hook",
                font=('Segoe UI', 11),
                bg='white',
                fg='#3498db'
            )
            next_steps.pack(pady=10)
            
            # Close button
            close_btn = tk.Button(
                success_window,
                text='Done',
                font=('Segoe UI', 11, 'bold'),
                bg='#2ecc71',
                fg='white',
                relief='flat',
                padx=40,
                pady=12,
                cursor='hand2',
                command=success_window.destroy
            )
            close_btn.pack(pady=20)
    
    def get_predefined_scenarios(self):
        """Load predefined test scenario templates from JSON files"""
        import json
        import os
        
        # Get the templates directory path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.dirname(script_dir)
        templates_dir = os.path.join(workspace_root, '.kiro', 'templates')
        
        # Template file mapping
        template_files = {
            "Inbound Interface": "inbound_interface_template.json",
            "Outbound Interface": "outbound_interface_template.json",
            "Approval Workflow": "approval_workflow_template.json"
        }
        
        scenarios = {}
        
        # Load each template file
        for interface_type, filename in template_files.items():
            template_path = os.path.join(templates_dir, filename)
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    scenarios[interface_type] = data.get('scenarios', [])
            except FileNotFoundError:
                print(f"Warning: Template file not found: {template_path}")
                scenarios[interface_type] = []
            except json.JSONDecodeError as e:
                print(f"Warning: Invalid JSON in {template_path}: {e}")
                scenarios[interface_type] = []
        
        return scenarios


def main():
    root = tk.Tk()
    
    # Try to use modern theme
    if MODERN_THEME:
        root = ttk_boot.Window(themename="flatly")
    
    app = ModernTestScenarioBuilder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
