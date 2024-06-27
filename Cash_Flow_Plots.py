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
    else:
        return None
    

# Streamlit app setup
st.title('Stock Cash Flow and Dividend Per Share Analysis')  # Added a title for the Streamlit app
ticker = st.text_input('Enter Ticker: ')  # Replaced input() with Streamlit's text_input

if ticker:  # Check if a ticker was entered
    try:    
        cashflow_data = cashflow(ticker)
        balance_sheet_data = balance_sheet(ticker)
        financial_data = financial(ticker)
        cashflow_per_share = process_cashflow(cashflow_data, balance_sheet_data, financial_data)
        dividend_per_share = dividend_per_share(cashflow_data, balance_sheet_data)
    
        Cname = yf.Ticker(ticker).info.get('longName', 'Unknown Company Name')
        st.write(f'Cash Flow and Dividend Per Share for {Cname}')  # Display the text in the Streamlit app
    
        # Extracting years for the x-axis
        cashflow_years = cashflow_per_share.index.year
        
        if dividend_per_share is not None:
            dividend_years = dividend_per_share.index.year
    
        # Plotting using matplotlib and displaying with Streamlit
        fig, ax1 = plt.subplots(figsize=(10, 8))
    
        ax1.set_xlabel('Year', fontsize=14)
        ax1.set_ylabel('Cash Flow Per Share', color='black', fontsize=14)
        ax1.plot(cashflow_years, cashflow_per_share.values, label='Cash Flow Per Share', color='tab:blue',
                     linewidth=2)
        ax1.tick_params(axis='y', labelcolor='black')
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax1.set_xticks(cashflow_years)
        ax1.set_xticklabels(cashflow_years.astype(int), rotation=45, ha='right')
    
        if dividend_per_share is not None:
            ax2 = ax1.twinx()
            ax2.set_ylabel('Dividend Per Share', color='black', fontsize=14)
            ax2.plot(dividend_years, dividend_per_share.values, label='Dividend Per Share', color='tab:orange',
                         linewidth=2, linestyle='--')
            ax2.tick_params(axis='y', labelcolor='black')
    
        # Add title and legends
        plt.title(f'Cash Flow Per Share and Dividend Per Share for {Cname}', fontsize=16)
        fig.tight_layout()
        ax1.legend(loc='upper left', fontsize=12)
        if dividend_per_share is not None:
            ax2.legend(loc='upper right', fontsize=12)
            
        st.pyplot(fig)
    
    except Exception as e:
        st.error(f"Please enter a valid ticker symbol.")
    
        # I am trying to figure out how to insert a table with the values
