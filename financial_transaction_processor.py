
from itertools import count
import pandas as pd
import tkinter as tk

class FinancialTranascationProcessor(object):

    def __init__(self):
        self.window = tk.Tk()
        self.window.bind('<Escape>', lambda event: self.window.destroy())
        self.current_row_gen = lambda c=count(): next(c)
        self.categories = self.read_categories()
        self.transaction_data = self.read_data('sample_data.csv')

    @staticmethod
    def read_categories():
        return (pd.read_csv('categories.csv')
            .Category
            .tolist()
        )
    
    @staticmethod
    def read_data(filename):
        df = pd.read_csv(filename)
        data = df.to_dict(orient='records')
        return data
    
    def create_title_bar(self):
        title_bar = tk.Label(
            text="Financial Transaction Processor",
            fg="white",
            bg="black",
        )
        title_bar.grid(row=self.current_row_gen(), column=0)
    
    def create_table(self):

        table = tk.Frame()
        table.grid(row=self.current_row_gen(), column=0)
        
        columns = ['Transaction Date', 'Description', 'Amount']
        for row_num, transaction in enumerate(self.transaction_data):
            for column_num, column in enumerate(columns):
                label = tk.Label(table, text=transaction[column])
                label.grid(row=row_num, column=column_num)
        
            var = tk.StringVar(self.window)
            dropdown = tk.OptionMenu(table, var, *self.categories)
            dropdown.grid(row=row_num, column=column_num+2)
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
        
        pd.DataFrame(self.transaction_data).to_csv('sample_data_processed.csv')
        self.window.destroy()





