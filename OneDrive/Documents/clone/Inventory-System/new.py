# =========================================================
# MODERN INVENTORY SYSTEM
# CATEGORY REMOVED
# HEADER TITLE REMOVED
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
def save_product(item_no, name, unit, quantity, price):

    try:
        with open(INVENTORY_FILE, "a") as file:

            file.write(
                f"{item_no}{SEPARATOR}"
                f"{name}{SEPARATOR}"
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

                if len(parts) == 5:

                    products.append({
                        "item_no": parts[0],
                        "name": parts[1],
                        "unit": parts[2],
                        "quantity": parts[3],
                        "price": parts[4]
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

        self.title("Modern Inventory System")
        self.geometry("1450x820")
        self.resizable(False, False)
        self.configure(bg="#DDE7D8")

        self.BG = "#DDE7D8"
        self.SIDEBAR = "#C8D7C1"
        self.CARD = "#F4F4F4"
        self.ACCENT = "#6DAA63"
        self.TEXT = "#1F1F1F"
        self.RED = "#E8A7A7"

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
            height=30
        )

        header.pack(fill="x")

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
            "Unit",
            "Quantity",
            "Price"
        )

        style = ttk.Style()
        style.theme_use("clam")

        tree = ttk.Treeview(
            parent,
            columns=cols,
            show="headings",
            height=16
        )

        for col in cols:

            tree.heading(col, text=col)

            tree.column(
                col,
                anchor="center",
                width=160
            )

        tree.pack(fill="both", expand=True)

        for p in load_products():

            tree.insert(
                "",
                "end",
                values=(
                    p["item_no"],
                    p["name"],
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

        self.create_inventory_table(frame)

    # =====================================================
    # ADD PRODUCT
    # =====================================================
    def view_add(self):

        self.two_panel_layout(self.add_form)

    # =====================================================
    # SEARCH PRODUCT
    # =====================================================
    def view_search(self):

        self.two_panel_layout(self.search_form)

    # =====================================================
    # UPDATE PRODUCT
    # =====================================================
    def view_update(self):

        self.two_panel_layout(self.update_form)

    # =====================================================
    # DELETE PRODUCT
    # =====================================================
    def view_delete(self):

        self.two_panel_layout(self.delete_form)

    # =====================================================
    # TWO PANEL LAYOUT
    # =====================================================
    def two_panel_layout(self, form_function):

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

        form_function(left_frame)

        right_frame = tk.Frame(
            main_frame,
            bg=self.CARD,
            padx=30,
            pady=30
        )

        right_frame.pack(side="right", fill="both", expand=True)

        self.create_inventory_table(right_frame)

    # =====================================================
    # ADD FORM
    # =====================================================
    def add_form(self, frame):

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
                frame,
                text=field,
                font=self.header_font,
                bg=self.CARD
            ).pack(anchor="w")

            e = tk.Entry(
                frame,
                font=self.normal_font,
                width=30
            )

            e.pack(pady=8, ipady=6)

            entries[field] = e

        def add():

            item_no = entries["Item Number"].get().strip()
            name = entries["Product Name"].get().strip()
            unit = entries["Unit"].get().strip()
            quantity = entries["Quantity"].get().strip()
            price = entries["Price"].get().strip()

            if (
                item_no == "" or
                name == "" or
                unit == "" or
                quantity == "" or
                price == ""
            ):

                messagebox.showerror(
                    "Input Error",
                    "All fields are required."
                )

                return

            if not quantity.isdigit():

                messagebox.showerror(
                    "Input Error",
                    "Quantity must be a whole number."
                )

                return

            try:
                float(price)

            except ValueError:

                messagebox.showerror(
                    "Input Error",
                    "Price must be a valid number."
                )

                return

            for p in load_products():

                if p["item_no"] == item_no:

                    messagebox.showerror(
                        "Duplicate Error",
                        "Item Number already exists."
                    )

                    return

            success = save_product(
                item_no,
                name,
                unit,
                quantity,
                price
            )

            if success:

                messagebox.showinfo(
                    "Success",
                    "Product added successfully!"
                )

                self.show_view("add")

        tk.Button(
            frame,
            text="Add Product",
            font=self.button_font,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            width=20,
            height=2,
            command=add
        ).pack(pady=20)

    # =====================================================
    # SEARCH FORM
    # =====================================================
    def search_form(self, frame):

        entry = tk.Entry(
            frame,
            font=self.normal_font,
            width=30
        )

        entry.pack(pady=10, ipady=6)

        result = tk.Listbox(
            frame,
            width=35,
            height=10,
            font=self.normal_font
        )

        result.pack(pady=15)

        def search():

            result.delete(0, tk.END)

            keyword = entry.get().strip().lower()

            found = False

            for p in load_products():

                if keyword == p["name"].lower():

                    result.insert(
                        tk.END,
                        f"{p['item_no']} | "
                        f"{p['name']} | "
                        f"{p['quantity']} | "
                        f"₱{p['price']}"
                    )

                    found = True

            if not found:
                result.insert(tk.END, "Product not found.")

        tk.Button(
            frame,
            text="Search Product",
            font=self.button_font,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            width=20,
            height=2,
            command=search
        ).pack(pady=10)

    # =====================================================
    # UPDATE FORM
    # =====================================================
    def update_form(self, frame):

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
                frame,
                text=field,
                font=self.header_font,
                bg=self.CARD
            ).pack(anchor="w")

            e = tk.Entry(
                frame,
                font=self.normal_font,
                width=30
            )

            e.pack(pady=8, ipady=6)

            entries[field] = e

        def update_product():

            data = load_products()

            target = entries["Current Item Number"].get().strip()

            found = False

            for p in data:

                if p["item_no"] == target:

                    if entries["New Product Name"].get().strip():
                        p["name"] = entries["New Product Name"].get()

                    if entries["New Unit"].get().strip():
                        p["unit"] = entries["New Unit"].get()

                    if entries["New Quantity"].get().strip():
                        p["quantity"] = entries["New Quantity"].get()

                    if entries["New Price"].get().strip():
                        p["price"] = entries["New Price"].get()

                    found = True
                    break

            if not found:

                messagebox.showerror(
                    "Error",
                    "Product not found."
                )

                return

            write_all_products(data)

            messagebox.showinfo(
                "Success",
                "Product updated successfully!"
            )

            self.show_view("update")

        tk.Button(
            frame,
            text="Update Product",
            font=self.button_font,
            bg=self.ACCENT,
            fg="white",
            relief="flat",
            width=20,
            height=2,
            command=update_product
        ).pack(pady=20)

    # =====================================================
    # DELETE FORM
    # =====================================================
    def delete_form(self, frame):

        entry = tk.Entry(
            frame,
            font=self.normal_font,
            width=30
        )

        entry.pack(pady=10, ipady=6)

        def delete_product():

            keyword = entry.get().strip().lower()

            data = load_products()

            original_length = len(data)

            data = [
                p for p in data
                if (
                    p["item_no"].lower() != keyword and
                    p["name"].lower() != keyword
                )
            ]

            if len(data) == original_length:

                messagebox.showerror(
                    "Delete Error",
                    "Product not found."
                )

                return

            write_all_products(data)

            messagebox.showinfo(
                "Success",
                "Product deleted successfully!"
            )

            self.show_view("delete")

        tk.Button(
            frame,
            text="Delete Product",
            font=self.button_font,
            bg=self.RED,
            fg="black",
            relief="flat",
            width=20,
            height=2,
            command=delete_product
        ).pack(pady=20)


# =========================================================
# GLOBAL ERROR HANDLER
# =========================================================
def handle_global_exception(exc_type, exc_value, exc_traceback):

    messagebox.showerror(
        "Application Error",
        f"An unexpected error occurred.\n\n{exc_value}"
    )


# =========================================================
# RUN APPLICATION
# =========================================================
if __name__ == "__main__":

    app = InventoryApp()

    app.report_callback_exception = handle_global_exception

    app.mainloop()