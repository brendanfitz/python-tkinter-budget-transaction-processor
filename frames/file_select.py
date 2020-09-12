from os import path, getcwd
from tkinter import Frame, Label, Button, PhotoImage, filedialog, BOTH, TOP

class FileSelectFrame(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller
        self.padding_kwargs = dict(padx=10, pady=10)
        self.font_kwargs = dict(font=("Arial", 10))
        self.pack_kwargs = dict(expand=True, fill=BOTH)
        self.create_title()
        self.create_empty_frame()
        self.create_select_file_btn()
        self.create_file_label()

    def create_title(self):
        title = Label(self, text="Bank Transaction Processor", font=("Arial", 18), )
        title.pack(**self.pack_kwargs)

    def create_select_file_btn(self):
        img_path = path.join(getcwd(), 'img', 'file_open.png')
        image = PhotoImage(file=img_path).subsample(4, 4)
        self.select_file_btn_frame = Frame(self)
        self.select_file_btn_frame.pack(**self.pack_kwargs)
        self.select_file_btn = Button(self.select_file_btn_frame,
            text="Load Transactions",
            image=image,
            compound=TOP,
            command=self.file_dialog,
            **self.font_kwargs
        )
        self.select_file_btn.photo = image
        self.select_file_btn.pack()
    
    def create_empty_frame(self):
        frame = Frame(self)
        frame.pack(**self.pack_kwargs)
        Label(frame, text="").pack()

    def create_file_label(self):
        filename_text = "data/sample_data.csv" if self.controller.testing_mode else ""
        self.filepath = filename_text
        self.file_label_frame = Frame(self)
        self.file_label_frame.pack(**self.pack_kwargs)
        self.file_label = Label(self.file_label_frame, text=filename_text, **self.font_kwargs)
        self.file_label.config(height=2, width=30)
        self.file_label.pack()

    def file_dialog(self):
        self.filepath = filedialog.askopenfilename(
            parent=self,
            initialdir="./data",
            title='Choose a file',
            filetype = (("csv files","*.csv"),("all files","*.*")),
        )
        _, filename = path.split(self.filepath)
        self.file_label.config(text=filename)
        self.submit()
    
    def submit(self):
        if self.filepath is not None:
            self.controller.backend.read_data(self.filepath)
            self.controller.home_frame.create_widgets()
            self.controller.show_frame('home')
        # TODO: write a popup for errors

