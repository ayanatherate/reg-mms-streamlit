import streamlit as st
import pandas as pd 
import numpy as np  
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


ad_cost=st.select_slider(label='',options='Enter the cost you want to spend on Advertisement',value=[upper_lim_ad_cost,lower_lim_ad_cost])
ad_cost=st.select_slider(label='',options='Enter the cost you want to spend on Advertisement',value=[upper_lim_ad_cost,lower_lim_ad_cost])
     



def make_linear_reg_mods(data):
    
    import warnings
    warnings.filterwarnings('ignore')
    
    
    numeric_cols=data
    
    
    
    
    
    
    ad_cost=st.text_input(f'Enter the cost you want to spend on Advertisement UL {upper_lim_ad_cost}:')
    tranf_price=st.text_input(f'Enter the estimated cost on Transfer Price UL {upper_lim_ad_tp}:')
    dist_cost_sc=st.text_input(f'Enter the estimated cost on Distribution Cost of Supply Chain UL{upper_lim_ad_dsc}:')
    dist_cost_reg=st.text_input(f'Enter the estimated cost on Distribution Cost of Supply Chain in Region UL{upper_lim_ad_dr}:')


    ad_cost=st.select_slider('Enter the cost you want to spend on Advertisement',value=[upper_lim_ad_cost,lower_lim_ad_cost])
    ad_cost=st.select_slider('Enter the cost you want to spend on Advertisement',value=[upper_lim_ad_cost,lower_lim_ad_cost])
     
        
    
    
    
    
    
    
    for col in brand_df.columns.tolist():
        brand_df[col]=np.log(brand_df[col])
        
    brand_df.dropna(inplace=True)   
    X=brand_df.drop(['Gross_Sales'],axis=1)
    y=brand_df['Gross_Sales']
    
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    
    linreg=linreg()
    
    linreg.fit(X_train,y_train)
    y_pred=linreg.predict(X_test)
    
    coefficients = linreg.coef_
    intercept=linreg.intercept_
                     
    ad_coef=coefficients[0]
    transf_coef=coefficients[1]
    dist_sc=coefficients[2]
    dist_sc_region=coefficients[3]
    
    print(coefficients)
    print(ad_cost)
    
    ans=(ad_coef*ad_cost)+(transf_coef*tranf_price)+(dist_sc*dist_cost_sc)+(dist_sc_region*dist_cost_reg)+intercept
    
    print(f'Intercept: {intercept}')

    ans=np.exp(ans)
    
    
        
                     
    
    print(f'Based on a regression model trained on {len(X_train)} records, with a R2 score of {r2(y_test,y_pred)}\
    it can be said that, the estimated GROSS SALES would be {round(ans,3)}')
    
    
    
    
    
    
    
    
    
