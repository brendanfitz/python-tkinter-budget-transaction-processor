import tkinter as tk
from widgets.dropdown import DropDown

class CanvasTable(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master, width=1150, height=250, background='white')
        self.grid(row=3, column=0)
        self.create_scrolly()
        self.create_table_frame()
        self.create_table()

    def create_scrolly(self):
        self.scrolly = tk.Scrollbar(self.master, orient="vertical", command=self.yview)
        self.scrolly.grid(row=3, column=1, rowspan=1, sticky='ns')
    
    def create_table_frame(self):
        self.table_frame = tk.Frame(self, background="white")
        self.table_frame.grid(row=0, column=0, sticky="EW")
        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.bind(
            "<Configure>",
            lambda e: self.configure(
                scrollregion=self.bbox("all")
            )
        )
        self.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.configure(yscrollcommand=self.scrolly.set)
    
    def create_table(self):
        columns = ['Transaction Date','Description','Amount']
        
        for r, transaction in enumerate(self.master.backend.transaction_data):
            table_row = tk.Frame(self.table_frame, background="white")
            table_row.grid(row=r, column=0, sticky="EW")
            for c, column in enumerate(columns):
                width = self.master.calc_column_width(column)
                label = tk.Label(
                    table_row,
                    text=transaction[column],
                    width=width,
                    height=1,
                    bd=1,
                    relief="groove",
                    background="white",
                    highlightbackground="blue",
                    **self.master.font_kwargs
                )
                label.grid(row=0, column=c)
        
            trans_id = transaction['Transaction ID']
        
            var, dropdown = self.create_vendor_dropdown(table_row, c, trans_id)
            transaction['vendor_dropdown'] = dropdown 
            transaction['vendor_var'] = var

            var, dropdown = self.create_category_dropdown(table_row, c, trans_id)
            transaction['category_dropdown'] = dropdown 
            transaction['category_var'] = var

    def create_category_dropdown(self, table_row, c, trans_id):
        var = tk.StringVar(self.master, name="category_"+str(trans_id))
        dropdown = DropDown(table_row, self.master, var, 'Category')
        dropdown.grid(row=0, column=c+2)
        return var, dropdown
    
    def create_vendor_dropdown(self, table_row, c, trans_id):
        var = tk.StringVar(self.master, name="vendor_"+str(trans_id))
        dropdown = DropDown(table_row, self.master, var, 'Vendor')
        var.trace('w', dropdown.vendor_change_callback)
        dropdown.grid(row=0, column=c+1)
        return var, dropdown
