from itertools import count
import tkinter as tk
from backend import Backend
from widgets.canvas_table import CanvasTable

class HomeFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0)
        self.backend = Backend()
        self.current_row_gen = lambda c=count(): next(c)
        self.font_kwargs = dict(font=('Arial', 10))
        self.create_column_widths_dict()
        self.create_title()
        self.create_top_bar()
        self.create_canvas()
        self.create_submit_button()

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