"""
Test Scenario Builder - GUI Version

A user-friendly graphical interface for functional consultants to create
test scenario JSON files without writing any code.

Usage:
    python ReusableTools/test_scenario_builder_gui.py

Requirements:
    - tkinter (included with Python on Windows)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
from pathlib import Path
from datetime import datetime


class TestScenarioBuilderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Scenario Builder")
        self.root.geometry("900x700")
        
        # Data storage
        self.scenarios = []
        self.current_scenario = None
        
        # Predefined scenario templates
        self.scenario_templates = self.get_predefined_scenarios()
        
        # Create main container with tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Interface Info
        self.create_interface_tab()
        
        # Tab 2: Prerequisites
        self.create_prerequisites_tab()
        
        # Tab 3: Scenarios
        self.create_scenarios_tab()
        
        # Tab 4: Review & Generate
        self.create_review_tab()
        
        # Bottom buttons
        self.create_bottom_buttons()
    
    def create_interface_tab(self):
        """Tab 1: Interface Information"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="1. Interface Info")
        
        # Create form
        row = 0
        
        ttk.Label(frame, text="Interface ID:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.interface_id = ttk.Entry(frame, width=40)
        self.interface_id.grid(row=row, column=1, padx=10, pady=5)
        ttk.Label(frame, text="e.g., INT_FIN_013", foreground='gray').grid(row=row, column=2, sticky='w')
        row += 1
        
        ttk.Label(frame, text="Interface Name:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.interface_name = ttk.Entry(frame, width=40)
        self.interface_name.grid(row=row, column=1, padx=10, pady=5)
        ttk.Label(frame, text="e.g., GL Transaction Interface", foreground='gray').grid(row=row, column=2, sticky='w')
        row += 1
        
        ttk.Label(frame, text="Interface Type:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.interface_type = ttk.Combobox(frame, width=37, values=["inbound", "outbound", "approval"])
        self.interface_type.set("inbound")
        self.interface_type.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        ttk.Label(frame, text="Client Name:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.client_name = ttk.Entry(frame, width=40)
        self.client_name.insert(0, "State of New Hampshire")
        self.client_name.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        ttk.Label(frame, text="Author Name:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.author = ttk.Entry(frame, width=40)
        self.author.grid(row=row, column=1, padx=10, pady=5)
        row += 1
        
        ttk.Label(frame, text="Environment:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', padx=10, pady=5)
        self.environment = ttk.Combobox(frame, width=37, values=["ACUITY_TST", "ACUITY_PRD", "TAMICS10_AX1"])
        self.environment.set("ACUITY_TST")
        self.environment.grid(row=row, column=1, padx=10, pady=5)
    
    def create_prerequisites_tab(self):
        """Tab 2: Prerequisites"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="2. Prerequisites")
        
        row = 0
        
        ttk.Label(frame, text="User Roles (one per line):", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='nw', padx=10, pady=5)
        row += 1
        self.user_roles = scrolledtext.ScrolledText(frame, width=70, height=5)
        self.user_roles.grid(row=row, column=0, padx=10, pady=5, columnspan=2)
        self.user_roles.insert('1.0', "Process Server Administrator\nFinancials Processor")
        row += 1
        
        ttk.Label(frame, text="Test Data Requirements:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='nw', padx=10, pady=5)
        row += 1
        self.test_data = scrolledtext.ScrolledText(frame, width=70, height=5)
        self.test_data.grid(row=row, column=0, padx=10, pady=5, columnspan=2)
        row += 1
        
        ttk.Label(frame, text="Configuration Prerequisites:", font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='nw', padx=10, pady=5)
        row += 1
        self.config_prereqs = scrolledtext.ScrolledText(frame, width=70, height=5)
        self.config_prereqs.grid(row=row, column=0, padx=10, pady=5, columnspan=2)
    
    def create_scenarios_tab(self):
        """Tab 3: Test Scenarios"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="3. Test Scenarios")
        
        # Left side: Scenario list
        left_frame = ttk.Frame(frame)
        left_frame.pack(side='left', fill='both', expand=False, padx=5, pady=5)
        
        ttk.Label(left_frame, text="Scenarios:", font=('Arial', 10, 'bold')).pack()
        
        self.scenario_listbox = tk.Listbox(left_frame, width=30, height=20)
        self.scenario_listbox.pack(fill='both', expand=True)
        self.scenario_listbox.bind('<<ListboxSelect>>', self.on_scenario_select)
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill='x', pady=5)
        ttk.Button(btn_frame, text="New Scenario", command=self.new_scenario).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Load Template", command=self.load_template).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_scenario).pack(side='left', padx=2)
        
        # Right side: Scenario editor
        right_frame = ttk.Frame(frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=5, pady=5)
        
        self.scenario_editor = ttk.Frame(right_frame)
        self.scenario_editor.pack(fill='both', expand=True)
        
        ttk.Label(self.scenario_editor, text="Scenario Title:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.scenario_title = ttk.Entry(self.scenario_editor, width=60)
        self.scenario_title.pack(fill='x', pady=5)
        
        ttk.Label(self.scenario_editor, text="Description:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.scenario_desc = scrolledtext.ScrolledText(self.scenario_editor, width=60, height=4)
        self.scenario_desc.pack(fill='x', pady=5)
        
        ttk.Label(self.scenario_editor, text="Test Steps:", font=('Arial', 10, 'bold')).pack(anchor='w')
        
        # Steps frame with scrollbar
        steps_container = ttk.Frame(self.scenario_editor)
        steps_container.pack(fill='both', expand=True, pady=5)
        
        self.steps_canvas = tk.Canvas(steps_container, height=200)
        scrollbar = ttk.Scrollbar(steps_container, orient="vertical", command=self.steps_canvas.yview)
        self.steps_frame = ttk.Frame(self.steps_canvas)
        
        self.steps_frame.bind("<Configure>", lambda e: self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all")))
        self.steps_canvas.create_window((0, 0), window=self.steps_frame, anchor="nw")
        self.steps_canvas.configure(yscrollcommand=scrollbar.set)
        
        self.steps_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        ttk.Button(self.scenario_editor, text="Add Test Step", command=self.add_test_step).pack(pady=5)
        
        ttk.Button(self.scenario_editor, text="Save Scenario", command=self.save_scenario).pack(pady=10)
    
    def create_review_tab(self):
        """Tab 4: Review & Generate"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="4. Review & Generate")
        
        ttk.Label(frame, text="Review Your Test Scenarios", font=('Arial', 12, 'bold')).pack(pady=10)
        
        self.review_text = scrolledtext.ScrolledText(frame, width=100, height=30)
        self.review_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Refresh Preview", command=self.refresh_review).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save JSON", command=self.save_json).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Generate TES-070", command=self.generate_tes070).pack(side='left', padx=5)
    
    def create_bottom_buttons(self):
        """Bottom navigation buttons"""
        frame = ttk.Frame(self.root)
        frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame, text="← Previous", command=self.prev_tab).pack(side='left', padx=5)
        ttk.Button(frame, text="Next →", command=self.next_tab).pack(side='left', padx=5)
        ttk.Button(frame, text="Exit", command=self.root.quit).pack(side='right', padx=5)
    
    def prev_tab(self):
        current = self.notebook.index(self.notebook.select())
        if current > 0:
            self.notebook.select(current - 1)
    
    def next_tab(self):
        current = self.notebook.index(self.notebook.select())
        if current < 3:
            self.notebook.select(current + 1)
    
    def get_predefined_scenarios(self):
        """Return predefined test scenario templates"""
        return {
            "Inbound Interface": [
                {
                    "title": "Successful Import",
                    "description": "Verify that valid data is successfully imported from file and interfaced to FSM",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Upload valid CSV/XML file to SFTP server",
                            "result": "PASS",
                            "screenshot": "01_file_upload"
                        },
                        {
                            "number": "2",
                            "description": "Wait for File Channel to pick up file and trigger IPA process",
                            "result": "PASS",
                            "screenshot": "02_file_channel_trigger"
                        },
                        {
                            "number": "3",
                            "description": "Navigate to Process Server Administrator and check work unit status",
                            "result": "PASS",
                            "screenshot": "03_work_unit_completed"
                        },
                        {
                            "number": "4",
                            "description": "Verify data in FSM using appropriate role",
                            "result": "PASS",
                            "screenshot": "04_data_verification"
                        }
                    ],
                    "results": ["Data successfully imported", "All records processed", "No errors in work unit"]
                },
                {
                    "title": "Invalid Data Error",
                    "description": "Verify that invalid data is rejected with appropriate error messages",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Upload file with invalid data (e.g., invalid account numbers, missing required fields)",
                            "result": "PASS",
                            "screenshot": "01_invalid_file_upload"
                        },
                        {
                            "number": "2",
                            "description": "Wait for File Channel to pick up file and trigger IPA process",
                            "result": "PASS",
                            "screenshot": "02_file_channel_trigger"
                        },
                        {
                            "number": "3",
                            "description": "Check work unit status - should show error or completed with errors",
                            "result": "PASS",
                            "screenshot": "03_work_unit_error"
                        },
                        {
                            "number": "4",
                            "description": "Verify error message is clear and actionable",
                            "result": "PASS",
                            "screenshot": "04_error_message"
                        },
                        {
                            "number": "5",
                            "description": "Confirm invalid records were not imported to FSM",
                            "result": "PASS",
                            "screenshot": "05_no_invalid_data"
                        }
                    ],
                    "results": ["Invalid data rejected", "Clear error message displayed", "No corrupt data in FSM"]
                },
                {
                    "title": "Duplicate Record Handling",
                    "description": "Verify that duplicate records are handled correctly per business rules",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Upload file containing duplicate records",
                            "result": "PASS",
                            "screenshot": "01_duplicate_file_upload"
                        },
                        {
                            "number": "2",
                            "description": "Wait for File Channel to trigger IPA process",
                            "result": "PASS",
                            "screenshot": "02_process_triggered"
                        },
                        {
                            "number": "3",
                            "description": "Check work unit status and logs",
                            "result": "PASS",
                            "screenshot": "03_work_unit_status"
                        },
                        {
                            "number": "4",
                            "description": "Verify duplicate handling per business rules (reject, update, or skip)",
                            "result": "PASS",
                            "screenshot": "04_duplicate_handling"
                        }
                    ],
                    "results": ["Duplicates handled per business rules", "Appropriate messages logged"]
                }
            ],
            "Outbound Interface": [
                {
                    "title": "Successful Export",
                    "description": "Verify that data is successfully extracted from FSM and exported to file",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Trigger outbound interface manually or via schedule",
                            "result": "PASS",
                            "screenshot": "01_trigger_interface"
                        },
                        {
                            "number": "2",
                            "description": "Check work unit status - should show completed",
                            "result": "PASS",
                            "screenshot": "02_work_unit_completed"
                        },
                        {
                            "number": "3",
                            "description": "Verify output file exists in expected location (FSM File Storage or SFTP)",
                            "result": "PASS",
                            "screenshot": "03_file_exists"
                        },
                        {
                            "number": "4",
                            "description": "Download and validate file contents (format, data accuracy, completeness)",
                            "result": "PASS",
                            "screenshot": "04_file_validation"
                        }
                    ],
                    "results": ["File generated successfully", "Data accurate and complete", "File format correct"]
                },
                {
                    "title": "No Data to Export",
                    "description": "Verify interface behavior when no data meets export criteria",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Ensure no data meets export criteria (e.g., no new transactions)",
                            "result": "PASS",
                            "screenshot": "01_no_data_setup"
                        },
                        {
                            "number": "2",
                            "description": "Trigger outbound interface",
                            "result": "PASS",
                            "screenshot": "02_trigger_interface"
                        },
                        {
                            "number": "3",
                            "description": "Check work unit status and logs",
                            "result": "PASS",
                            "screenshot": "03_work_unit_status"
                        },
                        {
                            "number": "4",
                            "description": "Verify appropriate message (e.g., 'No records to export') and no empty file created",
                            "result": "PASS",
                            "screenshot": "04_no_data_message"
                        }
                    ],
                    "results": ["Appropriate 'no data' message", "No empty or corrupt file generated"]
                },
                {
                    "title": "Large Volume Export",
                    "description": "Verify interface handles large data volumes without timeout or memory issues",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Set up test data with large volume (e.g., 10,000+ records)",
                            "result": "PASS",
                            "screenshot": "01_large_volume_setup"
                        },
                        {
                            "number": "2",
                            "description": "Trigger outbound interface",
                            "result": "PASS",
                            "screenshot": "02_trigger_interface"
                        },
                        {
                            "number": "3",
                            "description": "Monitor work unit - should complete without timeout",
                            "result": "PASS",
                            "screenshot": "03_work_unit_completed"
                        },
                        {
                            "number": "4",
                            "description": "Verify file contains all expected records",
                            "result": "PASS",
                            "screenshot": "04_record_count_validation"
                        }
                    ],
                    "results": ["Large volume processed successfully", "No timeout or memory errors", "All records exported"]
                }
            ],
            "Approval Workflow": [
                {
                    "title": "Successful Approval",
                    "description": "Verify that approval workflow completes successfully when approved",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Trigger approval workflow (e.g., submit invoice for approval)",
                            "result": "PASS",
                            "screenshot": "01_submit_for_approval"
                        },
                        {
                            "number": "2",
                            "description": "Verify User Action created for approver",
                            "result": "PASS",
                            "screenshot": "02_user_action_created"
                        },
                        {
                            "number": "3",
                            "description": "Log in as approver and approve the request",
                            "result": "PASS",
                            "screenshot": "03_approve_action"
                        },
                        {
                            "number": "4",
                            "description": "Verify status updated to 'Approved' in FSM",
                            "result": "PASS",
                            "screenshot": "04_status_approved"
                        },
                        {
                            "number": "5",
                            "description": "Verify downstream actions triggered (if applicable)",
                            "result": "PASS",
                            "screenshot": "05_downstream_actions"
                        }
                    ],
                    "results": ["Approval workflow completed", "Status updated correctly", "Downstream actions triggered"]
                },
                {
                    "title": "Rejection Handling",
                    "description": "Verify that rejection workflow handles rejected requests correctly",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Trigger approval workflow",
                            "result": "PASS",
                            "screenshot": "01_submit_for_approval"
                        },
                        {
                            "number": "2",
                            "description": "Verify User Action created for approver",
                            "result": "PASS",
                            "screenshot": "02_user_action_created"
                        },
                        {
                            "number": "3",
                            "description": "Log in as approver and reject the request with comments",
                            "result": "PASS",
                            "screenshot": "03_reject_action"
                        },
                        {
                            "number": "4",
                            "description": "Verify status updated to 'Rejected' in FSM",
                            "result": "PASS",
                            "screenshot": "04_status_rejected"
                        },
                        {
                            "number": "5",
                            "description": "Verify rejection comments captured and visible",
                            "result": "PASS",
                            "screenshot": "05_rejection_comments"
                        }
                    ],
                    "results": ["Rejection handled correctly", "Status updated to Rejected", "Comments captured"]
                },
                {
                    "title": "Multi-Level Approval",
                    "description": "Verify multi-level approval workflow with multiple approvers",
                    "test_steps": [
                        {
                            "number": "1",
                            "description": "Trigger approval workflow requiring multiple approvers",
                            "result": "PASS",
                            "screenshot": "01_submit_for_approval"
                        },
                        {
                            "number": "2",
                            "description": "Verify User Actions created for all required approvers",
                            "result": "PASS",
                            "screenshot": "02_multiple_user_actions"
                        },
                        {
                            "number": "3",
                            "description": "First approver approves the request",
                            "result": "PASS",
                            "screenshot": "03_first_approval"
                        },
                        {
                            "number": "4",
                            "description": "Verify status shows 'Pending' (not fully approved yet)",
                            "result": "PASS",
                            "screenshot": "04_status_pending"
                        },
                        {
                            "number": "5",
                            "description": "Second approver approves the request",
                            "result": "PASS",
                            "screenshot": "05_second_approval"
                        },
                        {
                            "number": "6",
                            "description": "Verify status updated to 'Approved' after all approvals",
                            "result": "PASS",
                            "screenshot": "06_status_approved"
                        }
                    ],
                    "results": ["Multi-level approval completed", "All approvers processed", "Final status correct"]
                }
            ]
        }
    
    def load_template(self):
        """Load a predefined scenario template"""
        # Determine interface type
        interface_type = self.interface_type.get()
        
        # Map interface types to template categories
        template_map = {
            "inbound": "Inbound Interface",
            "outbound": "Outbound Interface",
            "approval": "Approval Workflow"
        }
        
        category = template_map.get(interface_type, "Inbound Interface")
        templates = self.scenario_templates.get(category, [])
        
        if not templates:
            messagebox.showinfo("No Templates", f"No templates available for {interface_type}")
            return
        
        # Create selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Template")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text=f"Select a template for {category}:", font=('Arial', 10, 'bold')).pack(pady=10)
        
        listbox = tk.Listbox(dialog, width=50, height=10)
        listbox.pack(padx=10, pady=10, fill='both', expand=True)
        
        for template in templates:
            listbox.insert('end', template['title'])
        
        def on_select():
            selection = listbox.curselection()
            if not selection:
                return
            
            idx = selection[0]
            template = templates[idx]
            
            # Load template into editor
            self.scenario_title.delete(0, 'end')
            self.scenario_title.insert(0, template['title'])
            
            self.scenario_desc.delete('1.0', 'end')
            self.scenario_desc.insert('1.0', template['description'])
            
            self.clear_steps()
            for step in template['test_steps']:
                self.add_test_step()
                step_frame = self.steps_frame.winfo_children()[-1]
                step_frame.desc_widget.insert('1.0', step['description'])
                step_frame.result_widget.set(step.get('result', 'PASS'))
                if 'screenshot' in step:
                    step_frame.screenshot_widget.insert(0, step['screenshot'])
            
            dialog.destroy()
            messagebox.showinfo("Template Loaded", f"Template '{template['title']}' loaded! You can now edit it as needed.")
        
        ttk.Button(dialog, text="Load Selected Template", command=on_select).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack()
    
    
    def new_scenario(self):
        """Create new scenario"""
        self.current_scenario = {
            "title": "",
            "description": "",
            "test_steps": [],
            "results": []
        }
        self.scenario_title.delete(0, 'end')
        self.scenario_desc.delete('1.0', 'end')
        self.clear_steps()
    
    def add_test_step(self):
        """Add a test step to current scenario"""
        step_frame = ttk.LabelFrame(self.steps_frame, text=f"Step {len(self.steps_frame.winfo_children()) + 1}", padding=5)
        step_frame.pack(fill='x', pady=5)
        
        ttk.Label(step_frame, text="Description:").grid(row=0, column=0, sticky='w')
        desc = scrolledtext.ScrolledText(step_frame, width=50, height=3)
        desc.grid(row=1, column=0, columnspan=2, pady=2)
        
        ttk.Label(step_frame, text="Result:").grid(row=2, column=0, sticky='w')
        result = ttk.Combobox(step_frame, values=["PASS", "FAIL", "In Progress"], width=15)
        result.set("PASS")
        result.grid(row=2, column=1, sticky='w', pady=2)
        
        ttk.Label(step_frame, text="Screenshot:").grid(row=3, column=0, sticky='w')
        screenshot = ttk.Entry(step_frame, width=30)
        screenshot.grid(row=3, column=1, sticky='w', pady=2)
        
        # Store widgets for later retrieval
        step_frame.desc_widget = desc
        step_frame.result_widget = result
        step_frame.screenshot_widget = screenshot
    
    def clear_steps(self):
        """Clear all test steps"""
        for widget in self.steps_frame.winfo_children():
            widget.destroy()
    
    def save_scenario(self):
        """Save current scenario to list"""
        title = self.scenario_title.get().strip()
        if not title:
            messagebox.showwarning("Missing Title", "Please enter a scenario title")
            return
        
        # Collect test steps
        steps = []
        for i, step_frame in enumerate(self.steps_frame.winfo_children(), 1):
            step = {
                "number": str(i),
                "description": step_frame.desc_widget.get('1.0', 'end').strip(),
                "result": step_frame.result_widget.get()
            }
            screenshot = step_frame.screenshot_widget.get().strip()
            if screenshot:
                step["screenshot"] = screenshot
            steps.append(step)
        
        scenario = {
            "title": title,
            "description": self.scenario_desc.get('1.0', 'end').strip(),
            "test_steps": steps,
            "results": []
        }
        
        self.scenarios.append(scenario)
        self.scenario_listbox.insert('end', title)
        
        messagebox.showinfo("Success", f"Scenario '{title}' saved!")
        self.new_scenario()
    
    def on_scenario_select(self, event):
        """Load selected scenario"""
        selection = self.scenario_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        scenario = self.scenarios[idx]
        
        self.scenario_title.delete(0, 'end')
        self.scenario_title.insert(0, scenario['title'])
        
        self.scenario_desc.delete('1.0', 'end')
        self.scenario_desc.insert('1.0', scenario['description'])
        
        self.clear_steps()
        for step in scenario['test_steps']:
            self.add_test_step()
            step_frame = self.steps_frame.winfo_children()[-1]
            step_frame.desc_widget.insert('1.0', step['description'])
            step_frame.result_widget.set(step['result'])
            if 'screenshot' in step:
                step_frame.screenshot_widget.insert(0, step['screenshot'])
    
    def delete_scenario(self):
        """Delete selected scenario"""
        selection = self.scenario_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        if messagebox.askyesno("Confirm Delete", "Delete this scenario?"):
            del self.scenarios[idx]
            self.scenario_listbox.delete(idx)
    
    def refresh_review(self):
        """Refresh the review preview"""
        data = self.collect_all_data()
        self.review_text.delete('1.0', 'end')
        self.review_text.insert('1.0', json.dumps(data, indent=2))
    
    def collect_all_data(self):
        """Collect all form data"""
        roles = [r.strip() for r in self.user_roles.get('1.0', 'end').strip().split('\n') if r.strip()]
        
        return {
            "interface_id": self.interface_id.get(),
            "interface_name": self.interface_name.get(),
            "interface_type": self.interface_type.get(),
            "client_name": self.client_name.get(),
            "author": self.author.get(),
            "environment": self.environment.get(),
            "user_roles": roles,
            "test_data_requirements": self.test_data.get('1.0', 'end').strip(),
            "configuration_prerequisites": self.config_prereqs.get('1.0', 'end').strip(),
            "scenarios": self.scenarios
        }
    
    def save_json(self):
        """Save to JSON file"""
        data = self.collect_all_data()
        
        if not data['interface_id']:
            messagebox.showwarning("Missing Data", "Please fill in Interface ID")
            return
        
        default_name = f"TestScripts/{data['interface_type']}/{data['interface_id']}_test_scenarios.json"
        filename = filedialog.asksaveasfilename(
            initialfile=default_name,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", f"Saved to:\n{filename}")
    
    def generate_tes070(self):
        """Generate TES-070 document"""
        data = self.collect_all_data()
        
        if not data['interface_id'] or not self.scenarios:
            messagebox.showwarning("Missing Data", "Please complete interface info and add at least one scenario")
            return
        
        # Save JSON first
        temp_json = f"temp_{data['interface_id']}_scenarios.json"
        with open(temp_json, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Show command to run
        msg = f"JSON file created: {temp_json}\n\n"
        msg += "To generate TES-070 document, run:\n\n"
        msg += f"python ReusableTools/generate_tes070_from_json.py {temp_json}"
        
        messagebox.showinfo("Next Step", msg)


def main():
    root = tk.Tk()
    app = TestScenarioBuilderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
