import tkinter as tk
from tkinter import ttk

class DropDown(ttk.Combobox):
    COLUMN_WIDTHS = {
        'Transaction Date': 15,
        'Description': 64,
        'Amount': 9,
        'Vendor': 31,
        'Category': 25, 
    }

    def __init__(self, master, controller, var, type_, width=None):
        self.controller = controller 
        self.var = var
        self.set_values(type_, var)
        self.width = width or DropDown.COLUMN_WIDTHS[type_]
        ttk.Combobox.__init__(self, 
            master,
            text="Choose Vendor/Category",
            textvariable=var,
            values=self.values,
            font=("Arial", 10),
            width=self.width,
        )

    def set_values(self, type_, var):
        if type_ == 'Vendor':
            self.values = (self.controller.backend.vendor_df.Vendor
                .unique()
                .tolist()
            )
            var.trace('w', self.vendor_change_callback)
        elif type_ == 'Category':
            self.values = self.controller.backend.categories
        else:
            raise ValueError("Type must be 'Vendor' or 'Category'")

    def vendor_change_callback(self, var_name, idx, access_mode):
        trans_id = var_name.split('_')[1]
        var_name_filter = lambda x: x['Transaction ID'] == trans_id 
        row = next(filter(var_name_filter, self.controller.backend.transaction_data))

        category_var = row['category_var']
        vendor = row['vendor_var'].get()

        category = self.controller.backend.category_lookup(vendor)

        category_var.set(category)
    
    def add_vendor(self, vendor):
        self['values'] = (*self['values'], vendor)
       
    def add_category(self, category):
        self['values'] = (*self['values'], category)
       

