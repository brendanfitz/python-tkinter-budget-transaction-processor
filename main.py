import time
import argparse
from financial_transaction_processor import FinancialTranascationProcessor

# try:
    # from ctypes import windll
    # windll.shcore.SetProcessDpiAwareness(1)
# except:
    # pass

def main(args):
    app = FinancialTranascationProcessor(args.test)
    time.sleep(2)
    app.mainloop()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', '--test',
        help="test by running with 'data/sample.csv' file",
        action="store_true",
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)