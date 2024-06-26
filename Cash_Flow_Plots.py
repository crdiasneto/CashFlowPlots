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

def process_cashflow(cashflow, balance_sheet, financial):
    cashflow_per_share = (financial.loc[:, 'Net Income'] + cashflow.loc[:,'Depreciation And Amortization']) / balance_sheet.loc[:,'Ordinary Shares Number']

    return cashflow_per_share

def dividend_per_share(cashflow, balance_sheet):
    if 'Cash Dividends Paid' in cashflow:
        dividend_per_share = (-cashflow.loc[:,'Cash Dividends Paid'])/ balance_sheet.loc[:,'Ordinary Shares Number']
        return dividend_per_share

# Streamlit app setup
st.title('Stock Cash Flow and Dividend Per Share Analysis')  # Added a title for the Streamlit app
ticker = st.text_input('Enter Ticker: ')  # Replaced input() with Streamlit's text_input

if ticker:  # Check if a ticker was entered
    cashflow_data = cashflow(ticker)
    balance_sheet_data = balance_sheet(ticker)
    financial_data = financial(ticker)
    cashflow_per_share = process_cashflow(cashflow_data, balance_sheet_data, financial_data)
    dividend_per_share = dividend_per_share(cashflow_data, balance_sheet_data)

    Cname = yf.Ticker(ticker).info.get('longName', 'Unknown Company Name')
    st.write(f'Cash Flo and Dividend Per Share for {Cname}')  # Display the text in the Streamlit app

# Plotting using matplotlib and displaying with Streamlit
    # Plotting using matplotlib and displaying with Streamlit
    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Cash Flow Per Share', color='tab:blue')
    ax1.plot(cashflow_per_share.index, cashflow_per_share.values, label='Cash Flow Per Share',
             color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Dividend Per Share', color='tab:orange')
    ax2.plot(dividend_per_share.index, dividend_per_share.values, label='Dividend Per Share',
             color='tab:orange')
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    fig.tight_layout()
    st.pyplot(fig)
