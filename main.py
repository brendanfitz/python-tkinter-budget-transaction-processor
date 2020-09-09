# Python program to create a table 
   
from tkinter import *
import pandas as pd
from itertools import count
import random
from financial_transaction_processor import FinancialTranascationProcessor

current_row_gen = lambda c=count(): next(c)

ftproc = FinancialTranascationProcessor()

categories = pd.read_csv('categories.csv').Category.tolist()

window = Tk()

title_bar = Label(
    text="Financial Transaction Processor",
    fg="white",
    bg="black",
)

title_bar.grid(row=current_row_gen(), column=0)

df = pd.read_csv('sample_data.csv')
data = df.to_dict(orient='records')

table = Frame()
table.grid(row=current_row_gen(), column=0)

columns = ['Transaction Date', 'Description', 'Amount']

for row_num, transaction in enumerate(data):
    for column_num, column in enumerate(columns):
        label = Label(table, text=transaction[column])
        label.grid(row=row_num, column=column_num)

    tkvar = StringVar(window)
    dropdown = OptionMenu(table, tkvar, *categories)
    dropdown.grid(row=row_num, column=column_num+2)
    transaction['category_dropdown'] = dropdown 

b1 = Button(text="Submit")
b1.grid(row=current_row_gen(), column=0)

window.bind('<Escape>', lambda event: window.destroy())

window.mainloop()
  