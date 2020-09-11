from tkinter import Tk, Frame
from backend import Backend
from frames.home import HomeFrame
from frames.file_select import FileSelectFrame

class FinancialTranascationProcessor(Tk):

    def __init__(self, filename, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
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

        self.file_select_frame.tkraise()
    
    def show_frame(self, name):
        if name == 'home':
            self.home_frame.tkraise()
        elif name == 'file_select':
            self.file_select_frame.tkraise()
        else:
            raise ValueError("name must be either 'home' or 'file_select'")