import streamlit as st
import pandas as pd 
import numpy as np  
import math
from sklearn.linear_model import LinearRegression as linreg
from sklearn.model_selection import train_test_split


data=pd.read_csv('https://raw.githubusercontent.com/ayanatherate/reg-mms-streamlit/main/df_data_for_streamlit.csv')
numeric_cols=data

brand_choices=list(set(data['Brand_Family_Desc'].tolist()))
brand_name=st.selectbox('Choose a Brand',options=brand_choices)
brand_df=numeric_cols[numeric_cols['Brand_Family_Desc']==brand_name]


upper_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[-1]
lower_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[0]

upper_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[-1]
lower_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[0]
    
upper_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[-1]
lower_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[0]
    
upper_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[-1]
lower_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[0]


ad_cost=st.slider(label='Enter your cost spent on Advertisement',min_value=0,max_value=math.ceil(upper_lim_ad_cost),value=1000000,step=1000)
tranf_price=st.slider(label='Enter your cost on Transfer Price',min_value=0,max_value=math.ceil(upper_lim_ad_tp),value=1000000,step=1000)
dist_cost_sc=st.slider(label='Enter your cost spent on Distribution Costs, Supply Chain',min_value=0,max_value=math.ceil(upper_lim_ad_dsc),value=1000000,step=1000)
dist_cost_reg=st.slider(label='Enter your cost spent on Distribution Costs, Region',min_value=0,max_value=math.ceil(upper_lim_ad_dr),value=1000000,step=1000)
     




    
    
        
                     
    
    
    
    
    
    
    
    
    
    
    
