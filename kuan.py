# =========================================================
# MODERN INVENTORY SYSTEM
# COMPLETE UPDATED VERSION
# =========================================================

import tkinter as tk
from tkinter import ttk, messagebox, font
import os

# =========================================================
# FILE SETTINGS
# =========================================================
INVENTORY_FILE = "inventory.txt"
SEPARATOR = "|"


# =========================================================
# SAVE PRODUCT
# =========================================================
def save_product(item_no, name, category, unit, quantity, price):

    try:
        with open(INVENTORY_FILE, "a") as file:

            file.write(
                f"{item_no}{SEPARATOR}"
                f"{name}{SEPARATOR}"
                f"{category}{SEPARATOR}"
                f"{unit}{SEPARATOR}"
                f"{quantity}{SEPARATOR}"
                f"{price}\n"
            )

        return True

    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return False


# =========================================================
# LOAD PRODUCTS
# =========================================================
def load_products():

    products = []

    if not os.path.exists(INVENTORY_FILE):
        return products

    try:
        with open(INVENTORY_FILE, "r") as file:

            for line in file:

                parts = line.strip().split(SEPARATOR)

                if len(parts) == 6:

                    products.append({
                        "item_no": parts[0],
                        "name": parts[1],
                        "category": parts[2],
                        "unit": parts[3],
                        "quantity": parts[4],
                        "price": parts[5]
                    })

    except Exception as e:
        messagebox.showerror("File Error", str(e))

    return products


# =========================================================
# WRITE ALL PRODUCTS
# =========================================================
def write_all_products(products):

    try:
        with open(INVENTORY_FILE, "w") as file:

            for p in products:

                file.write(
                    f"{p['item_no']}{SEPARATOR}"
                    f"{p['name']}{SEPARATOR}"
                    f"{p['category']}{SEPARATOR}"
                    f"{p['unit']}{SEPARATOR}"
                    f"{p['quantity']}{SEPARATOR}"
                    f"{p['price']}\n"
                )

        return True

    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return False


