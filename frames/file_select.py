
from os import path
from tkinter import Frame, Label, Button, filedialog

class FileSelectFrame(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.padding_kwargs = dict(padx=10, pady=10)
        self.font_kwargs = dict(font=("Arial", 10))

        title = Label(self, text="Bank Transaction Processor", font=("Arial", 18))
        title.grid(row=0, column=0, **self.padding_kwargs)

        self.select_file_btn = Button(self, text="Select File", command=self.file_dialog, **self.font_kwargs)
        self.select_file_btn.config(height=1, width=15)
        self.select_file_btn.grid(row=1, column=0, **self.padding_kwargs)

        filename_text = "data/sample_data.csv" if self.controller.testing_mode else ""
        self.filepath = filename_text
        self.file_label = Label(self, text=filename_text, **self.font_kwargs)
        self.file_label.config(height=2, width=30)
        self.file_label.grid(row=2, column=0, **self.padding_kwargs)

        self.submit_btn = Button(self, text="Submit", command=self.submit, **self.font_kwargs)
        self.submit_btn.config(height=1, width=15)
        self.submit_btn.grid(row=3, column=0, **self.padding_kwargs)

    def file_dialog(self):
        self.filepath = filedialog.askopenfilename(
            parent=self,
            initialdir="./data",
            title='Choose a file',
            filetype = (("csv files","*.csv"),("all files","*.*")),
        )
        _, filename = path.split(self.filepath)
        self.file_label.config(text=filename)
    
    def submit(self):
        if self.filepath is not None:
            self.controller.backend.read_data(self.filepath)
            self.controller.home_frame.create_widgets()
            self.controller.show_frame('home')
        # TODO: write a popup for errors

