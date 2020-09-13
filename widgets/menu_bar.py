from tkinter import Menu
from widgets.vendor_entry_popup import VendorEntryPopup
from widgets.category_entry_popup import CategoryEntryPopup 

class MenuBar(Menu):

    def __init__(self, master):
        super().__init__(master)
        self.master.config(menu=self)
        self.file_menu = Menu(self, tearoff=0)

    def add_commands(self):
        self.file_menu.add_command(
            label="Select File Screen",
            command=lambda: self.master.show_frame('file_select')
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: self.master.destroy())

        self.add_cascade(label="File", menu=self.file_menu)

        self.insert_menu = Menu(self, tearoff=0)
        self.insert_menu.add_command(label="Category", command=lambda: CategoryEntryPopup(self.master.home_frame))
        self.insert_menu.add_command(label="Vendor", command=lambda: VendorEntryPopup(self.master.home_frame))

        self.add_cascade(label="Insert", menu=self.insert_menu)