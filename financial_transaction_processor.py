from tkinter import Tk, Frame
from backend import Backend
from frames.home import HomeFrame

class FinancialTranascationProcessor(Tk):

    def __init__(self, filename, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.backend = Backend(filename)
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.home_frame = HomeFrame(self.container, self)
