from tkinter import Tk
from backend import Backend
from frames.home import HomeFrame

class FinancialTranascationProcessor(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.backend = Backend()
        self.home_frame = HomeFrame(self)
