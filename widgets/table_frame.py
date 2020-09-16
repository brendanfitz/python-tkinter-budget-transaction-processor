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
        self.column_widths = self.create_column_widths_dict()
        self.top_bar = self.create_top_bar()
        self.top_bar.grid(row=0, column=0, sticky='nsw')
        self.canvas = CanvasTable(self)
        self.canvas.grid(row=1, column=0, sticky='nsw')
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
                relief="solid",
                padx=2,
                anchor=TableFrame.COLUMN_ALIGNMENTS[column],
                **TableFrame.FONT_KWARGS
            )
            if column in ['Vendor', 'Category']:
                grid_pad['padx'] = (0, 26) # padding for dropdown arrow
            label = tk.Label(top_bar, text=column, **fmt_kwargs)
            label.grid(row=0, column=c, sticky='ns', **grid_pad)
        return top_bar

    def calc_column_width(self, column):
        if column == 'Category':
            return max([len(x) for x in self.backend.categories + ['Category']])
        elif column == 'Vendor':
            vendors = self.backend.vendor_df.Vendor.unique().tolist()
            return max([len(x) for x in vendors + ['Vendor']])
        elif column == 'Description':
            return 65
        return self.column_widths[column]
    
    def create_column_widths_dict(self):
        df = self.backend.transaction_data_to_df()

        def max_of_column_name_or_longest_element(x):
            """
            computes the max of either:
                the column name length
                the length of largest string in the column
            """
            return max(len(x.name), x.astype(str).str.len().max())

        return df.apply(max_of_column_name_or_longest_element)

    def create_scrolly(self):
        scrolly = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=scrolly.set)
        return scrolly
    

