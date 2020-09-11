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
        self.create_navbar()

    def create_title(self):
        self.title = tk.Label(
            self,
            text="Financial Transaction Processor",
            font=("Arial", 18),
            pady=15
        )
        self.title.grid(row=1, column=0, columnspan=2)

    def create_top_bar(self):
        columns = ['Transaction Date','Description','Amount']
        self.top_bar = tk.Frame(self)
        self.top_bar.grid(row=2, column=0)
        self.top_bar.grid_columnconfigure(0, weight=10)
        for c, column in enumerate(columns + ['Vendor', 'Category']):
            width = self.calc_column_width(column)
            if column in ['Vendor', 'Category']:
                width -= 1
            fmt_kwargs = dict(width=width, fg="white", background="dark slate gray", bd=1, relief="groove", **self.font_kwargs)
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
        elif column == 'Description':
            return 65
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
        btn.grid(row=4, column=0)
    
    def submit(self):
        self.backend.process_button_variables()
        self.controller.destroy()
    
    def create_navbar(self):
        self.navbar = tk.Frame(
            self,
            bd=2,
            relief="groove",
        )
        self.navbar.grid(row=0, column=0, columnspan=2, sticky='NSEW')

        self.menu = tk.Menu(self.navbar)
        self.controller.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)

        self.file_menu.add_command(
            label="Select File Screen",
            command=lambda: self.controller.show_frame('file_select')
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda: self.controller.destroy())

        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.insert_menu = tk.Menu(self.menu, tearoff=0)
        self.insert_menu.add_command(label="Vendor", command=lambda: VendorEntryPopup(self))
        self.insert_menu.add_command(label="Category", command=lambda: CategoryEntryPopup(self))

        self.menu.add_cascade(label="Insert", menu=self.insert_menu)