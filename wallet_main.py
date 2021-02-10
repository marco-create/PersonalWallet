import PySimpleGUI as  sg
from functions import call_popup, create_wallet
import webbrowser
import pandas
import traceback
from datetime import date
import os

# Constants and handles
WIDTH = 400
HEIGHT = 500
bt = {"size": (6, 1)}
today = date.today()
when = today.strftime("%b-%d-%Y")
sg.theme("Green")
new_events = [] # just to handle Clean option

## ---- Call the initial popup message with few instructions (function defined in functions.py)
call_popup()
## ---- Main Window
menu_def = [['File', ['Show', 'Reset wallet', '---', 'Exit'  ]],
            ['Help', ['Instructions', 'About...']],
]
layout = [
		[sg.Text("My Wallet!", size=(35,1) , justification="center")],
		[sg.Menu(menu_def)],
		[sg.Text("Amount:"), sg.Input(key="-INPUT-")],
		[sg.Button("bills", key="-BILLS-", **bt), sg.Button("tickets", key="-TICKETS-", **bt), sg.Button("shopping", key="-SHOPPING-", **bt)],
		[sg.Button("presents", key="-PRESENTS-", **bt), sg.Button("fun", key="-FUN-", **bt), sg.Button("travels", key="-TRAVELS-", **bt)],
		[sg.Button("house", key="-HOUSE-", **bt), sg.Button("car", key="-CAR-", **bt), sg.Button("incomes", key="-INCOMES-", **bt)],
		[sg.MLine(key="-ML-", size=(55,10), do_not_clear=False, disabled=True)], # auto_refresh=False)]
		[sg.Button("go", key="-GO-", **bt), sg.Button("clear", key="-CLEAR-", **bt), sg.Button("exit", key="-EXIT-", **bt)],
		[sg.Text(f"Today: ({today.strftime('%b-%d-%Y')})")],
		[sg.Text(size=(35, 1), key="-OUTPUT-")]
]
window = sg.Window(
          "GUI", 
					layout, 
					size=(WIDTH,HEIGHT),
					finalize=True,
					element_justification="c"
)
## ---- Main loop. Open the csv file and wait for user buttons
# check if the wallet file exists. Otherwise, create that.
if os.path.isfile("guiWallet.csv"):
	print("HERE")
else:
	create_wallet()
	
filePath = r".\guiWallet.csv"
with open(filePath) as file:
	data = pandas.read_csv(file)
				
	while True:
		# button saved as event
		# user input stored in values["-INPUT-"]
		# {button : input}
		event, values = window.read()
		
		if event in data:
			new_events.append(event)  # take trace of events	
			# print(new_events)
			try:	
				data[event] += float(values["-INPUT-"]) # update wallet with new values
				window["-ML-"].Update("")
				for idx, item in data.stack().items():
					window["-ML-"].print(idx[1], item)
				
			except ValueError as e:	# if input is blank or non numeric
				window["-ML-"].Update("")
				window["-OUTPUT-"].Update("")
				window["-INPUT-"].Update("")
				tb = traceback.format_exc()
				sg.Print('''Please fill the "Amount" field with a numeric value!

_༼ ಥ ‿ ಥ ༽_/¯	_༼ ಥ ‿ ಥ ༽_/¯
				''')

		else:	# every other button not in data keys
		
			if event == "About...":
				webbrowser.open_new_tab("https://github.com/marco-create/PersonalWallet")

			elif event == "Instructions":
				call_popup()

			elif event == "Reset wallet":
				choose = sg.popup_yes_no("Do you REALLY want to reset the wallet?\nThe application will be closed.", title="WARNING")
        # choose can be Yes or No
				if choose == "Yes":
					create_wallet() # call from instruction.py
					break
			
			elif event == "Show":
				for idx, item in data.stack().items():
					window["-ML-"].print(idx[1], item)

			elif event == "-CLEAR-":
				try:
					to_clean = new_events.pop(-1) # reset the last input from new_events list
					data[to_clean] -= float(values["-INPUT-"])  # subtract from that value the same value that has been added
					window["-ML-"].Update("")
					window["-OUTPUT-"].Update("")
					window["-INPUT-"].Update("")	
				except IndexError:	# if user tries to clean empty dictionary
							sg.Print('''Before you clean, you should insert some values!''')
							continue

			elif event in ("-EXIT-", "Exit", None):
				window["-OUTPUT-"].Update("")
				window["-INPUT-"].Update("")
				break		

			elif event == "-GO-": # update the wallet
				try:
					print()
          # take the output from Multiline element and convert it into a dictionary
					new = dict([each_pair.split(" ") for each_pair in values["-ML-"][:-2].split("\n")]) # [:-2] to avoid the last empty value
					new_float = {k : float(new[k]) for k in new}
					data.to_csv(r".\guiWallet.csv", index=False)
					# returns the sum of the expenses minus the income. Extract the resulting value from single-value list
					window["-OUTPUT-"].Update(f'Total amount of expenses: {data.loc[0, data.columns != "-INCOMES-"].sum() - data["-INCOMES-"].values[0]}')
					file.close()
				
				except ValueError as e:
					window["-ML-"].Update("")
					window["-OUTPUT-"].Update("")
					window["-INPUT-"].Update("")
					sg.Print('''What are you trying to save?

༼ つ ◕_◕ ༽つ	༼ つ ◕_◕ ༽つ
''',
					size=(60, 10))

window.close()
