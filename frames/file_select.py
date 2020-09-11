
from os import path
from tkinter import Frame, Label, Button, filedialog, BOTH

class FileSelectFrame(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.padding_kwargs = dict(padx=10, pady=10)
        self.font_kwargs = dict(font=("Arial", 10))
        self.pack_kwargs = dict(expand=True, fill=BOTH)
        self.create_title()
        self.create_select_file_btn()
        self.create_file_label()
        self.create_submit_btn()

    def create_title(self):
        title = Label(self, text="Bank Transaction Processor", font=("Arial", 18), )
        title.pack(**self.pack_kwargs)

    def create_select_file_btn(self):
        self.select_file_btn_frame = Frame(self)
        self.select_file_btn_frame.pack(**self.pack_kwargs)
        self.select_file_btn = Button(self.select_file_btn_frame,
            text="Select File",
            command=self.file_dialog,
            **self.font_kwargs
        )
        self.select_file_btn.config(height=1, width=15)
        self.select_file_btn.pack()

    def create_file_label(self):
        filename_text = "data/sample_data.csv" if self.controller.testing_mode else ""
        self.filepath = filename_text
        self.file_label_frame = Frame(self)
        self.file_label_frame.pack(**self.pack_kwargs)
        self.file_label = Label(self.file_label_frame, text=filename_text, **self.font_kwargs)
        self.file_label.config(height=2, width=30)
        self.file_label.pack()

    def create_submit_btn(self):
        self.submit_btn_frame = Frame(self)
        self.submit_btn_frame.pack(**self.pack_kwargs)
        self.submit_btn = Button(self.submit_btn_frame, text="Submit", command=self.submit, **self.font_kwargs)
        self.submit_btn.config(height=1, width=15)
        self.submit_btn.pack()

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

