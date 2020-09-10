# Python program to create a table 
   
import tkinter as tk
from financial_transaction_processor import FinancialTranascationProcessor

def main():
    root = tk.Tk()
    root.bind('<Escape>', lambda event: root.destroy())
    app = FinancialTranascationProcessor(root)
    app.create_title_bar()
    app.create_canvas()
    app.create_table()
    app.create_submit_button()
    root.mainloop()

if __name__ == '__main__':
    main()
  