#!/usr/bin/env python
# coding: utf-8

# Attributes of the data
# 
# 1.data of the year 2016
# 
# 2.total miles 
# 
# 3.start location 
# 
# 4.end location 
# 
# 5.category 
# 
# 6.purpose
# 
# 7.start date & end date 

# In[2]:


#importing required libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import warnings 
warnings.filterwarnings('ignore')
import time,datetime 
#start and end date is an object so we need to convert it 
#into date time format for further analysis 


# In[3]:


df=pd.read_csv("uber_data.csv")


# In[4]:


df


# In[5]:


df.info()


# In[6]:


df.columns


# In[7]:


#appropriate column names 
df.columns=df.columns.str.replace("*","")


# In[8]:


df.columns


# In[9]:


#dropping last row (wrong data, no use)
#inplace : If True, fill in place
df.drop(index=1155,inplace=True)


# In[10]:


df


# In[11]:


#checking nulls
df.isnull().sum()


# In[12]:


#in the purpose column, checking what percentage of data 
#is missing (1155 rows and 502 null values)

percentage=df['PURPOSE'].isnull().sum()*100/len(df['PURPOSE'])
print("percentage of missing values is {} % ".format(round(percentage,2)))


# 1.handling missing values in purpose column 
# 
# 2.‘ffill’ stands for ‘forward fill’
# 
# 3.fills based on the corresponding value in the previous row
# 
# 4.df.ffill(axis=1)-When ffill is applied across the column axis, then missing values are filled by the value in
# previous column in the same row

# In[13]:


df['PURPOSE'].fillna(method='ffill',inplace=True)


# In[14]:


#checking
df.isnull().sum()


# In[15]:


#only miles is numerical
df.describe()


# In[16]:


#correcting start and end date
#while converting, if any value is issue/not getting converting for eg. abc, don't stop execution and place 'na'
df['START_DATE']=pd.to_datetime(df['START_DATE'],errors='coerce')


# In[17]:


df['END_DATE']=pd.to_datetime(df['END_DATE'],errors='coerce')


# In[18]:


df.info()


# In[19]:


#checking majority start locations/frequency of all start locations 
start=df['START'].value_counts()


# In[20]:


start[start>10]


# Interpretation
# Make sure more cab services are available in Cary as people are frequently booking cabs in this location 

# In[21]:


stop=df['STOP'].value_counts()
stop


# Interpretation
# Cary is the location with frequent stops as well and is offering more business compared to other locations. 
# Therefore, prices can be increased a bit!

# In[22]:


#checking distance of trips usually booked 
miles=df['MILES'].value_counts()


# In[23]:


miles[miles>10]
#9.9 miles were travelled for 28 no. of times  


# Interpretation 
# Mile distance>10 no. of times i.e. 9.9 miles & 3.1 miles trips, compare price with the competetitor (ola charges),keep 5 rs. up(say) and offer something else for eg. give uber credits

# In[24]:


#visualization
plt.figure(figsize=(12,8)) #to improve plot size, do this step first
miles[miles>10].plot(kind='bar')
plt.xlabel('miles')
plt.ylabel('frequency')
plt.title('Most frequently booked miles ')


# In[25]:


df['PURPOSE'].value_counts()


# In[26]:


#for a particular purpose, finding the mean miles travel 
df.groupby(['PURPOSE'])['MILES'].mean()


# In[27]:


df.groupby(['PURPOSE']).agg({'MILES':['mean',max,min]})


# In[28]:


#visualizing outliers - boxplot  
sns.boxplot(data=df,x=df.PURPOSE,y=df.MILES)
plt.xticks(rotation=45)


# Interpretation - too many outliers 

# In[29]:


plt.figure(figsize=(15,6))
sns.countplot(df['PURPOSE'],order=df['PURPOSE'].value_counts().index,palette='viridis')


# In[30]:


#making new column
df['MINUTES']=df.END_DATE-df.START_DATE
df


# In[31]:


#converting complete values into seconds then into minutes  
df['MINUTES']=df['MINUTES'].dt.total_seconds()/60
df


# In[32]:


df.info()


# In[33]:


plt.figure(figsize=(16,7))
plt.subplot(1,2,1)
sns.boxplot(data=df,x=df.PURPOSE,y=df.MILES)
plt.xticks(rotation=45)
plt.subplot(1,2,2)
sns.boxplot(data=df,x=df.PURPOSE,y=df.MINUTES)
plt.xticks(rotation=45)


