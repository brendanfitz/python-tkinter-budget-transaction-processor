from tkinter import Tk, ttk, Frame, Menu
from backend import Backend
from frames import HomeFrame, FileSelectFrame
from widgets import VendorEntryPopup, CategoryEntryPopup 

class App(Tk):

    def __init__(self, testing_mode, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        
        icon_filepath = 'img/budget.ico'
        self.wm_iconbitmap(icon_filepath)
        self.iconbitmap(default=icon_filepath)

        self.resizable(False, False)

        self.set_style()

        self.testing_mode = testing_mode
        self.title("Budget Transaction Processor")
        self.backend = Backend()

        self.container = Frame(self)
        self.container.pack(side="top",
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.home_frame = HomeFrame(self.container, self)
        self.home_frame.grid(row=0, column=0, sticky='nsew')

        self.file_select_frame = FileSelectFrame(self.container, self)
        self.file_select_frame.grid(row=0, column=0, sticky='nsew')

        self.create_menubar()

        self.file_select_frame.tkraise()

        if self.testing_mode:
            self.file_select_frame.submit()

    def show_frame(self, name):
        if name == 'home':
            self.home_frame.tkraise()
        elif name == 'file_select':
            self.file_select_frame.tkraise()
        else:
            raise ValueError("name must be either 'home' or 'file_select'")

    def create_menubar(self):
        self.menu = Menu(self)
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
        self.insert_menu.add_command(
            label="Category",
            command=lambda: CategoryEntryPopup(self.home_frame)
        )
        self.insert_menu.add_command(
            label="Vendor",
            command=lambda: VendorEntryPopup(self.home_frame)
        )

        self.menu.add_cascade(label="Insert", menu=self.insert_menu)
    
    def set_style(self):
        style = ttk.Style(self)
        style.configure('.', font=('Arial', 9)) # set root style font
        style.configure(
            'DropDown.TCombobox',
            borderwidth=1,
            bordercolor='black',
            relief='solid',
        )
        style.configure('DropDown.TCombobox.textarea', font=('Arial', 9))
        style.configure('DropDown.TCombobox.border', relief='solid')
        style.configure('TableRow.TLabel',
            height=1,
            bd=1,
            relief="solid",
            background="white",
            highlightbackground="blue",
            padding=(1, 1, 0, 0)
        )
        style.configure('TableHeader.TLabel',
            foreground="white",
            background="dark slate gray",
            bd=1,
            relief="flat",
            padding=(1, 1, 0, 0)
        )
        style.configure('Submit.TButton',
            font=('Arial', 8)
        )
        style.configure('Title.TLabel',
            font=("Arial", 18),
            padding=(0, 15),
            anchor='center'
        )
        style.configure('SelectFile.TButton',
            font=('Arial', 8),
            padding=5
        )