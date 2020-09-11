from financial_transaction_processor import FinancialTranascationProcessor

def main():
    app = FinancialTranascationProcessor('sample_data.csv')
    app.mainloop()

if __name__ == '__main__':
    main()
  