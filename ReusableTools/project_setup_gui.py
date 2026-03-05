"""
Project Setup GUI - Multi-Tenant Support

A modern GUI for setting up FSM testing projects with support for:
- Multiple tenants (TST, PP1, PRD)
- Multiple user credentials per tenant
- Multiple SFTP servers
- Multiple file channels

Usage:
    python ReusableTools/project_setup_gui.py

Requirements:
    - tkinter (included with Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from pathlib import Path
from datetime import datetime
import os


class ProjectSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FSM Project Setup")
        
        # Set custom icon
        self.icon_path = None
        try:
            icon_path = Path(__file__).parent / 'app_icon.ico'
            if icon_path.exists():
                self.icon_path = str(icon_path)
                self.root.iconbitmap(self.icon_path)
        except:
            pass
        
        # Maximize window
        self.root.state('zoomed')
        
        # Data storage
        self.project_data = {
            'project_name': '',
            'tenants': [],
            'sftp_servers': [],
            'file_channels': []
        }
        
        # Create welcome screen
        self.create_welcome_screen()
    
    def center_dialog(self, dialog):
        """Center dialog on screen"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_dialog_icon(self, dialog):
        """Set app icon for dialog"""
        if self.icon_path:
            try:
                dialog.iconbitmap(self.icon_path)
            except:
                pass

    def create_welcome_screen(self):
        """Create welcome screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg='#2c3e50', height=140)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="🚀 FSM Project Setup",
            font=('Segoe UI', 28, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=(25, 5))
        
        subtitle = tk.Label(
            header,
            text="Configure multi-tenant projects with ease",
            font=('Segoe UI', 13),
            bg='#2c3e50',
            fg='#ecf0f1',
            pady=5
        )
        subtitle.pack(pady=(0, 20))
        
        # Content
        content = tk.Frame(main_frame, bg='#f8f9fa')
        content.pack(fill='both', expand=True, padx=50, pady=50)
        
        welcome_text = tk.Label(
            content,
            text="Let's set up your FSM testing project!",
            font=('Segoe UI', 16),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        welcome_text.pack(pady=(0, 40))
        
        # Options
        options_frame = tk.Frame(content, bg='#f8f9fa')
        options_frame.pack()
        
        # New project button
        new_btn = tk.Button(
            options_frame,
            text='➕ Create New Project',
            font=('Segoe UI', 14, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=40,
            pady=20,
            cursor='hand2',
            command=self.start_new_project
        )
        new_btn.pack(pady=10)
        
        # Import button
        import_btn = tk.Button(
            options_frame,
            text='📂 Import Existing Configuration',
            font=('Segoe UI', 12),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2',
            command=self.import_config
        )
        import_btn.pack(pady=10)

    def start_new_project(self):
        """Start new project setup"""
        # Ask for project name first
        dialog = tk.Toplevel(self.root)
        dialog.title("Project Name")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        tk.Label(
            dialog,
            text="Enter Project Name:",
            font=('Segoe UI', 12)
        ).pack(pady=20)
        
        name_entry = tk.Entry(dialog, font=('Segoe UI', 12), width=30)
        name_entry.pack(pady=10)
        name_entry.focus()
        
        def confirm():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Project name cannot be empty")
                return
            
            # Check if project already exists
            if Path(f"Projects/{name}").exists():
                if not messagebox.askyesno("Project Exists", 
                    f"Project '{name}' already exists. Continue editing?"):
                    return
            
            self.project_data['project_name'] = name
            dialog.destroy()
            self.create_main_editor()
        
        tk.Button(
            dialog,
            text='Continue',
            font=('Segoe UI', 11),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=confirm
        ).pack(pady=20)
        
        name_entry.bind('<Return>', lambda e: confirm())
    
    def import_config(self):
        """Import existing project configuration"""
        filename = filedialog.askopenfilename(
            title="Select Project Configuration",
            initialdir="Projects",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.project_data = json.load(f)
                self.create_main_editor()
            except Exception as e:
                messagebox.showerror("Import Error", f"Failed to import:\n{str(e)}")

    def create_main_editor(self):
        """Create main editor interface"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)
        
        # Top bar
        self.create_top_bar(main_frame)
        
        # Content with tabs
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create notebook (tabs)
        notebook = ttk.Notebook(content_frame)
        notebook.pack(fill='both', expand=True)
        
        # Tab 1: Tenants
        tenants_tab = tk.Frame(notebook, bg='white')
        notebook.add(tenants_tab, text='🏢 Tenants')
        self.create_tenants_tab(tenants_tab)
        
        # Tab 2: SFTP Servers
        sftp_tab = tk.Frame(notebook, bg='white')
        notebook.add(sftp_tab, text='🌐 SFTP Servers')
        self.create_sftp_tab(sftp_tab)
        
        # Tab 3: File Channels
        channels_tab = tk.Frame(notebook, bg='white')
        notebook.add(channels_tab, text='📁 File Channels')
        self.create_channels_tab(channels_tab)
        
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
        
        # Project name
        title = tk.Label(
            top_bar,
            text=f"📋 {self.project_data['project_name']}",
            font=('Segoe UI', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(side='left', padx=10)
        
        # Counts
        counts_frame = tk.Frame(top_bar, bg='#2c3e50')
        counts_frame.pack(side='left', padx=20)
        
        self.tenant_count_label = tk.Label(
            counts_frame,
            text=f"{len(self.project_data['tenants'])} tenants",
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            padx=12,
            pady=4
        )
        self.tenant_count_label.pack(side='left', padx=5)
        
        self.sftp_count_label = tk.Label(
            counts_frame,
            text=f"{len(self.project_data['sftp_servers'])} SFTP",
            font=('Segoe UI', 10),
            bg='#2ecc71',
            fg='white',
            padx=12,
            pady=4
        )
        self.sftp_count_label.pack(side='left', padx=5)
        
        self.channel_count_label = tk.Label(
            counts_frame,
            text=f"{len(self.project_data['file_channels'])} channels",
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            padx=12,
            pady=4
        )
        self.channel_count_label.pack(side='left', padx=5)

    def update_counts(self):
        """Update count badges"""
        self.tenant_count_label.config(text=f"{len(self.project_data['tenants'])} tenants")
        self.sftp_count_label.config(text=f"{len(self.project_data['sftp_servers'])} SFTP")
        self.channel_count_label.config(text=f"{len(self.project_data['file_channels'])} channels")
    
    def create_tenants_tab(self, parent):
        """Create tenants management tab"""
        # Header
        header = tk.Frame(parent, bg='white')
        header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            header,
            text="🏢 FSM Tenants",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        tk.Button(
            header,
            text='➕ Add Tenant',
            font=('Segoe UI', 11, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.add_tenant
        ).pack(side='right')
        
        # Scrollable list
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.tenants_frame = tk.Frame(canvas, bg='white')
        
        self.tenants_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.tenants_frame, anchor='nw', width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        # Display existing tenants
        self.refresh_tenants_display()
    
    def refresh_tenants_display(self):
        """Refresh tenants display"""
        for widget in self.tenants_frame.winfo_children():
            widget.destroy()
        
        for i, tenant in enumerate(self.project_data['tenants']):
            self.create_tenant_card(self.tenants_frame, tenant, i)
    
    def create_tenant_card(self, parent, tenant, index):
        """Create tenant card"""
        card = tk.Frame(parent, bg='#ecf0f1', relief='solid', borderwidth=1)
        card.pack(fill='x', pady=10)
        
        # Header
        header = tk.Frame(card, bg='#3498db')
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=f"🏢 {tenant.get('environment', 'TST')} - {tenant.get('tenant_id', 'N/A')}",
            font=('Segoe UI', 13, 'bold'),
            bg='#3498db',
            fg='white',
            padx=15,
            pady=10
        ).pack(side='left')
        
        # Controls
        controls = tk.Frame(header, bg='#3498db')
        controls.pack(side='right', padx=10)
        
        tk.Button(
            controls,
            text='✏️ Edit',
            font=('Segoe UI', 9),
            bg='#2980b9',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=lambda: self.edit_tenant(index)
        ).pack(side='left', padx=2)
        
        tk.Button(
            controls,
            text='🗑️ Delete',
            font=('Segoe UI', 9),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=lambda: self.delete_tenant(index)
        ).pack(side='left', padx=2)
        
        # Body
        body = tk.Frame(card, bg='white')
        body.pack(fill='x', padx=15, pady=15)
        
        # Display info in grid
        info = [
            ('FSM URL:', tenant.get('fsm_url', 'N/A')),
            ('Username:', tenant.get('fsm_username', 'N/A')),
            ('Password:', '•' * 8 if tenant.get('fsm_password') else 'Not set'),
        ]
        
        for row, (label, value) in enumerate(info):
            tk.Label(
                body,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg='#7f8c8d'
            ).grid(row=row, column=0, sticky='w', padx=5, pady=5)
            
            tk.Label(
                body,
                text=value,
                font=('Segoe UI', 10),
                bg='white',
                fg='#2c3e50'
            ).grid(row=row, column=1, sticky='w', padx=5, pady=5)

    def add_tenant(self):
        """Add new tenant"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Tenant")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        # Form
        form = tk.Frame(dialog, bg='white')
        form.pack(fill='both', expand=True, padx=20, pady=20)
        
        fields = {}
        
        # Environment
        tk.Label(form, text="Environment:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        env_combo = ttk.Combobox(form, values=['TRN', 'TST', 'PP1', 'PRD'], width=30)
        env_combo.set('TST')
        env_combo.grid(row=0, column=1, pady=5)
        fields['environment'] = env_combo
        
        # Tenant ID
        tk.Label(form, text="Tenant ID:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        tenant_id_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        tenant_id_entry.grid(row=1, column=1, pady=5)
        fields['tenant_id'] = tenant_id_entry
        
        # FSM URL
        tk.Label(form, text="FSM Portal URL:", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        url_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        url_entry.grid(row=2, column=1, pady=5)
        fields['fsm_url'] = url_entry
        
        # Username
        tk.Label(form, text="FSM Username:", font=('Segoe UI', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        username_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        username_entry.grid(row=3, column=1, pady=5)
        fields['fsm_username'] = username_entry
        
        # Password
        tk.Label(form, text="FSM Password:", font=('Segoe UI', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        password_entry = tk.Entry(form, font=('Segoe UI', 10), width=32, show='•')
        password_entry.grid(row=4, column=1, pady=5)
        fields['fsm_password'] = password_entry
        
        # ION API file (optional)
        tk.Label(form, text="ION API File:", font=('Segoe UI', 10), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        ionapi_frame = tk.Frame(form, bg='white')
        ionapi_frame.grid(row=5, column=1, pady=5, sticky='w')
        ionapi_entry = tk.Entry(ionapi_frame, font=('Segoe UI', 10), width=22)
        ionapi_entry.pack(side='left')
        tk.Button(
            ionapi_frame,
            text='Browse',
            font=('Segoe UI', 9),
            command=lambda: self.browse_ionapi(ionapi_entry)
        ).pack(side='left', padx=5)
        fields['ionapi_file'] = ionapi_entry
        
        def save():
            tenant = {
                'environment': env_combo.get(),
                'tenant_id': tenant_id_entry.get().strip(),
                'fsm_url': url_entry.get().strip(),
                'fsm_username': username_entry.get().strip(),
                'fsm_password': password_entry.get().strip(),
                'ionapi_file': ionapi_entry.get().strip()
            }
            
            if not tenant['tenant_id'] or not tenant['fsm_url']:
                messagebox.showerror("Error", "Tenant ID and FSM URL are required")
                return
            
            self.project_data['tenants'].append(tenant)
            self.refresh_tenants_display()
            self.update_counts()
            dialog.destroy()
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text='Cancel',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text='Save',
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=save
        ).pack(side='right', padx=5)
    
    def browse_ionapi(self, entry_widget):
        """Browse for ION API file"""
        filename = filedialog.askopenfilename(
            title="Select ION API File",
            filetypes=[("ION API files", "*.ionapi"), ("All files", "*.*")]
        )
        if filename:
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, filename)
    
    def edit_tenant(self, index):
        """Edit existing tenant"""
        tenant = self.project_data['tenants'][index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Tenant")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        # Similar form as add_tenant but pre-filled
        form = tk.Frame(dialog, bg='white')
        form.pack(fill='both', expand=True, padx=20, pady=20)
        
        fields = {}
        
        # Environment
        tk.Label(form, text="Environment:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        env_combo = ttk.Combobox(form, values=['TST', 'PP1', 'PRD', 'DEV', 'TRN', 'AX1', 'AX2', 'AX3', 'AX4', 'AX5', 'AX6'], width=30)
        env_combo.set(tenant.get('environment', 'TST'))
        env_combo.grid(row=0, column=1, pady=5)
        fields['environment'] = env_combo
        
        # Tenant ID
        tk.Label(form, text="Tenant ID:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        tenant_id_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        tenant_id_entry.insert(0, tenant.get('tenant_id', ''))
        tenant_id_entry.grid(row=1, column=1, pady=5)
        fields['tenant_id'] = tenant_id_entry
        
        # FSM URL
        tk.Label(form, text="FSM Portal URL:", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        url_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        url_entry.insert(0, tenant.get('fsm_url', ''))
        url_entry.grid(row=2, column=1, pady=5)
        fields['fsm_url'] = url_entry
        
        # Username
        tk.Label(form, text="FSM Username:", font=('Segoe UI', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        username_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        username_entry.insert(0, tenant.get('fsm_username', ''))
        username_entry.grid(row=3, column=1, pady=5)
        fields['fsm_username'] = username_entry
        
        # Password
        tk.Label(form, text="FSM Password:", font=('Segoe UI', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        password_entry = tk.Entry(form, font=('Segoe UI', 10), width=32, show='•')
        password_entry.insert(0, tenant.get('fsm_password', ''))
        password_entry.grid(row=4, column=1, pady=5)
        fields['fsm_password'] = password_entry
        
        # ION API file
        tk.Label(form, text="ION API File:", font=('Segoe UI', 10), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        ionapi_frame = tk.Frame(form, bg='white')
        ionapi_frame.grid(row=5, column=1, pady=5, sticky='w')
        ionapi_entry = tk.Entry(ionapi_frame, font=('Segoe UI', 10), width=22)
        ionapi_entry.insert(0, tenant.get('ionapi_file', ''))
        ionapi_entry.pack(side='left')
        tk.Button(
            ionapi_frame,
            text='Browse',
            font=('Segoe UI', 9),
            command=lambda: self.browse_ionapi(ionapi_entry)
        ).pack(side='left', padx=5)
        fields['ionapi_file'] = ionapi_entry
        
        def save():
            self.project_data['tenants'][index] = {
                'environment': env_combo.get(),
                'tenant_id': tenant_id_entry.get().strip(),
                'fsm_url': url_entry.get().strip(),
                'fsm_username': username_entry.get().strip(),
                'fsm_password': password_entry.get().strip(),
                'ionapi_file': ionapi_entry.get().strip()
            }
            
            self.refresh_tenants_display()
            dialog.destroy()
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text='Cancel',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text='Save',
            font=('Segoe UI', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=save
        ).pack(side='right', padx=5)
    
    def delete_tenant(self, index):
        """Delete tenant"""
        tenant = self.project_data['tenants'][index]
        if messagebox.askyesno("Confirm Delete", 
            f"Delete tenant '{tenant.get('tenant_id', 'N/A')}'?"):
            self.project_data['tenants'].pop(index)
            self.refresh_tenants_display()
            self.update_counts()

    def create_sftp_tab(self, parent):
        """Create SFTP servers management tab"""
        # Header
        header = tk.Frame(parent, bg='white')
        header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            header,
            text="🌐 SFTP Servers",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        tk.Button(
            header,
            text='➕ Add SFTP Server',
            font=('Segoe UI', 11, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.add_sftp_server
        ).pack(side='right')
        
        # Scrollable list
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.sftp_frame = tk.Frame(canvas, bg='white')
        
        self.sftp_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.sftp_frame, anchor='nw', width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        # Display existing SFTP servers
        self.refresh_sftp_display()
    
    def refresh_sftp_display(self):
        """Refresh SFTP servers display"""
        for widget in self.sftp_frame.winfo_children():
            widget.destroy()
        
        for i, sftp in enumerate(self.project_data['sftp_servers']):
            self.create_sftp_card(self.sftp_frame, sftp, i)
    
    def create_sftp_card(self, parent, sftp, index):
        """Create SFTP server card"""
        card = tk.Frame(parent, bg='#ecf0f1', relief='solid', borderwidth=1)
        card.pack(fill='x', pady=10)
        
        # Header
        header = tk.Frame(card, bg='#2ecc71')
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=f"🌐 {sftp.get('server_name', 'N/A')}",
            font=('Segoe UI', 13, 'bold'),
            bg='#2ecc71',
            fg='white',
            padx=15,
            pady=10
        ).pack(side='left')
        
        # Controls
        controls = tk.Frame(header, bg='#2ecc71')
        controls.pack(side='right', padx=10)
        
        tk.Button(
            controls,
            text='✏️ Edit',
            font=('Segoe UI', 9),
            bg='#27ae60',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=lambda: self.edit_sftp_server(index)
        ).pack(side='left', padx=2)
        
        tk.Button(
            controls,
            text='🗑️ Delete',
            font=('Segoe UI', 9),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=lambda: self.delete_sftp_server(index)
        ).pack(side='left', padx=2)
        
        # Body
        body = tk.Frame(card, bg='white')
        body.pack(fill='x', padx=15, pady=15)
        
        # Display info
        info = [
            ('Host:', sftp.get('host', 'N/A')),
            ('Port:', sftp.get('port', '22')),
            ('Username:', sftp.get('username', 'N/A')),
            ('Password:', '•' * 8 if sftp.get('password') else 'Not set'),
            ('Inbound Path:', sftp.get('inbound_path', 'N/A')),
            ('Outbound Path:', sftp.get('outbound_path', 'N/A')),
        ]
        
        for row, (label, value) in enumerate(info):
            tk.Label(
                body,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg='#7f8c8d'
            ).grid(row=row, column=0, sticky='w', padx=5, pady=5)
            
            tk.Label(
                body,
                text=value,
                font=('Segoe UI', 10),
                bg='white',
                fg='#2c3e50'
            ).grid(row=row, column=1, sticky='w', padx=5, pady=5)

    def add_sftp_server(self):
        """Add new SFTP server"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add SFTP Server")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        # Form
        form = tk.Frame(dialog, bg='white')
        form.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Server Name
        tk.Label(form, text="Server Name:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        name_entry.grid(row=0, column=1, pady=5)
        
        # Host
        tk.Label(form, text="Host:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        host_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        host_entry.insert(0, 'sftp.inforcloudsuite.com')
        host_entry.grid(row=1, column=1, pady=5)
        
        # Port
        tk.Label(form, text="Port:", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        port_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        port_entry.insert(0, '22')
        port_entry.grid(row=2, column=1, pady=5)
        
        # Username
        tk.Label(form, text="Username:", font=('Segoe UI', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        username_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        username_entry.grid(row=3, column=1, pady=5)
        
        # Password
        tk.Label(form, text="Password:", font=('Segoe UI', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        password_entry = tk.Entry(form, font=('Segoe UI', 10), width=32, show='•')
        password_entry.grid(row=4, column=1, pady=5)
        
        # Inbound Path
        tk.Label(form, text="Inbound Path:", font=('Segoe UI', 10), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        inbound_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        inbound_entry.insert(0, '/Infor_FSM/Inbound/')
        inbound_entry.grid(row=5, column=1, pady=5)
        
        # Outbound Path
        tk.Label(form, text="Outbound Path:", font=('Segoe UI', 10), bg='white').grid(row=6, column=0, sticky='w', pady=5)
        outbound_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        outbound_entry.insert(0, '/Infor_FSM/Outbound/')
        outbound_entry.grid(row=6, column=1, pady=5)
        
        def save():
            sftp = {
                'server_name': name_entry.get().strip(),
                'host': host_entry.get().strip(),
                'port': port_entry.get().strip(),
                'username': username_entry.get().strip(),
                'password': password_entry.get().strip(),
                'inbound_path': inbound_entry.get().strip(),
                'outbound_path': outbound_entry.get().strip()
            }
            
            if not sftp['server_name'] or not sftp['host']:
                messagebox.showerror("Error", "Server name and host are required")
                return
            
            self.project_data['sftp_servers'].append(sftp)
            self.refresh_sftp_display()
            self.update_counts()
            dialog.destroy()
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text='Cancel',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text='Save',
            font=('Segoe UI', 10),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=save
        ).pack(side='right', padx=5)
    
    def edit_sftp_server(self, index):
        """Edit SFTP server - similar to add but pre-filled"""
        sftp = self.project_data['sftp_servers'][index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit SFTP Server")
        dialog.geometry("500x500")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        form = tk.Frame(dialog, bg='white')
        form.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Pre-fill form fields
        tk.Label(form, text="Server Name:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        name_entry.insert(0, sftp.get('server_name', ''))
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form, text="Host:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        host_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        host_entry.insert(0, sftp.get('host', ''))
        host_entry.grid(row=1, column=1, pady=5)
        
        tk.Label(form, text="Port:", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        port_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        port_entry.insert(0, sftp.get('port', '22'))
        port_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(form, text="Username:", font=('Segoe UI', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        username_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        username_entry.insert(0, sftp.get('username', ''))
        username_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(form, text="Password:", font=('Segoe UI', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        password_entry = tk.Entry(form, font=('Segoe UI', 10), width=32, show='•')
        password_entry.insert(0, sftp.get('password', ''))
        password_entry.grid(row=4, column=1, pady=5)
        
        tk.Label(form, text="Inbound Path:", font=('Segoe UI', 10), bg='white').grid(row=5, column=0, sticky='w', pady=5)
        inbound_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        inbound_entry.insert(0, sftp.get('inbound_path', ''))
        inbound_entry.grid(row=5, column=1, pady=5)
        
        tk.Label(form, text="Outbound Path:", font=('Segoe UI', 10), bg='white').grid(row=6, column=0, sticky='w', pady=5)
        outbound_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        outbound_entry.insert(0, sftp.get('outbound_path', ''))
        outbound_entry.grid(row=6, column=1, pady=5)
        
        def save():
            self.project_data['sftp_servers'][index] = {
                'server_name': name_entry.get().strip(),
                'host': host_entry.get().strip(),
                'port': port_entry.get().strip(),
                'username': username_entry.get().strip(),
                'password': password_entry.get().strip(),
                'inbound_path': inbound_entry.get().strip(),
                'outbound_path': outbound_entry.get().strip()
            }
            
            self.refresh_sftp_display()
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text='Cancel',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text='Save',
            font=('Segoe UI', 10),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=save
        ).pack(side='right', padx=5)
    
    def delete_sftp_server(self, index):
        """Delete SFTP server"""
        sftp = self.project_data['sftp_servers'][index]
        if messagebox.askyesno("Confirm Delete", 
            f"Delete SFTP server '{sftp.get('server_name', 'N/A')}'?"):
            self.project_data['sftp_servers'].pop(index)
            self.refresh_sftp_display()
            self.update_counts()

    def create_channels_tab(self, parent):
        """Create file channels management tab"""
        # Header
        header = tk.Frame(parent, bg='white')
        header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            header,
            text="📁 File Channels",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        tk.Button(
            header,
            text='➕ Add File Channel',
            font=('Segoe UI', 11, 'bold'),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.add_file_channel
        ).pack(side='right')
        
        # Scrollable list
        canvas = tk.Canvas(parent, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
        self.channels_frame = tk.Frame(canvas, bg='white')
        
        self.channels_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=self.channels_frame, anchor='nw', width=1000)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=20)
        scrollbar.pack(side='right', fill='y')
        
        # Display existing channels
        self.refresh_channels_display()
    
    def refresh_channels_display(self):
        """Refresh file channels display"""
        for widget in self.channels_frame.winfo_children():
            widget.destroy()
        
        for i, channel in enumerate(self.project_data['file_channels']):
            self.create_channel_card(self.channels_frame, channel, i)
    
    def create_channel_card(self, parent, channel, index):
        """Create file channel card"""
        card = tk.Frame(parent, bg='#ecf0f1', relief='solid', borderwidth=1)
        card.pack(fill='x', pady=10)
        
        # Header
        header = tk.Frame(card, bg='#e74c3c')
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=f"📁 {channel.get('channel_name', 'N/A')}",
            font=('Segoe UI', 13, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=15,
            pady=10
        ).pack(side='left')
        
        # Controls
        controls = tk.Frame(header, bg='#e74c3c')
        controls.pack(side='right', padx=10)
        
        tk.Button(
            controls,
            text='✏️ Edit',
            font=('Segoe UI', 9),
            bg='#c0392b',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=lambda: self.edit_file_channel(index)
        ).pack(side='left', padx=2)
        
        tk.Button(
            controls,
            text='🗑️ Delete',
            font=('Segoe UI', 9),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=lambda: self.delete_file_channel(index)
        ).pack(side='left', padx=2)
        
        # Body
        body = tk.Frame(card, bg='white')
        body.pack(fill='x', padx=15, pady=15)
        
        # Display info
        info = [
            ('SFTP Server:', channel.get('sftp_server', 'N/A')),
            ('Scan Interval:', f"{channel.get('scan_interval', '5')} minutes"),
            ('File Pattern:', channel.get('file_pattern', 'N/A')),
            ('IPA Process:', channel.get('ipa_process', 'N/A')),
        ]
        
        for row, (label, value) in enumerate(info):
            tk.Label(
                body,
                text=label,
                font=('Segoe UI', 10, 'bold'),
                bg='white',
                fg='#7f8c8d'
            ).grid(row=row, column=0, sticky='w', padx=5, pady=5)
            
            tk.Label(
                body,
                text=value,
                font=('Segoe UI', 10),
                bg='white',
                fg='#2c3e50'
            ).grid(row=row, column=1, sticky='w', padx=5, pady=5)

    def add_file_channel(self):
        """Add new file channel"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add File Channel")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        # Form
        form = tk.Frame(dialog, bg='white')
        form.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Channel Name
        tk.Label(form, text="Channel Name:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        name_entry.grid(row=0, column=1, pady=5)
        
        # SFTP Server (dropdown)
        tk.Label(form, text="SFTP Server:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        sftp_names = [s['server_name'] for s in self.project_data['sftp_servers']]
        sftp_combo = ttk.Combobox(form, values=sftp_names, state='readonly', width=30)
        if sftp_names:
            sftp_combo.set(sftp_names[0])
        sftp_combo.grid(row=1, column=1, pady=5)
        
        # Scan Interval
        tk.Label(form, text="Scan Interval (min):", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        interval_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        interval_entry.insert(0, '5')
        interval_entry.grid(row=2, column=1, pady=5)
        
        # File Pattern
        tk.Label(form, text="File Pattern:", font=('Segoe UI', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        pattern_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        pattern_entry.insert(0, '*.csv')
        pattern_entry.grid(row=3, column=1, pady=5)
        
        # IPA Process
        tk.Label(form, text="IPA Process:", font=('Segoe UI', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        ipa_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        ipa_entry.grid(row=4, column=1, pady=5)
        
        def save():
            channel = {
                'channel_name': name_entry.get().strip(),
                'sftp_server': sftp_combo.get(),
                'scan_interval': interval_entry.get().strip(),
                'file_pattern': pattern_entry.get().strip(),
                'ipa_process': ipa_entry.get().strip()
            }
            
            if not channel['channel_name']:
                messagebox.showerror("Error", "Channel name is required")
                return
            
            self.project_data['file_channels'].append(channel)
            self.refresh_channels_display()
            self.update_counts()
            dialog.destroy()
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text='Cancel',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text='Save',
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=save
        ).pack(side='right', padx=5)
    
    def edit_file_channel(self, index):
        """Edit file channel"""
        channel = self.project_data['file_channels'][index]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit File Channel")
        dialog.geometry("500x450")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Set icon and center
        self.set_dialog_icon(dialog)
        self.center_dialog(dialog)
        
        form = tk.Frame(dialog, bg='white')
        form.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Pre-fill fields
        tk.Label(form, text="Channel Name:", font=('Segoe UI', 10), bg='white').grid(row=0, column=0, sticky='w', pady=5)
        name_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        name_entry.insert(0, channel.get('channel_name', ''))
        name_entry.grid(row=0, column=1, pady=5)
        
        tk.Label(form, text="SFTP Server:", font=('Segoe UI', 10), bg='white').grid(row=1, column=0, sticky='w', pady=5)
        sftp_names = [s['server_name'] for s in self.project_data['sftp_servers']]
        sftp_combo = ttk.Combobox(form, values=sftp_names, state='readonly', width=30)
        sftp_combo.set(channel.get('sftp_server', ''))
        sftp_combo.grid(row=1, column=1, pady=5)
        
        tk.Label(form, text="Scan Interval (min):", font=('Segoe UI', 10), bg='white').grid(row=2, column=0, sticky='w', pady=5)
        interval_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        interval_entry.insert(0, channel.get('scan_interval', '5'))
        interval_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(form, text="File Pattern:", font=('Segoe UI', 10), bg='white').grid(row=3, column=0, sticky='w', pady=5)
        pattern_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        pattern_entry.insert(0, channel.get('file_pattern', ''))
        pattern_entry.grid(row=3, column=1, pady=5)
        
        tk.Label(form, text="IPA Process:", font=('Segoe UI', 10), bg='white').grid(row=4, column=0, sticky='w', pady=5)
        ipa_entry = tk.Entry(form, font=('Segoe UI', 10), width=32)
        ipa_entry.insert(0, channel.get('ipa_process', ''))
        ipa_entry.grid(row=4, column=1, pady=5)
        
        def save():
            self.project_data['file_channels'][index] = {
                'channel_name': name_entry.get().strip(),
                'sftp_server': sftp_combo.get(),
                'scan_interval': interval_entry.get().strip(),
                'file_pattern': pattern_entry.get().strip(),
                'ipa_process': ipa_entry.get().strip()
            }
            
            self.refresh_channels_display()
            dialog.destroy()
        
        btn_frame = tk.Frame(dialog, bg='white')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            btn_frame,
            text='Cancel',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=dialog.destroy
        ).pack(side='right', padx=5)
        
        tk.Button(
            btn_frame,
            text='Save',
            font=('Segoe UI', 10),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=save
        ).pack(side='right', padx=5)
    
    def delete_file_channel(self, index):
        """Delete file channel"""
        channel = self.project_data['file_channels'][index]
        if messagebox.askyesno("Confirm Delete", 
            f"Delete file channel '{channel.get('channel_name', 'N/A')}'?"):
            self.project_data['file_channels'].pop(index)
            self.refresh_channels_display()
            self.update_counts()

    def create_action_bar(self, parent):
        """Create bottom action bar"""
        action_bar = tk.Frame(parent, bg='#ecf0f1', height=80)
        action_bar.pack(fill='x', side='bottom')
        action_bar.pack_propagate(False)
        
        # Right side buttons
        btn_frame = tk.Frame(action_bar, bg='#ecf0f1')
        btn_frame.pack(side='right', padx=20, pady=15)
        
        # Export config button
        tk.Button(
            btn_frame,
            text='💾 Export Config',
            font=('Segoe UI', 11),
            bg='#9b59b6',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.export_config
        ).pack(side='left', padx=5)
        
        # Preview button
        tk.Button(
            btn_frame,
            text='👁️ Preview',
            font=('Segoe UI', 11),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.preview_config
        ).pack(side='left', padx=5)
        
        # Generate project button
        tk.Button(
            btn_frame,
            text='🚀 Generate Project',
            font=('Segoe UI', 12, 'bold'),
            bg='#2ecc71',
            fg='white',
            relief='flat',
            padx=30,
            pady=10,
            cursor='hand2',
            command=self.generate_project
        ).pack(side='left', padx=5)
    
    def export_config(self):
        """Export configuration to JSON"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            initialfile=f"{self.project_data['project_name']}_config.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.project_data, f, indent=2)
                messagebox.showinfo("Success", f"Configuration exported to:\n{filename}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export:\n{str(e)}")
    
    def preview_config(self):
        """Preview configuration as JSON"""
        preview = tk.Toplevel(self.root)
        preview.title("Configuration Preview")
        preview.geometry("700x600")
        preview.transient(self.root)
        
        # Set icon and center
        self.set_dialog_icon(preview)
        self.center_dialog(preview)
        
        # JSON text area
        text = tk.Text(preview, font=('Consolas', 10), wrap='word')
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Insert formatted JSON
        json_str = json.dumps(self.project_data, indent=2)
        text.insert('1.0', json_str)
        text.config(state='disabled')
        
        # Close button
        tk.Button(
            preview,
            text='Close',
            font=('Segoe UI', 10),
            bg='#95a5a6',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=preview.destroy
        ).pack(pady=10)
    
    def generate_project(self):
        """Generate project structure"""
        if not self.project_data['project_name']:
            messagebox.showerror("Error", "Project name is required")
            return
        
        if not self.project_data['tenants']:
            messagebox.showerror("Error", "At least one tenant is required")
            return
        
        try:
            self.create_project_structure()
            messagebox.showinfo("Success", 
                f"Project '{self.project_data['project_name']}' created successfully!\n\n"
                f"Location: Projects/{self.project_data['project_name']}/\n\n"
                f"Next steps:\n"
                f"1. Verify credentials in Credentials/ folders\n"
                f"2. Copy .ionapi files if needed\n"
                f"3. NEVER commit credential files to git!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project:\n{str(e)}")
    
    def create_project_structure(self):
        """Create actual project folder structure"""
        project_name = self.project_data['project_name']
        base_path = Path(f"Projects/{project_name}")
        
        # Create base folders
        folders = [
            "TestScripts/inbound",
            "TestScripts/outbound",
            "TestScripts/approval",
            "TestScripts/test_data",
            "TES-070/Generated_TES070s",
            "Temp"
        ]
        
        for folder in folders:
            (base_path / folder).mkdir(parents=True, exist_ok=True)
        
        # Create tenant-specific credential folders
        for tenant in self.project_data['tenants']:
            env = tenant['environment']
            cred_path = base_path / "Credentials" / env
            cred_path.mkdir(parents=True, exist_ok=True)
            
            # Create .env.fsm
            env_fsm_content = f"""# FSM Login Credentials - {project_name} {env}
# DO NOT COMMIT TO VERSION CONTROL

# Tenant: {tenant['tenant_id']}
{project_name.upper()}_{env}_URL={tenant['fsm_url']}
{project_name.upper()}_{env}_USERNAME={tenant['fsm_username']}
{project_name.upper()}_{env}_PASSWORD=${{{project_name.upper()}_{env}_PASSWORD}}
"""
            
            with open(cred_path / ".env.fsm", 'w', encoding='utf-8') as f:
                f.write(env_fsm_content)
            
            # Create .env.passwords
            env_passwords_content = f"""# FSM Password File - {project_name} {env}
# DO NOT COMMIT TO VERSION CONTROL

{project_name.upper()}_{env}_PASSWORD={tenant['fsm_password']}
"""
            
            with open(cred_path / ".env.passwords", 'w', encoding='utf-8') as f:
                f.write(env_passwords_content)
            
            # Copy ION API file if specified
            if tenant.get('ionapi_file') and Path(tenant['ionapi_file']).exists():
                import shutil
                dest = cred_path / f"{tenant['tenant_id']}.ionapi"
                shutil.copy(tenant['ionapi_file'], dest)
        
        # Create SFTP credentials file (consolidated)
        if self.project_data['sftp_servers']:
            sftp_content = f"""# SFTP Credentials - {project_name}
# DO NOT COMMIT TO VERSION CONTROL

"""
            for sftp in self.project_data['sftp_servers']:
                sftp_content += f"""
# {sftp['server_name']}
{sftp['server_name'].upper().replace(' ', '_')}_HOST={sftp['host']}
{sftp['server_name'].upper().replace(' ', '_')}_PORT={sftp['port']}
{sftp['server_name'].upper().replace(' ', '_')}_USERNAME={sftp['username']}
{sftp['server_name'].upper().replace(' ', '_')}_PASSWORD={sftp['password']}
{sftp['server_name'].upper().replace(' ', '_')}_INBOUND_PATH={sftp['inbound_path']}
{sftp['server_name'].upper().replace(' ', '_')}_OUTBOUND_PATH={sftp['outbound_path']}
"""
            
            with open(base_path / "Credentials" / "sftp_credentials.env", 'w', encoding='utf-8') as f:
                f.write(sftp_content)
        
        # Create README.md
        readme_content = f"""# {project_name} Project

## Overview
FSM testing project with multi-tenant support.

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Tenants
"""
        for tenant in self.project_data['tenants']:
            readme_content += f"- **{tenant['environment']}**: {tenant['tenant_id']} - {tenant['fsm_url']}\n"
        
        readme_content += f"""
## SFTP Servers
"""
        for sftp in self.project_data['sftp_servers']:
            readme_content += f"- **{sftp['server_name']}**: {sftp['host']}\n"
        
        readme_content += f"""
## File Channels
"""
        for channel in self.project_data['file_channels']:
            readme_content += f"- **{channel['channel_name']}**: {channel['sftp_server']} → {channel['ipa_process']}\n"
        
        readme_content += """
## Structure
- `Credentials/` - Tenant-specific credentials organized by environment
- `TestScripts/` - Test scenarios and test data
- `TES-070/Generated_TES070s/` - Test results documents
- `Temp/` - Test execution screenshots

## Security
⚠️ **NEVER commit credential files to version control!**
"""
        
        with open(base_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Create test data README
        test_data_readme = """# Test Data Files

This folder contains CSV, XML, and JSON test data files.

## Generating Test Data
Use "Step 0: Generate Test Data" hook to create fresh test data.
"""
        
        with open(base_path / "TestScripts" / "test_data" / "README.md", 'w', encoding='utf-8') as f:
            f.write(test_data_readme)
        
        # Save configuration
        with open(base_path / "project_config.json", 'w', encoding='utf-8') as f:
            json.dump(self.project_data, f, indent=2)


def main():
    root = tk.Tk()
    app = ProjectSetupGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
