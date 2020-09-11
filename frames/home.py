from itertools import count
import tkinter as tk
from widgets.canvas_table import CanvasTable
from widgets.vendor_entry_popup import VendorEntryPopup
from widgets.category_entry_popup import CategoryEntryPopup 

class HomeFrame(tk.Frame):

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.backend = self.controller.backend

        self.current_row_gen = lambda c=count(): next(c)
        self.font_kwargs = dict(font=('Arial', 10))

    def create_widgets(self):
        self.pack_forget()
        self.create_column_widths_dict()
        self.create_title()
        self.create_top_bar()
        self.create_canvas()
        self.create_submit_button()
        self.create_bottom_bar()
        self.create_add_vendor_button()
        self.create_add_category_button()
        self.create_file_select_frame_button()

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
        btn = tk.Button(self, text="Submit", command=self.submit)
        btn.grid(row=3, column=0)
    
    def submit(self):
        self.backend.process_button_variables()
        self.controller.destroy()
    
    def create_bottom_bar(self):
        self.bottom_bar_frame = tk.Frame(self)
        self.bottom_bar_frame.grid(row=4, column=0)
    
    def create_add_vendor_button(self):
        btn = tk.Button(self.bottom_bar_frame, text="Add Vendor", command=lambda: VendorEntryPopup(self))
        btn.grid(row=0, column=0)
    
    def create_add_category_button(self):
        btn = tk.Button(self.bottom_bar_frame, text="Add Category", command=lambda: CategoryEntryPopup(self))
        btn.grid(row=0, column=1)
    
    def create_file_select_frame_button(self):
        btn = tk.Button(self.bottom_bar_frame, text="Select File", command=lambda: self.controller.show_frame('file_select'))
        btn.grid(row=0, column=2)
