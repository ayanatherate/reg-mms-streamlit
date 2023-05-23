
import numpy as np
from sklearn.linear_model import LinearRegression as linreg
from sklearn.model_selection import train_test_split


def make_linear_reg_mods(brand_df,ad_cost,tranf_price,dist_cost_sc,dist_cost_reg):
    
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
    
    ans=(ad_coef*ad_cost)+(transf_coef*tranf_price)+(dist_sc*dist_cost_sc)+(dist_sc_region*dist_cost_reg)+intercept
    ans=np.exp(ans)

    return coefficients, intercept, ans


if '__name__'=='__main__':
    make_linear_reg_mods(brand_df,ad_cost,tranf_price,dist_cost_sc,dist_cost_reg)