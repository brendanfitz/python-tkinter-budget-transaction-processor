# Python program to create a table 
   
from tkinter import *
import pandas as pd
from itertools import count

current_row_gen = lambda c=count(): next(c)


window = Tk()

title_bar = Label(
    text="Financial Transaction Processor",
    fg="white",
    bg="black",
)

title_bar.grid(row=current_row_gen(), column=0)

df = pd.read_csv('sample_data.csv')

table = Frame()
table.grid(row=current_row_gen(), column=0)

columns = ['Transaction Date', 'Description', 'Amount']

for row_num, transaction in df.iterrows():
    for column_num, column in enumerate(columns):
        label = Label(table, text=transaction[column])
        label.grid(row=row_num, column=column_num)
    e1 = Entry(table)
    e1.grid(row=row_num, column=column_num+1)

b1 = Button(text="Submit")
b1.grid(row=current_row_gen(), column=0)

window.mainloop()
  