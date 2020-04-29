# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os.path

#paths
GDPPath = os.path.join("Data","GDP_DATA.csv")
PaxDataPath = os.path.join("Data","UK_Air_Pax.csv")

#read data
GDPData = pd.read_csv(GDPPath)
PaxData = pd.read_csv(PaxDataPath)

#combine the two datasets into 1 data frame
CombiData = pd.concat([GDPData,PaxData['Passengers']],axis =1)
CombiData.set_index('Year', inplace = True)
CombiData.rename(columns={'Gross Domestic Product at market prices: Current price: Seasonally adjusted £m':'GDP'}, inplace = True)

plt.subplot(2, 1, 1)
plt.plot(CombiData['Passengers'])
plt.title('Passenger count and GDP Data')
plt.ylabel('Passenger counts')
plt.ticklabel_format(style='plain')


plt.subplot(2, 1, 2)
plt.plot(CombiData['GDP'])
plt.xlabel('Year', fontsize = 12, fontfamily = 'sans-serif')
plt.ylabel('Real GDP £m')
plt.ticklabel_format(style='plain')

plt.show()

#fit polynomial regression to data
x_pr = CombiData.iloc[0:50, 0:1].values 
y_pr = CombiData.iloc[0:50, 1].values 

X_train, X_test, y_train, y_test = train_test_split(CombiData.iloc[15:50, 0:1].values,CombiData.iloc[15:50, 1].values)

poly = PolynomialFeatures(degree = 2)
X_poly = poly.fit_transform(X_train) 
  
poly.fit(X_poly, y_train) 
lin2 = LinearRegression() 
lin2.fit(X_poly, y_train) 

y_test_sorted = np.sort(y_test, axis = 0)
X_test_sorted = np.sort(X_test, axis = 0)

plt.plot(X_test_sorted, lin2.predict(poly.fit_transform(X_test_sorted)), color='r', label = 'Predicted Values')
plt.scatter(X_test, y_test, label = 'Actual Values')
plt.title('Testing dataset actual vs polynomial predicted')
plt.legend()
plt.show()


plt.scatter(X_train, lin2.predict(poly.fit_transform(X_train)), color='r')
plt.scatter(X_train, y_train)
plt.show()


# Visualising the Polynomial Regression results 
plt.scatter(x_pr, y_pr, color = 'blue') 
  
plt.plot(x_pr, lin2.predict(poly.fit_transform(x_pr)), color = 'red') 
plt.title('Polynomial Regression of GDP vs Passenger Numbers [2008 - 2018]') 
plt.ticklabel_format(useOffset=False,style = 'plain')
plt.ylabel('UK Air Passengers (count)')
plt.xlabel('GDP: chained volume measures: Seasonally adjusted £m')
plt.show() 


years = [2018,2019,2020,2021,2022,2023]

ONS_GROWTH = pd.DataFrame([[2019,2020,2021,2022,2023],[1.012,1.014,1.016,1.016,1.016]]).transpose()
ONS_GROWTH.rename(columns={0:'Year',1:'Growth Rate'}, inplace = True)
ONS_GROWTH.set_index('Year', inplace = True)

HM_TRES_GROWTH = pd.DataFrame([[2019,2020,2021,2022,2023],[0.942,1.05,1.015,1.013,1.014]]).transpose()
HM_TRES_GROWTH.rename(columns={0:'Year',1:'Growth Rate'}, inplace = True)
HM_TRES_GROWTH.set_index('Year', inplace = True)

Pred_GDP_ONS = np.empty((6,1))
Pred_GDP_ONS[0,0] = CombiData.loc[2018,'GDP']

for i in range(0,len(ONS_GROWTH.index)):
    Pred_GDP_ONS[i+1,0] = ONS_GROWTH.iloc[i,0]* Pred_GDP_ONS[i,0]

Pred_GDP_HMT = np.empty((6,1))
Pred_GDP_HMT[0,0] = CombiData.loc[2018,'GDP']

for i in range(0,len(HM_TRES_GROWTH.index)):
    Pred_GDP_HMT[i+1,0] = HM_TRES_GROWTH.iloc[i,0] * Pred_GDP_HMT[i,0]

Pax_ONS = np.empty((6,2))
Pax_ONS[:,0] = years

Pax_HMT = np.empty((6,2))
Pax_HMT[:,0] = years

Pax_ONS[:,1] = lin2.predict(poly.fit_transform(Pred_GDP_ONS))
Pax_HMT[:,1] = lin2.predict(poly.fit_transform(Pred_GDP_HMT))

fig, ax = plt.subplots()

ax.plot(CombiData.loc[2012:2018,'Passengers'], label = 'Actual Passengers')
ax.plot(years, Pax_ONS[:,1], ls ='--', label = 'Predicted average pre-covid')
ax.plot(years, Pax_HMT[:,1], label = 'Predicted post-covid')
ax.legend()
ax.ticklabel_format(style = 'plain')
plt.show()
