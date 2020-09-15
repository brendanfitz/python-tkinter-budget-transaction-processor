from os import path, mkdir
import pandas as pd
import hashlib

class Backend(object):

    def __init__(self):
        self.datapath = 'data'
        if not path.isdir('data'):
            mkdir('data')

        self.transaction_data = None
        self.columns = None

        self.categories_filepath = path.join(self.datapath, 'categories.csv')
        self.categories = self.read_categories()

        self.vendors_filepath = path.join(self.datapath, 'vendors.csv')
        self.vendor_df = self.read_vendor_lookup()

    def read_data(self, filepath):
        self.filepath = filepath
        self.path, self.filename = path.split(filepath)

        df = pd.read_csv(self.filepath)
        self.columns = df.columns.tolist()
        self.transaction_data = df.to_dict(orient='records')
        self.add_transaction_hash()
    
    def add_transaction_hash(self):
        for transaction in self.transaction_data:
            rowstring = (
                transaction['Transaction Date']
                + transaction['Description']
                + str(transaction['Amount'])
            )
            transaction_hash = hashlib.md5(rowstring.encode()).hexdigest()
            transaction['Transaction ID'] = transaction_hash
        self.columns.insert(0, 'Transaction ID')
        self.check_hash_uniqueness()
    
    def add_filename_id(self):
    
    def check_hash_uniqueness(self):
        df = self.transaction_data_to_df()
        if df.loc[:, 'Transaction ID'].duplicated().any():
            raise ValueError("Duplicates across Transaction Date, Description and Amount dimensions")
    
    def read_categories(self):
        return (pd.read_csv(self.categories_filepath)
            .Category
            .tolist()
        )
    
    def category_lookup(self, vendor):
        mask = self.vendor_df.Vendor == vendor
        category_row = self.vendor_df.loc[mask, 'Category']
        if not category_row.empty:
            return category_row.values[0]

    def read_vendor_lookup(self):
        return (pd.read_csv(self.vendors_filepath)
            .sort_values(['Vendor', 'Category'])
        )
    
    def transaction_data_to_df(self):
        return pd.DataFrame(self.transaction_data, columns=self.columns)
    
    def process_button_variables(self):
        for transaction in self.transaction_data:
            transaction['category'] = transaction['category_var'].get()
            del transaction['category_dropdown']
            del transaction['category_var']

            transaction['vendor'] = transaction['vendor_var'].get()
            del transaction['vendor_dropdown']
            del transaction['vendor_var']
        
        self.write_transactions()
    
    def add_vendor(self, vendor, category):
        mask = self.vendor_df.loc[:, 'Vendor'] == vendor
        if not self.vendor_df.loc[mask, ].empty:
            raise ValueError("Vendor already exists")
        
        new_row = pd.DataFrame(
            [[category, vendor]],
            columns=self.vendor_df.columns
        )
        self.vendor_df = self.vendor_df.append(new_row)
        self.write_vendors()
    
    def add_category(self, category):
        if category in self.categories:
            raise ValueError("Category already exists")
        self.categories.append(category)
        self.write_categories()

    def write_categories(self):
        (pd.DataFrame(self.categories, columns=['Category'])
            .to_csv(self.categories_filepath, index=False)
        )
        
    def write_vendors(self):
        self.vendor_df.to_csv(self.vendors_filepath, index=False)
    
    def write_transactions(self):
        root, ext= path.splitext(self.filename)
        filename = root + '_processed' + ext 
        filepath = path.join(self.datapath, filename)
        (pd.DataFrame(self.transaction_data)
            .to_csv(filepath, index=False)
        )