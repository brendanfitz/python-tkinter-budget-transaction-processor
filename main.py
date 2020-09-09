# Python program to create a table 
   
from tkinter import *
import pandas as pd

window = Tk()

title_bar = Label(
    text="Financial Transaction Processor",
    fg="white",
    bg="black",
)

title_bar.grid(row=0, column=0)

df = pd.read_csv('sample_data.csv')

table = Frame()
table.grid(row=1, column=0)

columns = ['Transaction Date', 'Description', 'Amount']

for row_num, transaction in df.iterrows():
    for column_num, column in enumerate(columns):
        label = Label(table, text=transaction[column])
        label.grid(row=row_num, column=column_num)

window.mainloop()
  