from os import path
from itertools import count
import tkinter as tk
from widgets.table_frame import TableFrame
from widgets.vendor_entry_popup import VendorEntryPopup
from widgets.category_entry_popup import CategoryEntryPopup 

class HomeFrame(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.backend = self.controller.backend
        self.current_row_gen = lambda c=count(): next(c)

    def create_widgets(self):
        self.pack_forget()

        self.title = self.create_title()
        self.title.grid(row=0, column=0)

        self.table_frame = TableFrame(self, self.backend)
        self.table_frame.grid(row=1, column=0, padx=25, sticky='EW')

        self.submit_btn = self.create_submit_button()
        self.submit_btn.grid(row=3, column=0, columnspan=2, padx=15, pady=15)

    def create_title(self):
        title = tk.Label(
            self,
            text="Financial Transaction Processor",
            font=("Arial", 18),
            pady=15
        )
        return title

    def create_submit_button(self):
        img_path = path.join('img', 'save.png')
        image = tk.PhotoImage(file=img_path).subsample(5, 5)
        submit_btn = tk.Button(
            self,
            text="Save & Quit",
            image=image,
            command=self.submit,
            compound=tk.TOP,
            font=('Arial', 8)
        )
        submit_btn.photo = image
        return submit_btn
    
    def submit(self):
        self.backend.process_button_variables()
        self.controller.destroy()
    