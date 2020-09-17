from os import path
from itertools import count
import tkinter as tk
from tkinter import ttk
from widgets import TableFrame, VendorEntryPopup, CategoryEntryPopup 

class HomeFrame(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.backend = self.controller.backend

    def create_widgets(self):
        self.pack_forget()

        self.title = self.create_title()
        self.title.grid(row=0, column=0)

        self.table_frame = TableFrame(self, self.backend)
        self.table_frame.grid(row=1, column=0, padx=15, sticky='EW')

        self.submit_btn = self.create_submit_button()
        self.submit_btn.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=15,
            pady=(15, 0)
        )

    def create_title(self):
        title = ttk.Label(
            self,
            text="Budget Transaction Processor",
            style="Title.TLabel"
        )
        return title

    def create_submit_button(self):
        img_path = path.join('img', 'save.png')
        image = tk.PhotoImage(file=img_path).subsample(5, 5)
        submit_btn = ttk.Button(
            self,
            text="Save & Quit",
            image=image,
            command=self.submit,
            compound=tk.TOP,
            style='Submit.TButton'
        )
        submit_btn.photo = image
        return submit_btn
    
    def submit(self):
        self.backend.process_button_variables()
        self.controller.destroy()