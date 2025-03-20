import streamlit as st
import pandas as pd
import mysql.connector
from connection import getConnection
import json
from utility.livedata import get_live_stocks_price

# Fetch data
def fetch_data(query):
    con = getConnection()
    df = pd.read_sql(query, con)
    con.close()
    return df

def get_stocks_broker_info():
    
    path="./broker&stocks_details.json"
    data=None
    with open(path,'r') as jsonfile:
        data=json.load(jsonfile)
        jsonfile.close()
    
    brokers=data[0]['brokers'] 
    stocks=data[0]['stocks']
    
    broker_df=pd.DataFrame(brokers)
    stocks_df=pd.DataFrame(stocks)
    
    live_price_df=get_live_stocks_price(stocks_df)
    return broker_df,stocks_df,live_price_df

def run_dashboard():
        
    '''
    # Streamlit app
    st.title("Stock Portfolio Dashboard")
    
    # Fetch total investment
    total_invested = fetch_data("SELECT SUM(total_amount) AS total_invested FROM invest.trnsc_fact WHERE trnsc_type='BUY'")
    st.metric(label="Total Invested Amount", value=total_invested.iloc[0, 0])
    
    # Fetch total sold amount
    total_sold = fetch_data("SELECT SUM(total_amount) AS total_sold FROM invest.trnsc_fact WHERE trnsc_type='SELL'")
    st.metric(label="Total Sold Amount", value=total_sold.iloc[0, 0])
    
    # Amount still invested
    still_invested_query = """
    WITH summary AS (
        SELECT stock_id, broker_id,
            SUM(CASE WHEN trnsc_type IN ('BUY', 'BONUS') THEN qty ELSE 0 END) -
            SUM(CASE WHEN trnsc_type = 'SELL' THEN qty ELSE 0 END) AS remain_qty,
            ROUND(SUM(CASE WHEN trnsc_type IN ('BUY', 'BONUS') THEN total_amount ELSE 0 END) /
            SUM(CASE WHEN trnsc_type IN ('BUY', 'BONUS') THEN qty ELSE 0 END), 2) AS avg_buy_price
        FROM invest.trnsc_fact
        GROUP BY broker_id, stock_id
    )
    SELECT SUM(remain_qty * avg_buy_price) AS Amount_still_invest FROM summary WHERE remain_qty > 0;
    """
    amount_still_invested = fetch_data(still_invested_query)
    st.metric(label="Total Amount Still Invested", value=amount_still_invested.iloc[0, 0])
    
    # Profit/Loss from Sold Stocks
    profit_loss_sold_query = """
    WITH summary AS (
        SELECT broker_id, stock_id,
            SUM(CASE WHEN trnsc_type = 'SELL' THEN qty ELSE 0 END) AS sold_qty,
            ROUND(SUM(CASE WHEN trnsc_type = 'SELL' THEN total_amount ELSE 0 END) /
            SUM(CASE WHEN trnsc_type = 'SELL' THEN qty ELSE 0 END), 2) AS Avg_sell_price,
            ROUND(SUM(CASE WHEN trnsc_type IN ('BUY', 'BONUS') THEN total_amount ELSE 0 END) /
            SUM(CASE WHEN trnsc_type IN ('BUY', 'BONUS') THEN qty ELSE 0 END), 2) AS avg_buy_price
        FROM invest.trnsc_fact
        GROUP BY broker_id, stock_id
    )
    SELECT SUM((Avg_sell_price - avg_buy_price) * sold_qty) AS netPNL FROM summary WHERE sold_qty > 0;
    """
    profit_loss_sold = fetch_data(profit_loss_sold_query)
    st.metric(label="Total Profit/Loss from Sold Stocks", value=profit_loss_sold.iloc[0, 0])
    '
    '''
    
    #7. Total consolidated profit/loss on still invested stocks from both brokers
    avgprice_qtyleft_query="""
    with summry as(
    select stock_id,broker_id,sum(case when trnsc_type in ('BUY','BONUS') then qty else 0 END ) -
     sum(case when trnsc_type ='SELL' then qty else 0 END ) as remain_qty,
    round(sum(case when trnsc_type in ('BUY','BONUS') then total_amount else 0 END )/
    sum(case when trnsc_type in ('BUY','BONUS') then qty else 0 END ),2) as avg_buy_price
     from invest.trnsc_fact group by broker_id,stock_id)
    select * from summry where remain_qty>0
    """
    avgprice_qtyleft_df = fetch_data(avgprice_qtyleft_query)
    broker_df,stocks_df,live_price_df=get_stocks_broker_info()
    
    
    res_df=avgprice_qtyleft_df.merge(stocks_df.merge(live_price_df,how="inner",on="symbol"),how="left",on="stock_id")
    
    res_df['PNL']=(res_df['ltp']-res_df['avg_buy_price'])*res_df['remain_qty']
    print(round(res_df['PNL'].sum(),2))
    