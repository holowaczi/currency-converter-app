from sre_compile import dis
from tkinter import CENTER
import requests
import PySimpleGUI as sg
import json

        
def convert(data, from_curr, to_curr, amount):
    currencies = data["rates"]

    if from_curr != "USD":
        amount = amount/float(currencies[from_curr])

    amount = round(amount * float(currencies[to_curr]), 4)
    return amount

sg.theme("DarkAmber")
url = 'https://api.exchangerate-api.com/v4/latest/USD'
try:
    data = requests.get(url).json()
    data_json = json.dumps(data)
    with open('rates.json', 'w') as f:
        f.write(data_json)
        f.close
except:
    data = json.load(open('rates.json'))
currencies = list(data["rates"].keys())
rates = data["rates"]
date = data['date']
col1 = [
    [sg.Text(text="FROM:", justification=CENTER, expand_x=True, font=("Courier", 10,"bold"))],
    [sg.Combo(currencies, default_value="USD", key="input_currency", pad=(10,10),readonly=True,enable_events=True)]
]
col2=[
    [sg.Text(text="TO:", justification=CENTER, expand_x=True, font=("Courier", 10,"bold"))],
    [sg.Combo(currencies, default_value="PLN", key="output_currency",readonly=True,pad=(10,10),enable_events=True)]
]
col3=[
    [sg.Text(text="AMOUNT", justification=CENTER, expand_x=True, font=("Courier", 10,"bold"))],
    [sg.Input(background_color="#FAFAD2", text_color="black",enable_events=True, default_text=0,key="input_value", size=(10,1))]
]
layout=[
    [sg.Text(text="CURRENCY CONVERTER", justification=CENTER, expand_x=True, font=("Courier", 15,"bold"))],
    [sg.Column(col1,element_justification="center"), sg.Column(col2, element_justification="center")],
    [sg.Column(col3,element_justification="center")],
    [sg.Button(button_text="CONVERT",key="convert",enable_events=True)],
    [sg.Text(text="", justification=CENTER, expand_x=True, font=("Courier", 15,"bold"), key="output_value")],
    [sg.Text(text=f'For day {date}', justification=CENTER, expand_x=True, font=("Courier", 15,"bold"), key="date")],
    [sg.Button("QUIT")],
    
]

window = sg.Window('Currency Converter', layout, icon="icon.ico", element_justification="center",auto_size_buttons=True,auto_size_text=True,scaling=2.5, resizable=True)

while True:             
    event, values = window.read()
    if event in (None, 'QUIT'):
        break
    if event == "convert":
        try:
            window["output_value"].Update(f'{values["input_value"]} {values["input_currency"]} = {convert(data,values["input_currency"],values["output_currency"],float(values["input_value"]))} {values["output_currency"]}')
        except:
            window["output_value"].Update('Improper input value')
window.close()
