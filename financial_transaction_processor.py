from tkinter import Tk
from frames.home import HomeFrame

class FinancialTranascationProcessor(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.home_frame = HomeFrame(self)
