import tkinter as tk
from widgets.dropdown import DropDown

class CanvasTable(tk.Canvas):
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
    FONT_KWARGS = dict(font=('Arial', 10))

    def __init__(self, master):
        tk.Canvas.__init__(self, 
            master,
            width=1666,
            height=315,
            background='purple',
            bd=0,
            highlightthickness=0,
        )
        self.create_table_frame()
        self.create_table()

    def create_table_frame(self):
        self.table_frame = tk.Frame(self, background="gray")
        self.table_frame.grid(row=0, column=0, sticky="w")
        self.table_frame.bind(
            "<Configure>",
            lambda e: self.configure(
                scrollregion=self.bbox("all")
            )
        )
        self.create_window((0, 0), window=self.table_frame, anchor="nw")
    
    def create_table(self):
        columns = ['Transaction Date','Description','Amount']
        
        for r, transaction in enumerate(self.master.backend.transaction_data):
            table_row = tk.Frame(self.table_frame, background="white")
            table_row.grid(row=r, column=0, sticky="w")
            for c, column in enumerate(columns):
                text = transaction[column]
                if column == 'Description' and len(text) > 64:
                    text = text[:(82-3)] + '...' 
                label = tk.Label(
                    table_row,
                    text=text,
                    width=CanvasTable.COLUMN_WIDTHS[column],
                    height=1,
                    bd=1,
                    relief="solid",
                    background="white",
                    highlightbackground="blue",
                    padx=2,
                    anchor=CanvasTable.COLUMN_ALIGNMENTS[column],
                    **CanvasTable.FONT_KWARGS
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
        var = tk.StringVar(self.master, name="category_"+trans_id)
        dropdown = DropDown(table_row, self.master, var, 'Category')
        dropdown.grid(row=0, column=c+2)
        return var, dropdown
    
    def create_vendor_dropdown(self, table_row, c, trans_id):
        var = tk.StringVar(self.master, name="vendor_"+trans_id)
        dropdown = DropDown(table_row, self.master, var, 'Vendor')
        var.trace('w', dropdown.vendor_change_callback)
        dropdown.grid(row=0, column=c+1)
        return var, dropdown
