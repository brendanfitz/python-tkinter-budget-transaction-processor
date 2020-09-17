import argparse
from budget_transaction_processor import App
from windows import set_dpi_awareness


def main(args):
    set_dpi_awareness()
    app = App(args.test)
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