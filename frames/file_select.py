
from os import path
from tkinter import Frame, Label, Button, filedialog

class FileSelectFrame(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.filepath = None

        title = Label(self, text="File Select Frame")
        title.grid(row=0, column=0)

        self.select_file_btn = Button(self, text="Select File", command=self.file_dialog)
        self.select_file_btn.grid(row=1, column=0)

        self.file_label = Label(self, text="")
        self.file_label.grid(row=1, column=1)

        self.submit_btn = Button(self, text="Submit", command=self.submit)
        self.submit_btn.grid(row=2, column=0)

    def file_dialog(self):
        self.filepath = filedialog.askopenfilename(
            parent=self,
            initialdir="./data",
            title='Choose a file',
            filetype = (("csv files","*.csv"),("all files","*.*")),
        )
        self.file_label.config(text=self.filepath)
    
    def submit(self):
        if self.filepath is not None:
            self.controller.backend.read_data(self.filepath)
            self.controller.home_frame.create_widgets()
            self.controller.show_frame('home')
        # TODO: write a popup for errors

