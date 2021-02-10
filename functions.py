import PySimpleGUI as sg
import pandas as pd

def create_wallet():
  ''' Function that creates the wallet from zero.
      No arguments needed.
  '''
  shopping = pd.DataFrame({"-BILLS-"  :["0.0"],
                          "-TICKETS-" :["0.0"],
                          "-SHOPPING-":["0.0"],
                          "-PRESENTS-":["0.0"],
                          "-FUN-"     :["0.0"],
                          "-TRAVELS-" :["0.0"],
                          "-HOUSE-"   :["0.0"],
                          "-CAR-"     :["0.0"],
                          "-INCOMES-" :["0.0"],}
                          )

  shopping = shopping.apply(pd.to_numeric)  # convert values to numeric
  print(shopping.dtypes)
  print(shopping.loc[ 0 , shopping.columns != "-INCOMES-"].sum() - shopping["-INCOMES-"])

  shopping.to_csv(r".\guiWallet.csv", index=False)  # save it

def call_popup():
	'''Open popup message with instructions
	'''
	sg.popup('''Welcome!!
Enter how much and how you spent your money.
- Use dot (".") for decimals.

- CLEAR ->  to clear your inputs.
- GO    ->  to calculate your expenses and save the wallet.
- EXIT  ->  when you are done.
	''', title="Wallet!", keep_on_top=True)

# if this script has been run, it creates the new wallet
if __name__ == "__main__":
    create_wallet()
