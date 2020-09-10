
import pandas as pd

class Backend(object):

    def __init__(self):
        self.read_data('sample_data.csv')
        self.categories = self.read_categories()
        self.vendor_df = self.read_vendor_lookup()

    def read_data(self, filename):
        df = pd.read_csv(filename)
        self.columns = df.columns.tolist()
        self.transaction_data = df.to_dict(orient='records')
        self.add_transaction_hash()
    
    def add_transaction_hash(self):
        for transaction in self.transaction_data:
            transaction_hash = hash(
                (
                    transaction['Transaction Date'],
                    transaction['Description'],
                    transaction['Amount'],
                )
            )
            transaction['Transaction ID'] = transaction_hash
        self.columns.insert(0, 'Transaction ID')
        self.check_hash_uniqueness()
    
    def check_hash_uniqueness(self):
        df = self.transaction_data_to_df()
        if df.loc[:, 'Transaction ID'].duplicated().any():
            raise ValueError("Duplicates across Transaction Date, Description and Amount dimensions")
    
    @staticmethod
    def read_categories():
        return (pd.read_csv('categories.csv')
            .Category
            .tolist()
        )
    
    def category_lookup(self, vendor):
        mask = self.vendor_df.Vendor == vendor
        category_row = self.vendor_df.loc[mask, 'Category']
        if not category_row.empty:
            return category_row.values[0]

    @staticmethod
    def read_vendor_lookup():
        return (pd.read_csv('vendor_lookup.csv')
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
        
        (pd.DataFrame(self.transaction_data)
            .to_csv('sample_data_processed.csv', index=False)
        )
    