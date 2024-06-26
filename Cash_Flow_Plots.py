import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def cashflow(ticker):
    stock = yf.Ticker(ticker)
    cashflow = stock.cashflow.transpose()
    return cashflow


def financial(ticker):
    stock = yf.Ticker(ticker)
    financial = stock.financials.transpose()
    return financial

def balance_sheet(ticker):
    stock = yf.Ticker(ticker)
    balance_sheet = stock.balance_sheet.transpose()
    return balance_sheet

def process_cashflow(cashflow, balance_sheet):
    cashflow_per_share = cashflow.loc[:,'Cash Flow From Continuing Operating Activities']/ balance_sheet.loc[:,'Ordinary Shares Number']
    return cashflow_per_share

# Streamlit app setup
st.title('Stock Cash Flow Per Share Analysis')  # Added a title for the Streamlit app
ticker = st.text_input('Enter Ticker:', 'AAPL')  # Replaced input() with Streamlit's text_input

if ticker:  # Check if a ticker was entered
    cashflow_data = cashflow(ticker)
    balance_sheet_data = balance_sheet(ticker)
    cashflow_per_share = process_cashflow(cashflow_data, balance_sheet_data)

    st.write(f'Cash Flow Per Share for {ticker}')  # Display the text in the Streamlit app

# Plotting using matplotlib and displaying with Streamlit
    plt.figure(figsize=(10, 6))
    plt.plot(cashflow_per_share.index, cashflow_per_share.values, label='Cash Flow Per Share')
    plt.title(f'Cash Flow Per Share for {ticker}')
    plt.xlabel('Year')
    plt.ylabel('Cash Flow Per Share')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)
