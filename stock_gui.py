import datetime as dt
from datetime import timedelta
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import tkinter
import os

from tkinter import *
from tkinter import messagebox
    
def generateGraph(csv_file, time_frame, start_date, end_date):
    '''
    This will generate a line chart for the data downloaded.
    '''
    
    # Reads the downloaded csv file.
    df = pd.read_csv(csv_file, index_col=False)
    
    # Gets the values for the x and y axis, respectively.
    x_values = df["Date"]
    y_values = df["Close"]

    # Gets the ticker.
    ticker = csv_file[:-4]
    
    # Creates the label for the x-axis.
    plt.xlabel("\nDate")
    
    # Creates the label for the y-axis.
    plt.ylabel("Price")
    
    # Changes the axes based on the frequency.
    if (time_frame == 1):
        
        # Creates the title of the chart.
        plt.title(ticker.upper() + " Historical data for past 5 business days")
        
        # Rotates the x-axis tickers by 45 degrees CCW.
        plt.xticks(rotation=45)
        
        # Sets the ticks for the y-axis for intervals of 0.2.
        plt.yticks(np.arange(min(y_values), max(y_values) + 1, 0.2))
        
    elif (time_frame == 2):
        
        # Creates the title of the chart.
        plt.title(ticker.upper() + " Historical data for past month")
        
        # Rotates the x-axis tickers by 45 degrees CCW.
        plt.xticks(rotation=45)
        
        # Sets the ticks for the y-axis for intervals of 0.5.
        plt.yticks(np.arange(min(y_values), max(y_values) + 1, 0.5))
    
    else:
        
        # Creates the title of the chart.
        plt.title(ticker.upper() + " Historical data for past year")        
        
        # Hides the x-axis ticks
        plt.xticks([])
        
        # Sets the ticks for the y-axis for intervals of 5.
        plt.yticks(np.arange(min(y_values), max(y_values) + 1, 5))        

    plt.tight_layout()
    
    # Plots the graph.
    plt.plot(x_values, y_values)
    
    # Shows the graph.
    plt.show()
    
    # Deletes the csv file.
    os.remove(csv_file)

def get_data(symbol, time_frame):
    '''
    This downloads the csv file for the ticker and gets the data for a week, month or year.
    '''
    
    # Gets the start and end dates.
    end_time = dt.datetime.today()
    frequency = ""
    
    if (time_frame == 1):
        # Sets the start date to exactly 1 week prior.
        start_time = end_time - timedelta(days=7)
        
    elif (time_frame == 2):
        # Sets the start date to exactly 1 month prior.
        # If the month is January, we have to get December of last year.
        if (end_time.month == 1):
            start_time = dt.datetime(end_time.year - 1, 12, end_time.day)
        else:
            start_time = dt.datetime(end_time.year, end_time.month - 1, end_time.day)        
   
    else:
        # Sets the start date to exactly 1 year prior.
        start_time = dt.datetime(end_time.year - 1, end_time.month, end_time.day)
    
    try:
        df = web.DataReader(symbol, "yahoo", start_time, end_time)
        csv_file = symbol + '.csv'
        df.to_csv(csv_file)      
        generateGraph(csv_file, time_frame, str(start_time)[:10], str(end_time)[:10])

    except Exception as e:
        print(e)
        messagebox.showinfo("ERROR", e)

def search():
    '''
    Checks if the user inputted a stock ticker symbol.
    '''
    
    # Gets the entry and radiobutton values.
    symbol = entry.get()
    time_frame = v.get()
    
    # Checks if the user searched for a ticker.
    if (len(symbol) == 0):
        messagebox.showinfo("ERROR", "You did not enter a stock ticker symbol.")
        return
    
    # Calls get_data function with
    get_data(symbol, time_frame)

if __name__ == "__main__":
    # Creates an window.
    windows = tkinter.Tk()
    
    # Sets the dimensions of the window.
    windows.geometry("520x270")
    
    # Configures the background colour.
    windows.configure(background='light green')
    
    # Creates the title of the window.
    windows.title("Stock Data Viewer")
    
    # Creates the message of the window.
    title = Label(windows, text="Enter a stock ticker symbol", fg="Black", bg = "light green", font=("Arial", 25, "bold"))
    title.pack(pady = (4,4))
    
    # Creates a place where the user can enter the stock ticker symbol.
    entry = Entry(windows)
    entry.pack()
    
    # Creates the message of the window.
    title2 = Label(windows, text="Choose a time frame from below.", fg="Black", bg = "light green", font=("Arial", 25, "bold"))
    title2.pack(pady = (4,4))
    
    # Sets the default choice to be 5 past business days.
    v = IntVar(windows, 1) 
    
    # Dictionary to create multiple buttons 
    values = {"Past Week" : 1, 
          "Past Month" : 2, 
          "Past Year" : 3} 
    
    # Loop is used to create multiple Radiobuttons 
    # rather than creating each button separately 
    for (text, value) in values.items(): 
        Radiobutton(windows, text = text, variable = v,  
                    value = value, bg = "light green").pack(side = TOP, ipady = 2, anchor=CENTER)
    
    # Creates a button for the user to click after entering the stock ticker symbol.
    button = Button(windows, text="Search", command=search, fg="Black", bg="white", font=("Arial", 15, "bold"))
    button.pack(pady = (4,4))
    
    windows.mainloop()