from itertools import count
import pandas as pd
import tkinter as tk
from backend import Backend

class FinancialTranascationProcessor(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.backend = Backend()
        self.current_row_gen = lambda c=count(): next(c)
        self.font_kwargs = dict(font=('Arial', 12))
        self.create_column_widths_dict()

    def create_title(self):
        self.title = tk.Label(
            self,
            text="Financial Transaction Processor",
            fg="white",
            bg="black",
        )
        self.title.grid(row=0, column=0, columnspan=2)

    def create_top_bar(self):
        columns = ['Transaction ID','Transaction Date','Description','Amount']
        self.top_bar = tk.Frame(self)
        self.top_bar.grid(row=1, column=0, sticky='W')
        for c, column in enumerate(columns + ['Vendor', 'Category']):
            width = self.calc_column_width(column)
            if column in ['Vendor', 'Category']:
                width += 4

            fmt_kwargs = dict(width=width, borderwidth=2, relief='sunken', **self.font_kwargs)
            label = tk.Label(self.top_bar, text=column, **fmt_kwargs)
            label.grid(row=0, column=c)

    def create_canvas(self):
        self.Canvas = CanvasTable(self)

    def calc_column_width(self, column):
        if column == 'Category':
            return max([len(x) for x in self.backend.categories + ['Category']])
        elif column == 'Vendor':
            vendors = self.backend.vendor_df.Vendor.unique().tolist()
            return max([len(x) for x in vendors + ['Vendor']])
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

        self.column_widths = df.apply(max_of_column_name_or_longest_element)

    def create_submit_button(self):
        b = tk.Button(self, text="Submit", command=self.submit)
        b.grid(row=3, column=0)
    
    def submit(self):
        self.backend.process_button_variables()

        self.master.destroy()
    
    
class CanvasTable(tk.Canvas):

    def __init__(self, master):
        tk.Canvas.__init__(self, master, width=1250, height=250)
        self.grid(row=2, column=0)
        self.create_scrolly()
        self.create_table_frame()
        self.create_table()

    def create_scrolly(self):
        self.scrolly = tk.Scrollbar(self.master, orient="vertical", command=self.yview)
        self.scrolly.grid(row=2, column=1, rowspan=1, sticky='ns')
    
    def create_table_frame(self):
        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=0, column=0)
        self.table_frame.bind(
            "<Configure>",
            lambda e: self.configure(
                scrollregion=self.bbox("all")
            )
        )
        self.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.configure(yscrollcommand=self.scrolly.set)
    
    def create_table(self):
        columns = ['Transaction ID','Transaction Date','Description','Amount']
        
        for r, transaction in enumerate(self.master.backend.transaction_data):
            for c, column in enumerate(columns):
                width = self.master.calc_column_width(column)
                label = tk.Label(self.table_frame, text=transaction[column],
                    width=width,
                    relief='sunken',
                    **self.master.font_kwargs
                )
                label.grid(row=r, column=c)
        
            trans_id = transaction['Transaction ID']
        
            var, dropdown = self.create_vendor_dropdown(r, c, trans_id)
            transaction['vendor_dropdown'] = dropdown 
            transaction['vendor_var'] = var

            var, dropdown = self.create_category_dropdown(r, c, trans_id)
            transaction['category_dropdown'] = dropdown 
            transaction['category_var'] = var

    def create_category_dropdown(self, r, c, trans_id):
        var = tk.StringVar(self.master, name="category_"+str(trans_id))
        dropdown = tk.OptionMenu(self.table_frame, var, *self.master.backend.categories)
        dropdown.config(
            width=max([len(x) for x in self.master.backend.categories]),
            relief='sunken', **self.master.font_kwargs)
        dropdown.grid(row=r, column=c+2)
        return var, dropdown
    
    def create_vendor_dropdown(self, r, c, trans_id):
        vendors = self.master.backend.vendor_df.Vendor.unique().tolist()

        var = tk.StringVar(self.master, name="vendor_"+str(trans_id))
        var.trace('w', self.vendor_change_callback)

        dropdown = tk.OptionMenu(self.table_frame, var, *vendors)
        dropdown.config(
            width=max([len(x) for x in vendors]),
            relief='sunken', **self.master.font_kwargs)
        dropdown.grid(row=r, column=c+1)

        return var, dropdown

    def vendor_change_callback(self, var_name, idx, access_mode):
        trans_id = int(var_name.split('_')[1])
        var_name_filter = lambda x: x['Transaction ID'] == trans_id 
        row = next(filter(var_name_filter, self.master.backend.transaction_data))

        category_var = row['category_var']
        vendor = row['vendor_var'].get()

        category = self.master.backend.category_lookup(vendor)

        category_var.set(category)
        

