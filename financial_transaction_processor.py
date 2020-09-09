
from itertools import count
import pandas as pd
import tkinter as tk

class FinancialTranascationProcessor(object):

    def __init__(self):
        self.window = tk.Tk()
        self.window.bind('<Escape>', lambda event: self.window.destroy())
        self.current_row_gen = lambda c=count(): next(c)
        self.categories = self.read_categories()
        self.read_data('sample_data.csv')
        self.font_kwargs = dict(font=('Arial',14))

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
        # computes the max of either:
        #    the column name length
        #    the length of largest string in the column
        return df.apply(lambda x: max(len(x.name), x.astype(str).str.len().max()))
    
    def create_title_bar(self):
        title_bar = tk.Label(
            text="Financial Transaction Processor",
            fg="white",
            bg="black",
        )
        title_bar.grid(row=self.current_row_gen(), column=0)
    
    def create_table(self):

        column_widths = self.create_column_widths_dict()

        table = tk.Frame()
        table.grid(row=self.current_row_gen(), column=0)
        
        columns = ['Transaction Date', 'Description', 'Amount']
        for column_num, column in enumerate(columns + ['Category']):
            width = max([len(x) for x in self.categories])+1 if column == 'Category' else column_widths[column]
            fmt_kwargs = dict(width=width, borderwidth=2, relief='sunken', font=('Arial', 14, 'bold'))
            label = tk.Label(table, text=column, **fmt_kwargs)
            label.grid(row=0, column=column_num)


        for row_num, transaction in enumerate(self.transaction_data):
            for column_num, column in enumerate(columns):
                label = tk.Label(table, text=transaction[column],
                    width=column_widths[column],
                    relief='sunken',
                    **self.font_kwargs
                )
                label.grid(row=row_num+1, column=column_num)
        
            var = tk.StringVar(self.window)
            dropdown = tk.OptionMenu(table, var, *self.categories)
            dropdown.config(
                width=max([len(x) for x in self.categories]),
                relief='sunken', **self.font_kwargs)
            dropdown.grid(row=row_num+1, column=column_num+1)
            transaction['category_dropdown'] = dropdown 
            transaction['category_var'] = var
    

    def create_submit_button(self):
        b = tk.Button(text="Submit", command=self.submit)
        b.grid(row=self.current_row_gen(), column=0)
    
    def submit(self):
        for transaction in self.transaction_data:
            transaction['category'] = transaction['category_var'].get()
            del transaction['category_dropdown']
            del transaction['category_var']
        
        (pd.DataFrame(self.transaction_data)
            .to_csv('sample_data_processed.csv', index=False)
        )
        self.window.destroy()