# In[34]:


#deriving month column from start date & end date 
df['MONTH']=pd.DatetimeIndex(df['START_DATE']).month
df


# In[35]:


#converting month no.s into month names 
dic={1:'jan',2:'feb',3:'march',4:'april',5:'may',6:'june',7:'july',8:'aug',9:'sept',10:'oct',11:'nov',12:'dec'}


# In[36]:


df['MONTH']=df['MONTH'].map(dic)
df


# In[37]:


plt.figure(figsize=(12,7))
sns.countplot(df['MONTH'],order=df['MONTH'].value_counts().index)


# Interpretation 
# In the festive months like december, there is much more use of cabs 

# In[38]:


#round trips
def round(x):
    if x['START']==x['STOP']:
        return 'yes'
    else:
        return'no'


# In[39]:


df['ROUND_TRIP']=df.apply(round,axis=1)


# In[40]:


plt.figure(figsize=(8,5))
sns.countplot(df['ROUND_TRIP'])


# In[41]:


df['ROUND_TRIP'].value_counts()


# Interpretation
# Majority of the trips are not round trips 

# In[42]:


#months having more round trips(start and end location=same)
df.groupby(['MONTH','ROUND_TRIP'])['ROUND_TRIP'].count()


# In[43]:


plt.figure(figsize=(12,7))
sns.countplot(df['ROUND_TRIP'],hue=df['MONTH'],palette='viridis')


# In[44]:


a=df.groupby(['MONTH','ROUND_TRIP']).agg({'ROUND_TRIP':'count'})


# In[45]:


a.columns=['COUNT_DATA']


# In[46]:


a=a.reset_index()


# In[47]:


a[a['ROUND_TRIP']=='yes'].sort_values(by=['COUNT_DATA'],ascending=False)


# In[48]:


pd.set_option('display.max_rows',None)


# In[49]:


#specifically in december
df[df['MONTH']=='dec'].groupby(['PURPOSE','MONTH','ROUND_TRIP']).count()


# In[50]:


#visualizing if x axis=minutes are increasing with y axis=miles 
#line plot 
#scatter plot 
plt.figure(figsize=(16,7))
plt.subplot(1,2,1)
sns.lineplot(data=df,x=df.MINUTES,y=df.MILES)
plt.subplot(1,2,2)
sns.scatterplot(data=df,x=df.MINUTES,y=df.MILES)
#Line plot depicts better 


# In[51]:


#2 categories-business & personal 
#in every purpose which is business and which is personal 


# In[52]:


plt.figure(figsize=(9,5))
sns.countplot(data=df,x='PURPOSE',hue='CATEGORY',dodge=False)
plt.xticks(rotation=45)


# Interpretation
# Most of the trips are for business purposes 

# In[78]:


#Relation between category and count of trips 
a=df.groupby(['CATEGORY','START']).agg({'START':'count'})


# In[82]:


a.head()


# In[83]:


a.columns=['COUNT_DATA']
a.head()


# In[85]:


a.reset_index().head()


# In[89]:


a.reset_index().sort_values(by=['CATEGORY','COUNT_DATA'],ascending=False)


# Interpretation 
# Personal trip - Whitebridge is the major start point 
# Business trip - Cary, Morrisville & Whitebridge 

# In[91]:


#relationship between category and miles 
df.groupby(['CATEGORY'])['MILES'].mean()


# Interpretation 
# Usual miles travelled in business trips is approx. 10 and 9 for personal trips 

# INSIGHTS FROM EDA 
# 
# 1.Majority trips are for business category 
# 2.Majority round trips were in dec
# 3.highest overall booking is in dec
# 4.Cary is the most frequent start & stop location 
# 5.Majority times purpose of the trip is meeting 
# 6.For airport - only business trips were booked 
# 7.For commute - Charity & moving - only personal trips were booked
# 8.All trips booked in Islamabad were round trips 
# 9.Seasonality is there in the date 
# 10.Least booking is in Sept 
# 11.For round trips - average miles travelled is 7.7 
# 12.Very few cabs were booked for charity,commute & moving 
# 13.Very short trips are there when Cary is the start & stop location 

# In[ ]:




