
from tkinter import Frame, Label, Button

class FileSelectFrame(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        title = Label(self, text="File Select Frame")
        title.grid(row=0, column=0)

        btn = Button(self, text="Submit", command=lambda: self.controller.show_frame('home'))
        btn.grid(row=1, column=0)

