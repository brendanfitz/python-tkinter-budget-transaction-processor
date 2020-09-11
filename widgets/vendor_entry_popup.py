from tkinter import Toplevel, Frame, Label, Entry, Button, StringVar, messagebox
from widgets.dropdown import DropDown


class VendorEntryPopup(Toplevel):

    def __init__(self, controller):
        self.controller = controller
        Toplevel.__init__(self)
        self.title("Add Vendor")
        self.frame = Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        Label(self.frame, text="Vendor:").grid(row=0, column=0, padx=(0, 50), pady=(15, 5))
        self.vendor_entry = Entry(self.frame, width=50+2, **self.controller.font_kwargs)
        self.vendor_entry.grid(row=0, column=1)
        Label(self.frame, text="Category:").grid(row=1, column=0, padx=(0, 50), pady=(5, 15))
        self.category_var = StringVar(self.controller)
        self.category_dropdown = DropDown(self.frame, self.controller, self.category_var, 'Category', width=50)
        self.category_dropdown.grid(row=1, column=1)
        btn = Button(self.frame, text="Submit", command=self.add_vendor)
        btn.grid(row=2, column=0, columnspan=2, padx=10, pady=15)
        self.vendor_entry.focus_set()
    
    def add_vendor(self):
        vendor = self.vendor_entry.get()
        category = self.category_var.get()
        if vendor == '':
            messagebox.showerror('Error', 'No vendor provided')
        elif category == '':
            messagebox.showerror('Error', 'No category provided')
        else:
            try:
                self.controller.backend.add_vendor(vendor, category)
                for transaction in self.controller.backend.transaction_data:
                    transaction['vendor_dropdown'].add_vendor(vendor)
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Vendor Already Exists")



