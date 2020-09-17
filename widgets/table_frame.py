import tkinter as tk
from tkinter import ttk
from widgets.dropdown import DropDown

class TableFrame(tk.Frame):
    COLUMN_ALIGNMENTS = {
        'Transaction Date': tk.W,
        'Description': tk.W,
        'Amount': tk.E,
        'Vendor': tk.W,
        'Category': tk.W, 
    }
    COLUMN_WIDTHS = {
        'Transaction Date': 15,
        'Description': 64,
        'Amount': 9,
        'Vendor': 31,
        'Category': 25, 
    }

    def __init__(self, master, backend):
        ttk.Frame.__init__(self, master)
        self.backend = backend
        self.top_bar = self.create_top_bar()
        self.top_bar.grid(row=0, column=0, sticky='nsew')
        self.canvas = self.create_canvas()
        self.canvas.grid(row=1, column=0, sticky='nsew')
        self.table_frame = self.create_table_frame()
        self.create_table()
        self.scrolly = self.create_scrolly()
        self.scrolly.grid(row=1, column=1, rowspan=1, sticky='nsw')
    
    def create_top_bar(self):
        columns = ['Transaction Date', 'Description', 'Amount']
        top_bar = tk.Frame(self, background='dark slate gray')
        for c, column in enumerate(columns + ['Vendor', 'Category']):
            label = ttk.Label(
                top_bar,
                text=column,
                width=TableFrame.COLUMN_WIDTHS[column],
                anchor=TableFrame.COLUMN_ALIGNMENTS[column],
                style="TableHeader.TLabel"
            )
            grid_pad = dict()
            if column in ['Vendor', 'Category']:
                grid_pad['padx'] = (0, 26) # padding for dropdown arrow
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
    
    def create_canvas(self):
        canvas = tk.Canvas(
            self, 
            # width=1466,
            height=315,
            background='purple',
            bd=0,
            highlightthickness=0,
        )
        return canvas

    def create_table_frame(self):
        table_frame = tk.Frame(self.canvas, background="gray")
        table_frame.grid(row=0, column=0, sticky="ew")
        table_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=table_frame, anchor="nw")
        return table_frame
    
    def create_table(self):
        columns = ['Transaction Date','Description','Amount']
        
        for r, transaction in enumerate(self.backend.transaction_data):
            table_row = tk.Frame(self.table_frame, background="white")
            table_row.grid(row=r, column=0, sticky="w")
            for c, column in enumerate(columns):
                text = transaction[column]
                if column == 'Description' and len(text) > 64:
                    text = text[:(82-3)] + '...' 
                label = ttk.Label(
                    table_row,
                    text=text,
                    width=TableFrame.COLUMN_WIDTHS[column],
                    anchor=TableFrame.COLUMN_ALIGNMENTS[column],
                    style='TableRow.TLabel'
                )
                label.grid(row=0, column=c, sticky='ns')
        
            trans_id = transaction['Transaction ID']
        
            var, dropdown = self.create_vendor_dropdown(table_row, c, trans_id)
            transaction['vendor_dropdown'] = dropdown 
            transaction['vendor_var'] = var

            var, dropdown = self.create_category_dropdown(table_row, c, trans_id)
            transaction['category_dropdown'] = dropdown 
            transaction['category_var'] = var

    def create_category_dropdown(self, table_row, c, trans_id):
        var = tk.StringVar(self, name="category_"+trans_id)
        dropdown = DropDown(table_row, self, var, 'Category')
        dropdown.grid(row=0, column=c+2)
        return var, dropdown
    
    def create_vendor_dropdown(self, table_row, c, trans_id):
        var = tk.StringVar(self, name="vendor_"+trans_id)
        dropdown = DropDown(table_row, self, var, 'Vendor')
        var.trace('w', dropdown.vendor_change_callback)
        dropdown.grid(row=0, column=c+1)
        return var, dropdown