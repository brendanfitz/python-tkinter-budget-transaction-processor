from tkinter import Toplevel, Entry, Button, StringVar, messagebox
from widgets.dropdown import DropDown


class CategoryEntryPopup(Toplevel):

    def __init__(self, controller):
        self.controller = controller
        Toplevel.__init__(self)
        self.title("Add Category")
        self.category_entry = Entry(self)
        self.category_entry.grid(row=0, column=0)
        btn = Button(self, text="Submit", command=self.add_category)
        btn.grid(row=1, column=0)
    
    def add_category(self):
        category = self.category_entry.get()
        if category == '':
            messagebox.showerror('Error', 'No category provided')
        else:
            try:
                self.controller.backend.add_category(category)
                for transaction in self.controller.backend.transaction_data:
                    transaction['category_dropdown'].add_category(category)
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Category Already Exists")



