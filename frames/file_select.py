from os import path, getcwd
from tkinter import Frame, Label, Button, PhotoImage, filedialog, BOTH, TOP, ttk

class FileSelectFrame(Frame):

    def __init__(self, master, controller):
        Frame.__init__(self, master, padx=25, pady=25)
        self.controller = controller
        self.create_title()
        self.create_select_file_btn()
        if self.controller.testing_mode:
            self.filepath = "data/sample_data.csv"
        else:
            self.filepath = None

    def create_title(self):
        title = ttk.Label(
            self,
            text="Budget Transaction Processor",
            style='Title.TLabel'
        )
        title.pack(expand=True, fill='both')

    def create_select_file_btn(self):
        img_path = path.join(getcwd(), 'img', 'file_open.png')
        image = PhotoImage(file=img_path).subsample(4, 4)
        self.select_file_btn_frame = Frame(self)
        self.select_file_btn_frame.pack(expand=True, fill='both', pady=(25, 25))
        self.select_file_btn = ttk.Button(
            self.select_file_btn_frame,
            text="Load Transactions",
            image=image,
            compound=TOP,
            command=self.file_dialog,
            style='SelectFile.TButton'
        )
        self.select_file_btn.photo = image # make sure GC doesn't collect image
        self.select_file_btn.pack()
    
    def file_dialog(self):
        self.filepath = filedialog.askopenfilename(
            parent=self,
            initialdir="./data",
            title='Choose a file',
            filetype = (("csv files","*.csv"),("all files","*.*")),
        )
        if self.filepath == '':
            return
        else:
            self.submit()
    
    def submit(self):
        if self.filepath is not None:
            self.controller.backend.read_data(self.filepath)
            self.controller.home_frame.create_widgets()
            self.controller.show_frame('home')

