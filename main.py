# Python program to create a table 
   
from financial_transaction_processor import FinancialTranascationProcessor


if __name__ == '__main__':
    app = FinancialTranascationProcessor()
    
    app.create_title_bar()
    app.create_canvas()
    app.create_table()
    app.create_submit_button()
    
    app.window.mainloop()
  