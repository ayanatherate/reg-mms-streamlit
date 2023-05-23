import streamlit as st
import pandas as pd 
import numpy as np  
import math
import time

from perf_regression import make_linear_reg_mods


data=pd.read_csv('https://raw.githubusercontent.com/ayanatherate/reg-mms-streamlit/main/data_for_streamlit.csv')
numeric_cols=data

brand_choices=list(set(data['Brand_Family_Desc'].tolist()))
region_choices=list(set(data['region_desc'].tolist()))

brand_name=st.selectbox('Choose a Brand',options=brand_choices)
region_name=st.selectbox('Choose a Region',options=region_choices)

brand_df=numeric_cols[(numeric_cols['Brand_Family_Desc']==brand_name) & (numeric_cols['Brand_Family_Desc']==region_name)]

brand_df.drop(['Unnamed: 0','Brand_Family_Desc'],axis=1,inplace=True)

brand_df['Advertisement_and_discount_cost']=brand_df['Advertisement_and_discount_cost'].astype('float64')
brand_df['Transfer_Price_COGS']=brand_df['Transfer_Price_COGS'].astype('float64')
brand_df['Distribution_cost_supply_chain']=brand_df['Distribution_cost_supply_chain'].astype('float64')
brand_df['Distribution_cose_Sales_-_Region']=brand_df['Distribution_cose_Sales_-_Region'].astype('float64')


upper_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[-1]
lower_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[0]

upper_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[-1]
lower_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[0]
    
upper_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[-1]
lower_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[0]
    
upper_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[-1]
lower_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[0]


ad_cost=st.slider(label='Enter your cost spent on Advertisement',min_value=1,max_value=math.ceil(upper_lim_ad_cost),value=1000000,step=1000)
time.sleep(1)
tranf_price=st.slider(label='Enter your cost on Transfer Price',min_value=1,max_value=math.ceil(upper_lim_ad_tp),value=1000000,step=1000)
time.sleep(1)
dist_cost_sc=st.slider(label='Enter your cost spent on Distribution Costs, Supply Chain',min_value=1,max_value=math.ceil(upper_lim_ad_dsc),value=1000000,step=1000)
time.sleep(1)
dist_cost_reg=st.slider(label='Enter your cost spent on Distribution Costs, Region',min_value=1,max_value=math.ceil(upper_lim_ad_dr),value=1000000,step=1000)
time.sleep(1)

brand_df.replace(0,0.007,inplace=True)

ad_cost=np.log(ad_cost)
tranf_price=np.log(tranf_price)
dist_cost_sc=np.log(dist_cost_sc)
dist_cost_reg=np.log(dist_cost_reg)

coef,intrcpt,ans=make_linear_reg_mods(brand_df,ad_cost,tranf_price,dist_cost_sc,dist_cost_reg)

st.title(f'The estimated Gross Sales is {ans}')

st.caption('SEE ALSO:')
st.write(f'Coefficients: {coef[0]}, {coef[1]}, {coef[2]}, {coef[3]}')
st.write(f'Intercept value: {intrcpt}')
     




    
    
        
                     
    
    
    
    
    
    
    
    
    
    
    
