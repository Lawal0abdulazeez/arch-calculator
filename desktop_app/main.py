# desktop_app/main.py

import tkinter as tk
from tkinter import ttk, messagebox
from core_logic.calculations import BuildingProject, calculate_material_quantities

class ArchCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QS Materials Calculator")
        self.geometry("800x700")

        # Initialize the project logic
        # For simplicity, we'll start with a default mix ratio
        self.project = BuildingProject(mix_ratio="1:2:4")

        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Top Frame for Inputs ---
        input_frame = ttk.LabelFrame(main_frame, text="Add a Structural Element", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        self._create_input_widgets(input_frame)
        
        # --- Middle Frame for Element List ---
        list_frame = ttk.LabelFrame(main_frame, text="Project Elements", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self._create_list_widgets(list_frame)

        # --- Bottom Frame for Results ---
        result_frame = ttk.LabelFrame(main_frame, text="Final Calculation", padding="10")
        result_frame.pack(fill=tk.X, pady=5)
        self._create_result_widgets(result_frame)

    '''def _create_input_widgets(self, parent):
        # Element Type
        ttk.Label(parent, text="Element Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.element_type_entry = ttk.Entry(parent)
        self.element_type_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.element_type_entry.insert(0, "Column") # Default example

        # Quantity
        ttk.Label(parent, text="Quantity:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(parent)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.quantity_entry.insert(0, "4") # Default example

        # Dimensions
        ttk.Label(parent, text="Length (m):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.length_entry = ttk.Entry(parent)
        self.length_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.length_entry.insert(0, "0.4")

        ttk.Label(parent, text="Width (m):").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.width_entry = ttk.Entry(parent)
        self.width_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.width_entry.insert(0, "0.4")

        ttk.Label(parent, text="Height/Depth (m):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.height_entry = ttk.Entry(parent)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.height_entry.insert(0, "3.0")

        # Buttons
        add_button = ttk.Button(parent, text="Add Element to List", command=self.add_element_to_list)
        add_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")
        
        add_deduction_button = ttk.Button(parent, text="Add as Deduction (Opening)", command=self.add_deduction_to_list)
        add_deduction_button.grid(row=3, column=3, padx=5, pady=10, sticky="ew")

        parent.columnconfigure((1, 3), weight=1)
'''
    def _create_input_widgets(self, parent):
        # Element Type
        ttk.Label(parent, text="Element Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.element_type_entry = ttk.Entry(parent)
        self.element_type_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.element_type_entry.insert(0, "Wall") # Default example is now a wall

        # Quantity
        ttk.Label(parent, text="Quantity:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.quantity_entry = ttk.Entry(parent)
        self.quantity_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.quantity_entry.insert(0, "1") # Default example

        # Dimensions
        ttk.Label(parent, text="Length (m):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.length_entry = ttk.Entry(parent)
        self.length_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.length_entry.insert(0, "8.0") # Wall length

        ttk.Label(parent, text="Thickness (m):").grid(row=1, column=2, padx=5, pady=5, sticky="w") # More descriptive label
        self.width_entry = ttk.Entry(parent)
        self.width_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.width_entry.insert(0, "0.225") # Wall thickness

        ttk.Label(parent, text="Height (m):").grid(row=2, column=0, padx=5, pady=5, sticky="w") # More descriptive label
        self.height_entry = ttk.Entry(parent)
        self.height_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.height_entry.insert(0, "3.0") # Wall height

        # Buttons
        add_button = ttk.Button(parent, text="Add Element to List", command=self.add_element_to_list)
        add_button.grid(row=3, column=1, padx=5, pady=10, sticky="ew")
        
        add_deduction_button = ttk.Button(parent, text="Add as Deduction (Opening)", command=self.add_deduction_to_list)
        add_deduction_button.grid(row=3, column=3, padx=5, pady=10, sticky="ew")

        parent.columnconfigure((1, 3), weight=1)

    def _create_list_widgets(self, parent):
        cols = ("type", "qty", "dims", "volume")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings")
        
        self.tree.heading("type", text="Element Type")
        self.tree.heading("qty", text="Quantity")
        self.tree.heading("dims", text="Dimensions (L x W x H)")
        self.tree.heading("volume", text="Total Volume (m³)")

        self.tree.column("qty", width=60, anchor="center")
        self.tree.column("volume", width=120, anchor="e")

        self.tree.pack(fill=tk.BOTH, expand=True)

    '''def _create_result_widgets(self, parent):
        self.total_button = ttk.Button(parent, text="Calculate Total Materials for All Elements", command=self.calculate_final_materials)
        self.total_button.pack(pady=5, fill=tk.X)
        self.results_label = ttk.Label(parent, text="Results will be shown here.", font=("TkDefaultFont", 10), wraplength=750)
        self.results_label.pack(pady=5, fill=tk.X)
'''
    def _create_result_widgets(self, parent):
        self.total_button = ttk.Button(parent, text="Calculate Total Materials for All Elements", command=self.calculate_final_materials)
        self.total_button.pack(pady=5, fill=tk.X, expand=False)

        # Create a frame to hold the text widget and scrollbar together
        text_frame = ttk.Frame(parent)
        text_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Create the scrollable Text widget for results
        self.results_text = tk.Text(text_frame, height=8, wrap=tk.WORD, state="disabled", relief=tk.SUNKEN, borderwidth=1)
        self.results_text.grid(row=0, column=0, sticky="nsew")

        # Create the Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Link the Text widget to the scrollbar
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Configure the grid to make the text widget expand
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

    def add_element_to_list(self, is_deduction=False):
        try:
            # Get and validate data from entry fields
            elem_type = self.element_type_entry.get()
            qty = int(self.quantity_entry.get())
            dims = {
                "length": float(self.length_entry.get()),
                "width": float(self.width_entry.get()),
                "height": float(self.height_entry.get()),
            }
            if not elem_type or qty <= 0:
                raise ValueError("Element Type cannot be empty and Quantity must be positive.")

            # Add to project logic
            if is_deduction:
                self.project.add_deduction(elem_type, qty, dims)
                prefix = "[DEDUCTION] "
            else:
                self.project.add_element(elem_type, qty, dims)
                prefix = ""
            
            # Add to visual list (Treeview)
            volume = self.project._calculate_element_volume(dims) * qty
            dims_str = f"{dims['length']} x {dims['width']} x {dims['height']}"
            self.tree.insert("", "end", values=(prefix + elem_type, qty, dims_str, f"{volume:.3f}"))

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input. Please check your values.\nDetails: {e}")

    def add_deduction_to_list(self):
        self.add_element_to_list(is_deduction=True)

    '''def calculate_final_materials(self):
        if not self.project.elements and not self.project.deductions:
            messagebox.showinfo("Information", "The project list is empty. Please add elements first.")
            return

        net_volume = self.project.calculate_total_net_volume()
        materials = self.project.calculate_total_materials()

        gross_vol = sum(el['total_volume'] for el in self.project.elements)
        deduction_vol = sum(d['total_volume'] for d in self.project.deductions)

        result_text = (
            f"--- Final Quantity Survey ---\n"
            f"Gross Volume of all elements: {gross_vol:.3f} m³\n"
            f"Total Deductions (openings, etc.): -{deduction_vol:.3f} m³\n"
            f"NET CONCRETE VOLUME: {net_volume:.3f} m³\n\n"
            f"--- Required Materials for {self.project.mix_ratio} Mix ---\n"
            f"Cement: {materials['cement_bags']:.2f} bags (50kg)\n"
            f"Sand: {materials['sand_cubic_meters']:.3f} m³\n"
            f"Gravel: {materials['gravel_cubic_meters']:.3f} m³"
        )
        self.results_label.config(text=result_text)'''


    def calculate_final_materials(self):
        if not self.project.elements and not self.project.deductions:
            messagebox.showinfo("Information", "The project list is empty. Please add elements first.")
            return

        net_volume = self.project.calculate_total_net_volume()
        materials = self.project.calculate_total_materials()

        gross_vol = sum(el['total_volume'] for el in self.project.elements)
        deduction_vol = sum(d['total_volume'] for d in self.project.deductions)

        result_text = (
            f"--- Final Quantity Survey ---\n\n"
            f"Total Gross Volume of all elements: {gross_vol:.3f} m³\n"
            f"Total Deductions (openings, etc.): -{deduction_vol:.3f} m³\n"
            f"--------------------------------------------------\n"
            f"NET CONCRETE VOLUME REQUIRED: {net_volume:.3f} m³\n"
            f"--------------------------------------------------\n\n"
            f"--- Required Materials for {self.project.mix_ratio} Mix ---\n\n"
            f"Cement: {materials['cement_bags']:.2f} bags (of 50kg)\n"
            f"Sand: {materials['sand_cubic_meters']:.3f} m³\n"
            f"Gravel: {materials['gravel_cubic_meters']:.3f} m³\n"
        )
        
        # This is the corrected block. It uses self.results_text.
        self.results_text.config(state="normal")      # Enable writing
        self.results_text.delete("1.0", tk.END)      # Clear previous content
        self.results_text.insert(tk.END, result_text) # Insert new content
        self.results_text.config(state="disabled")     # Disable writing to make it read-only

if __name__ == "__main__":
    app = ArchCalculatorApp()
    app.mainloop()