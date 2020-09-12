from tkinter import Toplevel, Frame, Label, Entry, Button, StringVar, messagebox
from widgets.dropdown import DropDown


class CategoryEntryPopup(Toplevel):

    def __init__(self, controller):
        self.controller = controller
        Toplevel.__init__(self)
        self.title("Add Category")
        self.frame = Frame(self)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        Label(self.frame, text="Category:").grid(
            row=0,
            column=0,
            padx=(0, 50),
            pady=(15, 5),
            sticky='NSW',
        )
        self.category_entry = Entry(self.frame, width=50)
        self.category_entry.grid(row=0, column=1, pady=25)
        btn = Button(self.frame, text="Submit", command=self.add_category)
        btn.grid(row=1, column=0, columnspan=2, padx=10, pady=15)
        self.category_entry.focus_set()
    
    def add_category(self):
        category = self.category_entry.get()
        if category == '':
            messagebox.showerror('Error', 'No category provided')
        else:
            try:
                self.controller.backend.add_category(category)
                if self.controller.backend.transaction_data:
                    for transaction in self.controller.backend.transaction_data:
                        transaction['category_dropdown'].add_category(category)
                self.destroy()
            except ValueError:
                messagebox.showerror("Error", "Category Already Exists")



