#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing the required libraries.

import pandas as pd
import json
import numpy as np


# In[2]:


#Reading the 3 json files into the dataframes

df_brands = pd.read_json("brands.json", lines=True)
df_users= pd.read_json("users.json",lines=True)
df_receipts = pd.read_json("receipts.json", lines=True)


# In[3]:


#Displaying the Receipts table data below.

df_receipts.tail()


# In[4]:


#Displaying the Brand table data below.

df_brands.head()


# In[5]:


#Displaying the Users table data.

df_users.head()


# In[6]:


#The date format in Receipts json file looks very complicated.
#When imported in MySQLworkbench, the format cannot be used to query.Hence, by using pandas in python, converted it into datetime format(which can be understood easily).

pd.to_datetime(df_receipts['dateScanned'].apply(lambda x: x['$date']),infer_datetime_format=True).describe()


# In[7]:


from datetime import datetime
pd.set_option('display.max_rows',None)
df3 = pd.to_datetime(df_receipts['dateScanned'].apply(lambda x: datetime.fromtimestamp(int(str(x['$date'])[:10])).strftime('%Y-%m-%d %I:%M:%S %p'))).tolist()


# In[8]:


#Adding the converted datescanned to the dataframe.
#Converted to csv so it is easy to work with.

df_receipts = df_receipts.drop('dateScanned', 1)
df_receipts['dateScanned1'] = df3
df_receipts.to_csv('receipts.csv')


# In[9]:


#Trying to understand the different fields in the field "rewardsReceiptItemList".
df_receipts.loc[2,'rewardsReceiptItemList']
df_receipts['rewardsReceiptItemList'].explode()


# In[10]:


df_receipts['rewardsReceiptItemList'].explode().dropna().apply(lambda x: list(x.keys())).explode().unique()


# In[11]:


#Taking just the brandcodes from the rewardsReceiptItemList in receipts file
barcodes = df_receipts['rewardsReceiptItemList'].explode().dropna().apply(lambda x: x['brandCode'] if 'brandCode' in x.keys() else '')


# In[12]:


#Converting the dataframe into a list.

df3 = pd.DataFrame(df_receipts['rewardsReceiptItemList'].explode().dropna().tolist())
df3.head()


# In[13]:


df_receipts['rewardsReceiptItemList'].explode().dropna().apply(lambda x: list(x.keys())).explode().unique()


# In[14]:


#Understanding the link between Receipts data and Brand data
#comparing the brandcodes from receipts json file and brandcodes from Brand json file
#the common key between receipts and Brand files is brandcode as shown below.

brands2 = barcodes[barcodes.isin(df_brands['brandCode'])]
brands2[brands2!='']


# In[15]:


#The above code shows that a direct link couldn't be established between Receipts and Brand tables which is definitely a Data Quality issue.
#I debugged and analyzed the field "rewardsReceiptItemList" as shown above.


# In[16]:


#Fields like pointsAwardedDate,purchaseDate and other fields like these have many NaN which is definitely a data quality issue.

df_receipts[df_receipts['rewardsReceiptItemList'].isna()]


# In[17]:


#the other data quality issue is description has a "Item not found" in many rows which shows data inadequacy
df3[df3['description']=='ITEM NOT FOUND']


# In[23]:


#The other Data Quality issue is the brandCode is empty in the Brand table.
#This field is one of the important field used in SQL queries to get data and also to link the itemlist and brand table.

df3["brandCode"]


# In[ ]:




