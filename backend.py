
import pandas as pd

class Backend(object):

    def __init__(self):
        self.read_data('sample_data.csv')

    def read_data(self, filename):
        df = pd.read_csv(filename)
        self.columns = df.columns
        self.transaction_data = df.to_dict(orient='records')
        self.categories = self.read_categories()
        self.vendor_df = self.read_vendor_lookup()
    
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
    