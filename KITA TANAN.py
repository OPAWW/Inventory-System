import tkinter as tk
from tkinter import ttk, messagebox, font
import os

# =============================================================================
# [APPLE] IMPORTS & FILE HANDLING
# Responsible for: all import statements, INVENTORY_FILE, SEPARATOR,
#                  save_product(), load_products(), write_all_products()
# Lines: 1 – 68
# These functions handle all reading and writing to inventory.txt.
# ============================================================================

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


