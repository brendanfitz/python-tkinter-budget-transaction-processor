# Python program to create a table 
   
from financial_transaction_processor import FinancialTranascationProcessor

app = FinancialTranascationProcessor()

app.create_title_bar()
app.create_table()
app.create_submit_button()

app.window.mainloop()
  