# =========================================================
# MAIN APP
# =========================================================
class InventoryApp(tk.Tk):

    def __init__(self):

        super().__init__()

        # WINDOW
        self.title("Modern Inventory System")
        self.geometry("1450x820")
        self.resizable(False, False)
        self.configure(bg="#DDE7D8")

        # COLORS
        self.BG = "#DDE7D8"
        self.SIDEBAR = "#C8D7C1"
        self.CARD = "#F4F4F4"
        self.ACCENT = "#6DAA63"
        self.TEXT = "#1F1F1F"
        self.RED = "#E8A7A7"

        # FONTS
        self.title_font = font.Font(
            family="Times New Roman",
            size=38,
            weight="bold"
        )

        self.header_font = font.Font(
            family="Calibri",
            size=12,
            weight="bold"
        )

        self.normal_font = font.Font(
            family="Calibri",
            size=11
        )

        self.button_font = font.Font(
            family="Calibri",
            size=11,
            weight="bold"
        )

        self.nav_buttons = {}

        self.build_header()
        self.build_sidebar()
        self.build_content()

        self.show_view("display")

    # =====================================================
    # HEADER
    # =====================================================
    def build_header(self):

        header = tk.Frame(
            self,
            bg="white",
            height=100
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="Inventory List",
            font=self.title_font,
            bg="white",
            fg=self.TEXT
        ).pack(pady=20)

    # =====================================================
    # SIDEBAR
    # =====================================================
    def build_sidebar(self):

        self.sidebar = tk.Frame(
            self,
            bg=self.SIDEBAR,
            width=180
        )

        self.sidebar.pack(side="left", fill="y")

        tk.Label(
            self.sidebar,
            text="MENU",
            font=self.header_font,
            bg=self.SIDEBAR,
            fg=self.TEXT
        ).pack(pady=25)

        menu = [
            ("Inventory", "display"),
            ("Add Product", "add"),
            ("Search Product", "search"),
            ("Update Product", "update"),
            ("Delete Product", "delete")
        ]

        for text, view in menu:

            btn = tk.Button(
                self.sidebar,
                text=text,
                font=self.button_font,
                bg=self.SIDEBAR,
                fg=self.TEXT,
                relief="flat",
                bd=0,
                activebackground="#B8C9B0",
                activeforeground=self.TEXT,
                width=18,
                height=2,
                cursor="hand2",
                command=lambda v=view: self.show_view(v)
            )

            btn.pack(pady=8)

            self.nav_buttons[view] = btn

    # =====================================================
    # CONTENT
    # =====================================================
    def build_content(self):

        self.content = tk.Frame(
            self,
            bg=self.BG
        )

        self.content.pack(fill="both", expand=True)

    # =====================================================
    # CLEAR CONTENT
    # =====================================================
    def clear(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # =====================================================
    # SWITCH VIEW
    # =====================================================
    def show_view(self, view):

        self.clear()

        for k, b in self.nav_buttons.items():

            if k == view:
                b.config(bg=self.ACCENT, fg="white")

            else:
                b.config(bg=self.SIDEBAR, fg=self.TEXT)

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

    # =====================================================
    # INVENTORY TABLE
    # =====================================================
    def create_inventory_table(self, parent):

        cols = (
            "Item No",
            "Product",
            "Category",
            "Unit",
            "Quantity",
            "Price"
        )

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#F3F3F3",
            foreground=self.TEXT,
            fieldbackground="#F3F3F3",
            rowheight=42,
            font=("Calibri", 11),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#C8D7C1",
            foreground=self.TEXT,
            font=("Calibri", 11, "bold"),
            relief="flat"
        )

        tree = ttk.Treeview(
            parent,
            columns=cols,
            show="headings",
            height=18
        )

        for col in cols:

            tree.heading(col, text=col)

            tree.column(
                col,
                anchor="center",
                width=140
            )

        tree.pack(fill="both", expand=True)

        for p in load_products():

            tree.insert(
                "",
                "end",
                values=(
                    p["item_no"],
                    p["name"],
                    p["category"],
                    p["unit"],
                    p["quantity"],
                    p["price"]
                )
            )

    # =====================================================
    # DISPLAY
    # =====================================================
    def view_display(self):

        frame = tk.Frame(
            self.content,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        frame.pack(fill="both", expand=True, padx=30, pady=30)

        tk.Label(
            frame,
            text="Inventory List",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="center", pady=(0, 25))

        self.create_inventory_table(frame)

    # =====================================================
    # ADD PRODUCT
    # =====================================================
    def view_add(self):

        main_frame = tk.Frame(
            self.content,
            bg=self.BG
        )

        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        left_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            width=360,
            padx=30,
            pady=30
        )

        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="Add Product",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w", pady=(0, 25))

        entries = {}

        fields = [
            "Item Number",
            "Product Name",
            "Unit",
            "Quantity",
            "Price"
        ]

        for field in fields:

            tk.Label(
                left_frame,
                text=field,
                font=self.header_font,
                bg=self.CARD,
                fg=self.TEXT
            ).pack(anchor="w")

            e = tk.Entry(
                left_frame,
                font=self.normal_font,
                width=30,
                relief="solid",
                bd=1
            )

            e.pack(pady=8, ipady=6)

            entries[field] = e

        tk.Label(
            left_frame,
            text="Category",
            font=self.header_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w")

        category_combo = ttk.Combobox(
            left_frame,
            values=[
                "Food",
                "Drinks",
                "Electronics",
                "Clothing",
                "School Supplies",
                "Accessories",
                "Others"
            ],
            state="readonly",
            width=27
        )

        category_combo.pack(pady=8, ipady=5)
        category_combo.set("Food")

        def add():

            item_no = entries["Item Number"].get().strip()
            name = entries["Product Name"].get().strip()
            unit = entries["Unit"].get().strip()
            quantity = entries["Quantity"].get().strip()
            price = entries["Price"].get().strip()
            category = category_combo.get()

            if (
                item_no == "" or
                name == "" or
                unit == "" or
                quantity == "" or
                price == ""
            ):

                messagebox.showerror(
                    "Input Error",
                    "Please fill all fields."
                )

                return

            save_product(
                item_no,
                name,
                category,
                unit,
                quantity,
                price
            )

            messagebox.showinfo(
                "Success",
                "Product added successfully!"
            )

            self.show_view("add")

        tk.Button(
            left_frame,
            text="Add Product",
            font=self.button_font,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            bd=0,
            width=20,
            height=2,
            cursor="hand2",
            command=add
        ).pack(pady=20)

        right_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_frame,
            text="Inventory List",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="center", pady=(0, 20))

        self.create_inventory_table(right_frame)

    # =====================================================
    # SEARCH PRODUCT
    # =====================================================
    def view_search(self):

        main_frame = tk.Frame(
            self.content,
            bg=self.BG
        )

        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        left_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            width=360,
            padx=30,
            pady=30
        )

        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="Search Product",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w", pady=(0, 25))

        tk.Label(
            left_frame,
            text="Product Name",
            font=self.header_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w")

        entry = tk.Entry(
            left_frame,
            font=self.normal_font,
            width=30,
            relief="solid",
            bd=1
        )

        entry.pack(pady=8, ipady=6)

        result = tk.Listbox(
            left_frame,
            width=40,
            height=12,
            font=self.normal_font,
            bg="white",
            fg=self.TEXT,
            relief="solid",
            bd=1
        )

        result.pack(pady=15)

        def search():

            result.delete(0, tk.END)

            keyword = entry.get().strip().lower()

            found = False

            for p in load_products():

                if keyword == p["name"].lower():

                    result.insert(tk.END, f"Item #: {p['item_no']}")
                    result.insert(tk.END, f"Product: {p['name']}")
                    result.insert(tk.END, f"Category: {p['category']}")
                    result.insert(tk.END, f"Quantity: {p['quantity']}")
                    result.insert(tk.END, f"Price: ₱{p['price']}")
                    result.insert(tk.END, "-----------------------")

                    found = True

            if not found:
                result.insert(tk.END, "Product not found.")

        tk.Button(
            left_frame,
            text="Search Product",
            font=self.button_font,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            bd=0,
            width=20,
            height=2,
            command=search
        ).pack(pady=10)

        right_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_frame,
            text="Inventory List",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="center", pady=(0, 20))

        self.create_inventory_table(right_frame)

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================
    def view_update(self):

        main_frame = tk.Frame(
            self.content,
            bg=self.BG
        )

        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        left_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            width=360,
            padx=30,
            pady=30
        )

        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="Update Product",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w", pady=(0, 25))

        entries = {}

        fields = [
            "Current Item Number",
            "New Product Name",
            "New Unit",
            "New Quantity",
            "New Price"
        ]

        for field in fields:

            tk.Label(
                left_frame,
                text=field,
                font=self.header_font,
                bg=self.CARD
            ).pack(anchor="w")

            e = tk.Entry(
                left_frame,
                font=self.normal_font,
                width=30
            )

            e.pack(pady=8, ipady=6)

            entries[field] = e

        tk.Button(
            left_frame,
            text="Update Product",
            font=self.button_font,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            bd=0,
            width=20,
            height=2
        ).pack(pady=20)

        right_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_frame,
            text="Inventory List",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="center", pady=(0, 20))

        self.create_inventory_table(right_frame)

    # =====================================================
    # DELETE PRODUCT
    # =====================================================
    def view_delete(self):

        main_frame = tk.Frame(
            self.content,
            bg=self.BG
        )

        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        left_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            width=360,
            padx=30,
            pady=30
        )

        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)

        tk.Label(
            left_frame,
            text="Delete Product",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="w", pady=(0, 25))

        entry = tk.Entry(
            left_frame,
            font=self.normal_font,
            width=30
        )

        entry.pack(ipady=6)

        tk.Button(
            left_frame,
            text="Delete Product",
            font=self.button_font,
            bg=self.RED,
            fg="red",
            relief="flat",
            bd=0,
            width=20,
            height=2
        ).pack(pady=20)

        right_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_frame,
            text="Inventory List",
            font=self.title_font,
            bg=self.CARD,
            fg=self.TEXT
        ).pack(anchor="center", pady=(0, 20))

        self.create_inventory_table(right_frame)


# =========================================================
# RUN APP
# =========================================================
if __name__ == "__main__":

    app = InventoryApp()
    app.mainloop()