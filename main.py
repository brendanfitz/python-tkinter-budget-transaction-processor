# Python program to create a table 
   
from tkinter import *
import pandas as pd
from itertools import count
import random

current_row_gen = lambda c=count(): next(c)


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
    entry = Entry(table)
    entry.grid(row=row_num, column=column_num+1)
    transaction['entry'] = entry


def print_random_trans():
    row = random.choice(data)
    row['entry'] = row['entry'].get()
    print(row)


b1 = Button(text="Submit", command=print_random_trans)
b1.grid(row=current_row_gen(), column=0)

window.bind('<Escape>', lambda event: window.destroy())

window.mainloop()
  