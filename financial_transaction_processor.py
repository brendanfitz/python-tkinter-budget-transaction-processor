
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

        self.font_kwargs = dict(font=('Arial', 14))


    @staticmethod
    def read_categories():
        return (pd.read_csv('categories.csv')
            .Category
            .tolist()
        )
    
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
        return df.apply(lambda x: max(len(x.name), x.astype(str).str.len().max()))
    
    def create_title_bar(self):
        title_bar = tk.Label(
            self.window,
            text="Financial Transaction Processor",
            fg="white",
            bg="black",
        )
        title_bar.grid(row=0, column=0, columnspan=2)
    
    def create_table(self):

        column_widths = self.create_column_widths_dict()

        
        columns = ['Transaction Date', 'Description', 'Amount']
        for column_num, column in enumerate(columns + ['Category']):
            width = max([len(x) for x in self.categories]) if column == 'Category' else column_widths[column]
            fmt_kwargs = dict(width=width, borderwidth=2, relief='sunken', font=('Arial', 14))
            label = tk.Label(self.table_frame, text=column, **fmt_kwargs)
            label.grid(row=0, column=column_num)

        for row_num, transaction in enumerate(self.transaction_data):
            for column_num, column in enumerate(columns):
                label = tk.Label(self.table_frame, text=transaction[column],
                    width=column_widths[column],
                    relief='sunken',
                    **self.font_kwargs
                )
                label.grid(row=row_num+1, column=column_num)
        
            var = tk.StringVar(self.window)
            dropdown = tk.OptionMenu(self.table_frame, var, *self.categories)
            dropdown.config(
                width=max([len(x) for x in self.categories]),
                relief='sunken', **self.font_kwargs)
            dropdown.grid(row=row_num+1, column=column_num+1)
            transaction['category_dropdown'] = dropdown 
            transaction['category_var'] = var
    

    def create_submit_button(self):
        b = tk.Button(text="Submit", command=self.submit)
        b.grid(row=2, column=0)
    
    def submit(self):
        for transaction in self.transaction_data:
            transaction['category'] = transaction['category_var'].get()
            del transaction['category_dropdown']
            del transaction['category_var']
        
        (pd.DataFrame(self.transaction_data)
            .to_csv('sample_data_processed.csv', index=False)
        )
        self.window.destroy()
    
    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, width=1000, height=250)
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








