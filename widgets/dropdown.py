from tkinter import OptionMenu

class DropDown(OptionMenu):

    def __init__(self, master, controller, var, type):
        self.controller = controller 
        if type == 'Vendor':
            self.values = (self.controller.backend.vendor_df.Vendor
                .unique()
                .tolist()
            )
            var.trace('w', self.vendor_change_callback)
        elif type == 'Category':
            self.values = self.controller.backend.categories
        else:
            raise ValueError("Type must be 'Vendor' or 'Category'")
        OptionMenu.__init__(self, master, var, *self.values)
        self.config(
            width=max([len(x) for x in self.values]),
            relief='sunken',
            **self.controller.font_kwargs
        )

    def vendor_change_callback(self, var_name, idx, access_mode):
        trans_id = int(var_name.split('_')[1])
        var_name_filter = lambda x: x['Transaction ID'] == trans_id 
        row = next(filter(var_name_filter, self.controller.backend.transaction_data))

        category_var = row['category_var']
        vendor = row['vendor_var'].get()

        category = self.controller.backend.category_lookup(vendor)

        category_var.set(category)
    
    def add_vendor(self, vendor):
        self['menu'].add_command(label=vendor, command=None)
       
    def add_category(self, category):
        self['menu'].add_command(label=category, command=None)
       

