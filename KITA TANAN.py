import tkinter as tk
from tkinter import ttk, messagebox, font
import os


INVENTORY_FILE = "inventory.txt"   # Name of the flat-file database
SEPARATOR = "|"                     # Delimiter used between fields in each line


def save_product(name, unit, quantity, price):
    """Appends a new product as one line to the inventory file."""
    try:
        with open(INVENTORY_FILE, "a") as file:
            file.write(f"{name}{SEPARATOR}{unit}{SEPARATOR}{quantity}{SEPARATOR}{price}\n")
        return True
    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return False


def load_products():
    """Reads all products from the inventory file and returns them as a list of dicts."""
    products = []

    # Return empty list if the file does not exist yet
    if not os.path.exists(INVENTORY_FILE):
        return products

    try:
        with open(INVENTORY_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(SEPARATOR)
                # Only accept lines that have exactly 4 fields
                if len(parts) == 4:
                    products.append({
                        "name":     parts[0],
                        "unit":     parts[1],
                        "quantity": parts[2],
                        "price":    parts[3]
                    })
    except Exception as e:
        messagebox.showerror("File Error", str(e))

    return products


def write_all_products(products):
    """Overwrites the inventory file with the current list of products (used for update/delete)."""
    try:
        with open(INVENTORY_FILE, "w") as file:
            for p in products:
                file.write(
                    f"{p['name']}{SEPARATOR}{p['unit']}{SEPARATOR}"
                    f"{p['quantity']}{SEPARATOR}{p['price']}\n"
                )
        return True
    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return False
    
class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Window configuration ---
        self.title("Inventory Management System")
        self.geometry("900x620")
        self.resizable(False, False)
        self.configure(bg="#0f0f0f")

        # --- Font definitions (shared across all views) ---
        self.title_font  = font.Font(family="Arial", size=18, weight="bold")
        self.header_font = font.Font(family="Arial", size=11, weight="bold")
        self.normal_font = font.Font(family="Arial", size=10)
        self.button_font = font.Font(family="Arial", size=10, weight="bold")
        self.record_font = font.Font(family="Consolas", size=10)

        # --- Color palette (dark theme) ---
        self.BG        = "#0f0f0f"   # Main background
        self.PANEL     = "#1c1c1c"   # Sidebar / panel background
        self.ACCENT    = "#2a2a2a"   # Inactive button background
        self.HIGHLIGHT = "#4e4e4e"   # Active/hovered button background
        self.TEXT      = "#e6e6e6"   # Primary text color
        self.GREEN     = "#4ecca3"   # Confirm / add action color

        self.nav_buttons = {}        # Stores sidebar button references for highlight toggling

        # --- Build the three main layout regions ---
        self._build_header()
        self._build_sidebar()
        self._build_content()

        # --- Start on the display (inventory list) view ---
        self.show_view("display")

    # -------------------------------------------------------------------------
    # HEADER — top bar with app title
    # -------------------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self, bg="#111111", height=55)
        header.pack(fill="x")

        tk.Label(
            header,
            text="📦 INVENTORY MANAGEMENT SYSTEM",
            font=self.title_font,
            bg="#111111",
            fg=self.TEXT
        ).pack(side="left", padx=15)

    # -------------------------------------------------------------------------
    # SIDEBAR — navigation menu buttons
    # -------------------------------------------------------------------------
    def _build_sidebar(self):
        self.sidebar = tk.Frame(self, bg=self.PANEL, width=190)
        self.sidebar.pack(fill="y", side="left")

        tk.Label(
            self.sidebar, text="MENU",
            font=self.header_font, bg=self.PANEL, fg="#a0a0a0"
        ).pack(pady=10)

        # Each tuple: (button label, view name)
        menu = [
            ("View Inventory",  "display"),
            ("Add Product",     "add"),
            ("Search Product",  "search"),
            ("Update Stock",    "update"),
            ("Delete Product",  "delete"),
        ]

        for text, view in menu:
            btn = tk.Button(
                self.sidebar,
                text=text,
                font=self.button_font,
                bg=self.ACCENT,
                fg=self.TEXT,
                activebackground=self.HIGHLIGHT,
                activeforeground="white",
                relief="flat",
                width=18,
                command=lambda v=view: self.show_view(v)
            )
            btn.pack(pady=5)
            self.nav_buttons[view] = btn   # Save reference for active-state toggling

    # -------------------------------------------------------------------------
    # CONTENT AREA — blank frame that each view renders into
    # -------------------------------------------------------------------------
    def _build_content(self):
        self.content = tk.Frame(self, bg=self.BG)
        self.content.pack(fill="both", expand=True)

    def clear(self):
        """Destroys all widgets inside the content frame before loading a new view."""
        for w in self.content.winfo_children():
            w.destroy()

    # -------------------------------------------------------------------------
    # VIEW ROUTER — clears content and highlights the correct nav button
    # -------------------------------------------------------------------------
    def show_view(self, view):
        self.clear()

        # Highlight the active nav button, reset all others
        for k, b in self.nav_buttons.items():
            b.config(bg=self.HIGHLIGHT if k == view else self.ACCENT)

        # Dispatch to the correct view method
        if view == "display":
            self.view_display()
        elif view == "add":
            self.view_add()
        elif view == "search":
            self.view_search()
        elif view == "update":
            self.view_update()
        elif view == "delete":
            self.view_delete()

    def view_display(self):
        tk.Label(
            self.content, text="Inventory Records",
            font=self.title_font, bg=self.BG, fg=self.TEXT
        ).pack(pady=10)

        cols = ("Name", "Unit", "Quantity", "Price")

        # Create the table with column headers
        tree = ttk.Treeview(self.content, columns=cols, show="headings", height=15)

        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        # Apply dark theme styling to the Treeview widget
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        font=("Consolas", 10),
                        background=self.PANEL,
                        foreground=self.TEXT,
                        fieldbackground=self.PANEL)
        style.configure("Treeview.Heading",
                        font=("Consolas", 10, "bold"),
                        background=self.ACCENT,
                        foreground=self.TEXT)

        tree.pack(fill="both", expand=True, padx=20)

        # Populate table rows from the inventory file
        for p in load_products():
            tree.insert("", "end",
                        values=(p["name"], p["unit"], p["quantity"], p["price"]))

    def view_add(self):
        tk.Label(
            self.content, text="Add Product",
            font=self.title_font, bg=self.BG, fg=self.TEXT
        ).pack(pady=10)

        entries = {}

        # Render one label + entry pair for each field
        for field in ["Name", "Unit", "Quantity", "Price"]:
            tk.Label(
                self.content, text=field,
                font=self.header_font, bg=self.BG, fg=self.TEXT
            ).pack()

            e = tk.Entry(self.content, font=self.normal_font)
            e.pack()
            entries[field] = e

        def add():
            # Call save_product with values from all four entry fields
            save_product(
                entries["Name"].get(),
                entries["Unit"].get(),
                entries["Quantity"].get(),
                entries["Price"].get()
            )
            messagebox.showinfo("Success", "Product Added!")
            self.show_view("display")   # Return to inventory list after adding

        tk.Button(
            self.content, text="Add Product",
            font=self.button_font,
            bg=self.GREEN,
            fg="black",
            command=add
        ).pack(pady=10)



