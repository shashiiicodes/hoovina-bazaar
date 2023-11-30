# project title - Hoovina Bazaar (ಹೂವಿನ ಬಜಾರ್)
# author - shashank
# UI_page

# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Constants
FILE_PATH = 'C:/Users/Shashank/Desktop/Pre-thesis/A3/Data/Flower_rose.csv'


# Get current day of the week and time for prediction
day_of_week = datetime.today().weekday()

# Function to train the regression model
def train_regression_model(df):
    X = df[['TOS', 'DOW', 'Wholesale', 'QTY' ]]  # independent
    y = df['FUP1000']  # dependent

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Create and train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


# Function to predict price per kg using the trained model
def predict_price(time_of_sale, day_of_week, wholesale_price, quantity ):
    # Read data from CSV file into a Pandas DataFrame
    df = pd.read_csv(FILE_PATH)
    # Drop rows with NaN values
    df = df.dropna()
    # Train the regression model
    regression_model = train_regression_model(df)
    input_data = np.array([time_of_sale, day_of_week, wholesale_price, quantity]).reshape(1, -1)
    return round(regression_model.predict(input_data)[0])

