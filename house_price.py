# -*- coding: utf-8 -*-
"""House_Price.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iMwYTcCz-JueCpR50MG3ZiAYFBrwEcsf

# **HOUSE PRICE PREDICTION**

**IMPORTING LIBRARIES**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,mean_absolute_percentage_error,mean_squared_error,r2_score

"""**DATA LOADING**"""

df=pd.read_csv('/content/house.csv')
df

"""**DATA PREPROCESSING**"""

# Printing first five rows
df.head()

# Printing the last 5 rows
df.tail()

# Printing column names
df.columns

# Printing the datatype
df.dtypes

# Dimensions of the DataFrame
df.shape

#Summary Statistics
df.describe()

#Informations
df.info()

#Finding missing values
df.isna().sum()

#Count of Duplicated Rows
df.duplicated().sum()

for i in df:
  value=df[i].value_counts()
  print(value)
  print('_'*1000)

df['date']=df['date'].str.replace('00:00:00','')
df['statezip']=df['statezip'].str.replace('WA','')
df.loc[df['price']==0.0,'price']=np.NaN
df.loc[df['bedrooms']==0.0,'price']=np.NaN
df.loc[df['bathrooms']==0.0,'bathrooms']=np.NaN
df.loc[df['sqft_basement']==0,'sqft_basement']=np.NaN
df.loc[df['yr_renovated']==0,'yr_renovated']=np.NaN

df.isna().sum()

#dropping unwanted columns
df.drop(['sqft_basement','yr_renovated','country','street','date'],axis=1,inplace=True)

#filling missing values
df['price']=df['price'].fillna(df['price'].median())
df['bathrooms']=df['bathrooms'].fillna(df['bathrooms'].median())
df.isna().sum()

#label encoding
from sklearn.preprocessing import LabelEncoder
lab=LabelEncoder()
df['city']=lab.fit_transform(df['city'])

#converting datatype to numerical
df['statezip']=df['statezip'].astype(float)
df.dtypes

#boxplot
for i in ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
         'condition', 'sqft_above','statezip']:
  sns.boxplot(x=i,data=df)
  plt.show()

#Outliers Treating
def wisker(col):
  q1=col.quantile(0.25)
  q3=col.quantile(0.75)
  IQR=q3-q1
  LW=q1-1.5*IQR  #lower wisker
  UW=q3+1.5*IQR  #upper wisker
  return LW,UW

for i in ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
         'condition', 'sqft_above','statezip']:
  LW,UW=wisker(df[i])
  df[i]=np.where(df[i]<LW,LW,df[i])
  df[i]=np.where(df[i]>UW,UW,df[i])

for i in ['price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
         'condition', 'sqft_above','statezip']:
  sns.boxplot(x=i,data=df)
  plt.show()

"""**DATA VISUALISATION**"""

#Exploring Property Views Distribution
df['view'].value_counts()
df['view'].plot(kind="hist",color='g')
plt.xticks([0,1,2,3,4])
plt.xlabel("Views")
plt.ylabel("Count")
plt.title("Property View Distribution");

#Top 10 Cities with the Highest View Counts
df['city'].value_counts().sort_values().tail(10).plot(kind="bar",color='g')
plt.xlabel("City")
plt.ylabel("Count")

plt.figure(figsize=(10,7))

"""**SEPERATING X AND Y**"""

x=df.drop(['price'],axis=1)
x

y=df['price']
y

"""**SPLITTING DATA FOR TRAINING AND TESTING**"""

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.30,random_state=42)
x_train

x_test

y_train

y_test

"""**MODEL CREATION**"""

forest=RandomForestRegressor(random_state=42)
linear=LinearRegression()
tree=DecisionTreeRegressor(random_state=42)
model=[forest,linear,tree]

"""**PERFORMANCE EVALUATION**"""

for i in model:
  i.fit(x_train,y_train)
  print(i)
  y_pred=i.predict(x_test)
  print(y_pred)
  print('absolute percentage error=',mean_absolute_percentage_error(y_test,y_pred))
  print('score=',r2_score(y_test,y_pred))
  plt.scatter(y_test, y_pred,color='g')
  plt.xlabel("Actual Value")
  plt.ylabel("Predicted Value")
  plt.title("Actual Value vs Predicted Value")
  plt.show()
  print('_'*1000)