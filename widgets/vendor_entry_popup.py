from tkinter import Toplevel, Entry, Button, StringVar, messagebox
from widgets.dropdown import DropDown


class VendorEntryPopup(Toplevel):

    def __init__(self, controller):
        self.controller = controller
        Toplevel.__init__(self)
        self.title("Add Vendor")
        self.vendor_entry = Entry(self)
        self.vendor_entry.grid(row=0, column=0)
        self.category_var = StringVar(self.controller)
        self.category_dropdown = DropDown(self, self.controller, self.category_var, 'Category')
        self.category_dropdown.grid(row=1, column=0)
        btn = Button(self, text="Submit", command=self.add_vendor)
        btn.grid(row=2, column=0)
    
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
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Vendor Already Exists")



