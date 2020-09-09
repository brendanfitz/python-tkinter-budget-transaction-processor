from itertools import count
import pandas as pd
import tkinter as tk

class FinancialTranascationProcessor(object):

    def __init__(self):
        self.window = tk.Tk()
        self.window.bind('<Escape>', lambda event: self.window.destroy())
        self.current_row_gen = lambda c=count(): next(c)
        self.read_data('sample_data.csv')
        self.categories = self.read_categories()
        self.vendor_df = self.read_vendor_lookup()
        self.font_kwargs = dict(font=('Arial', 14))
        self.create_column_widths_dict()
    @staticmethod
    def read_categories():
        return (pd.read_csv('categories.csv')
            .Category
            .tolist()
        )

    @staticmethod
    def read_vendor_lookup():
        return pd.read_csv('vendor_lookup.csv')
    
    def read_data(self, filename):
        df = pd.read_csv(filename)
        self.columns = df.columns
        self.transaction_data = df.to_dict(orient='records')
    
    def transaction_data_to_df(self):
        return pd.DataFrame(self.transaction_data, columns=self.columns)
    
    def create_column_widths_dict(self):
        df = self.transaction_data_to_df()
        """
        computes the max of either:
            the column name length
            the length of largest string in the column
        """
        def max_of_column_name_or_longest_element(x):
            return max(len(x.name), x.astype(str).str.len().max())
        self.column_widths = df.apply(max_of_column_name_or_longest_element)
    
    def create_title_bar(self):
        title_bar = tk.Label(
            self.window,
            text="Financial Transaction Processor",
            fg="white",
            bg="black",
        )
        title_bar.grid(row=0, column=0, columnspan=2)
    
    def calc_column_width(self, column):
        if column == 'Category':
            return max([len(x) for x in self.categories + ['Category']])
        elif column == 'Vendor':
            vendors = self.vendor_df.Vendor.unique().tolist()
            return max([len(x) for x in vendors + ['Vendor']])
        return self.column_widths[column]
    
    def create_table(self):

        columns = ['Transaction Date', 'Description', 'Amount']
        for column_num, column in enumerate(columns + ['Vendor', 'Category']):
            width = self.calc_column_width(column)
            fmt_kwargs = dict(width=width, borderwidth=2, relief='sunken', font=('Arial', 14))
            label = tk.Label(self.table_frame, text=column, **fmt_kwargs)
            label.grid(row=0, column=column_num)

        for r, transaction in enumerate(self.transaction_data):
            for c, column in enumerate(columns):
                width = self.calc_column_width(column)
                label = tk.Label(self.table_frame, text=transaction[column],
                    width=width,
                    relief='sunken',
                    **self.font_kwargs
                )
                label.grid(row=r+1, column=c)
        
        
            var, dropdown = self.create_vendor_dropdown(r, c)
            transaction['vendor_dropdown'] = dropdown 
            transaction['vendor_var'] = var

            var, dropdown = self.create_category_dropdown(r, c)
            transaction['category_dropdown'] = dropdown 
            transaction['category_var'] = var
    
    def create_category_dropdown(self, r, c):
        var = tk.StringVar(self.window)
        dropdown = tk.OptionMenu(self.table_frame, var, *self.categories)
        dropdown.config(
            width=max([len(x) for x in self.categories]),
            relief='sunken', **self.font_kwargs)
        dropdown.grid(row=r+1, column=c+2)
        return var, dropdown
    

    def create_vendor_dropdown(self, r, c):
        vendors = self.vendor_df.Vendor.unique().tolist()
        var = tk.StringVar(self.window)
        dropdown = tk.OptionMenu(self.table_frame, var, *vendors)
        dropdown.config(
            width=max([len(x) for x in vendors]),
            relief='sunken', **self.font_kwargs)
        dropdown.grid(row=r+1, column=c+1)
        return var, dropdown

    def create_submit_button(self):
        b = tk.Button(text="Submit", command=self.submit)
        b.grid(row=2, column=0)
    
    def submit(self):
        for transaction in self.transaction_data:
            transaction['category'] = transaction['category_var'].get()
            del transaction['category_dropdown']
            del transaction['category_var']

            transaction['vendor'] = transaction['vendor_var'].get()
            del transaction['vendor_dropdown']
            del transaction['vendor_var']
        
        (pd.DataFrame(self.transaction_data)
            .to_csv('sample_data_processed.csv', index=False)
        )
        self.window.destroy()
    
    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, width=1250, height=250)
        self.canvas.grid(row=1, column=0)
    
        self.scrolly = tk.Scrollbar(self.window, orient="vertical", command=self.canvas.yview)
        self.scrolly.grid(row=1, column=1, rowspan=1)
        self.table_frame = tk.Frame(self.canvas)
        self.table_frame.grid(row=0, column=0)

        self.table_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrolly.set)








