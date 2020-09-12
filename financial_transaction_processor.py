from tkinter import Tk, Frame, Menu
from backend import Backend
from frames.home import HomeFrame
from frames.file_select import FileSelectFrame
from widgets.vendor_entry_popup import VendorEntryPopup
from widgets.category_entry_popup import CategoryEntryPopup 

class FinancialTranascationProcessor(Tk):

    def __init__(self, testing_mode, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("1175x425")
        self.testing_mode = testing_mode
        self.title("Bank Transaction Processor")
        self.backend = Backend()

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.home_frame = HomeFrame(self.container, self)
        self.home_frame.grid(row=0, column=0, sticky='nsew')

        self.file_select_frame = FileSelectFrame(self.container, self)
        self.file_select_frame.grid(row=0, column=0, sticky='nsew')

        self.create_menubar()

        self.file_select_frame.tkraise()

    def show_frame(self, name):
        if name == 'home':
            self.home_frame.tkraise()
        elif name == 'file_select':
            self.file_select_frame.tkraise()
        else:
            raise ValueError("name must be either 'home' or 'file_select'")

    def create_menubar(self):
        self.navbar = Frame(
            self.container,
            bd=2,
            relief="groove",
        )
        self.navbar.grid(row=0, column=0, columnspan=2, sticky='NSEW')

        self.menu = Menu(self.navbar)
        self.config(menu=self.menu)

        self.file_menu = Menu(self.menu, tearoff=0)

        self.file_menu.add_command(
            label="Select File Screen",
            command=lambda: self.show_frame('file_select')
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: self.destroy())

        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.insert_menu = Menu(self.menu, tearoff=0)
        self.insert_menu.add_command(label="Category", command=lambda: CategoryEntryPopup(self.home_frame))
        self.insert_menu.add_command(label="Vendor", command=lambda: VendorEntryPopup(self.home_frame))

        self.menu.add_cascade(label="Insert", menu=self.insert_menu)