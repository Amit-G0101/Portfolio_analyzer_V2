import sys
import pandas as pd
import os
import re
from datetime import datetime


# filter required stock prices from live data  
def fetch_stock_data(stock_data_path,filter_columns,filter_stock_list):

    # list all the files 
    filenames= os.listdir(stock_data_path)
    file_pattern =r"NIFTY.*\.csv"
    filtered_files=[]
    
    for file in filenames:
        if os.path.isfile(os.path.join(stock_data_path,file)) and re.search(file_pattern,file):
            filtered_files.append(file)

    print(f"\n******** Files present *********\n{filtered_files}")
    

    # ----- select the lastet file to be processed ------
    files_df=pd.DataFrame(filtered_files,columns=["file_name"])
    date_pattern=r"(\d{2})-(\w{3})-(\d{4})"

    files_df["date"]=files_df["file_name"].apply(lambda x: datetime.strptime(re.search(date_pattern,x).group(),'%d-%b-%Y'))
    
    files_df=files_df.sort_values('date',ascending=False)
    final_file=files_df.iloc[0]['file_name']
    print(f"\nLatest File to be processed: {final_file}")
    
    live_data=pd.read_csv(stock_data_path + '\\' + final_file)
    
    # current_stock_columns=live_data.columns.to_list()
    # print(current_stock_columns)

    #clean live data column names
    live_data.columns=live_data.columns.str.replace('\n','',regex=False).str.strip().str.lower()

    filter_df=live_data[filter_columns]
    final_df=filter_df[filter_df['symbol'].isin(filter_stock_list)]
    final_df['ltp']=final_df['ltp'].str.replace(',', '')
    final_df['ltp']=pd.to_numeric(final_df['ltp'],errors='coerce')

    print(f"\n********* Filtered stocks' live price **********\n{final_df}\n")
    return final_df
  
   

def get_live_stocks_price(stocks_df):
    print("********** Fetching live stocks data ************")
    try:
        
        #Testing input
        #property_file_path=".\\utility\\stocks.properties"
        stock_data_path=".\\utility\\stock_data"
        
        print(f"*******stock_data_path: {stock_data_path} ********")

        # setting which columns and stocklist are fetched from NIFTY Live data
        filter_stock_list=list(stocks_df['symbol'])
        filter_columns=['symbol','ltp']


        print(f"filter_columns: {filter_columns}\nfilter_stock_list:{filter_stock_list}")
        
        # filter required stock prices from live data
        return fetch_stock_data(stock_data_path,filter_columns,filter_stock_list)
    
    except Exception as e:
        print("Exception caught: "+ str(e))
        sys.exit(1)
    


