import streamlit as st
import pandas as pd 
import numpy as np  
import math
import time

from perf_regression import make_linear_reg_mods


data=pd.read_csv('https://raw.githubusercontent.com/ayanatherate/reg-mms-streamlit/main/data_for_streamlit.csv')


data['Brand_Family_Desc'].fillna('ALL',inplace=True)
data['region_desc'].fillna('ALL',inplace=True)

numeric_cols=data

brand_choices=list(set(data['Brand_Family_Desc'].tolist()))
region_choices=list(set(data['region_desc'].tolist()))

#brand_choices=brand_choices.remove('nan')
#region_choices=region_choices.remove('nan')

brand_name=st.selectbox('Choose a Brand',options=brand_choices)
region_name=st.selectbox('Choose a Region',options=region_choices)

if brand_name=='ALL' and region_name!='ALL':
    brand_df=numeric_cols[numeric_cols['region_desc']==region_name]
elif region_name=='ALL' and brand_name!='ALL':
    brand_df=numeric_cols[numeric_cols['Brand_Family_Desc']==brand_name]
elif brand_name=='ALL' and region_name=='ALL':
    brand_df=numeric_cols
else:
    brand_df=numeric_cols[(numeric_cols['Brand_Family_Desc']==brand_name) & (numeric_cols['region_desc']==region_name)]
    if len(brand_df)==0:
        st.title('Insufficent Data in either Region or Brand to train a Model.')
        st.stop()
    
#st.write(len(brand_df))



#brand_df.drop(['Unnamed: 0','Brand_Family_Desc','region_desc'],axis=1,inplace=True)

brand_df['Advertisement_and_discount_cost']=brand_df['Advertisement_and_discount_cost'].astype('float64')
brand_df['Transfer_Price_COGS']=brand_df['Transfer_Price_COGS'].astype('float64')
brand_df['Distribution_cost_supply_chain']=brand_df['Distribution_cost_supply_chain'].astype('float64')
brand_df['Distribution_cose_Sales_-_Region']=brand_df['Distribution_cose_Sales_-_Region'].astype('float64')

brand_df['Advertisement_and_discount_cost']=brand_df['Advertisement_and_discount_cost'].fillna(brand_df['Advertisement_and_discount_cost'].median())
brand_df['Transfer_Price_COGS']=brand_df['Transfer_Price_COGS'].fillna(brand_df['Transfer_Price_COGS'].median())
brand_df['Distribution_cost_supply_chain']=brand_df['Distribution_cost_supply_chain'].fillna(brand_df['Distribution_cost_supply_chain'].median())
brand_df['Distribution_cose_Sales_-_Region']=brand_df['Distribution_cose_Sales_-_Region'].fillna(brand_df['Distribution_cose_Sales_-_Region'].median())
brand_df['Gross_Sales']=brand_df['Gross_Sales'].fillna(brand_df['Gross_Sales'].median())

brand_df.replace(0,0.007,inplace=True)

if brand_df['Advertisement_and_discount_cost'].isna().sum()>0 or brand_df['Transfer_Price_COGS'].isna().sum()>0 or brand_df['Distribution_cost_supply_chain'].isna().sum()>0 or brand_df['Distribution_cose_Sales_-_Region'].isna().sum()>0 or brand_df['Gross_Sales'].isna().sum()>0:
    st.title('Insufficient Data to train a Model.')
    st.stop()
else:
    pass

#st.write(brand_df)

brand_df.drop(['Unnamed: 0','Brand_Family_Desc','region_desc'],axis=1,inplace=True)


upper_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[-1]
lower_lim_ad_cost=sorted(brand_df['Advertisement_and_discount_cost'].values)[0]

upper_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[-1]
lower_lim_ad_tp=sorted(brand_df['Transfer_Price_COGS'].values)[0]
    
upper_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[-1]
lower_lim_ad_dsc=sorted(brand_df['Distribution_cost_supply_chain'].values)[0]
    
upper_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[-1]
lower_lim_ad_dr=sorted(brand_df['Distribution_cose_Sales_-_Region'].values)[0]


ad_cost=st.slider(label='Enter your cost spent on Advertisement',min_value=1,max_value=100000000,value=1000000,step=1000)
time.sleep(1)
tranf_price=st.slider(label='Enter your cost on Transfer Price',min_value=1,max_value=100000000,value=1000000,step=1000)
time.sleep(1)
dist_cost_sc=st.slider(label='Enter your cost spent on Distribution Costs, Supply Chain',min_value=1,max_value=100000000,value=1000000,step=1000)
time.sleep(1)
dist_cost_reg=st.slider(label='Enter your cost spent on Distribution Costs, Region',min_value=1,max_value=100000000,value=1000000,step=1000)
time.sleep(1)



ad_cost=np.log(ad_cost)
tranf_price=np.log(tranf_price)
dist_cost_sc=np.log(dist_cost_sc)
dist_cost_reg=np.log(dist_cost_reg)

coef,intrcpt,ans=make_linear_reg_mods(brand_df,ad_cost,tranf_price,dist_cost_sc,dist_cost_reg)

st.title(f'Based on a Regression model trained on {len(brand_df)} records, the estimated Gross Sales is {ans}')

st.caption('SEE ALSO:')
st.write(f'Coefficients: {coef[0]}, {coef[1]}, {coef[2]}, {coef[3]}')
st.write(f'Intercept value: {intrcpt}')
     




    
    
        
                     
    
    
    
    
    
    
    
    
    
    
    
