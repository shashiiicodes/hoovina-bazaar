# project title - Hoovina Bazaar (ಹೂವಿನ ಬಜಾರ್)
# author - shashank
# UI_page

# Import necessary libraries
import pandas as pd
from datetime import datetime
from nicegui import ui
from Multi_linear_Regression import predict_price

# Initialisation of global variable
total_kilos = 0
total_profits = 0
age = 0
remaining = 0
pred_price = 0
image_link = 'https://static.vecteezy.com/system/resources/previews/012/954/861/original/traditional-indian-flower-garland-frame-with-marigold-flowers-decoration-for-indian-hindu-holidays-illustration-isolated-on-white-background-vector.jpg'

# Constants
FILE_PATH = r'C:\Users\Shashank\Desktop\Pre-thesis\A3\Data\Flower_rose.csv'

# Read data from CSV file into a Pandas DataFrame and drop the rows with NaN values
df = pd.read_csv(FILE_PATH)
df = df.dropna()

# Initialisation of Predicted price global
pred_price = 0
pred_price_input = None

# Get current day of the week and time for prediction
day_of_week = datetime.today().weekday()

# Functions for the project------------------------------------------------------------------------------------

# Function to receive predicted price from another file and display predicted price
def predict():
    global pred_price,pred_price_input,time_of_sale
    
    current_time = datetime.now().time() # Extract hours and minutes 
    hours_part = str(current_time.hour).zfill(2)
    minutes_part = str(current_time.minute).zfill(2) # Convert minutes from 0-59 to 0-100
    minutes_part_int = int(minutes_part)
    minutes = str(int(minutes_part_int * 1.666))
    time_of_sale= int(hours_part + minutes)

    pred_price = predict_price(time_of_sale , day_of_week, float(wholesale_price_input.value), 1 )
    ui.label('Suggested Price :').style('color:#008000; width: 80vw; border: 2px solid #008000; padding: 5px; font-size: 20px; position: absolute; top: 240px; left: 50%; transform: translate(-50%, -50%); font-weight: bold; ')
    pred_price_input = ui.label(f'{pred_price}').style('color:#008000;width:50px; background-color:#ffffff;font-size: 20px; position: absolute; top: 240px; right: 20%; transform: translate(-50%, -50%); font-weight: bold; ')
        
# Function to receive the input data from GUI and add it to the DataFrame
def submit_all_data():
    global df ,pred_price # Declare df as a global variable
    if not wholesale_price_input.value or not total_quantity_input.value or not time_of_arrival_input.value or not final_price_input.value or not sale_quantity_input.value:
        ui.notify('Invalid input. Please enter valid numeric values in all fields.')
        return

    try:
        # Convert input values to appropriate data types
        wholesale_price = float(wholesale_price_input.value)
        selected_flower = flower_dropdown.value
        total_quantity = float(total_quantity_input.value)
       
        # Aonverting time of arrival from 0-69 to 0-99
        time_of_arrival = int(time_of_arrival_input.value)
        hour = time_of_arrival // 100
        minute = time_of_arrival % 100
        minute_scaled = (minute / 60) * 100
        arrival = int((hour * 100) + minute_scaled)
        
        final_price = int(final_price_input.value)
        sale_quantity = float(sale_quantity_input.value)
       
       # Run the calculation function before uploading data into DataFrame
        profits, fup1000, total_profits, total_kilos, age, remaining = calculation(final_price, wholesale_price, sale_quantity, time_of_sale, arrival, total_quantity)      

    except ValueError as e:
        ui.notify('Invalid input. Please enter valid numeric values.')
        return

    # Append new entry to the DataFrame 
    new_entry_upload = pd.DataFrame({'DOW' : [day_of_week],
                                     'Wholesale': [wholesale_price], 
                                     'TOA': [arrival],     
                                     'Total Quantity': [total_quantity], 
                                     'TOS' : [time_of_sale], 
                                     'AGE' :[age] ,   
                                     'QTY': [sale_quantity],           
                                     'FP': [final_price], 
                                     'FUP1000':[fup1000], 
                                     'PROFITS':profits,
                                     'Predicted':[pred_price] ,
                                     'Total sold' : [total_kilos], 
                                     'Total profits' :[total_profits],
                                     'Qty left' :[remaining], 
                                     'Flower': [selected_flower] })

    # Concatenate both entries
    df = pd.concat([df, new_entry_upload], ignore_index=True)

    # Save the updated DataFrame to the same CSV file
    df.to_csv(FILE_PATH, index=False)

    # Notify user about successful data append
    ui.notify('Data registered successfully for this sale.')

    # Reset input fields
    reset_input_fields()

