import streamlit as st
import pandas as pd 
import numpy as np  
import matplotlib.pyplot as plt
import math
import time

from perf_regression import make_linear_reg_mods
from helper_converts import convert_df

#reading data to memory
data=pd.read_csv('https://raw.githubusercontent.com/ayanatherate/reg-mms-streamlit/main/Ct_data_bv_state_wtht_dfnc.csv')
#st.write(len(data))
#data processing

data.dropna(subset=['Brand_Family_Desc'], inplace=True)
data.dropna(subset=['State_Desc'], inplace=True)

numeric_cols=data

brand_choices=list(set(data['Brand_Family_Desc'].tolist()))
region_choices=list(set(data['State_Desc'].tolist()))

region_choices.append('ALL')

#brand_choices=brand_choices.remove('nan')
#region_choices=region_choices.remove('nan')

brand_name=st.selectbox('Choose a Brand',options=brand_choices)
region_name=st.selectbox('Choose a Region',options=region_choices)

if brand_name=='ALL' and region_name!='ALL':
    brand_df=numeric_cols[numeric_cols['State_Desc']==region_name]
elif region_name=='ALL' and brand_name!='ALL':
    brand_df=numeric_cols[numeric_cols['Brand_Family_Desc']==brand_name]
elif brand_name=='ALL' and region_name=='ALL':
    brand_df=numeric_cols
else:
    brand_df=numeric_cols[(numeric_cols['Brand_Family_Desc']==brand_name) & (numeric_cols['State_Desc']==region_name)]
    if len(brand_df)==0:
        st.title('Insufficent Data in either Region or Brand to train a Model.')
        st.stop()
    
#st.write(len(brand_df))



#brand_df.drop(['Unnamed: 0','Brand_Family_Desc','region_desc'],axis=1,inplace=True)

#brand_df['Advertisement_and_discount_cost']=brand_df['Advertisement_and_discount_cost'].astype('float64')
#brand_df['Transfer_Price_COGS']=brand_df['Transfer_Price_COGS'].astype('float64')
#brand_df['Distribution_cost_supply_chain']=brand_df['Distribution_cost_supply_chain'].astype('float64')
#brand_df['Distribution_cose_Sales_-_Region']=brand_df['Distribution_cose_Sales_-_Region'].astype('float64')

brand_df['Advertisement_and_discount_cost']=brand_df['Advertisement_and_discount_cost'].fillna(brand_df['Advertisement_and_discount_cost'].median())
brand_df['Transfer_Price_COGS']=brand_df['Transfer_Price_COGS'].fillna(brand_df['Transfer_Price_COGS'].median())
brand_df['Distribution_cost_supply_chain']=brand_df['Distribution_cost_supply_chain'].fillna(brand_df['Distribution_cost_supply_chain'].median())
brand_df['Distribution_cose_Sales_-_Region']=brand_df['Distribution_cose_Sales_-_Region'].fillna(brand_df['Distribution_cose_Sales_-_Region'].median())
brand_df['Gross_Sales']=brand_df['Gross_Sales'].fillna(brand_df['Gross_Sales'].median())

#brand_df.replace(0,0.001,inplace=True)

brand_df['Advertisement_and_discount_cost'].replace(0,brand_df['Advertisement_and_discount_cost'].median(),inplace=True)
brand_df['Transfer_Price_COGS'].replace(0,brand_df['Transfer_Price_COGS'].median(),inplace=True)
brand_df['Distribution_cost_supply_chain'].replace(0,brand_df['Distribution_cost_supply_chain'].median(),inplace=True)
brand_df['Distribution_cose_Sales_-_Region'].replace(0,brand_df['Distribution_cose_Sales_-_Region'].median(),inplace=True)
brand_df['Gross_Sales'].replace(0,brand_df['Gross_Sales'].median(),inplace=True)


st.write(brand_df)

brand_df['Advertisement_and_discount_cost'].replace(0,brand_df['Advertisement_and_discount_cost'].mean(),inplace=True)
brand_df['Transfer_Price_COGS'].replace(0,brand_df['Transfer_Price_COGS'].mean(),inplace=True)
brand_df['Distribution_cost_supply_chain'].replace(0,brand_df['Distribution_cost_supply_chain'].mean(),inplace=True)
brand_df['Distribution_cose_Sales_-_Region'].replace(0,brand_df['Distribution_cose_Sales_-_Region'].mean(),inplace=True)
brand_df['Gross_Sales'].replace(0,brand_df['Gross_Sales'].mean(),inplace=True)



st.write(brand_df)
send_df_user=brand_df


if brand_df['Advertisement_and_discount_cost'].isna().sum()>0 or brand_df['Transfer_Price_COGS'].isna().sum()>0 or brand_df['Distribution_cost_supply_chain'].isna().sum()>0 or brand_df['Distribution_cose_Sales_-_Region'].isna().sum()>0 or brand_df['Gross_Sales'].isna().sum()>0:
    st.title('Insufficient Data to train a Model.')
    st.stop()
else:
    pass
csv = convert_df(send_df_user)
st.download_button("Press to Download User Interaction CSV",csv,"file.csv","text/csv",key='download-csv')
     

#st.write(send_df_user)

brand_df.drop(['Unnamed: 0','Brand_Family_Desc','State_Desc'],axis=1,inplace=True)


upper_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[-1]
lower_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[0]

upper_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[-1]
lower_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[0]
    
upper_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[-1]
lower_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[0]
    
upper_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[-1]
lower_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[0]


#ad_cost=st.slider(label='Enter your cost spent on Advertisement',min_value=1,max_value=100000000,value=1000000,step=1000)
#time.sleep(1)
#tranf_price=st.slider(label='Enter your cost on Transfer Price',min_value=1,max_value=100000000,value=1000000,step=1000)
#time.sleep(1)
#dist_cost_sc=st.slider(label='Enter your cost spent on Distribution Costs, Supply Chain',min_value=1,max_value=100000000,value=1000000,step=1000)
#time.sleep(1)
#dist_cost_reg=st.slider(label='Enter your cost spent on Distribution Costs, Region',min_value=1,max_value=100000000,value=1000000,step=1000)
#time.sleep(1)

ad_cost=st.text_input('Enter your cost spent on Advertisement')
tranf_price=st.text_input('Enter your cost on Transfer Price')
dist_cost_sc=st.text_input('Enter your cost spent on Distribution Costs, Supply Chain')
dist_cost_reg=st.text_input('Enter your cost spent on Distribution Costs, Region')

if ad_cost:
    ad_cost=np.log(int(ad_cost))
else:
    ad_cost=np.log(100000)

if tranf_price:
    tranf_price=np.log(int(tranf_price))
else:
    tranf_price=np.log(100000)

if dist_cost_sc:
    dist_cost_sc=np.log(int(dist_cost_sc))
else:
    dist_cost_sc=np.log(1)

if dist_cost_reg:
    dist_cost_reg=np.log(int(dist_cost_reg))
else:
    dist_cost_reg=np.log(1)

coef,intrcpt,ans=make_linear_reg_mods(brand_df,ad_cost,tranf_price,dist_cost_sc,dist_cost_reg)

st.title(f'Based on a Regression model trained on {len(brand_df)} records, the estimated Gross Sales is {ans}')

st.caption('SEE ALSO:')
st.write(f'Coefficients: {coef[0]}, {coef[1]}, {coef[2]}, {coef[3]}')
st.write(f'Intercept value: {intrcpt}')







    
    
        
                     
    
    
    
    
    
    
    
    
    
    
    
