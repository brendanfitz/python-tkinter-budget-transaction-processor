from tkinter import Tk, Frame, Menu
from backend import Backend
from frames.home import HomeFrame
from frames.file_select import FileSelectFrame
from widgets.menu_bar import MenuBar

class FinancialTranascationProcessor(Tk):

    def __init__(self, testing_mode, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("1175x425")
        self.resizable(False, False)
        self.testing_mode = testing_mode
        self.title("Bank Transaction Processor")
        self.backend = Backend()

        self.container = Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.menu = MenuBar(self)

        self.home_frame = HomeFrame(self.container, self)
        self.home_frame.pack(fill="both", expand=True)

        self.file_select_frame = FileSelectFrame(self.container, self)
        self.file_select_frame.pack(fill="both", expand=True)

        self.menu.add_commands()

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