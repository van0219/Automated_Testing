# -*- coding: utf-8 -*-
"""
Enhanced Test Scenario Builder - Full CRUD Edition

A complete test scenario builder with add/delete/edit capabilities for
scenarios and test steps.

Features:
- Add/Delete scenarios
- Add/Delete test steps
- Move scenarios up/down
- Import existing JSON files
- All original features from modern version

Usage:
    python ReusableTools/test_scenario_builder_enhanced.py

Requirements:
    - tkinter (included with Python)
    - ttkbootstrap (pip install ttkbootstrap) - optional
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


class EnhancedTestScenarioBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("FSM Test Scenario Builder - Enhanced")
        
        # Set custom icon
        try:
            icon_path = Path(__file__).parent / 'app_icon.ico'
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
        except:
            pass
        
        # Maximize window
        self.root.state('zoomed')
        
        # Data storage
        self.scenarios = []
        self.interface_type_selected = False
        self.form_fields = {}
        self.text_fields = {}
        
        # Create main container
        self.create_welcome_screen()
    
    def create_welcome_screen(self):
        """Create welcome screen with interface type selection and import option"""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Header
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
            text="Create professional test scenarios with full control",
            font=('Segoe UI', 13),
            bg='#2c3e50',
            fg='#ecf0f1',
            pady=5
        )
        subtitle.pack(pady=(0, 20))
        
        # Content area
        content = tk.Frame(main_frame, bg='#f8f9fa')
        content.pack(fill='both', expand=True, padx=50, pady=30)
        
        # Welcome message
        welcome_text = tk.Label(
            content,
            text="Let's get started! What type of interface are you testing?",
            font=('Segoe UI', 16),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        welcome_text.pack(pady=(0, 30))
        
        # Interface type cards
        cards_frame = tk.Frame(content, bg='#f8f9fa')
        cards_frame.pack()
        
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
    
    def create_interface_card(self, parent, data, column):
        """Create interface type selection card"""
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
        icon_label = tk.Label(card, text=data['icon'], font=('Segoe UI', 48), bg='white')
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
        
        card.config(width=280, height=300)
        card.grid_propagate(False)
    
    def on_card_hover(self, card, color):
        """Card hover effect"""
        card.config(highlightbackground=color, highlightthickness=3, cursor='hand2')
    
    def on_card_leave(self, card):
        """Card leave effect"""
        card.config(highlightbackground='#ecf0f1', highlightthickness=2)
    
    def select_interface_type(self, interface_type):
        """Handle interface type selection"""
        self.interface_type = interface_type
        self.interface_type_selected = True
        
        # Load predefined scenarios
        self.scenarios = self.get_predefined_scenarios()[self.get_category_name(interface_type)]
        
        # Show main editor
        self.create_main_editor()
    
    def import_json(self):
        """Import existing JSON file"""
        filename = filedialog.askopenfilename(
            title="Select Test Scenario JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load data
                self.interface_type = data.get('interface_type', 'inbound')
                self.scenarios = data.get('scenarios', [])
                self.interface_type_selected = True
                
                # Store form data for later
                self.imported_data = data
                
                # Show main editor
                self.create_main_editor()
                
                # Populate form fields
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
            self.form_fields['Client Name'].delete(0, 'end')
            self.form_fields['Client Name'].insert(0, data.get('client_name', ''))
        
        if 'Author Name' in self.form_fields:
            self.form_fields['Author Name'].delete(0, 'end')
            self.form_fields['Author Name'].insert(0, data.get('author', ''))
        
        if 'Environment' in self.form_fields:
            self.form_fields['Environment'].delete(0, 'end')
            self.form_fields['Environment'].insert(0, data.get('environment', ''))
        
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
        
        # Content area
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True)
        
        # Left sidebar - Interface info
        self.create_sidebar(content_frame)
        
        # Right content - Scenarios
        self.create_scenarios_panel(content_frame)
        
        # Bottom action bar
        self.create_action_bar(main_frame)
    
    def create_top_bar(self, parent):
        """Create top navigation bar"""
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
        self.count_badge = tk.Label(
            top_bar,
            text=f"{len(self.scenarios)} scenarios",
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            padx=12,
            pady=4
        )
        self.count_badge.pack(side='left', padx=10)
    
    def update_scenario_count(self):
        """Update scenario count badge"""
        if hasattr(self, 'count_badge'):
            self.count_badge.config(text=f"{len(self.scenarios)} scenarios")
    
    def create_sidebar(self, parent):
        """Create left sidebar with interface information"""
        # Sidebar container
        sidebar_container = tk.Frame(parent, bg='white', width=350, relief='solid', borderwidth=1)
        sidebar_container.pack(side='left', fill='y', padx=(20, 10), pady=20)
        sidebar_container.pack_propagate(False)
        
        # Canvas for scrolling
        canvas = tk.Canvas(sidebar_container, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(
            sidebar_container,
            orient='vertical',
            command=canvas.yview,
            width=12,
            bg='#ecf0f1',
            troughcolor='#f8f9fa',
            activebackground='#95a5a6'
        )
        
        # Scrollable frame
        sidebar = tk.Frame(canvas, bg='white')
        sidebar.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0, 0), window=sidebar, anchor='nw', width=330)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Store references
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
        self.create_form_field(sidebar, "Client Name", "State of New Hampshire")
        self.create_form_field(sidebar, "Author Name", "")
        self.create_form_field(sidebar, "Environment", "NMR2N66J9P445R7P_AX4")
        
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
    
    def create_form_field(self, parent, label, placeholder):
        """Create a form field"""
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
        
        entry = tk.Entry(
            container,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        entry.pack(fill='x', pady=(5, 0), ipady=8)
        entry.insert(0, placeholder)
        
        self.form_fields[label] = entry
        return entry
    
    def create_text_field(self, parent, label, placeholder, height=3):
        """Create a text area field"""
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
        
        self.text_fields[label] = text
        return text
    
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
        
        # Add scenario button
        add_btn = tk.Button(
            header,
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
        add_btn.pack(side='right')
        
        # Scrollable scenarios container
        canvas = tk.Canvas(panel, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(panel, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas_window = canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Make canvas window expand
        def _configure_canvas(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind('<Configure>', _configure_canvas)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Store references
        self.scenarios_canvas = canvas
        self.scenarios_panel = panel
        
        # Display scenarios
        self.refresh_scenarios_display()
        
        # Set up mousewheel handler
        self.setup_mousewheel_handler()
    
    def refresh_scenarios_display(self):
        """Refresh the scenarios display"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Display all scenarios
        for i, scenario in enumerate(self.scenarios):
            self.create_scenario_card(self.scrollable_frame, scenario, i)
        
        # Update count
        self.update_scenario_count()
    
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

    def delete_scenario(self, index):
        """Delete a scenario"""
        if len(self.scenarios) <= 1:
            messagebox.showwarning("Cannot Delete", "You must have at least one scenario")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Delete scenario '{self.scenarios[index]['title']}'?"):
            self.scenarios.pop(index)
            self.refresh_scenarios_display()
    
    def move_scenario_up(self, index):
        """Move scenario up in the list"""
        if index > 0:
            self.scenarios[index], self.scenarios[index-1] = self.scenarios[index-1], self.scenarios[index]
            self.refresh_scenarios_display()
    
    def move_scenario_down(self, index):
        """Move scenario down in the list"""
        if index < len(self.scenarios) - 1:
            self.scenarios[index], self.scenarios[index+1] = self.scenarios[index+1], self.scenarios[index]
            self.refresh_scenarios_display()
    
    def create_scenario_card(self, parent, scenario, index):
        """Create a scenario card with full CRUD controls"""
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
        
        # Card body
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
        
        # Test steps header
        steps_header = tk.Frame(body, bg='white')
        steps_header.pack(fill='x', pady=(0, 10))
        
        steps_label = tk.Label(
            steps_header,
            text=f"Test Steps ({len(scenario['test_steps'])} steps):",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#7f8c8d'
        )
        steps_label.pack(side='left')
        
        # Add step button
        add_step_btn = tk.Button(
            steps_header,
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
        add_step_btn.pack(side='right')
        
        # Steps container
        steps_container = tk.Frame(body, bg='white')
        steps_container.pack(fill='x')
        
        # Display steps
        for step_idx, step in enumerate(scenario['test_steps']):
            self.create_step_row(steps_container, step, index, step_idx)
        
        # Store references
        scenario['_widgets'] = {
            'title': title_entry,
            'description': desc_text,
            'body': body,
            'expand_btn': expand_btn,
            'steps_container': steps_container
        }
        
        # Toggle collapse
        def toggle_collapse():
            if body.winfo_viewable():
                body.pack_forget()
                expand_btn.config(text='▶')
            else:
                body.pack(fill='both', padx=20, pady=15)
                expand_btn.config(text='▼')
        
        expand_btn.bind('<Button-1>', lambda e: toggle_collapse())
    
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
    
    def create_step_row(self, parent, step, scenario_index, step_index):
        """Create a test step row with delete button"""
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
        desc_text = tk.Text(
            content_frame,
            font=('Segoe UI', 10),
            bg='#ecf0f1',
            relief='flat',
            height=2,
            wrap='word'
        )
        desc_text.insert('1.0', step['description'])
        desc_text.pack(fill='x')
        
        # Expected result
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
        
        # Screenshot name
        if 'screenshot' in step:
            screenshot_label = tk.Label(
                result_frame,
                text=f"📸 {step['screenshot']}",
                font=('Segoe UI', 9),
                bg='#ecf0f1',
                fg='#95a5a6'
            )
            screenshot_label.pack(side='right', padx=10)
        
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
        
        # Store widget references
        step['_widgets'] = {
            'description': desc_text,
            'result': result_entry
        }
    
    def setup_mousewheel_handler(self):
        """Set up unified mousewheel handler"""
        def _on_mousewheel(event):
            try:
                x = self.root.winfo_pointerx()
                y = self.root.winfo_pointery()
                widget = self.root.winfo_containing(x, y)
                
                if not widget:
                    return
                
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
                
                if in_sidebar and hasattr(self, 'sidebar_canvas'):
                    self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                elif in_scenarios and hasattr(self, 'scenarios_canvas'):
                    self.scenarios_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
                    
            except (tk.TclError, AttributeError):
                pass
        
        self.root.bind_all('<MouseWheel>', _on_mousewheel)
    
    def create_action_bar(self, parent):
        """Create bottom action bar"""
        action_bar = tk.Frame(parent, bg='white', height=80)
        action_bar.pack(fill='x', side='bottom')
        action_bar.pack_propagate(False)
        
        # Separator
        separator = tk.Frame(action_bar, bg='#e0e0e0', height=1)
        separator.pack(fill='x')
        
        # Buttons container
        btn_container = tk.Frame(action_bar, bg='white')
        btn_container.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Save button
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
            text=f"✨ {len(self.scenarios)} scenarios • Full edit control",
            font=('Segoe UI', 10),
            bg='white',
            fg='#7f8c8d'
        )
        info_label.pack(side='left')

    def collect_data(self):
        """Collect all data from form"""
        interface_id = self.form_fields.get('Interface ID', tk.Entry()).get()
        interface_name = self.form_fields.get('Interface Name', tk.Entry()).get()
        client_name = self.form_fields.get('Client Name', tk.Entry()).get()
        author = self.form_fields.get('Author Name', tk.Entry()).get()
        environment = self.form_fields.get('Environment', tk.Entry()).get()
        
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
                            'number': step['number'],
                            'description': step['_widgets']['description'].get('1.0', 'end').strip(),
                            'result': step['_widgets']['result'].get()
                        }
                        if 'screenshot' in step:
                            updated_step['screenshot'] = step['screenshot']
                        updated_scenario['test_steps'].append(updated_step)
                
                updated_scenarios.append(updated_scenario)
        
        return {
            'interface_id': interface_id,
            'interface_name': interface_name,
            'interface_type': self.interface_type,
            'client_name': client_name,
            'author': author,
            'environment': environment,
            'user_roles': [r for r in user_roles if r.strip()],
            'test_data_requirements': test_data,
            'configuration_prerequisites': config_prereqs,
            'scenarios': updated_scenarios
        }
    
    def preview_json(self):
        """Show JSON preview"""
        data = self.collect_data()
        
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
        
        # Determine save path
        client_folder = data['client_name'].replace(' ', '')
        default_path = f"Projects/{client_folder}/TestScripts/{data['interface_type']}"
        default_name = f"{data['interface_id']}_test_scenarios.json"
        
        # Create directory
        Path(default_path).mkdir(parents=True, exist_ok=True)
        
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
            success_window.geometry("500x300")
            success_window.configure(bg='white')
            
            icon = tk.Label(
                success_window,
                text='✅',
                font=('Segoe UI', 48),
                bg='white'
            )
            icon.pack(pady=30)
            
            msg = tk.Label(
                success_window,
                text='Test Scenarios Saved Successfully!',
                font=('Segoe UI', 16, 'bold'),
                bg='white',
                fg='#2ecc71'
            )
            msg.pack()
            
            path_label = tk.Label(
                success_window,
                text=f"Saved to:\n{filename}",
                font=('Segoe UI', 10),
                bg='white',
                fg='#7f8c8d'
            )
            path_label.pack(pady=20)
            
            next_steps = tk.Label(
                success_window,
                text="✨ Next: Click 'Step 2: Execute Tests in FSM' hook",
                font=('Segoe UI', 11),
                bg='white',
                fg='#3498db'
            )
            next_steps.pack(pady=10)
            
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
        import os
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.dirname(script_dir)
        templates_dir = os.path.join(workspace_root, '.kiro', 'templates')
        
        template_files = {
            "Inbound Interface": "inbound_interface_template.json",
            "Outbound Interface": "outbound_interface_template.json",
            "Approval Workflow": "approval_workflow_template.json"
        }
        
        scenarios = {}
        
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
    try:
        print("Starting Enhanced Test Scenario Builder...")
        root = tk.Tk()
        
        if MODERN_THEME:
            print("Using modern theme...")
            root = ttk_boot.Window(themename="flatly")
        else:
            print("Using standard tkinter...")
        
        print("Creating app...")
        app = EnhancedTestScenarioBuilder(root)
        print("Starting mainloop...")
        root.mainloop()
        print("App closed normally")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Script started!", flush=True)
    main()
