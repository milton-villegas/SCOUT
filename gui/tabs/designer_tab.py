"""
Design Tab - Factorial Designer
Simplified version adapted from factorial_designer_gui.pyw
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
from core.project import DoEProject, AVAILABLE_FACTORS
from core.doe_designer import DoEDesigner
from utils.data_io import export_volumes_to_csv

# Optional XLSX support
try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


class DesignerTab(ttk.Frame):
    """Factorial design interface"""

    def __init__(self, parent, project: DoEProject, main_window):
        super().__init__(parent)
        self.project = project
        self.main_window = main_window
        self.designer = DoEDesigner()

        self._create_ui()

    def _create_ui(self):
        """Setup UI elements"""
        # Main container
        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left panel - Factor management
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Factor list
        factors_frame = ttk.LabelFrame(left_panel, text="Factors", padding=10)
        factors_frame.pack(fill=tk.BOTH, expand=True)

        # Available factors dropdown
        select_frame = ttk.Frame(factors_frame)
        select_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(select_frame, text="Add Factor:").pack(side=tk.LEFT, padx=(0, 5))
        self.factor_var = tk.StringVar()
        factor_dropdown = ttk.Combobox(select_frame, textvariable=self.factor_var,
                                       values=list(AVAILABLE_FACTORS.keys()), state="readonly", width=20)
        factor_dropdown.pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(select_frame, text="Add", command=self._add_factor).pack(side=tk.LEFT)

        # Factor list display
        list_frame = ttk.Frame(factors_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.factor_listbox = tk.Listbox(list_frame, height=10)
        self.factor_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.factor_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.factor_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons
        btn_frame = ttk.Frame(factors_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="Edit", command=self._edit_factor).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remove", command=self._remove_factor).pack(side=tk.LEFT)

        # Right panel - Design controls
        right_panel = ttk.Frame(main_container, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)

        # Final volume
        volume_frame = ttk.LabelFrame(right_panel, text="Settings", padding=10)
        volume_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(volume_frame, text="Final Volume (µL):").pack(anchor=tk.W)
        self.final_vol_var = tk.StringVar(value="100")
        ttk.Entry(volume_frame, textvariable=self.final_vol_var, width=15).pack(anchor=tk.W, pady=(5, 0))

        # Combination counter
        counter_frame = ttk.LabelFrame(right_panel, text="Design Summary", padding=10)
        counter_frame.pack(fill=tk.X, pady=(0, 10))

        self.combo_label = ttk.Label(counter_frame, text="Combinations: 0", font=("TkDefaultFont", 11, "bold"))
        self.combo_label.pack()

        # Generate button
        ttk.Button(right_panel, text="Generate Design", command=self._generate_design,
                  style="Accent.TButton").pack(fill=tk.X, pady=(0, 10))

        # Export buttons
        export_frame = ttk.LabelFrame(right_panel, text="Export", padding=10)
        export_frame.pack(fill=tk.X)

        ttk.Button(export_frame, text="Export Excel", command=self.export_excel).pack(fill=tk.X, pady=(0, 5))
        ttk.Button(export_frame, text="Export CSV (Opentrons)", command=self.export_csv).pack(fill=tk.X)

        # Bottom - Design preview
        preview_frame = ttk.LabelFrame(left_panel, text="Design Preview", padding=10)
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=10, width=60)
        self.preview_text.pack(fill=tk.BOTH, expand=True)

    def _add_factor(self):
        """Add selected factor with simple dialog"""
        factor_name = self.factor_var.get()
        if not factor_name:
            messagebox.showwarning("No Factor", "Select a factor to add")
            return

        # Simple input dialog
        dialog = FactorInputDialog(self, factor_name)
        if dialog.result:
            levels, stock_conc = dialog.result
            try:
                self.project.add_factor(factor_name, levels, stock_conc)
                self._update_factor_list()
                self.main_window.update_status(f"Added factor: {AVAILABLE_FACTORS[factor_name]}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _edit_factor(self):
        """Edit selected factor"""
        selection = self.factor_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a factor to edit")
            return

        factor_name = list(self.project.get_factors().keys())[selection[0]]
        levels = self.project.get_factors()[factor_name]
        stock_conc = self.project.get_stock_conc(factor_name)

        dialog = FactorInputDialog(self, factor_name, levels, stock_conc)
        if dialog.result:
            new_levels, new_stock = dialog.result
            try:
                self.project.update_factor(factor_name, new_levels, new_stock)
                self._update_factor_list()
                self.main_window.update_status(f"Updated factor: {AVAILABLE_FACTORS[factor_name]}")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _remove_factor(self):
        """Remove selected factor"""
        selection = self.factor_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Select a factor to remove")
            return

        factor_name = list(self.project.get_factors().keys())[selection[0]]
        if messagebox.askyesno("Confirm", f"Remove factor '{AVAILABLE_FACTORS[factor_name]}'?"):
            self.project.remove_factor(factor_name)
            self._update_factor_list()
            self.main_window.update_status("Factor removed")

    def _update_factor_list(self):
        """Update factor listbox"""
        self.factor_listbox.delete(0, tk.END)
        factors = self.project.get_factors()

        for name, levels in factors.items():
            display = f"{AVAILABLE_FACTORS.get(name, name)}: {', '.join(map(str, levels))}"
            self.factor_listbox.insert(tk.END, display)

        # Update combination count
        total = 1
        for levels in factors.values():
            total *= len(levels)
        self.combo_label.config(text=f"Combinations: {total}")

    def _generate_design(self):
        """Generate factorial design"""
        try:
            final_vol = float(self.final_vol_var.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Final volume must be a number")
            return

        factors = self.project.get_factors()
        if not factors:
            messagebox.showwarning("No Factors", "Add factors first")
            return

        stock_concs = self.project.get_all_stock_concs()

        try:
            excel_df, volume_df = self.designer.build_factorial_design(factors, stock_concs, final_vol)

            # Store in project
            self.project.design_matrix = excel_df

            # Show preview
            preview = f"Design generated: {len(excel_df)} combinations\n\n"
            preview += excel_df.head(10).to_string()
            if len(excel_df) > 10:
                preview += f"\n\n... and {len(excel_df) - 10} more rows"

            self.preview_text.delete('1.0', tk.END)
            self.preview_text.insert('1.0', preview)

            self.main_window.update_status(f"Design generated: {len(excel_df)} combinations")

        except ValueError as e:
            messagebox.showerror("Design Error", str(e))

    def export_excel(self):
        """Export design to Excel"""
        if self.project.design_matrix is None:
            messagebox.showwarning("No Design", "Generate a design first")
            return

        if not HAS_OPENPYXL:
            messagebox.showerror("Missing Library", "openpyxl required. Install with: pip install openpyxl")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Export Design"
        )

        if filepath:
            try:
                self.project.design_matrix.to_excel(filepath, index=False)
                self.main_window.update_status(f"Exported: {filepath}")
                messagebox.showinfo("Success", f"Design exported to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))

    def export_csv(self):
        """Export Opentrons CSV"""
        if self.project.design_matrix is None:
            messagebox.showwarning("No Design", "Generate a design first")
            return

        messagebox.showinfo("Not Implemented", "CSV export will be implemented in next iteration")

    def refresh(self):
        """Refresh UI from project data"""
        self._update_factor_list()
        self.preview_text.delete('1.0', tk.END)


class FactorInputDialog(tk.Toplevel):
    """Simple dialog for factor input"""

    def __init__(self, parent, factor_name, levels=None, stock_conc=None):
        super().__init__(parent)
        self.title(f"Factor: {AVAILABLE_FACTORS.get(factor_name, factor_name)}")
        self.geometry("400x300")
        self.transient(parent)
        self.grab_set()

        self.result = None

        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Stock concentration (if not categorical)
        if factor_name not in ["buffer pH"]:
            ttk.Label(main_frame, text="Stock Concentration:").pack(anchor=tk.W)
            self.stock_var = tk.StringVar(value=str(stock_conc) if stock_conc else "")
            ttk.Entry(main_frame, textvariable=self.stock_var, width=20).pack(anchor=tk.W, pady=(5, 15))

        # Levels
        ttk.Label(main_frame, text="Levels (comma-separated):").pack(anchor=tk.W)
        self.levels_var = tk.StringVar(value=", ".join(map(str, levels)) if levels else "")
        ttk.Entry(main_frame, textvariable=self.levels_var, width=40).pack(anchor=tk.W, pady=(5, 20))

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack()

        ttk.Button(btn_frame, text="OK", command=self._ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)

    def _ok(self):
        """Process input"""
        levels_str = self.levels_var.get().strip()
        if not levels_str:
            messagebox.showwarning("Missing Input", "Enter at least one level")
            return

        levels = [l.strip() for l in levels_str.split(',')]

        stock_conc = None
        if hasattr(self, 'stock_var'):
            stock_str = self.stock_var.get().strip()
            if stock_str:
                try:
                    stock_conc = float(stock_str)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Stock concentration must be a number")
                    return

        self.result = (levels, stock_conc)
        self.destroy()
