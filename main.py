import argparse
from financial_transaction_processor import FinancialTranascationProcessor

def main(args):
    if args.test:
        print("testing mode")
    app = FinancialTranascationProcessor('sample_data.csv')
    app.mainloop()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--test',
        help="test by running with 'data/sample.csv' file",
        action="store_true",
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    main(args)
  