# Function to run calculations for variable to be displayed in the GUI
def calculation(final_price, wholesale_price, sale_quantity, time_of_sale, arrival, total_quantity):
    global total_profits, total_kilos,age,remaining
    profits = final_price - wholesale_price * sale_quantity
    fup1000 = final_price / sale_quantity # need to append into the excel
 
    total_profits+= profits
    total_kilos += sale_quantity
    remaining = total_quantity - total_kilos

    age1 = int(time_of_sale - arrival)
    hour = age1 // 100
    minute = age1 % 100
    minute_scaled = int(minute / 1.666 + 1)  # Convert to integer
    age = f'{hour:02d}:{minute_scaled:02d} hrs'  # Format as HH:MM
  
    
    # UI label for display the calculations of total profits and total sale quantity
    with ui.row():
        with ui.element('div').classes('p-5 bg-blue-100').style('width: 40vw;position: absolute; top: 430px; left: 20px;'):
            ui.label(f'Profits = {total_profits}')

        with ui.element('div').classes('p-5 bg-blue-100').style('width: 40vw;position: absolute; top: 430px; right: 20px;'):
            ui.label(f'Total sold={total_kilos}')

    # UI label for display the calculations of age of flowers and stock of flowers left
    with ui.row():
        with ui.element('div').classes('p-5 bg-blue-100').style('width: 40vw;position: absolute; top: 500px; left: 20px;'):
            ui.label(f'Age = {age}')

        with ui.element('div').classes('p-5 bg-blue-100').style('width: 40vw;position: absolute; top: 500px; right: 20px;'):
            ui.label(f'Stock left={remaining}')

    return profits, fup1000, total_profits, total_kilos, age, remaining 

# Function to reset input fields
def reset_input_fields():
    
    final_price_input.set_value('')
    sale_quantity_input.set_value('')


# Create labels for displaying information---------------------------------------------------------------------

# Label to displat time and day
with ui.row():
    time_label = ui.label().style('font-size: 20px;position: absolute; top:15px; right: 25px;')
    ui.timer(1.0, lambda: time_label.set_text(f'{datetime.now():%X}'))
    current_time_label = time_label     
    day_of_week_label = ui.label(datetime.today().strftime('%A')).style('font-size: 20px; position: absolute; top:35px; right: 25px;')

# Flower type, Time of arrival
# Input for flower type and time of arrival of flowers
with ui.row():
    flower_dropdown = ui.select(['Rose', 'Sevanthi'], value='Rose').style('font-size: 18px;position: absolute; top: 80px')
    time_of_arrival_input = ui.input('Arrival Time(HHMM)').style('font-size: 16px; position: absolute; top: 80px; right: 20px;width:150px;')

# Wholesale price and Total quantity
# Input for wholesale price of the flowers andtotal quantiy of flowers bought
with ui.row():
    wholesale_price_input = ui.input('Wholesale Price').style('font-size: 16px; position: absolute; top: 140px;width:150px;')
    total_quantity_input = ui.input('Total Quantity(kg)').style('font-size: 16px; position: absolute; top: 140px; right: 20px;width:150px;')

# Final price, Sale quantity
# Input for final price and sale quantity per transaction
with ui.row():
    final_price_input = ui.input('Sale Price').style('font-size: 16px;font-weight: bold; position: absolute; top: 370px;width:150px;')
    sale_quantity_input = ui.input('Sale Quantity(kg)').style('font-size: 16px; font-weight: bold;position: absolute; top: 370px; right: 20px; width:150px;')
    
# Code to add image of a flower and title
with ui.row():
    ui.label('ಹೂವಿನ ').style('color: #888;font-size:20px; font-weight: bold;position: absolute; top: 15px; left: 80px; ')
    ui.label('Bazaar').style('color: #888;font-size:20px; font-weight: bold;position: absolute; top: 35px; left: 80px; ')
    ui.image(image_link).style('width:60px; height:60px;position: absolute; top: 10px; left: 10px; ')

# Buttons to Predict and Submit data
pred_button = ui.button('Suggest Price', on_click= predict).style('font-size: 16px; position: absolute;width: 90vw; top: 300px; left: 50%; transform: translate(-50%, -50%);')
submit_button = ui.button('Submit', on_click=submit_all_data).style('width: 90vw;font-size: 20px; position: absolute; top: 610px; left: 50%; transform: translate(-50%, -50%);')

# Line to seperate Predicted price and Sale data
ui.separator().style('position: absolute; top: 340px;left:0%; border-bottom: 5px solid #000;')
   
# Run the NiceGUI interface
ui.run()
