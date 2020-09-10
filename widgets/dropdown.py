from tkinter import OptionMenu

class DropDown(OptionMenu):

    def __init__(self, master, root_frame, var, type):
        self.root_frame = root_frame
        if type == 'Vendor':
            self.values = (self.root_frame.backend.vendor_df.Vendor
                .unique()
                .tolist()
            )
            var.trace('w', self.vendor_change_callback)
        elif type == 'Category':
            self.values = self.root_frame.backend.categories
        else:
            raise ValueError("Type must be 'Vendor' or 'Category'")
        OptionMenu.__init__(self, master, var, *self.values)
        self.config(
            width=max([len(x) for x in self.values]),
            relief='sunken',
            **self.root_frame.font_kwargs
        )

    def vendor_change_callback(self, var_name, idx, access_mode):
        trans_id = int(var_name.split('_')[1])
        var_name_filter = lambda x: x['Transaction ID'] == trans_id 
        row = next(filter(var_name_filter, self.root_frame.backend.transaction_data))

        category_var = row['category_var']
        vendor = row['vendor_var'].get()

        category = self.root_frame.backend.category_lookup(vendor)

        category_var.set(category)

    


    

        
