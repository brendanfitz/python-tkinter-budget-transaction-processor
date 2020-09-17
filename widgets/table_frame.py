import tkinter as tk
from tkinter import ttk
from widgets.canvas_table import CanvasTable

class TableFrame(tk.Frame):
    COLUMN_ALIGNMENTS = {
        'Transaction Date': tk.W,
        'Description': tk.W,
        'Amount': tk.E,
        'Vendor': tk.W,
        'Category': tk.W, 
    }
    FONT_KWARGS = dict(font=('Arial', 10))

    def __init__(self, master, backend):
        tk.Frame.__init__(self, master)
        self.backend = backend
        self.top_bar = self.create_top_bar()
        self.top_bar.grid(row=0, column=0, sticky='nsw')
        self.canvas = CanvasTable(self)
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.scrolly = self.create_scrolly()
        self.scrolly.grid(row=1, column=1, rowspan=1, sticky='nsw')
    
    def create_top_bar(self):
        columns = ['Transaction Date', 'Description', 'Amount']
        top_bar = tk.Frame(self, background='dark slate gray')
        for c, column in enumerate(columns + ['Vendor', 'Category']):
            grid_pad = dict()
            fmt_kwargs = dict(
                width=CanvasTable.COLUMN_WIDTHS[column],
                fg="white",
                background="dark slate gray",
                bd=1,
                relief="flat",
                padx=2,
                anchor=TableFrame.COLUMN_ALIGNMENTS[column],
                **TableFrame.FONT_KWARGS
            )
            if column in ['Vendor', 'Category']:
                grid_pad['padx'] = (0, 26) # padding for dropdown arrow
            label = tk.Label(top_bar, text=column, **fmt_kwargs)
            label.grid(row=0, column=c, sticky='ns', **grid_pad)
        return top_bar

    def create_scrolly(self):
        scrolly = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=scrolly.set)
        return scrolly
    

